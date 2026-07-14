"""SceneRuntime — Transaction Container and Pipeline Coordinator.

Architecture contract: Scene Engine orchestrates, does NOT compute or mutate.
It provides the transaction boundary (snapshot, rollback) within which
the Pipeline operates. Scene is NOT an Authority layer.

Lifecycle: BEGIN → EXECUTE → COMMIT or ROLLBACK → END

MVP-1: Minimal transaction with Snapshot + Simulation + Commit/Rollback.
Future: EventFactory, Timeline, Memory, Narrative integration.
"""

from __future__ import annotations

from dataclasses import dataclass

from .commit import CommitPipeline
from .simulation import SimulationContext, SimulationRuntime
from .simulation_result import SimulationResult
from .snapshot import StateSnapshot
from .state import RuntimeState


@dataclass(frozen=True)
class SceneResult:
    """Result of a Scene execution — committed or rolled back."""

    scene_id: str
    outcome: str  # "committed" or "rolled_back"
    simulation_result: SimulationResult


class SceneRuntime:
    """Scene Engine — Transaction Container and Pipeline Coordinator.

    Orchestrates: BEGIN → EXECUTE → COMMIT or ROLLBACK.
    Does NOT compute (that's Simulation Authority ③).
    Does NOT mutate (that's State Authority ⑤, via CommitPipeline).
    """

    def __init__(self, scene_id: str = "scene_0") -> None:
        self.scene_id = scene_id
        self._state: RuntimeState | None = None
        self._snapshot: StateSnapshot | None = None
        self._result: SimulationResult | None = None
        self._finished: bool = False

    def begin(self, state: RuntimeState) -> StateSnapshot:
        """BEGIN: Create a snapshot for rollback safety.

        Every Scene starts from a Snapshot. If execution fails,
        the Engine rolls back to this Snapshot.
        """
        self._state = state
        self._snapshot = state.snapshot()
        return self._snapshot

    def execute(
        self,
        context: SimulationContext,
        simulation: SimulationRuntime,
    ) -> SimulationResult:
        """EXECUTE: Run one Simulation Tick within this Scene's transaction.

        Scene Engine passes the SimulationContext to SimulationRuntime.
        It does NOT interpret or modify the SimulationResult.
        """
        if self._snapshot is None:
            raise RuntimeError("Scene has not begun. Call begin() first.")

        self._result = simulation.tick(context)
        return self._result

    def finish(self, commit_pipeline: CommitPipeline) -> SceneResult:
        """Finish Scene: commit on success, rollback on failure.

        If SimulationResult status is success/partial_success → COMMIT.
        If failure → ROLLBACK to Snapshot.
        If commit itself fails → ROLLBACK to Snapshot (atomicity guarantee).
        """
        if self._result is None or self._state is None or self._snapshot is None:
            raise RuntimeError("Scene has not executed. Call execute() first.")
        if self._finished:
            raise RuntimeError("Scene has already finished.")

        self._finished = True

        if self._result.status in ("success", "partial_success"):
            try:
                commit_pipeline.apply(self._result, self._state)
                return SceneResult(
                    scene_id=self.scene_id,
                    outcome="committed",
                    simulation_result=self._result,
                )
            except Exception:
                # Commit failed → rollback for atomicity
                self._state.restore(self._snapshot)
                return SceneResult(
                    scene_id=self.scene_id,
                    outcome="rolled_back",
                    simulation_result=self._result,
                )
        else:
            # Failure → rollback
            self._state.restore(self._snapshot)
            return SceneResult(
                scene_id=self.scene_id,
                outcome="rolled_back",
                simulation_result=self._result,
            )
