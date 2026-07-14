"""Runtime core — 5-Layer Authority Pipeline (MVP-0).

Exposes core objects that validate the architecture contract:
Action → Simulation → SimulationResult → Commit → State → Replay
"""

from .action import Action
from .commit import CommitPipeline
from .simulation import (
    Handler,
    SimulationContext,
    SimulationRuntime,
    Validator,
    compute_action_hash,
)
from .simulation_result import Delta, SimulationResult
from .snapshot import StateSnapshot
from .state import CharacterState, FrozenCharacterState, RuntimeState

__all__ = [
    "Action",
    "RuntimeState",
    "CharacterState",
    "FrozenCharacterState",
    "StateSnapshot",
    "Delta",
    "SimulationResult",
    "SimulationContext",
    "SimulationRuntime",
    "Handler",
    "Validator",
    "compute_action_hash",
    "CommitPipeline",
]
