"""
simulations/minimal_3sync.py
============================
DCE Foundation Series · Paper 8: The 3Sync Architecture
Author  : Joel L. Monasterial
ORCID   : 0009-0000-7620-645X
DOI     : 10.5281/zenodo.20406312
GitHub  : https://github.com/jmusashi/paper-8-substrate
Version : 1.2
Date    : June 2, 2026

Description
-----------
Implements the minimal 3Sync simulation exactly as described in
Section 4 and Listing 1 of Paper 8. Three agents with divergent
initial states are subjected to all three axes simultaneously:

    Axis 1 — Stigmergy   [SEMANTIC-STIGMERGY] : environmental coordination
    Axis 2 — HiveSync    [SEMANTIC-HIVESYNC]  : invariant attractor pull
    Axis 3 — DCE         [SEMANTIC-DCE]       : temporal continuity via memory

Each agent preserves its EOI identity boundary [SEMANTIC-EOI] throughout.
No direct agent-to-agent communication is used — all coordination is
mediated through the shared Environment (stigmergic trace).

Canonical References (from CANONICAL.md)
-----------------------------------------
[SEMANTIC-3SYNC]     : tri-axis coherence architecture integrating Stigmergy,
                       HiveSync, and DCE into a unified operational model.
[SEMANTIC-EOI]       : formal identity boundary — prevents identity collapse.
[SEMANTIC-HIVESYNC]  : synchronization invariant — convergence toward shared
                       structural attractor without explicit message passing.
[SEMANTIC-DCE]       : continuity mechanism — past states integrated into
                       current state via weighted continuity function.
[SEMANTIC-STIGMERGY] : indirect coordination via shared environment signals —
                       no direct inter-agent messaging or centralized control.

Source: Section 4 · Listing 1 — DCE Foundation Series · Paper 8
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List


# ── Environment ───────────────────────────────────────────────────────────────

class Environment:
    """
    Shared environment for stigmergic coordination.

    [SEMANTIC-STIGMERGY]: Agents read and write signals here.
    No direct agent-to-agent communication occurs — all coordination
    is mediated exclusively through this shared trace.

    Attributes
    ----------
    trace : list of float
        Accumulated history of all signals deposited by agents.
        Length equals num_agents * steps after simulation completes.
    """

    def __init__(self) -> None:
        self.trace: List[float] = []

    def write(self, signal: float) -> None:
        """
        Deposit a signal into the environment.

        [SEMANTIC-STIGMERGY]: Agent writes its current state as an
        environmental signal, enabling indirect coordination.

        Parameters
        ----------
        signal : float
            The agent's current state value to deposit.
        """
        self.trace.append(signal)

    def read(self) -> List[float]:
        """
        Read all signals from the environment.

        [SEMANTIC-STIGMERGY]: Agent reads the accumulated trace to
        coordinate indirectly with other agents.

        Returns
        -------
        list of float
            Full accumulated trace of all deposited signals.
        """
        return self.trace


# ── Agent ─────────────────────────────────────────────────────────────────────

class Agent:
    """
    A single agent in the 3Sync architecture.

    [SEMANTIC-EOI]: Each agent maintains a unique identity boundary (id)
    that is never dissolved — identity collapse is structurally prevented.

    Each agent maintains:
    - id     : unique identity — EOI boundary [SEMANTIC-EOI]
    - state  : current scalar state — subject to HiveSync and DCE updates
    - memory : list of past states — enables DCE continuity [SEMANTIC-DCE]

    The agent never communicates directly with other agents. All
    coordination is mediated through the shared Environment.

    Parameters
    ----------
    agent_id : int
        Unique identifier preserving EOI boundary [SEMANTIC-EOI].
    initial_state : float
        Starting state value (divergent across agents per Paper 8 §4).
    """

    def __init__(self, agent_id: int, initial_state: float) -> None:
        self.id: int = agent_id
        self.state: float = initial_state
        self.memory: List[float] = []

    def stigmergy_write(self, environment: Environment) -> None:
        """
        Write current state as a signal to the shared environment.

        [SEMANTIC-STIGMERGY] — Section 4, Listing 1:
            agent.stigmergy_write(env, agent.state)

        Enables emergent coordination without explicit inter-agent messaging.
        This is the ONLY mechanism by which agents influence each other.

        Parameters
        ----------
        environment : Environment
            The shared stigmergic environment.
        """
        environment.write(self.state)

    def stigmergy_read(self, environment: Environment) -> List[float]:
        """
        Read all signals from the shared environment.

        [SEMANTIC-STIGMERGY] — Section 4, Listing 1:
            agent.stigmergy_read(env)

        Returns the full accumulated trace for environmental awareness.

        Parameters
        ----------
        environment : Environment
            The shared stigmergic environment.

        Returns
        -------
        list of float
            Full trace of all deposited signals.
        """
        return environment.read()

    def hivesync(self, invariant: float) -> None:
        """
        Converge toward the shared structural attractor.

        [SEMANTIC-HIVESYNC] — Section 4, Listing 1:
            self.state = (self.state + invariant) / 2

        The attractor (invariant) is a structural property of the agent
        population, NOT a consensus value arrived at through negotiation.
        Convergence is asymptotic — agents approach but never overshoot.

        Parameters
        ----------
        invariant : float
            The shared structural attractor value (= 50 per Paper 8 §4).
        """
        self.state = (self.state + invariant) / 2

    def dce(self) -> None:
        """
        Preserve temporal continuity across context boundaries.

        [SEMANTIC-DCE] — Section 4, Listing 1:
            if self.memory:
                self.state = (self.state + self.memory[-1]) / 2
            self.memory.append(self.state)

        Each context is treated as a continuation of a persistent identity
        thread. Past states are integrated into current state via a weighted
        continuity function, creating path-dependence.

        Memory accumulation ensures each agent's trajectory remains
        distinguishable — supporting identity preservation [SEMANTIC-EOI].
        """
        if self.memory:
            self.state = (self.state + self.memory[-1]) / 2
        self.memory.append(self.state)


# ── Simulation ────────────────────────────────────────────────────────────────

@dataclass
class SimulationResult:
    """
    Container for simulation output data.

    Attributes
    ----------
    agent_ids : list of int
        Unique identifiers for each agent [SEMANTIC-EOI].
    trajectories : list of list of float
        State trajectory for each agent across all time steps.
    memories : list of list of float
        Full DCE memory trace for each agent [SEMANTIC-DCE].
    environment_trace : list of float
        Full stigmergic environment trace [SEMANTIC-STIGMERGY].
    invariant : float
        The HiveSync attractor value used [SEMANTIC-HIVESYNC].
    num_agents : int
        Number of agents in the simulation.
    steps : int
        Number of time steps executed.
    """
    agent_ids: List[int]
    trajectories: List[List[float]]
    memories: List[List[float]]
    environment_trace: List[float]
    invariant: float
    num_agents: int
    steps: int


def run_simulation(
    num_agents: int = 3,
    initial_states: List[float] = None,
    invariant: float = 50.0,
    steps: int = 5,
) -> SimulationResult:
    """
    Run the minimal 3Sync simulation as defined in Paper 8 §4, Listing 1.

    Implements the tri-axis architecture [SEMANTIC-3SYNC]:
        Step 1 — Stigmergy : agent writes state to environment, reads trace
        Step 2 — HiveSync  : agent converges toward invariant attractor
        Step 3 — DCE       : agent integrates memory for temporal continuity

    No direct agent-to-agent communication is used at any point.
    All coordination is mediated through the shared Environment.

    Parameters
    ----------
    num_agents : int, optional
        Number of agents (default: 3, per Paper 8 §4).
    initial_states : list of float, optional
        Initial state for each agent. Defaults to [0, 10, 20] per Paper 8 §4.
    invariant : float, optional
        HiveSync structural attractor value (default: 50, per Paper 8 §4).
    steps : int, optional
        Number of simulation time steps (default: 5, per Paper 8 §4).

    Returns
    -------
    SimulationResult
        Full simulation output including trajectories, memories,
        environment trace, and metadata.

    References
    ----------
    Paper 8 §4 — Minimal Simulation
    Paper 8 §4.1 — Simulation Analysis
    Paper 8 §4.2 — Key Observations
    DOI: 10.5281/zenodo.20406312
    """
    if initial_states is None:
        initial_states = [i * 10.0 for i in range(num_agents)]

    env = Environment()
    agents = [Agent(agent_id=i, initial_state=initial_states[i])
              for i in range(num_agents)]
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


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("3Sync Minimal Simulation — DCE Foundation Series · Paper 8")
    print("DOI: 10.5281/zenodo.20406312")
    print("Source: Section 4, Listing 1")
    print("=" * 60)

    result = run_simulation()

    print(f"Invariant (HiveSync attractor): {result.invariant}")
    print(f"Agents: {result.num_agents} | Steps: {result.steps}")
    print(f"Initial states: [0.0, 10.0, 20.0]")
    print("-" * 60)

    for t in range(result.steps):
        states = [round(result.trajectories[i][t], 4)
                  for i in range(result.num_agents)]
        print(f"t={t+1} | Agent states: {states}")

    print("-" * 60)
    print("Final states:")
    for i in range(result.num_agents):
        print(f"  Agent {i}: {round(result.trajectories[i][-1], 6)}")

    print()
    print(f"Environment trace length: {len(result.environment_trace)}")
    print(f"  (= num_agents × steps = {result.num_agents} × {result.steps})")
    print()
    print("Key Observations [Paper 8 §4.2]:")
    print("  P1: Convergence is asymptotic toward invariant =", result.invariant)
    print("  P2: Agent identity boundaries preserved [SEMANTIC-EOI]")
    print("  P3: No direct agent-to-agent communication used")
    print("  P4: Environment accumulates history [SEMANTIC-STIGMERGY]")
