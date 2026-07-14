"""CommitPipeline — applies SimulationResult deltas to RuntimeState.

Architecture contract: This is the ONLY place where Persistent State is mutated.
State Authority (Layer ⑤) owns this. Simulation Authority (Layer ③) does NOT.

GPT suggestion (future refactor): Replace if/else dispatch with per-domain Appliers:
    StateAuthority
        CharacterApplier
        RelationshipApplier
        InventoryApplier
        QuestApplier
    CommitPipeline only dispatches, does not apply directly.
For MVP-0, the if/else approach is sufficient.
"""

from __future__ import annotations

from .simulation_result import Delta, SimulationResult
from .state import RuntimeState


class CommitPipeline:
    """Commit Pipeline — the sole mutation path for Persistent State.

    Takes a SimulationResult and applies its valid_deltas to RuntimeState.
    No other component may modify RuntimeState directly.

    Idempotency (Case-013): A committed result MUST NOT be applied twice.
    Double-commit raises RuntimeError to prevent silent state pollution.
    """

    def __init__(self) -> None:
        self._committed_result_ids: set[str] = set()

    def apply(self, result: SimulationResult, state: RuntimeState) -> None:
        """Apply valid deltas to RuntimeState. This is the sole mutation path.

        Raises RuntimeError if the same result has already been committed.
        """
        if result.result_id in self._committed_result_ids:
            raise RuntimeError(
                f"SimulationResult '{result.result_id}' has already been committed. "
                "Double-commit is not allowed — prevents state pollution from replay."
            )

        for delta in result.valid_deltas:
            self._apply_delta(delta, state)

        self._committed_result_ids.add(result.result_id)

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

    def has_committed(self, result_id: str) -> bool:
        """Check whether a SimulationResult has already been committed."""
        return result_id in self._committed_result_ids
