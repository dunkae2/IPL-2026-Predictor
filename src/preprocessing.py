import pandas as pd
from datetime import datetime
import numpy as np

def fix_team_names(df: pd.DataFrame):
    team_names = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiant": "Rising Pune Supergiants"
    }
    cols_to_fix = ["team1", "team2", "toss_winner", "eliminator", "winner"]
    for col in cols_to_fix:
        df[col] = df[col].replace(team_names)

    return df

def parse_match_dates(df: pd.DataFrame):
    df["match_date"] = pd.to_datetime(df["match_date"], format = "%Y-%m-%d")
    return df

def map_missing_cities(df: pd.DataFrame):
    stadium_mapping = {
    "Dubai International Cricket Stadium": "Dubai",
    "Sharjah Cricket Stadium": "Sharjah"
    }

    city_na_mask = df["city"].isna()
    df.loc[city_na_mask, "city"] = df.loc[city_na_mask, "venue"].replace(stadium_mapping)
    return df

def resolve_winner(df: pd.DataFrame):
    df = df[df["result"] != "no result"]
    tie_mask = df["result"] == "tie"
    df.loc[tie_mask, "winner"] = np.where(df.loc[tie_mask, "eliminator"] == df.loc[tie_mask, "team1"], df.loc[tie_mask, "team2"], df.loc[tie_mask, "team1"])
    return df

def parse_player_lists(df: pd.DataFrame):
    df["team1_players"] = df["team1_players"].fillna("").str.split(",").apply(lambda x: [name.strip() for name in x if name.strip()])
    df["team2_players"] = df["team2_players"].fillna("").str.split(",").apply(lambda x: [name.strip() for name in x if name.strip()])

    return df





