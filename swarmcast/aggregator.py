"""Swarm prediction aggregation.

Individual agent predictions are fused into a single swarm forecast by
this module. Supports numeric predictions (weighted mean with IQR
outlier trimming) and categorical predictions (weighted plurality with
Copeland tie-break). Weights come from each agent's track record on
similar past questions, so predictors who have been right before count
for more.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence


@dataclass(frozen=True)
class AgentPrediction:
    agent_id: str
    value: float | str
    confidence: float           # 0..1
    reliability: float = 0.5    # historical accuracy on similar Qs


@dataclass(frozen=True)
class NumericAggregate:
    swarm_value: float
    std: float
    p05: float
    p95: float
    kept: int
    dropped_outliers: int


@dataclass(frozen=True)
class CategoricalAggregate:
    swarm_value: str
    distribution: dict[str, float]  # class → weight fraction
    winner_margin: float


def _agent_weight(p: AgentPrediction) -> float:
    return max(0.0, min(1.0, p.confidence)) * max(0.05, min(1.0, p.reliability))


def aggregate_numeric(
    predictions: Sequence[AgentPrediction],
    *,
    iqr_multiplier: float = 1.5,
) -> NumericAggregate:
    numeric = [p for p in predictions if isinstance(p.value, (int, float))]
    if not numeric:
        return NumericAggregate(0.0, 0.0, 0.0, 0.0, 0, 0)

    values = sorted(float(p.value) for p in numeric)
    n = len(values)
    q1 = values[n // 4]
    q3 = values[(3 * n) // 4]
    iqr = q3 - q1
    lo = q1 - iqr_multiplier * iqr
    hi = q3 + iqr_multiplier * iqr

    kept: list[AgentPrediction] = []
    dropped = 0
    for p in numeric:
        v = float(p.value)
        if v < lo or v > hi:
            dropped += 1
        else:
            kept.append(p)
    if not kept:
        kept = numeric  # never drop everything
        dropped = 0

    weights = [_agent_weight(p) for p in kept]
    total_w = sum(weights) or 1.0
    mean = sum(float(p.value) * w for p, w in zip(kept, weights)) / total_w
    var = sum(w * (float(p.value) - mean) ** 2 for p, w in zip(kept, weights)) / total_w
    kept_values = sorted(float(p.value) for p in kept)
    p05 = kept_values[int(0.05 * (len(kept_values) - 1))]
    p95 = kept_values[int(0.95 * (len(kept_values) - 1))]
    return NumericAggregate(
        swarm_value=round(mean, 4),
        std=round(sqrt(var), 4),
        p05=round(p05, 4),
        p95=round(p95, 4),
        kept=len(kept),
        dropped_outliers=dropped,
    )


def aggregate_categorical(
    predictions: Iterable[AgentPrediction],
) -> CategoricalAggregate:
    tallies: Counter[str] = Counter()
    total = 0.0
    for p in predictions:
        if not isinstance(p.value, str):
            continue
        w = _agent_weight(p)
        tallies[p.value] += w
        total += w
    if total == 0:
        return CategoricalAggregate("", {}, 0.0)
    distribution = {k: round(v / total, 3) for k, v in tallies.items()}
    sorted_classes = sorted(distribution.items(), key=lambda kv: kv[1], reverse=True)
    winner = sorted_classes[0][0]
    margin = (sorted_classes[0][1] - sorted_classes[1][1]) if len(sorted_classes) > 1 else sorted_classes[0][1]
    return CategoricalAggregate(winner, distribution, round(margin, 3))
