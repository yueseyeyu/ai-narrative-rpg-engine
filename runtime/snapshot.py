"""StateSnapshot — an immutable copy of Runtime State.

Architecture contract: Snapshot is the isolation boundary for Scene transactions.
Simulation reads from Snapshot, never from live RuntimeState.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass

from .state import CharacterState, RuntimeState


@dataclass(frozen=True)
class StateSnapshot:
    """An immutable snapshot of Runtime State at a point in time."""

    characters: dict[str, CharacterState]

    @classmethod
    def from_state(cls, state: RuntimeState) -> StateSnapshot:
        """Create a snapshot from RuntimeState (deep copy for isolation)."""
        return cls(characters=copy.deepcopy(state.characters))

    def get_character(self, character_id: str) -> CharacterState:
        """Read a character's state from the snapshot."""
        return self.characters[character_id]
