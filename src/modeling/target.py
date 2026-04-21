import numpy as np
import pandas as pd

def random_assign_teams(df: pd.DataFrame):
    np.random.seed(42)
    random_list = np.random.randint(0, 2, size = len(df))

    df["teamA"] = np.where(random_list == 1, df["team1"], df["team2"])
    df["teamB"] = np.where(random_list == 1, df["team2"], df["team1"])

    df["target"] = np.where(df["teamA"] == df["winner"], 1, 0)

    df["teamA_rest_days"] = np.where(random_list == 1, df["team1_rest_days"], df["team2_rest_days"])
    df["teamB_rest_days"] = np.where(random_list == 1, df["team2_rest_days"], df["team1_rest_days"])

    df["teamA_rolling_win_rate"] = np.where(random_list == 1, df["team1_rolling_win_rate"], df["team2_rolling_win_rate"])
    df["teamB_rolling_win_rate"] = np.where(random_list == 1, df["team2_rolling_win_rate"], df["team1_rolling_win_rate"])

    df["teamA_venue_win_rate"] = np.where(random_list == 1, df["team1_venue_win_rate"], df["team2_venue_win_rate"])
    df["teamB_venue_win_rate"] = np.where(random_list == 1, df["team2_venue_win_rate"], df["team1_venue_win_rate"])

    df["rest_days_diff"] = df["teamA_rest_days"] - df["teamB_rest_days"]
    df["rolling_win_rate_diff"] = df["teamA_rolling_win_rate"] - df["teamB_rolling_win_rate"]
    df["venue_win_rate_diff"] = df["teamA_venue_win_rate"] - df["teamB_venue_win_rate"]

    df["teamA_elo"] = np.where(random_list == 1, df["team1_elo"], df["team2_elo"])
    df["teamB_elo"] = np.where(random_list == 1, df["team2_elo"], df["team1_elo"])
    df["elo_diff"] = df["teamA_elo"] - df["teamB_elo"]

    df = df.drop(columns=["team1_rest_days", "team2_rest_days", "team1_rolling_win_rate", "team2_rolling_win_rate", "team1_venue_win_rate", "team2_venue_win_rate", "team1_elo", "team2_elo"])

    return df

