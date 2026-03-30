# Data Audit Summary

## Dataset Overview

Match_Info.csv:
- 1169 rows
- 14 columns

Ball_By_Ball_Match_Data.csv:
- 278205 rows
- 16 columns

The match IDs appear to align correctly across both datasets.

## Match Outcome Findings

The result column contains:
- Win
- tie
- no result

For tied matches, the winner column is missing, but the eliminator column identifies the official winning team.

For no-result matches, there is no official winner, so those rows should be excluded from supervised model training.

## Leakage-Risk Columns

Unsafe for pre-toss prediction:
- toss_winner
- toss_decision
- result
- winner
- eliminator
- player_of_match
- team1_players
- team2_players

These columns are either unavailable before toss or directly reflect the match outcome.

## Main Cleaning Needs

Observed issues that will need cleaning later:
- team/franchise name changes across seasons
- venue naming inconsistencies
- city missing values
- possible player name normalization issues

## Sprint 1 Decisions

- MVP will start as a pre-toss model
- no-result matches will be excluded from training
- tie matches will use eliminator as the official winner
- toss columns will not be used in pre-toss features
- player list columns will not be used in the pre-toss MVP