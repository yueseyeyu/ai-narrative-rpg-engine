"""Runtime core — 5-Layer Authority Pipeline (MVP-0).

Exposes 6 core objects that validate the architecture contract:
Action → Simulation → SimulationResult → Commit → State → Replay
"""

from .action import Action
from .commit import CommitPipeline
from .simulation import Handler, SimulationContext, SimulationRuntime
from .simulation_result import Delta, SimulationResult
from .snapshot import StateSnapshot
from .state import CharacterState, RuntimeState

__all__ = [
    "Action",
    "RuntimeState",
    "CharacterState",
    "StateSnapshot",
    "Delta",
    "SimulationResult",
    "SimulationContext",
    "SimulationRuntime",
    "Handler",
    "CommitPipeline",
]
