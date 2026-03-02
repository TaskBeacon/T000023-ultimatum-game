# Task Logic Audit: Ultimatum Game (T000023)

## 1. Paradigm Intent

- Task: `ultimatum_game`
- Primary construct: fairness-sensitive social decision making in the responder role.
- Manipulated factors: proposer-responder split fairness (`fair`, `unfair`, `very_unfair`).
- Dependent measures: acceptance rate, response time, condition-wise acceptance profile, trial earnings, cumulative earnings.
- Key citations: `W2105347098`, `W2166757776`, `W2115247350`, `W2147965914`, `W2128769827`.

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: `3` in human mode; `1` in QA/sim modes.
- Trials per block: `24` in human mode; `9` in QA/sim modes.
- Randomization/counterbalancing: per-block condition list is balanced and shuffled by `Controller.prepare_block(...)`.
- Condition generation method:
  - Custom generator via `Controller.prepare_block(...)`.
  - Rationale: each trial needs pre-expanded proposer/responder shares and a reproducible `condition_id` tuple payload.
  - Generated condition data shape: `(condition, condition_label, proposer_share, responder_share, condition_id, trial_index)`.
- Runtime-generated trial values (if any):
  - Generated in `run_trial.py`: `accepted`, `rejected`, `timed_out`, `earned`, `total_earned`, and formatted outcome-dependent stimulus selection.
  - Determinism: block scheduling is seeded (`controller.seed`) and sim responders are seed-driven.

### Trial State Machine

1. `offer_cue`
   - Onset trigger: `{condition}_offer_cue_onset`
   - Stimuli shown: `offer_cue`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `pre_decision_fixation`
2. `pre_decision_fixation`
   - Onset trigger: `{condition}_pre_decision_fixation_onset`
   - Stimuli shown: `fixation`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `offer_decision`
3. `offer_decision`
   - Onset trigger: `{condition}_offer_decision_onset`
   - Stimuli shown: `offer_panel`
   - Valid keys: accept/reject keys from `task.key_list`
   - Timeout behavior: no response emits `decision_timeout`, handled as reject
   - Next state: `decision_confirmation`
4. `decision_confirmation`
   - Onset trigger: `decision_confirmation_onset`
   - Stimuli shown: one of `decision_accept`, `decision_reject`, `decision_timeout`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `payoff_feedback`
5. `payoff_feedback`
   - Onset trigger: `payoff_feedback_onset`
   - Stimuli shown: `payoff_feedback`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: `inter_trial_interval`
6. `inter_trial_interval`
   - Onset trigger: `iti_onset`
   - Stimuli shown: `fixation`
   - Valid keys: none
   - Timeout behavior: fixed-duration display
   - Next state: next trial or block end

## 3. Condition Semantics

- Condition ID: `fair`
- Participant-facing meaning: equal split offer.
- Concrete stimulus realization (visual/audio): `offer_panel` renders proposer `5`, responder `5`.
- Outcome rules: accept -> responder earns `5`; reject/timeout -> `0`.

- Condition ID: `unfair`
- Participant-facing meaning: moderately unfair split against responder.
- Concrete stimulus realization (visual/audio): `offer_panel` renders proposer `7`, responder `3`.
- Outcome rules: accept -> responder earns `3`; reject/timeout -> `0`.

- Condition ID: `very_unfair`
- Participant-facing meaning: strongly unfair split against responder.
- Concrete stimulus realization (visual/audio): `offer_panel` renders proposer `9`, responder `1`.
- Outcome rules: accept -> responder earns `1`; reject/timeout -> `0`.

Also document where participant-facing condition text/stimuli are defined:

- Participant-facing text source (config stimuli / code formatting / generated assets): config stimuli in `config/*.yaml`, with dynamic values inserted through `stim_bank.get_and_format(...)`.
- Why this source is appropriate for auditability: wording is centralized and visible in configuration artifacts.
- Localization strategy (how language variants are swapped via config without code edits): localized YAML config variants can replace all participant-facing text while `src/run_trial.py` remains unchanged.

## 4. Response and Scoring Rules

- Response mapping: first key in `task.key_list` = accept, second key = reject.
- Response key source (config field vs code constant): config field `task.key_list`.
- If code-defined, why config-driven mapping is not sufficient: not applicable.
- Missing-response policy: timeout in `offer_decision` is treated as reject.
- Correctness logic: no objective correctness; decision preference under fairness manipulation is measured.
- Reward/penalty updates: accept yields `responder_share`; reject/timeout yields `0`.
- Running metrics: controller tracks block-level and cumulative earnings plus condition-level decision history.

## 5. Stimulus Layout Plan

For every screen with multiple simultaneous options/stimuli:

- Screen name: `offer_decision`
- Stimulus IDs shown together: `offer_panel` (multi-line single object)
- Layout anchors (`pos`): centered (default text anchor)
- Size/spacing (`height`, width, wrap): `height=40`, `wrapWidth=980`
- Readability/overlap checks: QA run verifies full text visibility at `1280x720`
- Rationale: single focal panel minimizes scan complexity during timed decisions

- Screen name: `payoff_feedback`
- Stimulus IDs shown together: `payoff_feedback` (multi-line single object)
- Layout anchors (`pos`): centered
- Size/spacing (`height`, width, wrap): `height=38`, `wrapWidth=980`
- Readability/overlap checks: QA run verifies no clipping at `1280x720`
- Rationale: compact summary of trial and cumulative payoff

## 6. Trigger Plan

- Experiment boundaries: `exp_onset=1`, `exp_end=2`
- Block boundaries: `block_onset=10`, `block_end=11`
- Offer cue onsets: `fair=20`, `unfair=21`, `very_unfair=22`
- Pre-decision fixation onsets: `fair=23`, `unfair=24`, `very_unfair=25`
- Offer decision onsets: `fair=30`, `unfair=31`, `very_unfair=32`
- Decision events: `decision_response=50`, `decision_timeout=51`, `decision_confirmation_onset=52`
- Outcome and pacing: `payoff_feedback_onset=53`, `iti_onset=60`

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style (simple single flow / helper-heavy / why): simple mode-aware single flow (`human|qa|sim`) to keep execution path auditable.
- `utils.py` used? (yes/no): yes.
- If yes, exact purpose (adaptive controller / sequence generation / asset pool / other): sequence generation and payoff/history bookkeeping for UG condition scheduling.
- Custom controller used? (yes/no): yes.
- If yes, why PsyFlow-native path is insufficient: condition tuples need deterministic embedded share values and stable condition IDs for traceable trial logs.
- Legacy/backward-compatibility fallback logic required? (yes/no): no.
- If yes, scope and removal plan: not applicable.

## 8. Inference Log

- Decision: include `very_unfair` (`9/1`) condition in addition to fair/unfair.
- Why inference was required: references vary in exact offer sets and not all include identical three-bin gradients.
- Citation-supported rationale: unfairness-gradient manipulations are central to UG acceptance/rejection effects (`W2166757776`, `W2147965914`).

- Decision: use deterministic timeout-as-reject scoring.
- Why inference was required: timeout behavior is not consistently specified across cited implementations.
- Citation-supported rationale: reject-equivalent non-accept outcomes preserve UG payoff semantics (`W2128769827`).

- Decision: maintain explicit `decision_confirmation` phase between choice and payoff.
- Why inference was required: stage granularity differs across behavioral vs imaging-focused reports.
- Citation-supported rationale: phase-separated timing is consistent with event-structured UG implementations (`W2115247350`).
