"""Runtime core — 5-Layer Authority Pipeline (MVP-0).

Exposes 6 core objects that validate the architecture contract:
Action → Simulation → SimulationResult → Commit → State → Replay
"""

from .action import Action
from .state import RuntimeState, CharacterState
from .snapshot import StateSnapshot
from .simulation_result import Delta, SimulationResult
from .simulation import Simulation, Handler
from .commit import CommitPipeline

__all__ = [
    "Action",
    "RuntimeState",
    "CharacterState",
    "StateSnapshot",
    "Delta",
    "SimulationResult",
    "Simulation",
    "Handler",
    "CommitPipeline",
]
