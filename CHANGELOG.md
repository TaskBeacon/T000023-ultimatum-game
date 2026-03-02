# CHANGELOG

## [0.3.1-dev] - 2026-02-19

### Changed
- Refactored trial runtime contract in `src/run_trial.py` to ultimatum-specific unit labels and phases:
  - `cue/anticipation/target/decision_feedback/feedback/inter_trial_interval` -> `offer_cue/pre_decision_fixation/offer_decision/decision_confirmation/payoff_feedback/iti`.
- Added fallback-compatible semantic timing keys in runtime and synced all config profiles:
  - `offer_cue_duration`, `pre_decision_fixation_duration`, `offer_decision_duration`, `decision_confirmation_duration`, `payoff_feedback_duration`.
- Renamed trigger map keys across configs and runtime:
  - `{condition}_offer_cue_onset`, `{condition}_pre_decision_fixation_onset`, `{condition}_offer_decision_onset`, `decision_confirmation_onset`.
- Updated sampler responder decision gating to `offer_decision` (removed legacy `target` dependency) in `responders/task_sampler.py`.
- Updated QA acceptance schema from `target_response` to `offer_decision_response` in `config/config_qa.yaml`.
- Synchronized reference and documentation artifacts (`references/task_logic_audit.md`, `references/parameter_mapping.md`, `README.md`) to the repaired runtime contract.

## [0.3.0-dev] - 2026-02-18

### Changed
- Rebuilt literature evidence artifacts using curated Ultimatum references (`references/references.yaml`, `references/references.md`, `references/selected_papers.json`).
- Rewrote `references/task_logic_audit.md` with a complete, encoding-clean paradigm audit covering state machine, scoring rules, layout, triggers, and inference log.
- Replaced stale stimulus evidence rows in `references/stimulus_mapping.md` so stimulus IDs and citations match the implemented task.
- Replaced auto-generated parameter table with curated protocol mappings in `references/parameter_mapping.md`.
- Updated `README.md` to align metadata, language, trigger documentation, and controller summary with the implemented Chinese task configuration.

## [0.2.0-dev] - 2026-02-18

### Added
- Ultimatum-game controller (`src/utils.py`) with balanced block schedule and earnings tracking.
- Task-specific sampler responder (`responders/task_sampler.py`) using fairness-threshold decision policy.

### Changed
- Replaced MID placeholder trial logic with true ultimatum flow in `src/run_trial.py`: cue -> offer/decision -> decision feedback -> payoff feedback -> iti.
- Updated `main.py` to run planned conditions and report accept-rate / earnings summaries.
- Rebuilt all config profiles (`config.yaml`, `config_qa.yaml`, `config_scripted_sim.yaml`, `config_sampler_sim.yaml`) with Chinese, auditable task parameters.

### Fixed
- Removed incorrect MID adaptive-duration and hit/miss scoring logic from ultimatum task.
