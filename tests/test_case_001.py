"""Case-001: Determinism — Same input = Same output.

Architecture Rule: Same Snapshot + Same Action + Same Seed = Same SimulationResult.
                    The entire simulation is replayable and deterministic.
"""

from __future__ import annotations

from runtime import Action


def test_case_001_determinism(initial_state, simulation):
    """Two Simulation Ticks with identical inputs must produce identical results."""
    snapshot = initial_state.snapshot()
    action = Action(
        action_id="a1", action_type="say_hello", actor="A", target="B"
    )

    # Execute twice with identical inputs
    result1 = simulation.tick(action, snapshot, seed=42)
    result2 = simulation.tick(action, snapshot, seed=42)

    # Assert: status matches
    assert result1.status == result2.status

    # Assert: valid_deltas match
    assert result1.valid_deltas == result2.valid_deltas

    # Assert: result_hash matches (canonical hash for replay verification)
    hash1 = result1.result_hash()
    hash2 = result2.result_hash()
    assert hash1 == hash2, (
        f"Determinism violation: hashes differ.\n"
        f"  result1: {hash1}\n"
        f"  result2: {hash2}"
    )
