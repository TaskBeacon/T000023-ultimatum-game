# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `task_name` | `task.task_name` | `ultimatum_game` | `W2128769827` | Canonical Ultimatum Game responder paradigm identity. | `direct` | Task identity follows established UG protocol family. |
| `conditions` | `task.conditions` | `fair, unfair, very_unfair` | `W2166757776`, `W2147965914` | Fairness-gradient manipulation in UG responder decisions. | `adapted` | Three-level fairness bins used for stable condition contrasts. |
| `offer_profile_fair` | `controller.offer_profiles.fair` | `proposer=5, responder=5` | `W2166757776`, `W2128769827` | Equal split as fairness baseline in UG behavior. | `direct` | Baseline high-accept condition. |
| `offer_profile_unfair` | `controller.offer_profiles.unfair` | `proposer=7, responder=3` | `W2166757776`, `W2147965914` | Unfair split used to probe rejection sensitivity. | `direct` | Mid-level unfairness condition. |
| `offer_profile_very_unfair` | `controller.offer_profiles.very_unfair` | `proposer=9, responder=1` | `W2147965914`, `W2115247350` | Strongly unfair offers increase rejection pressure. | `inferred` | Added as high-inequity extension for range coverage. |
| `response_keys` | `task.key_list` | `f=accept, j=reject` | `W2115247350` | Binary forced-choice responder action. | `adapted` | Keyboard mapping adapted for desktop PsychoPy runtime. |
| `total_blocks_human` | `task.total_blocks` | `3` | `W2105347098` | Multi-block sampling improves estimate stability. | `inferred` | Practical session length vs. condition balance tradeoff. |
| `trials_per_block_human` | `task.trial_per_block` | `24` | `W2105347098`, `W2166757776` | Repeated fairness judgments across trials. | `inferred` | Balanced schedule for three conditions. |
| `total_trials_human` | `task.total_trials` | `72` | `W2105347098`, `W2166757776` | Sufficient trial count for condition-wise acceptance rates. | `inferred` | Derived as `3 x 24`. |
| `offer_cue_duration` | `timing.offer_cue_duration` | `0.5` | `W2115247350` | Distinct pre-offer phase in phase-separated UG implementations. | `adapted` | Maintains clean stage separation for triggers. |
| `pre_decision_fixation_duration` | `timing.pre_decision_fixation_duration` | `0.6` | `W2115247350` | Pre-decision fixation supports event isolation. | `adapted` | Used before offer presentation. |
| `offer_decision_duration` | `timing.offer_decision_duration` | `2.0` | `W2115247350`, `W2147965914` | Fixed responder decision window in computerized UG tasks. | `adapted` | Supports timeout handling in runtime. |
| `decision_confirmation_duration` | `timing.decision_confirmation_duration` | `0.6` | `W2115247350` | Brief post-choice confirmation phase. | `adapted` | Separate phase for choice acknowledgement. |
| `payoff_feedback_duration` | `timing.payoff_feedback_duration` | `1.0` | `W2115247350`, `W2147965914` | Outcome display stage after responder decision. | `adapted` | Shows trial earning and cumulative earning. |
| `iti_duration` | `timing.iti_duration` | `0.8` | `W2115247350` | Inter-trial interval for temporal separation. | `adapted` | Fixed ITI for reproducibility. |
| `timeout_policy` | `src/run_trial.py` | `timeout -> reject -> earned=0` | `W2128769827` | UG reject outcome implies no payout for responder. | `inferred` | Deterministic non-response handling for simulation and audit. |
| `exp_onset` | `triggers.map.exp_onset` | `1` | `inferred` | Standard experiment-boundary event coding. | `inferred` | Framework event marker. |
| `exp_end` | `triggers.map.exp_end` | `2` | `inferred` | Standard experiment-boundary event coding. | `inferred` | Framework event marker. |
| `block_onset` | `triggers.map.block_onset` | `10` | `inferred` | Block-level boundary marker. | `inferred` | Framework event marker. |
| `block_end` | `triggers.map.block_end` | `11` | `inferred` | Block-level boundary marker. | `inferred` | Framework event marker. |
| `offer_cue_onsets` | `triggers.map.{condition}_offer_cue_onset` | `fair=20, unfair=21, very_unfair=22` | `inferred` | Condition-resolved stage onset coding. | `inferred` | Enables per-condition cue epoch extraction. |
| `pre_decision_fixation_onsets` | `triggers.map.{condition}_pre_decision_fixation_onset` | `fair=23, unfair=24, very_unfair=25` | `inferred` | Condition-resolved stage onset coding. | `inferred` | Supports clean stage segmentation. |
| `offer_decision_onsets` | `triggers.map.{condition}_offer_decision_onset` | `fair=30, unfair=31, very_unfair=32` | `inferred` | Condition-resolved decision onset coding. | `inferred` | Used with `decision_response`/`decision_timeout`. |
| `decision_response` | `triggers.map.decision_response` | `50` | `inferred` | Response event marker. | `inferred` | Choice key captured in same phase. |
| `decision_timeout` | `triggers.map.decision_timeout` | `51` | `inferred` | Timeout event marker. | `inferred` | Mirrors non-response policy. |
| `decision_confirmation_onset` | `triggers.map.decision_confirmation_onset` | `52` | `inferred` | Post-choice confirmation onset marker. | `inferred` | Matches explicit confirmation phase. |
| `payoff_feedback_onset` | `triggers.map.payoff_feedback_onset` | `53` | `inferred` | Outcome display onset marker. | `inferred` | For payout-phase segmentation. |
| `iti_onset` | `triggers.map.iti_onset` | `60` | `inferred` | Inter-trial interval onset marker. | `inferred` | Trial boundary anchor. |
