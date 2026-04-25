import json
import pandas as pd
from pathlib import Path
import os

RAW_DIR = Path(__file__).parent.parent.parent / "data" / "raw" / "ipl_json"
MATCH_INFO_PATH = Path(__file__).parent.parent.parent / "data" / "raw" / "Match_Info.csv"
BALL_BY_BALL_PATH = Path(__file__).parent.parent.parent / "data" / "raw" / "Ball_By_Ball_Match_Data.csv"

def convert_match_info(data, match_id):
    info = data["info"]
    teams = info["teams"]
    outcome = info.get("outcome", {})
    
    if "winner" in outcome:
        result = "Win"
        winner = outcome["winner"]
    elif "no result" in str(outcome).lower() or not outcome:
        result = "no result"
        winner = None
    else:
        result = "Win"
        winner = outcome.get("winner")

    players = info.get("players", {})
    team1_players = ", ".join(players.get(teams[0], []))
    team2_players = ", ".join(players.get(teams[1], []))

    return {
        "match_number": match_id,
        "team1": teams[0],
        "team2": teams[1],
        "match_date": info["dates"][0],
        "toss_winner": info.get("toss", {}).get("winner", None),
        "toss_decision": info.get("toss", {}).get("decision", None),
        "result": result,
        "eliminator": None,
        "winner": winner,
        "player_of_match": info.get("player_of_match", [None])[0],
        "venue": info.get("venue"),
        "city": info.get("city"),
        "team1_players": team1_players,
        "team2_players": team2_players
    }

def convert_ball_by_ball(data, match_id):
    rows = []
    for innings_idx, innings in enumerate(data.get("innings", []), 1):
        batting_team = innings["team"]
        for over_data in innings.get("overs", []):
            over_num = over_data["over"]
            ball_num = 0
            for delivery in over_data.get("deliveries", []):
                ball_num += 1
                extras = delivery.get("extras", {})
                extra_type = list(extras.keys())[0] if extras else None
                extras_run = sum(extras.values()) if extras else 0
                
                wickets = delivery.get("wickets", [])
                is_wicket = 1 if wickets else 0
                player_out = wickets[0].get("player_out") if wickets else None
                kind = wickets[0].get("kind") if wickets else None
                fielders = wickets[0].get("fielders", []) if wickets else []
                fielders_str = ", ".join([f.get("name", "") for f in fielders]) if fielders else None

                rows.append({
                    "ID": match_id,
                    "Innings": innings_idx,
                    "Overs": over_num,
                    "BallNumber": ball_num,
                    "Batter": delivery.get("batter"),
                    "Bowler": delivery.get("bowler"),
                    "NonStriker": delivery.get("non_striker"),
                    "ExtraType": extra_type,
                    "BatsmanRun": delivery["runs"]["batter"],
                    "ExtrasRun": extras_run,
                    "TotalRun": delivery["runs"]["total"],
                    "IsWicketDelivery": is_wicket,
                    "PlayerOut": player_out,
                    "Kind": kind,
                    "FieldersInvolved": fielders_str,
                    "BattingTeam": batting_team
                })
    return rows

def main():
    match_info_rows = []
    ball_by_ball_rows = []

    files = list(RAW_DIR.glob("*.json"))
    print(f"Found {len(files)} JSON files")

    for filepath in files:
        with open(filepath, "r") as f:
            data = json.load(f)
        
        season = data["info"].get("season", "")
        if str(season) != "2026":
            continue

        match_id = filepath.stem
        
        match_row = convert_match_info(data, match_id)
        match_info_rows.append(match_row)
        
        ball_rows = convert_ball_by_ball(data, match_id)
        ball_by_ball_rows.extend(ball_rows)

    print(f"Found {len(match_info_rows)} IPL 2026 matches")
    print(f"Found {len(ball_by_ball_rows)} ball-by-ball deliveries")

    if match_info_rows:
        new_matches = pd.DataFrame(match_info_rows)
        existing_matches = pd.read_csv(MATCH_INFO_PATH)
        combined = pd.concat([existing_matches, new_matches], ignore_index=True)
        combined.to_csv(MATCH_INFO_PATH, index=False)
        print(f"Match_Info.csv updated: {len(combined)} total rows")

    if ball_by_ball_rows:
        new_bbb = pd.DataFrame(ball_by_ball_rows)
        existing_bbb = pd.read_csv(BALL_BY_BALL_PATH)
        combined_bbb = pd.concat([existing_bbb, new_bbb], ignore_index=True)
        combined_bbb.to_csv(BALL_BY_BALL_PATH, index=False)
        print(f"Ball_By_Ball.csv updated: {len(combined_bbb)} total rows")

if __name__ == "__main__":
    main()