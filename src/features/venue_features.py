import pandas as pd
import numpy as np

def compute_venue_win_rate(df: pd.DataFrame):
    team_rows = pd.unique(pd.concat([df["team1"], df["team2"]]))

    df["team1_venue_win_rate"] = None
    df["team2_venue_win_rate"] = None

    for team in team_rows:
        chron_matches = df[(df["team1"] == team) | (df["team2"] == team)].sort_values("match_date")
        win_series = (chron_matches["winner"] == team).astype(int)
        chron_matches = chron_matches.copy()
        chron_matches["win"] = win_series
        venue_win_rate = chron_matches.groupby("venue")["win"].expanding().mean().groupby(level=0).shift(1)
        venue_win_rate = venue_win_rate.reset_index(level=0, drop=True)
        
        team1_rate = df["team1"] == team
        df.loc[team1_rate, "team1_venue_win_rate"] = venue_win_rate[team1_rate]

        team2_rate = df["team2"] == team
        df.loc[team2_rate, "team2_venue_win_rate"] = venue_win_rate[team2_rate]

    return df

def compute_first_innings_avg_score(match_info: pd.DataFrame, ball_by_ball: pd.DataFrame):
    match_info = match_info.sort_values("match_date")
    first_innings = ball_by_ball[ball_by_ball["Innings"] == 1]
    matching_ID = first_innings.groupby("ID")
    total_run_sum = matching_ID["TotalRun"].sum()

    match_info["first_innings_score"] = match_info["match_number"].map(total_run_sum)

    rolling_venue_score = match_info.groupby("venue")["first_innings_score"].expanding().mean().groupby(level=0).shift(1)

    match_info["venue_avg_first_innings_score"] = rolling_venue_score.reset_index(level=0, drop=True)

    return match_info
    


    




        
