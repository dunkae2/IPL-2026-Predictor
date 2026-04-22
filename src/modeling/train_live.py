from pathlib import Path
import sys
import pandas as pd
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "features"))
from data_loader import load_clean_data
from live_features import compute_live_features
from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
import numpy as np


def main():
    match_info_path = Path(__file__).parent.parent.parent / "data" / "processed" / "match_info_clean.csv"
    ball_by_ball_path = Path(__file__).parent.parent.parent / "data" / "raw" / "Ball_By_Ball_Match_Data.csv"
    
    match_info, ball_by_ball = load_clean_data(match_info_path, ball_by_ball_path)

    live_data = compute_live_features(match_info, ball_by_ball)

    feature_cols = [
    "runs_required", "wickets_remaining", "balls_remaining",
    "current_run_rate", "required_run_rate", "run_rate_pressure"
    ]

    target_col = "target"

    match_dates = match_info.set_index("match_number")["match_date"]
    live_data["match_date"] = live_data["ID"].map(match_dates)

    training_data = live_data[live_data["match_date"] < "2024-01-01"]
    testing_data = live_data[live_data["match_date"] >= "2024-01-01"]

    x_train = training_data[feature_cols]
    y_train = training_data[target_col]
    x_test = testing_data[feature_cols]
    y_test = testing_data[target_col]

    model = CatBoostClassifier(verbose=0)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    model.save_model(str(Path(__file__).parent.parent.parent / "models" / "live_model.cbm"))

    print("Live model accuracy:", accuracy_score(y_test, predictions))
    print("Train size:", len(x_train))
    print("Test size:", len(x_test))

if __name__ == "__main__":
    main()