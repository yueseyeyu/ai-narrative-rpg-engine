"""Shared test fixtures for Contract Tests."""

from __future__ import annotations

import pytest

from handlers.say_hello import SayHelloHandler
from runtime import (
    CharacterState,
    RuntimeState,
    SimulationContext,
    SimulationRuntime,
)


@pytest.fixture
def initial_state() -> RuntimeState:
    """Create a minimal test state with two characters."""
    state = RuntimeState()
    state.characters["A"] = CharacterState("A", "Alice", trust=10.0)
    state.characters["B"] = CharacterState("B", "Bob", trust=10.0)
    return state


@pytest.fixture
def simulation() -> SimulationRuntime:
    """Create a SimulationRuntime with SayHelloHandler registered."""
    sim = SimulationRuntime()
    sim.register_handler("say_hello", SayHelloHandler())
    return sim


@pytest.fixture
def make_context():
    """Factory fixture to create SimulationContext."""

    def _make(action, snapshot, seed=42):
        return SimulationContext(action=action, snapshot=snapshot, seed=seed)

    return _make
