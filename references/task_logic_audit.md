# Task Logic Audit: Ultimatum Game (T000023)

## 1. Paradigm Intent

- Task: `ultimatum_game`
- Primary construct: fairness-sensitive social decision making as the responder in an Ultimatum Game.
- Manipulated factors: offer fairness level via proposer/responder split (`fair`, `unfair`, `very_unfair`).
- Dependent measures: acceptance rate, response time, condition-wise acceptance profile, per-trial and cumulative earnings.
- Key citations: `W2105347098`, `W2166757776`, `W2115247350`, `W2147965914`, `W2128769827`.

## 2. Block/Trial Workflow

### Block Structure

- Total blocks (human): `task.total_blocks = 3`.
- Trials per block (human): `task.trial_per_block = 24`.
- QA/sim profiles shorten to one block of nine trials for fast gate execution.
- Randomization/counterbalancing: `Controller.prepare_block(...)` balances condition counts within each block and shuffles trial order.

### Trial State Machine

1. `offer_cue`
   - Onset trigger: `{condition}_offer_cue_onset` (fallback-compatible with `{condition}_cue_onset`).
   - Stimuli shown: `offer_cue`.
   - Valid keys: none.
   - Timeout behavior: fixed-duration display.
   - Next state: `pre_decision_fixation`.
2. `pre_decision_fixation`
   - Onset trigger: `{condition}_pre_decision_fixation_onset` (fallback-compatible with `{condition}_anticipation_onset`).
   - Stimuli shown: `fixation`.
   - Valid keys: none.
   - Timeout behavior: fixed-duration display.
   - Next state: `offer_decision`.
3. `offer_decision`
   - Onset trigger: `{condition}_offer_decision_onset` (fallback-compatible with `{condition}_offer_onset`).
   - Stimuli shown: `offer_panel` (proposer/responder shares).
   - Valid keys: `f` (accept), `j` (reject).
   - Timeout behavior: missing response is treated as rejection; timeout trigger `decision_timeout`.
   - Next state: `decision_confirmation`.
4. `decision_confirmation`
   - Onset trigger: `decision_confirmation_onset` (fallback-compatible with `decision_feedback_onset`).
   - Stimuli shown: `decision_accept` or `decision_reject` or `decision_timeout`.
   - Valid keys: none.
   - Timeout behavior: fixed-duration display.
   - Next state: `payoff_feedback`.
5. `payoff_feedback`
   - Onset trigger: `payoff_feedback_onset`.
   - Stimuli shown: `payoff_feedback`.
   - Valid keys: none.
   - Timeout behavior: fixed-duration display.
   - Next state: `iti`.
6. `iti`
   - Onset trigger: `iti_onset`.
   - Stimuli shown: `fixation`.
   - Valid keys: none.
   - Timeout behavior: fixed-duration display.
   - Next state: next trial or block end.

Block boundaries emit `block_onset` and `block_end`. Experiment boundaries emit `exp_onset` and `exp_end`.

## 3. Condition Semantics

- Condition ID: `fair`
  - Participant-facing meaning: equal split offer.
  - Concrete stimulus realization: proposer `5`, responder `5` rendered in `offer_panel`.
  - Outcome rules: accept yields `5`; reject/timeout yields `0`.
- Condition ID: `unfair`
  - Participant-facing meaning: moderately unfair split against the responder.
  - Concrete stimulus realization: proposer `7`, responder `3` rendered in `offer_panel`.
  - Outcome rules: accept yields `3`; reject/timeout yields `0`.
- Condition ID: `very_unfair`
  - Participant-facing meaning: highly unfair split against the responder.
  - Concrete stimulus realization: proposer `9`, responder `1` rendered in `offer_panel`.
  - Outcome rules: accept yields `1`; reject/timeout yields `0`.

## 4. Response and Scoring Rules

- Response mapping: `f` = accept, `j` = reject.
- Missing-response policy: timeout is logged and handled as rejection (`earned = 0`).
- Correctness logic: no objective correctness; decisions reflect preference under fairness manipulation.
- Reward updates: `earned = responder_share` for accepted offers, else `0`.
- Running metrics: `controller.total_earned` is cumulative; block summaries report acceptance rate and block earnings.

## 5. Stimulus Layout Plan

- Screen: `instruction_text`
  - Stimulus IDs shown: `instruction_text`.
  - Layout: single centered text object (`wrapWidth=980`, `height=28`, `font=SimHei`).
  - Rationale: dense instruction content remains legible without overlap.
- Screen: `offer_cue`
  - Stimulus IDs shown: `offer_cue`.
  - Layout: single centered text object (`wrapWidth=980`, `height=34`).
  - Rationale: neutral pre-decision prompt without fairness-token leakage.
- Screen: `offer_decision`
  - Stimulus IDs shown: `offer_panel`.
  - Layout: single centered multi-line text object (`wrapWidth=980`, `height=40`) with separate lines for proposer and responder shares.
  - Rationale: preserves clear offer structure while enforcing a single decision focus.
- Screen: feedback and summaries
  - Stimulus IDs shown: `decision_*`, `payoff_feedback`, `block_break`, `good_bye`.
  - Layout: single centered text objects with controlled wrap and line spacing by explicit `height` + `wrapWidth`.
  - Rationale: minimizes overlap risk across 1280x720 QA/human windows.

QA logs show these single-text layouts render without overlap warnings for participant-facing elements.

## 6. Trigger Plan

- Experiment: `exp_onset=1`, `exp_end=2`.
- Block: `block_onset=10`, `block_end=11`.
- Offer-cue onsets: `fair=20`, `unfair=21`, `very_unfair=22`.
- Pre-decision fixation onsets: `fair=23`, `unfair=24`, `very_unfair=25`.
- Offer-decision onsets: `fair=30`, `unfair=31`, `very_unfair=32`.
- Decision events: `decision_response=50`, `decision_timeout=51`, `decision_confirmation_onset=52`.
- Payoff and ITI: `payoff_feedback_onset=53`, `iti_onset=60`.

## 7. Inference Log

- Decision: include three fairness bins (`fair`, `unfair`, `very_unfair`) with fixed 10-point budget splits.
  - Why inference was required: selected papers vary in exact offer sets across studies.
  - Citation-supported rationale: fairness-gradient acceptance behavior is central across UG references (`W2166757776`, `W2128769827`, `W2147965914`).
- Decision: include pre-offer cue and anticipation phase before response.
  - Why inference was required: timing structure differs between behavioral-only and neuroimaging implementations.
  - Citation-supported rationale: phase-separated trial timing aligns with neuroimaging-ready UG designs (`W2115247350`) while preserving responder offer-decision core.
- Decision: timeout treated as rejection.
  - Why inference was required: not all references explicitly define timeout policy.
  - Citation-supported rationale: responder payout logic in UG requires explicit reject-equivalent handling for non-responses in fixed-window computerized tasks.
- Decision: runtime output keys use ultimatum-specific unit labels (`offer_decision_*`, `decision_confirmation_*`, `payoff_feedback_*`) instead of template labels (`target_*`, `decision_feedback_*`).
  - Why inference was required: this is an implementation contract decision, not a paradigm manipulation.
  - Citation-supported rationale: preserves paradigm semantics while removing MID-template residue from event/data schemas.
