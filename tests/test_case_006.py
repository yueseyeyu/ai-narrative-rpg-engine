"""Case-006: Scene Failure Rollback — failed Scene restores Snapshot.

Architecture Rule: Failed Scene execution rolls back to Snapshot.
                    Persistent State is unmodified after rollback.

Protocol:
    1. BEGIN: create snapshot
    2. EXECUTE: simulation with invalid target → status="failure"
    3. ROLLBACK: Scene restores state to snapshot
    4. Assert: state is identical to pre-Scene state
"""

from __future__ import annotations

from runtime import Action, CommitPipeline, SceneRuntime


def test_case_006_scene_failure_rollback(initial_state, simulation, make_context):
    """Failed Scene execution rolls back to Snapshot — state is unmodified."""
    state = initial_state

    # Record state before Scene
    trust_a_before = state.characters["A"].trust
    trust_b_before = state.characters["B"].trust

    # BEGIN
    scene = SceneRuntime(scene_id="scene_006")
    snapshot = scene.begin(state)

    # EXECUTE with invalid target (does not exist in snapshot)
    action = Action(
        action_id="a1", action_type="say_hello", actor="A", target="NONEXISTENT"
    )
    context = make_context(action, snapshot)
    result = scene.execute(context, simulation)

    # Validator should mark delta as invalid (target not in snapshot)
    assert result.status == "failure"
    assert len(result.invalid_deltas) == 1
    assert len(result.valid_deltas) == 0

    # FINISH (should rollback because status="failure")
    commit = CommitPipeline()
    scene_result = scene.finish(commit)

    assert scene_result.outcome == "rolled_back"

    # State is identical to pre-Scene state
    assert state.characters["A"].trust == trust_a_before
    assert state.characters["B"].trust == trust_b_before
