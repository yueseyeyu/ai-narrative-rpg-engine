"""Case-002: Mutation Boundary — Only CommitPipeline mutates state.

Architecture Rule: Simulation computes deltas. CommitPipeline applies them.
                    No other component may modify Persistent State.

Flow:
    1. Record state before simulation
    2. Execute Simulation → state UNCHANGED
    3. Execute CommitPipeline → state CHANGED
    4. Verify delta was applied correctly
"""

from __future__ import annotations

from runtime import Action, CommitPipeline


def test_case_002_mutation_boundary(initial_state, simulation, make_context):
    """Only CommitPipeline may mutate RuntimeState. Simulation does not."""
    state = initial_state
    snapshot = state.snapshot()
    action = Action(action_id="a1", action_type="say_hello", actor="A", target="B")

    # Step 1: Record initial state
    trust_b_before = state.characters["B"].trust
    assert trust_b_before == 10.0

    # Step 2: Execute Simulation
    context = make_context(action, snapshot)
    result = simulation.tick(context)

    # Step 3: State is UNCHANGED after simulation
    assert state.characters["B"].trust == trust_b_before

    # Step 4: Execute CommitPipeline
    commit = CommitPipeline()
    commit.apply(result, state)

    # Step 5: State is CHANGED after commit
    assert state.characters["B"].trust == trust_b_before + 1.0
    assert state.characters["B"].trust == 11.0

    # Step 6: Actor's state is unchanged (say_hello only affects target)
    assert state.characters["A"].trust == 10.0
