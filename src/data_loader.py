import pandas as pd
from pathlib import Path

def load_raw_data(match_info_path, ball_by_ball_path):
    match_info = pd.read_csv(match_info_path)
    ball_by_ball = pd.read_csv(ball_by_ball_path)
    return match_info, ball_by_ball
