from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

print("Starting API...")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from catboost import CatBoostClassifier
import numpy as np

MODELS_DIR = Path(__file__).parent.parent.parent / "models"

try:
    prematch_model = CatBoostClassifier()
    prematch_model.load_model(str(MODELS_DIR / "prematch_model.cbm"))
    live_model = CatBoostClassifier()
    live_model.load_model(str(MODELS_DIR / "live_model.cbm"))
    print("Models loaded successfully")
except Exception as e:
    print(f"Model loading failed: {e}")

from pydantic import BaseModel

class LiveMatchInput(BaseModel):
    runs_required: float
    wickets_remaining: float
    balls_remaining: float
    current_run_rate: float
    required_run_rate: float
    run_rate_pressure: float

@app.post("/predict/live")
def predict_live(data: LiveMatchInput):
    features = np.array([[
        data.runs_required,
        data.wickets_remaining,
        data.balls_remaining,
        data.current_run_rate,
        data.required_run_rate,
        data.run_rate_pressure
    ]])
    prob = live_model.predict_proba(features)[0][1]
    return {"chasing_team_win_probability": round(float(prob), 4)}

class PreMatchInput(BaseModel):
    team_a: str
    team_b: str

@app.post("/predict/prematch")
def predict_prematch(data: PreMatchInput):
    features = np.array([[
        0.5, 0.5,  # rest_days (neutral - unknown)
        0.5, 0.5,  # rolling_win_rate (neutral)
        0.5, 0.5,  # venue_win_rate (neutral)
        162.0,     # venue_avg_first_innings_score (league average)
        0.0,       # rest_days_diff
        0.0,       # rolling_win_rate_diff
        0.0,       # venue_win_rate_diff
        0.0        # elo_diff
    ]])
    prob = prematch_model.predict_proba(features)[0][1]
    return {
        "team_a": data.team_a,
        "team_b": data.team_b,
        "team_a_win_probability": round(float(prob), 4),
        "team_b_win_probability": round(1 - float(prob), 4)
    }