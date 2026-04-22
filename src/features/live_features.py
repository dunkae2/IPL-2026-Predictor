import pandas as pd
import numpy as np

def compute_live_features(match_info: pd.DataFrame, ball_by_ball: pd.DataFrame):
    match_info = match_info.sort_values("match_date")
    first_innings = ball_by_ball[ball_by_ball["Innings"] == 1]
    matching_ID = first_innings.groupby("ID")
    total_run_sum = matching_ID["TotalRun"].sum()

    second_innings = ball_by_ball[ball_by_ball["Innings"] == 2]

    second_innings = second_innings.copy()
    second_innings["cumulative_runs"] = second_innings.groupby("ID")["TotalRun"].cumsum()
    second_innings["cumulative_wickets"] = second_innings.groupby("ID")["IsWicketDelivery"].cumsum()

    second_innings["target_score"] = second_innings["ID"].map(total_run_sum)
    runs_required = second_innings["target_score"] - second_innings["cumulative_runs"]

    wickets_remaining = (10 - second_innings["cumulative_wickets"])

    balls_remaining = (120 - ((second_innings["Overs"] * 6) + second_innings["BallNumber"]))

    current_run_rate = (second_innings["cumulative_runs"]/(((second_innings["Overs"] * 6) + second_innings["BallNumber"])/6))

    required_run_rate = (runs_required/(balls_remaining/6))

    run_rate_pressure = required_run_rate - current_run_rate

    second_innings["runs_required"] = runs_required
    second_innings["wickets_remaining"] = wickets_remaining
    second_innings["balls_remaining"] = balls_remaining
    second_innings["current_run_rate"] = current_run_rate
    second_innings["required_run_rate"] = required_run_rate
    second_innings["run_rate_pressure"] = run_rate_pressure

    winner_map = match_info.set_index("match_number")["winner"]
    second_innings["winner"] = second_innings["ID"].map(winner_map)

    second_innings["target"] = (second_innings["winner"] == second_innings["BattingTeam"]).astype(int)

    second_innings = second_innings.replace([np.inf, -np.inf], np.nan)
    second_innings = second_innings.dropna(subset=["runs_required", "wickets_remaining", "balls_remaining", "current_run_rate", "required_run_rate", "run_rate_pressure"])

    return second_innings