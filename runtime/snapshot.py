"""StateSnapshot — an immutable copy of Runtime State.

Architecture contract: Snapshot is the isolation boundary for Scene transactions.
Simulation reads from Snapshot, never from live RuntimeState.

Deep immutability (GPT Point 7): Uses FrozenCharacterState so that
snapshot.characters["A"].trust += 1 raises FrozenInstanceError.
"""

from __future__ import annotations

from dataclasses import dataclass

from .state import FrozenCharacterState, RuntimeState


@dataclass(frozen=True)
class StateSnapshot:
    """An immutable snapshot of Runtime State at a point in time.

    Characters are FrozenCharacterState — deep immutable.
    Any attempt to modify a character's field raises FrozenInstanceError.
    """

    characters: dict[str, FrozenCharacterState]

    @classmethod
    def from_state(cls, state: RuntimeState) -> StateSnapshot:
        """Create a snapshot from RuntimeState with frozen character copies."""
        return cls(
            characters={
                cid: FrozenCharacterState.from_character(c)
                for cid, c in state.characters.items()
            }
        )

    def get_character(self, character_id: str) -> FrozenCharacterState:
        """Read a character's frozen state from the snapshot."""
        return self.characters[character_id]
