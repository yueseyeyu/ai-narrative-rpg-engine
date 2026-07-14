"""Shared test fixtures for Contract Tests."""

from __future__ import annotations

import pytest

from handlers.say_hello import SayHelloHandler
from runtime import (
    CharacterState,
    RuntimeState,
    Simulation,
)


@pytest.fixture
def initial_state() -> RuntimeState:
    """Create a minimal test state with two characters."""
    state = RuntimeState()
    state.characters["A"] = CharacterState("A", "Alice", trust=10.0)
    state.characters["B"] = CharacterState("B", "Bob", trust=10.0)
    return state


@pytest.fixture
def simulation() -> Simulation:
    """Create a Simulation instance with SayHelloHandler registered."""
    sim = Simulation()
    sim.register_handler("say_hello", SayHelloHandler())
    return sim
