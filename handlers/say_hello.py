"""SayHelloHandler — the simplest possible Handler for MVP-0.

Rule: saying hello increases target's trust by 1.
Pure function: (Action, Snapshot, Seed) → (deltas, diagnostics)
No side effects. No state mutation. No Infrastructure access.
"""

from __future__ import annotations

from runtime.action import Action
from runtime.simulation_result import Delta
from runtime.snapshot import StateSnapshot


class SayHelloHandler:
    """Handler for 'say_hello' action type."""

    def execute(
        self, action: Action, snapshot: StateSnapshot, seed: int
    ) -> tuple[tuple[Delta, ...], dict[str, object]]:
        """Compute what happens when actor says hello to target.

        Returns a single delta: target.trust += 1
        This is a pure computation — no state is modified.
        """
        delta = Delta(
            target_id=action.target,
            target_type="character",
            op="add",
            path="trust",
            val=1.0,
            metadata={
                "rule": "say_hello_trust_bonus",
                "reason": "friendly greeting",
            },
        )
        diagnostics = {
            "rule_trace": ["say_hello_trust_bonus"],
            "handler": "SayHelloHandler",
        }
        return (delta,), diagnostics
