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
        rest_days = rest_days.where(rest_days <= 60, other=np.nan)

        team1_match = df["team1"] == team
        df.loc[team1_match, "team1_rest_days"] = rest_days[team1_match]

        team2_match = df["team2"] == team
        df.loc[team2_match, "team2_rest_days"] = rest_days[team2_match]

    return df


def compute_team_win_rate(df: pd.DataFrame, n: int = 10):
    team_rows = pd.unique(pd.concat([df["team1"], df["team2"]]))

    df["team1_rolling_win_rate"] = None
    df["team2_rolling_win_rate"] = None

    current_season = df["match_date"].dt.year.max()

    for team in team_rows:
        chron_matches = df[(df["team1"] == team) | (df["team2"] == team)].sort_values("match_date")
        wins = (chron_matches["winner"] == team).astype(float)
        weights = chron_matches["match_date"].dt.year.apply(lambda y: 3.0 if y == current_season else 1.0)

        weighted_win_rate = []
        for i in range(len(chron_matches)):
            start = max(0, i - n)
            w = weights.iloc[start:i].values
            v = wins.iloc[start:i].values
            if len(v) == 0:
                weighted_win_rate.append(np.nan)
            else:
                weighted_win_rate.append(np.average(v, weights=w))

        rolling = pd.Series(weighted_win_rate, index=chron_matches.index)

        team1_match = df["team1"] == team
        df.loc[team1_match, "team1_rolling_win_rate"] = rolling[team1_match]

        team2_match = df["team2"] == team
        df.loc[team2_match, "team2_rolling_win_rate"] = rolling[team2_match]

    return df


def record_elo(df: pd.DataFrame):
    team_names = pd.unique(pd.concat([df["team1"], df["team2"]]))
    team_dict = {team: 1500 for team in team_names}

    df["team1_elo"] = None
    df["team2_elo"] = None

    df = df.sort_values("match_date").reset_index(drop=True)

    for idx, row in df.iterrows():
        team1_elo = team_dict[row["team1"]]
        team2_elo = team_dict[row["team2"]]

        df.loc[idx, "team1_elo"] = team1_elo
        df.loc[idx, "team2_elo"] = team2_elo

        expected_a = 1 / (1 + 10 ** ((team2_elo - team1_elo) / 400))
        expected_b = 1 - expected_a

        actual_a = 1 if row["winner"] == row["team1"] else 0
        actual_b = 1 - actual_a

        K = 20
        team_dict[row["team1"]] = team1_elo + K * (actual_a - expected_a)
        team_dict[row["team2"]] = team2_elo + K * (actual_b - expected_b)

    return df