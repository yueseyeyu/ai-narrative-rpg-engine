"""SimulationResult — the sole external output of Simulation Layer (Layer ③).

Architecture contracts:
- Self-contained: carries everything needed for commit, debug, replay
- Immutable: once produced, cannot be modified
- Deterministic: same inputs always produce same result
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Delta:
    """A state change delta — computed by Simulation, applied by State Authority.

    Value type recommendation (GPT): restrict `val` to Primitive, Frozen Dataclass,
    or Tuple for deep immutability. Avoid list/dict which remain mutable.
    """

    target_id: str
    target_type: str  # "character", "relationship", "world", "progression"
    op: str  # "set", "add", "remove", "merge"
    path: str  # e.g., "trust", "mood"
    val: Any
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SimulationResult:
    """The complete, self-contained result of one Simulation Tick."""

    result_id: str
    source_action_id: str
    input_snapshot_id: str
    seed: int
    status: str  # "success", "partial_success", "failure", "interrupted", "cancelled"
    valid_deltas: tuple[Delta, ...]
    invalid_deltas: tuple[Delta, ...] = ()
    event_candidates: tuple[dict[str, Any], ...] = ()
    validated_state_hash: str = ""
    # Version info for cross-version replay verification (GPT suggestion)
    handler_version: str = "0.1.0"
    simulation_version: str = "0.1.0"

    def result_hash(self) -> str:
        """Compute a deterministic hash for replay verification.

        Includes: handler_version, simulation_version, status, valid_deltas,
        event_candidates. Excludes: result_id, input_snapshot_id (runtime-specific).
        Version info ensures cross-version replay mismatches are detectable.
        """
        data = {
            "handler_version": self.handler_version,
            "simulation_version": self.simulation_version,
            "status": self.status,
            "valid_deltas": [
                {
                    "target_id": d.target_id,
                    "target_type": d.target_type,
                    "op": d.op,
                    "path": d.path,
                    "val": d.val,
                }
                for d in self.valid_deltas
            ],
            "event_candidates": list(self.event_candidates),
        }
        serialized = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode()).hexdigest()
