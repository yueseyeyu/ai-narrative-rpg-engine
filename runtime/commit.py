"""CommitPipeline — applies SimulationResult deltas to RuntimeState.

Architecture contract: This is the ONLY place where Persistent State is mutated.
State Authority (Layer ⑤) owns this. Simulation Authority (Layer ③) does NOT.
"""

from __future__ import annotations

from .simulation_result import Delta, SimulationResult
from .state import RuntimeState


class CommitPipeline:
    """Commit Pipeline — the sole mutation path for Persistent State.

    Takes a SimulationResult and applies its valid_deltas to RuntimeState.
    No other component may modify RuntimeState directly.
    """

    def apply(self, result: SimulationResult, state: RuntimeState) -> None:
        """Apply valid deltas to RuntimeState. This is the sole mutation path."""
        for delta in result.valid_deltas:
            self._apply_delta(delta, state)

    def _apply_delta(self, delta: Delta, state: RuntimeState) -> None:
        if delta.target_type == "character":
            char = state.get_character(delta.target_id)
            if delta.op == "add":
                current = getattr(char, delta.path)
                setattr(char, delta.path, current + delta.val)
            elif delta.op == "set":
                setattr(char, delta.path, delta.val)
            elif delta.op == "remove":
                setattr(char, delta.path, None)
            else:
                raise ValueError(f"Unknown op: {delta.op}")
        else:
            raise NotImplementedError(
                f"target_type '{delta.target_type}' not implemented in MVP-0"
            )
