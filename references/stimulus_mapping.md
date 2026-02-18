# Stimulus Mapping

Task: `Ultimatum Game`

| Condition | Implemented Stimulus IDs | Source Paper ID | Evidence (quote/figure/table) | Implementation Mode | Notes |
|---|---|---|---|---|---|
| `fair` | `offer_cue`, `offer_panel`, `decision_accept/reject/timeout`, `payoff_feedback` | `W2166757776`, `W2128769827` | UG responder receives monetary split and can accept/reject; fair offers serve as high-acceptance baseline. | `psychopy_builtin` | Implemented as proposer/responder split `5/5` in `controller.offer_profiles.fair`. |
| `unfair` | `offer_cue`, `offer_panel`, `decision_accept/reject/timeout`, `payoff_feedback` | `W2166757776`, `W2147965914` | Unfair offers drive elevated rejection rates in canonical UG responder tasks. | `psychopy_builtin` | Implemented as split `7/3` in `controller.offer_profiles.unfair`. |
| `very_unfair` | `offer_cue`, `offer_panel`, `decision_accept/reject/timeout`, `payoff_feedback` | `W2147965914`, `W2115247350` | Strongly disadvantageous offers are commonly used in neuroeconomic UG paradigms to amplify unfairness sensitivity. | `psychopy_builtin` | Implemented as split `9/1`; marked as an inferred extension of unfair-offer manipulation. |
| Shared trial scaffolding | `fixation`, `instruction_text`, `block_break`, `good_bye` | `inferred` | Standard pacing/instruction scaffolding for computerized UG implementation. | `psychopy_builtin` | Non-decision scaffolding does not expose condition tokens directly. |

Implementation mode legend:
- `psychopy_builtin`: stimulus rendered via PsychoPy primitives in config.
- `generated_reference_asset`: task-specific synthetic assets generated from reference-described stimulus rules.
- `licensed_external_asset`: externally sourced licensed media with protocol linkage.
