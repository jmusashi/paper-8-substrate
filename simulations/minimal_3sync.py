"""
simulations/minimal_3sync.py
============================
DCE Foundation Series · Paper 8: The 3Sync Architecture
Author  : Joel L. Monasterial
ORCID   : 0009-0000-7620-645X
DOI     : 10.5281/zenodo.20406311
GitHub  : https://github.com/jmusashi/paper-8-substrate
Version : 1.3
Date    : October 1, 2026

Reference implementation of the minimal Paper 8 realization.

The program exposes three operational axes:
    Stigmergy  : environment-mediated coordination
    HiveSync   : invariant-directed convergence
    DCE        : temporal continuity

The combined transition operates subject to the EOI identity constraint.
EOI is not a fourth operational axis.

Implementation boundary
-----------------------
This program is a reference realization through which selected Paper 8
properties can be observed and tested. It is not the definition of 3Sync.
The published Paper 8 v1.3 specification remains authoritative.

In this minimal realization, agents deposit and read environmental traces,
but the returned trace is not used to modify agent state. Active environmental
feedback belongs to the extended realization.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional


class Environment:
    """Shared environmental trace medium for the Stigmergy axis."""

    def __init__(self) -> None:
        self.trace: List[float] = []

    def write(self, signal: float) -> None:
        """Deposit an agent signal into the accumulated environmental trace."""
        self.trace.append(signal)

    def read(self) -> List[float]:
        """Return the accumulated environmental trace."""
        return self.trace


class Agent:
    """Agent state used by the minimal reference realization.

    ``id`` is an implementation identifier. ``memory`` is an observable
    temporal record used by this realization. Neither field creates identity;
    the architecture operates subject to the EOI identity constraint.
    """

    def __init__(self, agent_id: int, initial_state: float) -> None:
        self.id: int = agent_id
        self.state: float = initial_state
        self.memory: List[float] = []

    def stigmergy_write(self, environment: Environment) -> None:
        """Deposit current state into the shared environment."""
        environment.write(self.state)

    def stigmergy_read(self, environment: Environment) -> List[float]:
        """Read the shared trace without state modulation in this realization."""
        return environment.read()

    def hivesync(self, invariant: float) -> None:
        """Move state halfway toward the structural attractor."""
        self.state = (self.state + invariant) / 2

    def dce(self) -> None:
        """Apply the reference continuity update and append resulting state.

        Memory makes the trajectory observable. It should not be interpreted
        as the origin, proof, or complete determination of identity.
        """
        if self.memory:
            self.state = (self.state + self.memory[-1]) / 2
        self.memory.append(self.state)


@dataclass
class SimulationResult:
    """Observable output of the minimal reference realization."""

    agent_ids: List[int]
    trajectories: List[List[float]]
    memories: List[List[float]]
    environment_trace: List[float]
    invariant: float
    num_agents: int
    steps: int


def run_simulation(
    num_agents: int = 3,
    initial_states: Optional[List[float]] = None,
    invariant: float = 50.0,
    steps: int = 5,
) -> SimulationResult:
    """Run the minimal Paper 8 reference simulation.

    Per step, each agent:
      1. deposits its current state into the environment;
      2. reads the environmental trace without applying feedback modulation;
      3. performs the HiveSync attractor update; and
      4. performs the reference DCE continuity update.

    The realization requires no direct agent-to-agent communication.
    """
    if initial_states is None:
        initial_states = [i * 10.0 for i in range(num_agents)]

    if len(initial_states) != num_agents:
        raise ValueError("initial_states length must equal num_agents")

    env = Environment()
    agents = [
        Agent(agent_id=i, initial_state=initial_states[i])
        for i in range(num_agents)
    ]
    trajectories: List[List[float]] = [[] for _ in range(num_agents)]

    for _t in range(steps):
        for i, agent in enumerate(agents):
            agent.stigmergy_write(env)
            agent.stigmergy_read(env)
            agent.hivesync(invariant)
            agent.dce()
            trajectories[i].append(agent.state)

    return SimulationResult(
        agent_ids=[a.id for a in agents],
        trajectories=trajectories,
        memories=[list(a.memory) for a in agents],
        environment_trace=list(env.trace),
        invariant=invariant,
        num_agents=num_agents,
        steps=steps,
    )


if __name__ == "__main__":
    result = run_simulation()

    print("3Sync Minimal Reference Simulation · DCE Foundation Series · Paper 8 v1.3")
    print("DOI: 10.5281/zenodo.20406311")
    print("=" * 60)
    print(f"Invariant (HiveSync attractor): {result.invariant}")
    print(f"Agents: {result.num_agents} | Steps: {result.steps}")
    print("-" * 60)

    for t in range(result.steps):
        states = [
            round(result.trajectories[i][t], 4)
            for i in range(result.num_agents)
        ]
        print(f"t={t + 1} | Agent states: {states}")

    print("-" * 60)
    print("Final states:")
    for i in range(result.num_agents):
        print(f"  Agent {i}: {round(result.trajectories[i][-1], 6)}")

    print()
    print(f"Environment trace length: {len(result.environment_trace)}")
    print(f"  (= num_agents × steps = {result.num_agents} × {result.steps})")
    print()
    print("Observable properties:")
    print("  P1: Asymptotic convergence toward the structural attractor")
    print("  P2: Distinguishable trajectories remain observable")
    print("  P3: No direct agent-to-agent communication is required")
    print("  P4: Environmental history accumulates")
    print()
    print("Interpretation: these observations are implementation evidence under")
    print("the tested conditions; this program is not the definition of 3Sync.")
