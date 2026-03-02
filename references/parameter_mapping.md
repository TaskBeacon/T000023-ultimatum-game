# Parameter Mapping

| Parameter | Implemented Value | Source Paper ID | Confidence | Rationale |
|---|---|---|---|---|
| `task.task_name` | `ultimatum_game` | `W2128769827` | `direct` | Canonical two-player ultimatum bargaining paradigm identity. |
| `task.conditions` | `['fair', 'unfair', 'very_unfair']` | `W2166757776`, `W2147965914` | `inferred` | Fairness-gradient manipulation consistent with UG offer inequity literature. |
| `controller.offer_profiles.fair` | `proposer=5, responder=5` | `W2166757776`, `W2128769827` | `direct` | Equal split used as fairness baseline in responder decisions. |
| `controller.offer_profiles.unfair` | `proposer=7, responder=3` | `W2166757776`, `W2147965914` | `direct` | Moderately unfair split used to probe rejection behavior. |
| `controller.offer_profiles.very_unfair` | `proposer=9, responder=1` | `W2147965914`, `W2115247350` | `inferred` | Strong unfairness extension for broader dynamic range in acceptance behavior. |
| `task.key_list` | `['f', 'j']` | `W2115247350` | `inferred` | Binary accept/reject keyboard mapping for desktop PsychoPy deployment. |
| `task.total_blocks` | `3` | `W2105347098` | `inferred` | Multi-block structure chosen for stable condition-wise estimates. |
| `task.trial_per_block` | `24` | `W2105347098`, `W2166757776` | `inferred` | Balanced per-block condition counts with practical session length. |
| `task.total_trials` | `72` | `W2105347098`, `W2166757776` | `inferred` | Three blocks x 24 trials for fairness-stratified acceptance analysis. |
| `timing.offer_cue_duration` | `0.5` | `W2115247350` | `inferred` | Short pre-offer cue for phase separation in trigger-aligned pipelines. |
| `timing.pre_decision_fixation_duration` | `0.6` | `W2115247350` | `inferred` | Pre-decision fixation interval to isolate offer-response stage onset. |
| `timing.offer_decision_duration` | `2.0` | `W2115247350`, `W2147965914` | `inferred` | Fixed response window for accept/reject decision capture. |
| `timing.decision_confirmation_duration` | `0.6` | `W2115247350` | `inferred` | Brief confirmation before payoff stage. |
| `timing.payoff_feedback_duration` | `1.0` | `W2115247350`, `W2147965914` | `inferred` | Dedicated payoff display for outcome encoding and cumulative tracking. |
| `timing.iti_duration` | `0.8` | `W2115247350` | `inferred` | Inter-trial pacing for event separation. |
| `run_trial.timeout_policy` | `timeout -> reject -> earned=0` | `W2128769827` | `inferred` | Non-response mapped to reject-equivalent economic outcome for deterministic scoring. |
| `triggers.map.exp_onset/exp_end` | `1/2` | `inferred` | `inferred` | Standard experiment boundary markers. |
| `triggers.map.block_onset/block_end` | `10/11` | `inferred` | `inferred` | Standard block boundary markers. |
| `triggers.map.{condition}_offer_cue_onset` | `20/21/22` | `inferred` | `inferred` | Condition-specific offer-cue encoding for downstream event parsing. |
| `triggers.map.{condition}_pre_decision_fixation_onset` | `23/24/25` | `inferred` | `inferred` | Condition-specific pre-decision fixation encoding. |
| `triggers.map.{condition}_offer_decision_onset` | `30/31/32` | `inferred` | `inferred` | Condition-specific offer-decision onset encoding. |
| `triggers.map.decision_response/timeout` | `50/51` | `inferred` | `inferred` | Response-vs-timeout event separation during decision stage. |
| `triggers.map.decision_confirmation_onset` | `52` | `inferred` | `inferred` | Decision confirmation onset marker. |
| `triggers.map.payoff_feedback_onset` | `53` | `inferred` | `inferred` | Outcome/payout feedback onset marker. |
| `triggers.map.iti_onset` | `60` | `inferred` | `inferred` | ITI onset marker for trial segmentation. |
