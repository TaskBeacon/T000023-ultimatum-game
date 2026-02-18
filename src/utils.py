from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from psychopy import logging


@dataclass(frozen=True)
class OfferProfile:
    label: str
    proposer_share: int
    responder_share: int


class Controller:
    """Ultimatum game scheduler and payoff tracker."""

    def __init__(
        self,
        *,
        offer_profiles: dict[str, dict[str, Any]],
        seed: int = 2023,
        enable_logging: bool = True,
    ) -> None:
        self.seed = int(seed)
        self.enable_logging = bool(enable_logging)
        self._rng = random.Random(self.seed)
        self._profiles = self._build_profiles(offer_profiles)
        self._history: list[dict[str, Any]] = []
        self._total_earned = 0

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "Controller":
        profiles = config.get("offer_profiles", {})
        if not isinstance(profiles, dict) or not profiles:
            raise ValueError("controller.offer_profiles must be a non-empty mapping")
        return cls(
            offer_profiles=profiles,
            seed=int(config.get("seed", 2023)),
            enable_logging=bool(config.get("enable_logging", True)),
        )

    def _build_profiles(self, raw: dict[str, dict[str, Any]]) -> dict[str, OfferProfile]:
        profiles: dict[str, OfferProfile] = {}
        for key, spec in raw.items():
            proposer_share = int(spec.get("proposer_share", 5))
            responder_share = int(spec.get("responder_share", 5))
            if proposer_share < 0 or responder_share < 0:
                raise ValueError(f"offer shares must be >=0 for condition {key!r}")
            profiles[str(key)] = OfferProfile(
                label=str(spec.get("label", key)),
                proposer_share=proposer_share,
                responder_share=responder_share,
            )
        return profiles

    @property
    def total_earned(self) -> int:
        return int(self._total_earned)

    @property
    def histories(self) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for item in self._history:
            grouped.setdefault(str(item["condition"]), []).append(item)
        return grouped

    def get_profile(self, condition: str) -> OfferProfile:
        condition = str(condition)
        if condition not in self._profiles:
            raise KeyError(f"Unknown condition: {condition!r}")
        return self._profiles[condition]

    def prepare_block(self, *, block_idx: int, n_trials: int, conditions: list[str]) -> list[tuple[Any, ...]]:
        if n_trials <= 0:
            return []
        valid_conditions = [str(c) for c in conditions if str(c) in self._profiles]
        if not valid_conditions:
            raise ValueError("No valid ultimatum conditions available")

        scheduled = [valid_conditions[i % len(valid_conditions)] for i in range(n_trials)]
        self._rng.shuffle(scheduled)

        planned: list[tuple[Any, ...]] = []
        for trial_index, cond in enumerate(scheduled, start=1):
            profile = self.get_profile(cond)
            condition_id = f"{cond}_P{profile.proposer_share}_R{profile.responder_share}_t{trial_index:03d}"
            planned.append(
                (
                    cond,
                    profile.label,
                    int(profile.proposer_share),
                    int(profile.responder_share),
                    condition_id,
                    int(trial_index),
                )
            )

        if self.enable_logging:
            logging.data(
                "[UltimatumController] "
                f"block={block_idx} n_trials={n_trials} seed={self.seed} "
                f"conditions={valid_conditions}"
            )
        return planned

    def register_decision(
        self,
        *,
        condition: str,
        block_idx: int,
        trial_index: int,
        choice: str,
        accepted: bool,
        earned: int,
        proposer_share: int,
        responder_share: int,
    ) -> int:
        self._total_earned += int(earned)
        item = {
            "condition": str(condition),
            "block_idx": int(block_idx),
            "trial_index": int(trial_index),
            "choice": str(choice),
            "accepted": bool(accepted),
            "earned": int(earned),
            "proposer_share": int(proposer_share),
            "responder_share": int(responder_share),
            "total_earned": int(self._total_earned),
        }
        self._history.append(item)
        if self.enable_logging:
            logging.data(
                "[UltimatumController] "
                f"trial={trial_index} block={block_idx} condition={condition} "
                f"choice={choice} accepted={accepted} earned={earned} total={self._total_earned}"
            )
        return int(self._total_earned)
