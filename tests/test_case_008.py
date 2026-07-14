"""Case-008: Replayability — SimulationResult can be regenerated from inputs.

Architecture Rule: Given the same Snapshot, Action, and Seed, replaying a
                    Simulation Tick must produce an identical SimulationResult.

Protocol:
    1. Execute original Simulation Tick → record result_hash
    2. Create a fresh state with identical initial conditions
    3. Re-execute with same inputs → record result_hash
    4. Assert hashes match (determinism verification)
"""

from __future__ import annotations

from runtime import Action, CharacterState, RuntimeState


def test_case_008_replayability(initial_state, simulation):
    """Replay must produce the same SimulationResult hash as the original."""
    # Original execution
    snapshot1 = initial_state.snapshot()
    action = Action(
        action_id="a1", action_type="say_hello", actor="A", target="B"
    )

    result1 = simulation.tick(action, snapshot1, seed=42)
    hash1 = result1.result_hash()

    # Replay: create a fresh state with identical initial conditions
    state2 = RuntimeState()
    state2.characters["A"] = CharacterState("A", "Alice", trust=10.0)
    state2.characters["B"] = CharacterState("B", "Bob", trust=10.0)
    snapshot2 = state2.snapshot()

    result2 = simulation.tick(action, snapshot2, seed=42)
    hash2 = result2.result_hash()

    # Assert: hashes match — determinism verified
    assert hash1 == hash2, (
        f"Replay determinism violation:\n"
        f"  original hash:  {hash1}\n"
        f"  replay hash:    {hash2}"
    )

    # Assert: full result comparison (not just hash)
    assert result1.status == result2.status
    assert result1.valid_deltas == result2.valid_deltas
