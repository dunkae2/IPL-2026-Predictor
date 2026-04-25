import pandas as pd
import numpy as np

def compute_player_features(match_info: pd.DataFrame, ball_by_ball: pd.DataFrame, n_innings: int = 10):
    match_info = match_info.sort_values("match_date").reset_index(drop=True)
    
    match_dates = match_info.set_index("match_number")["match_date"].to_dict()
    ball_by_ball["match_date"] = ball_by_ball["ID"].map(match_dates)
    ball_by_ball = ball_by_ball.dropna(subset=["match_date"])
    ball_by_ball["match_date"] = pd.to_datetime(ball_by_ball["match_date"])

    def batting_avg(batter, before_date):
        innings = ball_by_ball[
            (ball_by_ball["Batter"] == batter) &
            (ball_by_ball["match_date"] < before_date)
        ].groupby("ID").agg(
            runs=("BatsmanRun", "sum"),
            dismissed=("IsWicketDelivery", lambda x: 1 if (ball_by_ball.loc[x.index, "PlayerOut"] == batter).any() else 0)
        ).tail(n_innings)
        if len(innings) == 0:
            return np.nan
        total_runs = innings["runs"].sum()
        dismissals = innings["dismissed"].sum()
        return total_runs / dismissals if dismissals > 0 else total_runs / len(innings)

    def bowling_economy(bowler, before_date):
        overs = ball_by_ball[
            (ball_by_ball["Bowler"] == bowler) &
            (ball_by_ball["match_date"] < before_date)
        ].groupby("ID").agg(
            runs=("TotalRun", "sum"),
            balls=("TotalRun", "count")
        ).tail(n_innings)
        if len(overs) == 0:
            return np.nan
        total_runs = overs["runs"].sum()
        total_balls = overs["balls"].sum()
        return (total_runs / total_balls * 6) if total_balls > 0 else np.nan

    def team_batting_strength(team, before_date):
        team_balls = ball_by_ball[
            (ball_by_ball["BattingTeam"] == team) &
            (ball_by_ball["match_date"] < before_date)
        ]
        top_batters = team_balls.groupby("Batter")["BatsmanRun"].sum().nlargest(5).index.tolist()
        avgs = [batting_avg(b, before_date) for b in top_batters]
        avgs = [a for a in avgs if not np.isnan(a)]
        return np.mean(avgs) if avgs else np.nan

    def team_bowling_strength(team, before_date):
        team_balls = ball_by_ball[
            (ball_by_ball["BattingTeam"] != team) &
            (ball_by_ball["match_date"] < before_date)
        ]
        match_ids = match_info[
            ((match_info["team1"] == team) | (match_info["team2"] == team)) &
            (match_info["match_date"] < before_date)
        ]["match_number"].tolist()
        bowler_balls = ball_by_ball[ball_by_ball["ID"].isin(match_ids) & (ball_by_ball["BattingTeam"] != team)]
        top_bowlers = bowler_balls.groupby("Bowler")["TotalRun"].count().nlargest(5).index.tolist()
        econs = [bowling_economy(b, before_date) for b in top_bowlers]
        econs = [e for e in econs if not np.isnan(e)]
        return np.mean(econs) if econs else np.nan

    team1_bat, team2_bat = [], []
    team1_bowl, team2_bowl = [], []

    for idx, row in match_info.iterrows():
        date = row["match_date"]
        t1, t2 = row["team1"], row["team2"]
        if idx % 50 == 0:
            print(f"[player_features] Processing match {idx}/{len(match_info)}...")
        team1_bat.append(team_batting_strength(t1, date))
        team2_bat.append(team_batting_strength(t2, date))
        team1_bowl.append(team_bowling_strength(t1, date))
        team2_bowl.append(team_bowling_strength(t2, date))

    match_info["team1_batting_strength"] = team1_bat
    match_info["team2_batting_strength"] = team2_bat
    match_info["team1_bowling_strength"] = team1_bowl
    match_info["team2_bowling_strength"] = team2_bowl

    return match_info