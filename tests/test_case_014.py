"""Case-014: Scene Commit Atomicity — all deltas commit or none.

Architecture Rule: Scene Commit is atomic. Either all valid deltas are
                    applied, or none are. No partial commit.

    Also verifies: if commit itself fails (e.g., idempotency violation),
    Scene rolls back to Snapshot for atomicity.

Protocol:
    1. BEGIN: create snapshot
    2. EXECUTE: valid simulation → status="success"
    3. COMMIT: apply all deltas
    4. Assert: all deltas applied, state changed
    5. Second Scene: EXECUTE → COMMIT same result → idempotency triggers rollback
"""

from __future__ import annotations

from runtime import Action, CommitPipeline, SceneRuntime


def test_case_014_scene_commit_atomicity_success(initial_state, simulation, make_context):
    """Successful Scene commits all deltas atomically."""
    state = initial_state
    trust_b_before = state.characters["B"].trust

    # BEGIN
    scene = SceneRuntime(scene_id="scene_014a")
    snapshot = scene.begin(state)

    # EXECUTE
    action = Action(
        action_id="a1", action_type="say_hello", actor="A", target="B"
    )
    context = make_context(action, snapshot)
    result = scene.execute(context, simulation)

    assert result.status == "success"

    # COMMIT
    commit = CommitPipeline()
    scene_result = scene.finish(commit)

    assert scene_result.outcome == "committed"

    # All deltas applied
    assert state.characters["B"].trust == trust_b_before + 1.0
    assert state.characters["B"].trust == 11.0


def test_case_014_scene_commit_failure_triggers_rollback(
    initial_state, simulation, make_context
):
    """If commit fails, Scene rolls back for atomicity."""
    state = initial_state
    trust_b_before = state.characters["B"].trust

    # First Scene: commit successfully
    scene1 = SceneRuntime(scene_id="scene_014b1")
    snapshot1 = scene1.begin(state)
    action = Action(
        action_id="a1", action_type="say_hello", actor="A", target="B"
    )
    context = make_context(action, snapshot1)
    scene1.execute(context, simulation)
    commit = CommitPipeline()
    scene1.finish(commit)

    # State changed: trust is now 11
    assert state.characters["B"].trust == 11.0

    # Second Scene: try to commit same result_id → idempotency error → rollback
    scene2 = SceneRuntime(scene_id="scene_014b2")
    snapshot2 = scene2.begin(state)
    action2 = Action(
        action_id="a1",  # SAME action_id → same result_id → idempotency violation
        action_type="say_hello",
        actor="A",
        target="B",
    )
    context2 = make_context(action2, snapshot2)
    scene2.execute(context2, simulation)

    # COMMIT with the SAME commit pipeline (has_committed(result_id) = True)
    scene_result = scene2.finish(commit)

    # Should rollback because commit raised RuntimeError (idempotency)
    assert scene_result.outcome == "rolled_back"

    # State should be restored to snapshot2 (trust=11.0, not 12.0)
    assert state.characters["B"].trust == 11.0, (
        f"Atomicity violation: trust = {state.characters['B'].trust}, "
        "expected 11.0 (not 12.0) — commit failure did not rollback"
    )
