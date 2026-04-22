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
    "rest_days_diff", "rolling_win_rate_diff", "venue_win_rate_diff", "elo_diff"]
    target_col = "target"

    for col in feature_cols:
        if "win_rate" in col or "elo" in col:
            features_data[col] = features_data[col].fillna(0.5)
        elif "rest_days" in col:
            features_data[col] = features_data[col].fillna(3)
        else:
            features_data[col] = features_data[col].fillna(features_data[col].median())

    accuracies = {}

    for i in range(2019, 2025, 1):
        training_data = features_data[(features_data["match_date"] < f"{i}-01-01") & (features_data["match_date"] > "2015-01-01")]
        testing_data = features_data[(features_data["match_date"] >= f"{i}-01-01") & (features_data["match_date"] < f"{i+1}-01-01")]

        x_train = training_data[feature_cols]
        y_train = training_data[target_col]

        x_test = testing_data[feature_cols]
        y_test = testing_data[target_col]

        model = CatBoostClassifier(verbose=0)
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)

        accuracies[i] = accuracy_score(y_test, predictions)

        print(f"{i}: {len(x_test)} matches")
    
    model_final = CatBoostClassifier(verbose=0)
    model_final.fit(features_data[feature_cols], features_data[target_col])
    model_final.save_model(str(Path(__file__).parent.parent.parent / "models" / "prematch_model.cbm"))

    for year, acc in accuracies.items():
        print(f"{year}: {acc:.3f}")
    print(f"Mean accuracy: {sum(accuracies.values()) / len(accuracies):.3f}")

    print("Train size: ", len(x_train))
    print("Test size: ", len(x_test))



if __name__ == "__main__":
    main()
