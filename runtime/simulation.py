"""Simulation Layer — Layer ③ of the 5-Layer Authority Pipeline.

Architecture contract: Simulation computes, does NOT mutate.
It takes (Action, Snapshot, Seed) and returns SimulationResult.
"""

from __future__ import annotations

from typing import Protocol

from .action import Action
from .simulation_result import Delta, SimulationResult
from .snapshot import StateSnapshot


class Handler(Protocol):
    """Handler Protocol — functionally pure, no Persistent State side effects.

    Architecture contract (Handler Purity):
    Input: Action + Snapshot + Seed
    Output: (deltas, diagnostics)
    A Handler SHALL NOT modify Character State, Relationship State, Memory,
    commit Events, or access Infrastructure directly.
    """

    def execute(
        self, action: Action, snapshot: StateSnapshot, seed: int
    ) -> tuple[tuple[Delta, ...], dict[str, object]]:
        ...


class Simulation:
    """Simulation Layer — computes what happens when an Action meets the world.

    This is Layer ③. It produces SimulationResult (deltas, event candidates).
    It does NOT commit Events, does NOT mutate State, does NOT generate narrative.
    """

    def __init__(self) -> None:
        self._handlers: dict[str, Handler] = {}

    def register_handler(self, action_type: str, handler: Handler) -> None:
        """Register a Handler for an Action Type (like Action Registry)."""
        self._handlers[action_type] = handler

    def tick(
        self, action: Action, snapshot: StateSnapshot, seed: int
    ) -> SimulationResult:
        """Execute one Simulation Tick: Action + Snapshot + Seed → SimulationResult.

        This is the atomic execution unit. It either completes or fails.
        """
        handler = self._handlers.get(action.action_type)
        if handler is None:
            return SimulationResult(
                result_id=f"result_{action.action_id}",
                source_action_id=action.action_id,
                input_snapshot_id="mvp_snapshot",
                seed=seed,
                status="failure",
                valid_deltas=(),
            )

        deltas, diagnostics = handler.execute(action, snapshot, seed)

        return SimulationResult(
            result_id=f"result_{action.action_id}",
            source_action_id=action.action_id,
            input_snapshot_id="mvp_snapshot",
            seed=seed,
            status="success",
            valid_deltas=deltas,
        )
