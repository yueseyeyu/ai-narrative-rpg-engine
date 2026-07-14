"""SimulationRuntime — Layer ③ of the 5-Layer Authority Pipeline.

Architecture contract: Simulation computes, does NOT mutate.
It takes a SimulationContext and returns SimulationResult.

Named SimulationRuntime (not Simulation) to avoid God Object as it grows
into HandlerRegistry, RuleEngine, EventFactory, Validator, etc. (GPT suggestion).

GPT Point 9: Handler does NOT decide status. Handler returns RawDeltas.
Validator checks them and determines status (success/partial_success/failure).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Protocol

from .action import Action
from .simulation_result import Delta, SimulationResult
from .snapshot import StateSnapshot


@dataclass(frozen=True)
class SimulationContext:
    """Context passed to Handler.execute().

    Wraps all inputs to avoid interface changes when new context is needed.
    Future extensions: world_time, rng, tags, runtime_metadata, event_bus, debug.
    """

    action: Action
    snapshot: StateSnapshot
    seed: int


class Handler(Protocol):
    """Handler Protocol — functionally pure, no Persistent State side effects.

    Architecture contract (Handler Purity):
    Input: SimulationContext
    Output: (raw_deltas, diagnostics)
    A Handler SHALL NOT modify Character State, Relationship State, Memory,
    commit Events, or access Infrastructure directly.

    GPT Point 9: Handler does NOT decide status. It returns RawDeltas.
    The Validator determines whether deltas are valid or not.
    """

    version: str

    def execute(
        self, context: SimulationContext
    ) -> tuple[tuple[Delta, ...], dict[str, object]]:
        ...


class Validator:
    """Validator — determines SimulationResult status from raw deltas.

    GPT Point 9: Handler should not decide status.
    Handler returns RawDeltas; Validator checks them against the Snapshot
    and determines: all valid → "success", some → "partial_success", none → "failure".

    MVP-0 validation: checks if delta.target_id exists in snapshot.
    Future: ConflictResolver, RuleEngine, StateConsistency checks.
    """

    @staticmethod
    def validate(
        deltas: tuple[Delta, ...], snapshot: StateSnapshot
    ) -> tuple[tuple[Delta, ...], tuple[Delta, ...], str]:
        """Validate raw deltas against snapshot. Returns (valid, invalid, status)."""
        if not deltas:
            return (), (), "success"

        valid: list[Delta] = []
        invalid: list[Delta] = []

        for delta in deltas:
            if Validator._is_valid(delta, snapshot):
                valid.append(delta)
            else:
                invalid.append(delta)

        if not invalid:
            status = "success"
        elif valid:
            status = "partial_success"
        else:
            status = "failure"

        return tuple(valid), tuple(invalid), status

    @staticmethod
    def _is_valid(delta: Delta, snapshot: StateSnapshot) -> bool:
        """Check if a delta can be applied to the snapshot. MVP: target must exist."""
        if delta.target_type == "character":
            return delta.target_id in snapshot.characters
        return True  # Non-character targets not validated in MVP-0


class SimulationRuntime:
    """Simulation Runtime — computes what happens when an Action meets the world.

    Pipeline: Handler.execute() → RawDeltas → Validator.validate() → SimulationResult

    Handler produces raw deltas (what it thinks should happen).
    Validator checks them against the snapshot (whether they're legal).
    SimulationRuntime packages the result.

    Future evolution:
    - HandlerRegistry (query handlers by action_type)
    - RuleEngine (evaluate rules before/after Handler)
    - EventFactory (package deltas into Event Candidates)
    """

    VERSION = "0.1.0"

    def __init__(self) -> None:
        self._handlers: dict[str, Handler] = {}

    def register_handler(self, action_type: str, handler: Handler) -> None:
        self._handlers[action_type] = handler

    def tick(self, context: SimulationContext) -> SimulationResult:
        """Execute one Simulation Tick: SimulationContext → SimulationResult.

        Flow:
        1. Resolve Handler by action_type
        2. Handler.execute(context) → raw_deltas
        3. Validator.validate(raw_deltas, snapshot) → valid, invalid, status
        4. Package into SimulationResult
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
                action_hash=compute_action_hash(context.action),
            )

        # Step 1: Handler produces raw deltas
        raw_deltas, diagnostics = handler.execute(context)

        # Step 2: Validator determines status (GPT Point 9)
        valid_deltas, invalid_deltas, status = Validator.validate(
            raw_deltas, context.snapshot
        )

        # Step 3: Package into immutable SimulationResult
        handler_version = getattr(handler, "version", "0.1.0")

        return SimulationResult(
            result_id=f"result_{context.action.action_id}",
            source_action_id=context.action.action_id,
            input_snapshot_id="mvp_snapshot",
            seed=context.seed,
            status=status,
            valid_deltas=valid_deltas,
            invalid_deltas=invalid_deltas,
            handler_version=handler_version,
            simulation_version=self.VERSION,
            action_hash=compute_action_hash(context.action),
        )


def compute_action_hash(action: Action) -> str:
    """Compute a canonical hash of Action content for replay verification.

    GPT Point 6: source_action_id is just an ID, not the Action content.
    Two different Actions with the same ID would produce the same result_hash
    without action_hash — dangerous for replay correctness.
    """
    data = {
        "action_id": action.action_id,
        "action_type": action.action_type,
        "actor": action.actor,
        "target": action.target,
        "parameters": action.parameters,
    }
    serialized = json.dumps(data, sort_keys=True, default=str)
    return hashlib.sha256(serialized.encode()).hexdigest()
