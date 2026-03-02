from __future__ import annotations

from dataclasses import dataclass
from math import exp
import random as _py_random
from typing import Any

from psyflow.sim.contracts import Action, Feedback, Observation, SessionInfo


@dataclass
class TaskSamplerResponder:
    """Sampler responder for Ultimatum Game decisions."""

    accept_key: str = "f"
    reject_key: str = "j"
    continue_key: str = "space"
    fairness_threshold: float = 0.30
    inverse_temp: float = 10.0
    lapse_rate: float = 0.03
    rt_mean_s: float = 0.33
    rt_sd_s: float = 0.07
    rt_min_s: float = 0.15

    def __post_init__(self) -> None:
        self.fairness_threshold = float(self.fairness_threshold)
        self.inverse_temp = max(1e-6, float(self.inverse_temp))
        self.lapse_rate = max(0.0, min(1.0, float(self.lapse_rate)))
        self.rt_mean_s = float(self.rt_mean_s)
        self.rt_sd_s = max(1e-6, float(self.rt_sd_s))
        self.rt_min_s = max(0.0, float(self.rt_min_s))
        self._rng: Any = None

    def start_session(self, session: SessionInfo, rng: Any) -> None:
        self._rng = rng

    def on_feedback(self, fb: Feedback) -> None:
        return None

    def end_session(self) -> None:
        self._rng = None

    def _rand(self) -> float:
        rng = self._rng
        if hasattr(rng, "random"):
            return float(rng.random())
        return float(_py_random.random())

    def _normal(self, mean: float, sd: float) -> float:
        rng = self._rng
        if hasattr(rng, "normal"):
            return float(rng.normal(mean, sd))
        return float(rng.gauss(mean, sd))

    def _p_accept(self, responder_share: float, proposer_share: float) -> float:
        total = max(1e-9, float(responder_share) + float(proposer_share))
        fairness = float(responder_share) / total
        x = self.inverse_temp * (fairness - self.fairness_threshold)
        if x >= 0:
            z = exp(-x)
            return 1.0 / (1.0 + z)
        z = exp(x)
        return z / (1.0 + z)

    def act(self, obs: Observation) -> Action:
        valid_keys = list(obs.valid_keys or [])
        if not valid_keys:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "reason": "no_valid_keys"})

        if self.continue_key in valid_keys:
            return Action(
                key=self.continue_key,
                rt_s=max(self.rt_min_s, self.rt_mean_s - 0.08),
                meta={"source": "task_sampler", "policy": "continue"},
            )

        phase = str(obs.phase or "")
        if phase not in {"offer_decision", "ultimatum_decision"}:
            return Action(key=None, rt_s=None, meta={"source": "task_sampler", "phase": phase})

        factors = dict(obs.task_factors or {})
        responder_share = float(factors.get("responder_share", 0.0))
        proposer_share = float(factors.get("proposer_share", 0.0))
        p_accept = self._p_accept(responder_share=responder_share, proposer_share=proposer_share)

        rt = max(self.rt_min_s, self._normal(self.rt_mean_s, self.rt_sd_s))

        if self._rand() < self.lapse_rate:
            key = valid_keys[0] if self._rand() < 0.5 else valid_keys[-1]
            return Action(key=key, rt_s=rt, meta={"source": "task_sampler", "policy": "lapse"})

        accept = bool(self._rand() < p_accept)
        key = self.accept_key if accept else self.reject_key
        if key not in valid_keys:
            key = valid_keys[0]

        return Action(
            key=key,
            rt_s=rt,
            meta={
                "source": "task_sampler",
                "policy": "fairness_logit",
                "p_accept": p_accept,
                "responder_share": responder_share,
                "proposer_share": proposer_share,
            },
        )
