"""SayHelloHandler — the simplest possible Handler for MVP-0.

Rule: saying hello increases target's trust by 1.
Pure function: (SimulationContext) → (deltas, diagnostics)
No side effects. No state mutation. No Infrastructure access.
"""

from __future__ import annotations

from runtime.simulation import SimulationContext
from runtime.simulation_result import Delta


class SayHelloHandler:
    """Handler for 'say_hello' action type."""

    version = "0.1.0"  # Handler version for cross-version replay verification

    def execute(
        self, context: SimulationContext
    ) -> tuple[tuple[Delta, ...], dict[str, object]]:
        """Compute what happens when actor says hello to target.

        Returns a single delta: target.trust += 1
        This is a pure computation — no state is modified.
        """
        action = context.action
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
            "handler_version": self.version,
        }
        return (delta,), diagnostics
