"""Action — the input to Simulation Layer (Layer ③).

Architecture contract: Action is immutable. Simulation reads it, never modifies it.
Corresponds to Action Record in the Pipeline (produced by ② Execution Authority).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Action:
    """A validated Action Record — input to one Simulation Tick."""

    action_id: str
    action_type: str
    actor: str
    target: str | None = None
    parameters: dict[str, Any] = field(default_factory=dict)
