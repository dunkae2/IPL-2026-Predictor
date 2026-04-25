from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys
import pandas as pd
import httpx
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent.parent / ".env")
CRICAPI_KEY = os.getenv("CRICAPI_KEY")

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

prematch_model = CatBoostClassifier()
live_model = CatBoostClassifier()

def reload_models():
    global prematch_model, live_model
    try:
        prematch_model.load_model(str(MODELS_DIR / "prematch_model.cbm"))
        live_model.load_model(str(MODELS_DIR / "live_model.cbm"))
        print("[models] Reloaded successfully")
    except Exception as e:
        print(f"[models] Reload failed: {e}")

reload_models()

match_features_path = Path(__file__).parent.parent.parent / "data" / "processed" / "match_features.csv"
match_features = pd.read_csv(match_features_path)
match_features["match_date"] = pd.to_datetime(match_features["match_date"])

IPL_SERIES_ID = "87c62aac-bc3c-4738-ab93-19da0690488f"

def get_team_latest_features(team_name: str):
    team_matches = match_features[
        (match_features["team1"] == team_name) | (match_features["team2"] == team_name)
    ].sort_values("match_date")
    if len(team_matches) == 0:
        return None
    return team_matches.iloc[-1]


@app.get("/matches")
async def get_matches():
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.cricapi.com/v1/series_info?apikey={CRICAPI_KEY}&id={IPL_SERIES_ID}",
            timeout=10
        )
        data = resp.json()

    matches = data.get("data", {}).get("matchList", [])
    api_info = data.get("info", {})

    result = []
    for m in matches:
        match_started = m.get("matchStarted", False)
        match_ended = m.get("matchEnded", False)
        teams = m.get("teams", [])
        if len(teams) < 2:
            continue

        status = "upcoming"
        if match_ended:
            status = "completed"
        elif match_started:
            status = "live"

        result.append({
            "id": m.get("id"),
            "name": m.get("name"),
            "teams": teams,
            "date": m.get("dateTimeGMT"),
            "venue": m.get("venue", ""),
            "status": status,
            "match_status": m.get("status", ""),
        })

    return {
        "matches": result,
        "api_calls_today": api_info.get("hitsToday", 0)
    }


@app.get("/match/{match_id}/live")
async def get_live_match(match_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.cricapi.com/v1/match_info?apikey={CRICAPI_KEY}&id={match_id}",
            timeout=10
        )
        data = resp.json()

    match_data = data.get("data", {})
    score = match_data.get("score", [])

    return {
        "id": match_id,
        "name": match_data.get("name"),
        "status": match_data.get("status"),
        "teams": match_data.get("teams", []),
        "score": score,
        "matchStarted": match_data.get("matchStarted", False),
        "matchEnded": match_data.get("matchEnded", False),
    }

@app.get("/match/{match_id}/live_prediction")
async def get_live_prediction(match_id: str):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"https://api.cricapi.com/v1/match_info?apikey={CRICAPI_KEY}&id={match_id}",
            timeout=10
        )
        data = resp.json()

    match_data = data.get("data", {})
    score = match_data.get("score", [])
    teams = match_data.get("teams", [])

    if not match_data.get("matchStarted"):
        return {"status": "not_started", "score": score}

    if match_data.get("matchEnded"):
        return {"status": "ended", "score": score, "result": match_data.get("status", "")}

    # INNINGS 1 in progress
    if len(score) == 1:
        inn1 = score[0]
        runs = inn1["r"]
        wickets = inn1["w"]
        overs_done = inn1["o"]

        balls_done = int(overs_done) * 6 + round((overs_done % 1) * 10)
        balls_remaining = 120 - balls_done
        crr = (runs / overs_done) if overs_done > 0 else 0
        projected_total = int(crr * 20) if overs_done > 0 else 0

        batting_team = inn1.get("inning", "").replace(" Inning 1", "").replace(" Innings 1", "").strip()
        bowling_team = teams[1] if batting_team == teams[0] else teams[0]

        # Estimate win probability from projected total vs venue average
        # Simple heuristic: >180 projected = batting team 60-70%, <150 = 35-45%
        if overs_done < 1:
            batting_win_prob = 0.5
        else:
            proj = projected_total
            # Sigmoid-style mapping
            batting_win_prob = max(0.15, min(0.85, 0.5 + (proj - 165) * 0.008))
            # Wickets penalty
            batting_win_prob -= (wickets * 0.02)
            batting_win_prob = max(0.15, min(0.85, batting_win_prob))

        return {
            "status": "innings1",
            "batting_team": batting_team,
            "bowling_team": bowling_team,
            "batting_win_probability": round(float(batting_win_prob), 4),
            "bowling_win_probability": round(1 - float(batting_win_prob), 4),
            "match_state": {
                "runs": runs,
                "wickets": wickets,
                "overs_done": overs_done,
                "balls_remaining": balls_remaining,
                "current_run_rate": round(crr, 2),
                "projected_total": projected_total,
            },
            "score": score
        }

    # INNINGS 2 in progress
    if len(score) >= 2:
        inn1 = score[0]
        inn2 = score[1]

        target = inn1["r"] + 1
        runs_scored = inn2["r"]
        wickets_fallen = inn2["w"]
        overs_done = inn2["o"]

        balls_done = int(overs_done) * 6 + round((overs_done % 1) * 10)
        balls_remaining = 120 - balls_done
        runs_required = target - runs_scored
        wickets_remaining = 10 - wickets_fallen

        if balls_remaining <= 0 or runs_required <= 0:
            return {"status": "ended", "score": score}

        crr = (runs_scored / overs_done) if overs_done > 0 else 0
        overs_remaining = balls_remaining / 6
        rrr = (runs_required / overs_remaining) if overs_remaining > 0 else 99
        pressure = rrr - crr

        features = np.array([[
            runs_required, wickets_remaining, balls_remaining,
            crr, rrr, pressure
        ]])
        prob = live_model.predict_proba(features)[0][1]

        inn2_name = inn2.get("inning", "")
        chasing_team = teams[1] if teams[1] in inn2_name else teams[0]
        defending_team = teams[0] if chasing_team == teams[1] else teams[1]

        return {
            "status": "live",
            "chasing_team": chasing_team,
            "defending_team": defending_team,
            "chasing_win_probability": round(float(prob), 4),
            "defending_win_probability": round(1 - float(prob), 4),
            "match_state": {
                "target": target,
                "runs_scored": runs_scored,
                "runs_required": runs_required,
                "wickets_remaining": wickets_remaining,
                "balls_remaining": balls_remaining,
                "overs_done": overs_done,
                "current_run_rate": round(crr, 2),
                "required_run_rate": round(rrr, 2),
            },
            "score": score
        }

    return {"status": "not_live", "score": score}

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
    row_a = get_team_latest_features(data.team_a)
    row_b = get_team_latest_features(data.team_b)

    def extract(row, team, prefix):
        if row is None:
            return 3, 0.5, 0.5, 1500, 30.0, 8.0
        side = "team1" if row["team1"] == team else "team2"
        return (
            row[f"{side}_rest_days"],
            row[f"{side}_rolling_win_rate"],
            row[f"{side}_venue_win_rate"],
            row[f"{side}_elo"],
            row.get(f"{side}_batting_strength", 30.0),
            row.get(f"{side}_bowling_strength", 8.0),
        )

    a_rest, a_win_rate, a_venue, a_elo, a_bat, a_bowl = extract(row_a, data.team_a, "a")
    b_rest, b_win_rate, b_venue, b_elo, b_bat, b_bowl = extract(row_b, data.team_b, "b")
    venue_avg = row_a["venue_avg_first_innings_score"] if row_a is not None else 162.0

    features = np.array([[
        a_rest, b_rest,
        a_win_rate, b_win_rate,
        a_venue, b_venue,
        venue_avg,
        a_rest - b_rest,
        a_win_rate - b_win_rate,
        a_venue - b_venue,
        a_elo - b_elo,
        a_bat, b_bat,
        a_bowl, b_bowl
    ]])

    prob = prematch_model.predict_proba(features)[0][1]
    return {
        "team_a": data.team_a,
        "team_b": data.team_b,
        "team_a_win_probability": round(float(prob), 4),
        "team_b_win_probability": round(1 - float(prob), 4)
    }