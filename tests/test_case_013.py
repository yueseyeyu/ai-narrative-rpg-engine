"""Case-013: Commit Idempotency — applying the same SimulationResult twice is a no-op.

Architecture Rule: A committed SimulationResult SHALL NOT be applied twice.
                    Double-commit MUST NOT cause double-mutation.

This is critical for replay safety: if a replay accidentally triggers commit,
the state MUST NOT be polluted with duplicate deltas.

Protocol:
    1. Execute Simulation → SimulationResult
    2. Commit → state changes (trust +1)
    3. Commit same result again → state MUST NOT change
    4. Assert: trust is 11.0, not 12.0
"""

from __future__ import annotations

from runtime import Action, CommitPipeline


def test_case_013_commit_idempotency(initial_state, simulation, make_context):
    """Committing the same SimulationResult twice MUST NOT double-apply deltas."""
    state = initial_state
    snapshot = state.snapshot()
    action = Action(action_id="a1", action_type="say_hello", actor="A", target="B")

    # Step 1: Execute Simulation
    context = make_context(action, snapshot)
    result = simulation.tick(context)

    # Step 2: First commit — state changes
    commit = CommitPipeline()
    commit.apply(result, state)
    assert state.characters["B"].trust == 11.0

    # Step 3: Second commit of the SAME result — MUST NOT change state
    # The CommitPipeline should detect already-applied result and skip
    try:
        commit.apply(result, state)
        # If apply succeeds, state MUST NOT have changed
        assert state.characters["B"].trust == 11.0, (
            "Double-commit violation: trust changed from 11.0 to "
            f"{state.characters['B'].trust}. "
            "Commit is not idempotent."
        )
    except RuntimeError:
        # Alternative: commit may raise an error for already-applied results
        # This is also acceptable behavior
        pass

    # Final assertion: trust is still 11.0, not 12.0
    assert state.characters["B"].trust == 11.0, (
        f"Idempotency violation: trust = {state.characters['B'].trust}, "
        "expected 11.0 (not 12.0)"
    )
