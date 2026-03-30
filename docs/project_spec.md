# IPL 2026 Match Predictor - Project Spec

## Objective

Build a machine learning project that predicts the probability of one IPL team beating another.

The broader project will be designed as a multi-stage match prediction system with different prediction settings:
- pre-toss prediction
- post-toss prediction
- live in-match win probability later

The first version of the project will focus on pre-toss prediction, meaning the model should only use information that would realistically be known before the toss.

The goal is to create a strong portfolio-quality sports analytics and machine learning project that emphasizes leakage prevention, time-aware evaluation, feature engineering, calibration, and explainability.

## Planned Project Phases

The project is planned in three modeling stages:

1. Pre-toss model
   - predicts match winner probability before the toss
   - uses only information available before toss

2. Post-toss model
   - updates win probability after toss
   - can use toss winner, toss decision, and possibly confirmed playing XI if available

3. Live in-match win probability model
   - planned as a later extension
   - would update win probability during the match using match-state information such as score, wickets, overs, and chase context

These three stages are part of the overall project roadmap, but they will not all be built at once.

## First Model Version

The first model version will be a pre-toss match winner predictor.

This means:
- the prediction is made before the toss
- toss information is not allowed as input
- actual playing XI is not assumed to be known
- only past historical information can be used

The pre-toss model is the MVP because it is the cleanest starting point for defining the task, preventing leakage, and building the project foundation correctly.

## Prediction Target

Each row in the final modeling dataset will represent one past IPL match.

The target will be:
- team_a_win = 1 if Team A officially won the match
- team_a_win = 0 if Team B officially won the match

Team A and Team B assignment will be defined later during dataset construction.

## Match Inclusion Rules

Include:
- matches with result = "Win"
- matches with result = "tie" if there is an eliminator winner

Exclude:
- matches with result = "no result"

Official winner logic:
- if result = "Win", use winner
- if result = "tie", use eliminator
- if result = "no result", exclude from training

## Allowed Inputs for Pre-Toss Model

Allowed:
- teams
- match date
- season
- venue
- city
- historical team performance
- historical batting and bowling features
- historical venue-based features
- recency-weighted features built only from past matches

## Forbidden Inputs for Pre-Toss Model

Not allowed:
- toss_winner
- toss_decision
- result
- winner
- eliminator
- player_of_match
- any ball-by-ball data from the current match
- actual match-day player list columns unless they are proven to be realistic pre-toss inputs

## MVP Scope

The MVP will include:
- pre-toss prediction only
- leakage-safe feature engineering
- time-aware validation
- baseline models
- one strong tree-based model
- calibrated probabilities
- explainability

The MVP is intended to create a strong and reliable project foundation before adding post-toss and live in-match prediction stages.

## Deferred for Later

Not part of Sprint 1 or the MVP:
- post-toss model implementation
- expected XI model
- live win probability model
- automated external player enrichment
- full deployment pipeline

## Planned Next Versions

After the MVP is complete, the next planned extensions are:

1. Post-toss model
   - add toss winner and toss decision
   - compare performance against pre-toss model
   - optionally incorporate confirmed or expected lineups

2. Live in-match model
   - treat this as a separate later sprint
   - use current match state such as score, wickets, overs, and required run rate
   - evaluate it separately from the pre-match models