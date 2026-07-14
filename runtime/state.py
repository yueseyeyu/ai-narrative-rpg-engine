"""RuntimeState — the mutable, persistent game state.

Architecture contract: Only CommitPipeline (State Authority ⑤) may modify this.
Simulation Layer (③) reads via Snapshot, never writes directly.

MVP-0: Only Character State is modeled. Relationship, World, Progression, Timeline
are future extensions.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CharacterState:
    """Character State — mutable, owned by State Authority (Layer ⑤).

    This is the live state. Snapshot uses FrozenCharacterState for immutability.
    """

    character_id: str
    name: str
    mood: str = "neutral"
    trust: float = 0.0


@dataclass(frozen=True)
class FrozenCharacterState:
    """Frozen Character State — used in StateSnapshot for deep immutability.

    GPT (Point 7): "snapshot.characters['A'].trust += 1 理论上是允许的"
    Solution: Use frozen dataclass in Snapshot so modification raises FrozenInstanceError.
    """

    character_id: str
    name: str
    mood: str
    trust: float

    @classmethod
    def from_character(cls, c: CharacterState) -> FrozenCharacterState:
        """Create a frozen copy from a mutable CharacterState."""
        return cls(
            character_id=c.character_id,
            name=c.name,
            mood=c.mood,
            trust=c.trust,
        )


@dataclass
class RuntimeState:
    """Runtime State — the single source of ground truth at runtime."""

    characters: dict[str, CharacterState] = field(default_factory=dict)

    def get_character(self, character_id: str) -> CharacterState:
        return self.characters[character_id]

    def snapshot(self) -> StateSnapshot:
        """Create an immutable snapshot of current state."""
        from .snapshot import StateSnapshot

        return StateSnapshot.from_state(self)

    def restore(self, snapshot: StateSnapshot) -> None:
        """Restore state from a snapshot (rollback)."""
        self.characters = {
            cid: CharacterState(
                character_id=c.character_id,
                name=c.name,
                mood=c.mood,
                trust=c.trust,
            )
            for cid, c in snapshot.characters.items()
        }
