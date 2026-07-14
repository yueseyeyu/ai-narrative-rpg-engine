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
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True)
class Delta:
    """A state change delta — computed by Simulation, applied by State Authority.

    Value type recommendation (GPT): restrict `val` to Primitive, Frozen Dataclass,
    or Tuple for deep immutability. Avoid list/dict which remain mutable.

    metadata is wrapped in MappingProxyType for read-only access (GPT Point 7):
    `delta.metadata["x"] = "y"` raises TypeError. Deep immutability enforced.
    """

    target_id: str
    target_type: str
    op: str
    path: str
    val: Any
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Convert mutable dict to read-only MappingProxyType for deep immutability."""
        if not isinstance(self.metadata, MappingProxyType):
            object.__setattr__(
                self, "metadata", MappingProxyType(dict(self.metadata))
            )


@dataclass(frozen=True)
class SimulationResult:
    """The complete, self-contained result of one Simulation Tick.

    Includes action_hash for replay verification (GPT Point 6):
    source_action_id is just an ID, not the Action content.
    Two different Actions with the same ID would produce the same hash without
    action_hash — dangerous for replay correctness.
    """

    result_id: str
    source_action_id: str
    input_snapshot_id: str
    seed: int
    status: str
    valid_deltas: tuple[Delta, ...]
    invalid_deltas: tuple[Delta, ...] = ()
    event_candidates: tuple[dict[str, Any], ...] = ()
    validated_state_hash: str = ""
    handler_version: str = "0.1.0"
    simulation_version: str = "0.1.0"
    action_hash: str = ""  # Hash of source Action content for replay verification

    def result_hash(self) -> str:
        """Compute a deterministic hash for replay verification.

        Includes: action_hash, handler_version, simulation_version, status,
        valid_deltas, event_candidates.
        Excludes: result_id, input_snapshot_id (runtime-specific).

        action_hash (GPT Point 6): Ensures that even if two Actions share the
        same action_id but have different content, their hashes will differ.
        """
        data = {
            "action_hash": self.action_hash,
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
