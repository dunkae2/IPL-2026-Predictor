import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path(__file__).parent.parent.parent / ".env")
CRICAPI_KEY = os.getenv("CRICAPI_KEY")
IPL_SERIES_ID = "87c62aac-bc3c-4738-ab93-19da0690488f"
MATCH_INFO_PATH = Path(__file__).parent.parent.parent / "data" / "raw" / "Match_Info.csv"

def fetch_new_matches():
    resp = requests.get(
        f"https://api.cricapi.com/v1/series_info?apikey={CRICAPI_KEY}&id={IPL_SERIES_ID}",
        timeout=10
    )
    data = resp.json()
    matches = data.get("data", {}).get("matchList", [])

    existing = pd.read_csv(MATCH_INFO_PATH)
    existing_ids = set(existing["match_number"].astype(str))

    new_rows = []
    for m in matches:
        match_id = m.get("id")
        if not m.get("matchEnded", False):
            continue
        if str(match_id) in existing_ids:
            continue

        status = m.get("status", "")
        teams = m.get("teams", [])
        if len(teams) < 2:
            continue

        if " won" in status:
            winner = status.split(" won")[0].strip()
            result = "Win"
        else:
            winner = None
            result = "no result"

        new_rows.append({
            "match_number": match_id,
            "team1": teams[0],
            "team2": teams[1],
            "match_date": m.get("dateTimeGMT", "")[:10],
            "toss_winner": None,
            "toss_decision": None,
            "result": result,
            "eliminator": None,
            "winner": winner,
            "player_of_match": None,
            "venue": m.get("venue", ""),
            "city": m.get("venue", "").split(",")[-1].strip() if m.get("venue") else None,
            "team1_players": None,
            "team2_players": None
        })

    if new_rows:
        new_df = pd.DataFrame(new_rows)
        combined = pd.concat([existing, new_df], ignore_index=True)
        combined.to_csv(MATCH_INFO_PATH, index=False)
        print(f"[auto_update] Added {len(new_rows)} new matches")
    else:
        print("[auto_update] No new matches to add")

    return len(new_rows)

if __name__ == "__main__":
    fetch_new_matches()