from pathlib import Path
from data_loader import load_raw_data
from preprocessing import fix_team_names, parse_match_dates, map_missing_cities, resolve_winner, parse_player_lists

def main():
    match_info_path = Path(__file__).parent.parent / "data" / "raw" / "Match_Info.csv"
    ball_by_ball_path = Path(__file__).parent.parent / "data" / "raw" / "Ball_By_Ball_Match_Data.csv"
    
    match_info, ball_by_ball = load_raw_data(match_info_path, ball_by_ball_path)

    match_info = fix_team_names(match_info)
    match_info = parse_match_dates(match_info)
    match_info = map_missing_cities(match_info)
    match_info = resolve_winner(match_info)
    match_info = parse_player_lists(match_info)

    output_path = Path(__file__).parent.parent / "data" / "processed" / "match_info_clean.csv"
    match_info.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()


