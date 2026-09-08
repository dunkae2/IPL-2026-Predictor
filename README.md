# IPL 2026 Predictor

An end-to-end IPL match outcome predictor built with **CatBoost**, dynamic **ELO ratings**, walk-forward validation, and a **FastAPI** backend for live and pre-match predictions.

The project turns historical IPL data into continuously updated team-strength features, then serves model predictions through an API and frontend experience.

## Features

* Pre-match winner predictions for IPL fixtures
* Live win-probability updates during matches
* CatBoost classifier trained on match and team-performance features
* Dynamic ELO ratings to capture changing team strength
* Walk-forward validation to evaluate predictions without future-data leakage
* Player and innings-level features
* FastAPI backend for serving predictions
* Frontend for interacting with predictions
* Automated pipeline for updating data and model inputs

## How It Works

### 1. Historical match data

Historical IPL match data is cleaned and transformed into model-ready datasets. Features capture team performance, match context, venue information, innings state, and player-level signals.

### 2. ELO ratings

Each team has an ELO rating that changes after every match. Beating a highly rated team produces a larger rating gain than beating a lower-rated team, allowing the model to reflect current relative strength rather than relying only on season averages.

### 3. CatBoost model

CatBoost is used to predict the match winner from structured features, including team ELO, recent performance, venue context, and live innings information when available.

### 4. Walk-forward validation

Rather than randomly splitting historical matches, the model is trained on earlier matches and evaluated on later matches. This better simulates real-world deployment, where the model must predict games it has not yet seen.

## Tech Stack

* **Python**
* **CatBoost**
* **Pandas and NumPy**
* **Scikit-learn**
* **FastAPI**
* **Uvicorn**
* **Jupyter Notebooks**
* **JavaScript frontend**
* **ELO rating system**

## Repository Structure

```text
IPL-2026-Predictor/
├── catboost_info/      # CatBoost training outputs and logs
├── data/               # Raw and processed IPL data
├── docs/               # Project documentation
├── frontend/           # Prediction user interface
├── models/             # Saved model artifacts
├── notebooks/          # Exploratory analysis and experiments
├── src/                # Data processing, features, training, and API logic
├── .env                # Local environment variables
└── run_api.py          # FastAPI application entry point
```

## Getting Started

### Clone the repository

```bash
git clone https://github.com/vishnutumuluru/IPL-2026-Predictor.git
cd IPL-2026-Predictor
```

### Create a virtual environment

```bash
python -m venv .venv
```

Mac/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the API

```bash
python run_api.py
```

After starting the server, open the FastAPI documentation at:

```text
http://127.0.0.1:8000/docs
```

## Example Use Cases

### Pre-match prediction

Given two teams and match context, the model estimates each team’s chance of winning before the first ball is bowled.

### Live prediction

As a match progresses, live features such as score, overs, wickets, target, current run rate, and required run rate can be used to update the predicted win probability.

## Key Machine Learning Concepts Demonstrated

* Feature engineering from real sports data
* Time-aware model evaluation
* Prevention of data leakage
* Gradient-boosted classification with CatBoost
* Dynamic ELO rating systems
* Model serialization and API deployment
* Building ML systems for real-time inference

## Future Improvements

* Add richer player-level batting and bowling features
* Incorporate pitch, weather, and toss information
* Calibrate predicted probabilities
* Add automated retraining after completed matches
* Deploy the API and frontend to the cloud
* Add model monitoring and live accuracy tracking during the IPL season

## Disclaimer

This project is built for educational and analytical purposes. Predictions are probabilistic estimates, not guarantees, and should not be used as betting advice.
