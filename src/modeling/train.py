from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from pathlib import Path
import sys
import pandas as pd
sys.path.append(str(Path(__file__).parent.parent))
from target import random_assign_teams


def main():
    match_features = Path(__file__).parent.parent.parent / "data" / "processed" / "match_features.csv"
    features_data = pd.read_csv(match_features)
    features_data = random_assign_teams(features_data)
    feature_cols = [
    "teamA_rest_days", "teamB_rest_days",
    "teamA_rolling_win_rate", "teamB_rolling_win_rate",
    "teamA_venue_win_rate", "teamB_venue_win_rate",
    "venue_avg_first_innings_score",
    "rest_days_diff", "rolling_win_rate_diff", "venue_win_rate_diff"]
    target_col = "target"

    features_data = features_data.dropna(subset=feature_cols)

    training_data = features_data[features_data["match_date"] < "2024-01-01"]
    testing_data = features_data[features_data["match_date"] >= "2024-01-01"]

    x_train = training_data[feature_cols]
    y_train = training_data[target_col]

    x_test = testing_data[feature_cols]
    y_test = testing_data[target_col]

    print(x_train.shape)

    model = CatBoostClassifier(verbose=0)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    print("Accuracy score: ", accuracy_score(y_test, predictions))
    print("Train size: ", len(x_train))
    print("Test size: ", len(x_test))
    print(y_train.value_counts())
    print(y_test.value_counts())
    print(predictions)
    print(predictions.sum())
    print(training_data[["teamA_rolling_win_rate", "teamB_rolling_win_rate"]].mean())
    print(training_data[["teamA_venue_win_rate", "teamB_venue_win_rate"]].mean())
    print(features_data.columns.tolist())



if __name__ == "__main__":
    main()
