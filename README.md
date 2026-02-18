# Ultimatum Game

![Maturity: draft](https://img.shields.io/badge/Maturity-draft-64748b?style=flat-square&labelColor=111827)

| Field | Value |
|---|---|
| Name | Ultimatum Game |
| Version | v0.3.0-dev |
| URL / Repository | https://github.com/TaskBeacon/T000023-ultimatum-game |
| Short Description | Responder-side accept/reject decisions for fairness-manipulated monetary allocation offers. |
| Created By | TaskBeacon |
| Date Updated | 2026-02-18 |
| PsyFlow Version | 0.1.9 |
| PsychoPy Version | 2025.1.1 |
| Modality | Behavior |
| Language | Chinese |
| Voice Name | zh-CN-YunyangNeural (disabled) |

## 1. Task Overview

This task implements a responder-side Ultimatum Game with three fairness levels (`fair`, `unfair`, `very_unfair`). On each trial, participants observe a proposer/responder split and choose whether to accept or reject the offer.

Accepting yields the displayed responder share. Rejecting or timing out yields zero earnings for that trial. The task records condition, response key, response time, accepted/rejected status, per-trial earnings, and cumulative earnings.

## 2. Task Flow

### Block-Level Flow

| Step | Description |
|---|---|
| 1. Schedule trials | `Controller.prepare_block(...)` creates balanced `fair/unfair/very_unfair` offer sequences and shuffles order within each block. |
| 2. Execute trials | `BlockUnit(...).run_trial(...)` runs trial-level offer/decision logic. |
| 3. Block summary | Acceptance rate and block earnings are displayed. |
| 4. Final summary | Cumulative earnings and final metrics are displayed. |

### Trial-Level Flow

| Step | Description |
|---|---|
| Offer cue | Neutral pre-offer prompt is shown (`offer_cue`). |
| Pre-decision fixation | Central fixation before decision screen. |
| Offer decision | Offer panel displays proposer/responder shares; participant chooses accept (`F`) or reject (`J`) within a fixed response window. |
| Decision confirmation | Selected action (`accept`, `reject`, or `timeout`) is shown. |
| Payoff feedback | Trial payoff and cumulative total are shown. |
| Inter-trial interval | Fixation before next trial. |

### Controller Logic

| Component | Description |
|---|---|
| Offer balancing | Conditions are balanced and randomized per block. |
| Outcome calculation | Maps accept/reject/timeout to trial payoff (`responder_share` or `0`). |
| Aggregation | Tracks acceptance rate and cumulative earnings. |

### Other Logic

| Logic | Description |
|---|---|
| Timeout policy | Missing responses are treated as rejection with zero earnings. |
| Trigger policy | Condition-specific onset triggers for cue/anticipation/decision plus global block/experiment markers. |
| Runtime context phases | `offer_cue`, `pre_decision_fixation`, `offer_decision`, `decision_confirmation`, `payoff_feedback`, `inter_trial_interval`. |

## 3. Configuration Summary

### a. Subject Info

| Field | Meaning |
|---|---|
| `subject_id` | Participant identifier. |
| `subname` | Participant name token. |
| `age` | Participant age. |
| `gender` | Participant gender. |

### b. Window Settings

| Parameter | Value |
|---|---|
| `size` | `[1280, 720]` |
| `units` | `pix` |
| `screen` | `0` |
| `bg_color` | `gray` |
| `fullscreen` | `false` |
| `monitor_width_cm` | `35.5` |
| `monitor_distance_cm` | `60` |

### c. Stimuli

| Name | Type | Description |
|---|---|---|
| `instruction_text` | text | Task instructions and key mapping in Chinese (`font: SimHei`). |
| `offer_cue` | text | Neutral pre-offer cue. |
| `offer_panel` | text | Offer split display (`proposer_share`, `responder_share`). |
| `decision_accept/reject/timeout` | text | Decision confirmation messages. |
| `payoff_feedback` | text | Trial and cumulative earnings summary. |
| `fixation` | text | Center fixation marker for pre-decision and ITI phases. |
| `block_break`, `good_bye` | text | Between-block and final summary screens. |

### d. Timing

| Phase | Duration |
|---|---|
| cue | 0.5 s |
| anticipation | 0.6 s |
| offer | 2.0 s |
| decision_feedback | 0.6 s |
| feedback | 1.0 s |
| iti | 0.8 s |

### e. Triggers

| Trigger Group | Codes |
|---|---|
| Experiment | `exp_onset=1`, `exp_end=2` |
| Block | `block_onset=10`, `block_end=11` |
| Condition cue | `fair=20`, `unfair=21`, `very_unfair=22` |
| Condition anticipation | `fair=23`, `unfair=24`, `very_unfair=25` |
| Condition offer onset | `fair=30`, `unfair=31`, `very_unfair=32` |
| Decision events | `decision_response=50`, `decision_timeout=51`, `decision_feedback_onset=52` |
| Outcome/pacing | `payoff_feedback_onset=53`, `iti_onset=60` |

### f. Adaptive/Controller

| Item | Value |
|---|---|
| Controller seed | `23023` |
| Offer profiles | `fair: 5/5`, `unfair: 7/3`, `very_unfair: 9/1` |
| Block scheduler | Balanced condition counts, randomized trial order |
| Running state | Cumulative earnings and per-condition trial history |

## 4. Methods (for academic publication)

Participants completed a responder-side Ultimatum Game in which each trial presented a monetary split between proposer and responder. Fairness was manipulated across three offer classes, and participants made binary accept/reject decisions under fixed deadlines.

Behavioral outcomes were quantified using acceptance rate, response latency, and earnings trajectories across fairness conditions. Accept decisions yielded the offered responder share, while reject or timeout decisions yielded zero payoff.

The implementation is trigger-annotated and phase-structured to support both standalone behavioral use and synchronized acquisition pipelines (for example EEG/fMRI event locking) without changing core task logic.
