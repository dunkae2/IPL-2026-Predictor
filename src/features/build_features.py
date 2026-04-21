import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from data_loader import load_clean_data
from team_features import compute_rest_days, compute_team_win_rate, record_elo
from venue_features import compute_venue_win_rate, compute_first_innings_avg_score

def main():
    match_info_path = Path(__file__).parent.parent.parent / "data" / "processed" / "match_info_clean.csv"
    ball_by_ball_path = Path(__file__).parent.parent.parent / "data" / "raw" / "Ball_By_Ball_Match_Data.csv"
    
    match_info, ball_by_ball = load_clean_data(match_info_path, ball_by_ball_path)

    match_info = compute_rest_days(match_info)
    match_info = compute_team_win_rate(match_info) # has a default value for n = 10
    match_info = compute_venue_win_rate(match_info)
    match_info = record_elo(match_info)
    match_info = compute_first_innings_avg_score(match_info, ball_by_ball)
    

    output_path = Path(__file__).parent.parent.parent / "data" / "processed" / "match_features.csv"
    match_info.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()