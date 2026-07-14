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
    """A state change delta — computed by Simulation, applied by State Authority."""

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

    def result_hash(self) -> str:
        """Compute a deterministic hash for replay verification.

        Excludes result_id and input_snapshot_id (runtime-specific, not deterministic).
        Includes status, valid_deltas, event_candidates — the computational output.
        """
        data = {
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
