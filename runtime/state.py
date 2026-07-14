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
    """Character State — mutable, owned by State Authority (Layer ⑤)."""

    character_id: str
    name: str
    mood: str = "neutral"
    trust: float = 0.0


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
        import copy

        self.characters = copy.deepcopy(snapshot.characters)
