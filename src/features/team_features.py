import pandas as pd
import numpy as np

def compute_rest_days(df: pd.DataFrame):
    df["match_date"] = pd.to_datetime(df["match_date"])
    df["team1_rest_days"] = None
    df["team2_rest_days"] = None

    team_rows = pd.unique(pd.concat([df["team1"], df["team2"]]))

    for team in team_rows:
        dates_rows = df[(df["team1"] == team) | (df["team2"] == team)]
        sorted_dates = dates_rows.sort_values("match_date")
        rest_days = sorted_dates["match_date"].diff().dt.days
        rest_days = rest_days.where(rest_days <= 60, other = np.nan)

        team1_match = df["team1"] == team
        df.loc[team1_match, "team1_rest_days"] = rest_days[team1_match]

        team2_match = df["team2"] == team
        df.loc[team2_match, "team2_rest_days"] = rest_days[team2_match]

    return df

def compute_team_win_rate(df: pd.DataFrame, n: int = 10):
    team_rows = pd.unique(pd.concat([df["team1"], df["team2"]]))
    
    df["team1_rolling_win_rate"] = None
    df["team2_rolling_win_rate"] = None

    for team in team_rows:
        chron_matches = df[(df["team1"] == team) | (df["team2"] == team)].sort_values("match_date")
        wins = (chron_matches["winner"] == team).astype(int)
        rolling_win_rate = wins.rolling(window=n, min_periods=1).mean().shift(1)

        team1_match = df["team1"] == team
        df.loc[team1_match, "team1_rolling_win_rate"] = rolling_win_rate

        team2_match = df["team2"] == team
        df.loc[team2_match, "team2_rolling_win_rate"] = rolling_win_rate

    return df
        







        