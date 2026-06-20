from __future__ import annotations

from functools import partial
from psyflow import StimUnit, next_trial_id, resolve_deadline, set_trial_context

from .utils import parse_ultimatum_condition


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one Ultimatum Game trial."""
    parsed = parse_ultimatum_condition(condition)
    block_idx_val = int(block_idx) if block_idx is not None else 0
    trial_index = int(parsed["trial_index"]) if parsed["trial_index"] > 0 else 1
    trial_id = next_trial_id()
    accept_key, reject_key = list(settings.key_list)

    trial_data = {
        "trial_id": trial_id,
        "trial_index": trial_index,
        "block_id": str(block_id) if block_id is not None else "block_0",
        "block_idx": block_idx_val,
        "condition": parsed["condition"],
        "condition_id": parsed["condition_id"],
        "condition_label": parsed["condition_label"],
        "proposer_share": int(parsed["proposer_share"]),
        "responder_share": int(parsed["responder_share"]),
    }
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)

    cue = make_unit(unit_label="offer_cue").add_stim(stim_bank.get("offer_cue"))
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="offer_cue",
        deadline_s=resolve_deadline(settings.offer_cue_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={"stage": "offer_cue", "condition": parsed["condition"], "block_idx": block_idx_val},
        stim_id="offer_cue",
    )
    cue.show(
        duration=settings.offer_cue_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_offer_cue_onset"),
    ).to_dict(trial_data)

    pre_decision_fixation = make_unit(unit_label="pre_decision_fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        pre_decision_fixation,
        trial_id=trial_id,
        phase="pre_decision_fixation",
        deadline_s=resolve_deadline(settings.pre_decision_fixation_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={"stage": "pre_decision_fixation", "condition": parsed["condition"], "block_idx": block_idx_val},
        stim_id="fixation",
    )
    pre_decision_fixation.show(
        duration=settings.pre_decision_fixation_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_pre_decision_fixation_onset"),
    ).to_dict(trial_data)

    decision = make_unit(unit_label="offer_decision").add_stim(
        stim_bank.get_and_format(
            "offer_panel",
            proposer_share=int(parsed["proposer_share"]),
            responder_share=int(parsed["responder_share"]),
        )
    )
    set_trial_context(
        decision,
        trial_id=trial_id,
        phase="offer_decision",
        deadline_s=resolve_deadline(settings.offer_decision_duration),
        valid_keys=[accept_key, reject_key],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "offer_decision",
            "condition": parsed["condition"],
            "proposer_share": int(parsed["proposer_share"]),
            "responder_share": int(parsed["responder_share"]),
            "accept_key": accept_key,
            "reject_key": reject_key,
            "block_idx": block_idx_val,
        },
        stim_id="offer_panel",
    )
    decision.capture_response(
        keys=[accept_key, reject_key],
        duration=settings.offer_decision_duration,
        onset_trigger=settings.triggers.get(f"{parsed['condition']}_offer_decision_onset"),
        response_trigger=settings.triggers.get("decision_response"),
        timeout_trigger=settings.triggers.get("decision_timeout"),
    )
    decision.to_dict(trial_data)

    response = decision.get_state("response")
    accepted = bool(response == accept_key)
    rejected = bool(response == reject_key)
    timed_out = not (accepted or rejected)
    choice_label = "accept" if accepted else "reject" if rejected else "timeout"
    earned = int(parsed["responder_share"]) if accepted else 0
    total_earned = controller.register_decision(
        condition=parsed["condition"],
        block_idx=block_idx_val,
        trial_index=trial_index,
        choice=choice_label,
        accepted=accepted,
        earned=earned,
        proposer_share=int(parsed["proposer_share"]),
        responder_share=int(parsed["responder_share"]),
    )

    decision_confirmation_stim_id = "decision_accept" if accepted else "decision_reject" if rejected else "decision_timeout"
    decision_feedback = make_unit(unit_label="decision_confirmation").add_stim(
        stim_bank.get_and_format(decision_confirmation_stim_id, choice_label=choice_label)
    )
    set_trial_context(
        decision_feedback,
        trial_id=trial_id,
        phase="decision_confirmation",
        deadline_s=resolve_deadline(settings.decision_confirmation_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "decision_confirmation",
            "choice_label": choice_label,
            "accepted": accepted,
            "timed_out": timed_out,
            "block_idx": block_idx_val,
        },
        stim_id=decision_confirmation_stim_id,
    )
    decision_feedback.show(
        duration=settings.decision_confirmation_duration,
        onset_trigger=settings.triggers.get("decision_confirmation_onset"),
    ).to_dict(trial_data)

    payoff = make_unit(unit_label="payoff_feedback").add_stim(
        stim_bank.get_and_format(
            "payoff_feedback",
            earned=earned,
            total_earned=total_earned,
            proposer_share=int(parsed["proposer_share"]),
            responder_share=int(parsed["responder_share"]),
        )
    )
    set_trial_context(
        payoff,
        trial_id=trial_id,
        phase="payoff_feedback",
        deadline_s=resolve_deadline(settings.payoff_feedback_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={
            "stage": "payoff_feedback",
            "accepted": accepted,
            "earned": earned,
            "total_earned": total_earned,
            "block_idx": block_idx_val,
        },
        stim_id="payoff_feedback",
    )
    payoff.show(
        duration=settings.payoff_feedback_duration,
        onset_trigger=settings.triggers.get("payoff_feedback_onset"),
    ).to_dict(trial_data)

    iti = make_unit(unit_label="iti").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        iti,
        trial_id=trial_id,
        phase="inter_trial_interval",
        deadline_s=resolve_deadline(settings.iti_duration),
        valid_keys=[],
        block_id=trial_data["block_id"],
        condition_id=parsed["condition_id"],
        task_factors={"stage": "inter_trial_interval", "block_idx": block_idx_val},
        stim_id="fixation",
    )
    iti.show(duration=settings.iti_duration, onset_trigger=settings.triggers.get("iti_onset")).to_dict(trial_data)

    trial_data["choice_label"] = choice_label
    trial_data["accepted"] = accepted
    trial_data["rejected"] = rejected
    trial_data["timed_out"] = timed_out
    trial_data["earned"] = earned
    trial_data["total_earned"] = int(total_earned)
    trial_data["feedback_delta"] = earned

    return trial_data
