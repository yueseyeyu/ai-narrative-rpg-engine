"""Case-000: Architecture Test — Simulation MUST NOT modify RuntimeState.

This is the most fundamental architecture contract.
If this test passes, Mutation Boundary is enforced by code, not just documentation.

Architecture Rule: Only State Authority (Layer ⑤) may mutate Persistent State.
                    Simulation Authority (Layer ③) computes deltas, does NOT apply them.
"""

from __future__ import annotations

from runtime import Action


def test_case_000_simulation_does_not_mutate_state(
    initial_state, simulation, make_context
):
    """Simulation MUST NOT modify RuntimeState.

    After executing a Simulation Tick, the live RuntimeState must be
    byte-for-byte identical to its pre-simulation state.
    """
    # Setup: record state before simulation
    state = initial_state
    trust_a_before = state.characters["A"].trust
    trust_b_before = state.characters["B"].trust
    mood_a_before = state.characters["A"].mood

    # Create snapshot and action
    snapshot = state.snapshot()
    action = Action(action_id="a1", action_type="say_hello", actor="A", target="B")

    # Execute Simulation Tick
    context = make_context(action, snapshot)
    result = simulation.tick(context)

    # Assert: SimulationResult was produced
    assert result.status == "success"
    assert len(result.valid_deltas) == 1

    # Assert: RuntimeState is UNCHANGED after simulation
    assert state.characters["A"].trust == trust_a_before
    assert state.characters["B"].trust == trust_b_before
    assert state.characters["A"].mood == mood_a_before

    # Assert: Delta was computed but NOT applied
    delta = result.valid_deltas[0]
    assert delta.path == "trust"
    assert delta.val == 1.0
    assert state.characters["B"].trust == trust_b_before  # still unchanged
