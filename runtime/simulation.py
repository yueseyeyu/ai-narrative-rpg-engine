"""SimulationRuntime — Layer ③ of the 5-Layer Authority Pipeline.

Architecture contract: Simulation computes, does NOT mutate.
It takes a SimulationContext and returns SimulationResult.

Named SimulationRuntime (not Simulation) to avoid God Object as it grows
into HandlerRegistry, RuleEngine, EventFactory, etc. (GPT suggestion).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .action import Action
from .simulation_result import Delta, SimulationResult
from .snapshot import StateSnapshot


@dataclass(frozen=True)
class SimulationContext:
    """Context passed to Handler.execute().

    Wraps all inputs to avoid interface changes when new context is needed.
    Future extensions (not used in MVP-0 but available):
    - world_time: float
    - rng: Any
    - tags: dict[str, str]
    - runtime_metadata: dict[str, Any]
    """

    action: Action
    snapshot: StateSnapshot
    seed: int
    # Future fields (uncomment when needed):
    # world_time: float = 0.0
    # tags: dict[str, str] = field(default_factory=dict)


class Handler(Protocol):
    """Handler Protocol — functionally pure, no Persistent State side effects.

    Architecture contract (Handler Purity):
    Input: SimulationContext (Action + Snapshot + Seed + future extensions)
    Output: (deltas, diagnostics)
    A Handler SHALL NOT modify Character State, Relationship State, Memory,
    commit Events, or access Infrastructure directly.
    """

    version: str  # Handler version for replay verification

    def execute(
        self, context: SimulationContext
    ) -> tuple[tuple[Delta, ...], dict[str, object]]:
        ...


class SimulationRuntime:
    """Simulation Runtime — computes what happens when an Action meets the world.

    This is Layer ③. It produces SimulationResult (deltas, event candidates).
    It does NOT commit Events, does NOT mutate State, does NOT generate narrative.

    Future evolution (without changing Handler interface):
    - HandlerRegistry (query handlers by action_type)
    - RuleEngine (evaluate rules before/after Handler)
    - EventFactory (package deltas into Event Candidates)
    """

    VERSION = "0.1.0"

    def __init__(self) -> None:
        self._handlers: dict[str, Handler] = {}

    def register_handler(self, action_type: str, handler: Handler) -> None:
        """Register a Handler for an Action Type (like Action Registry)."""
        self._handlers[action_type] = handler

    def tick(self, context: SimulationContext) -> SimulationResult:
        """Execute one Simulation Tick: SimulationContext → SimulationResult.

        This is the atomic execution unit. It either completes or fails.
        """
        handler = self._handlers.get(context.action.action_type)
        if handler is None:
            return SimulationResult(
                result_id=f"result_{context.action.action_id}",
                source_action_id=context.action.action_id,
                input_snapshot_id="mvp_snapshot",
                seed=context.seed,
                status="failure",
                valid_deltas=(),
                handler_version="unknown",
                simulation_version=self.VERSION,
            )

        deltas, diagnostics = handler.execute(context)
        handler_version = getattr(handler, "version", "0.1.0")

        return SimulationResult(
            result_id=f"result_{context.action.action_id}",
            source_action_id=context.action.action_id,
            input_snapshot_id="mvp_snapshot",
            seed=context.seed,
            status="success",
            valid_deltas=deltas,
            handler_version=handler_version,
            simulation_version=self.VERSION,
        )
