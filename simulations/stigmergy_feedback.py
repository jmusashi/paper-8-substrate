"""
simulations/stigmergy_feedback.py
==================================
DCE Foundation Series · Paper 8: The 3Sync Architecture
Author  : Joel L. Monasterial
ORCID   : 0009-0000-7620-645X
DOI     : 10.5281/zenodo.20406312
GitHub  : https://github.com/jmusashi/paper-8-substrate
Version : 1.2
Date    : June 2, 2026

Description
-----------
Extends the minimal 3Sync simulation (Section 4, Listing 1) with a richer
stigmergic feedback mechanism. In this simulation, Stigmergy not only records
signals but also MODULATES agent state based on the environment trace —
specifically, using the mean of recent signals as an additional environmental
influence on the agent's state update.

The tri-axis structure is strictly preserved [SEMANTIC-3SYNC]:
    Axis 1 — Stigmergy   [SEMANTIC-STIGMERGY] : write signal + read + modulate
    Axis 2 — HiveSync    [SEMANTIC-HIVESYNC]  : invariant attractor pull
    Axis 3 — DCE         [SEMANTIC-DCE]       : temporal continuity via memory

The EOI identity boundary [SEMANTIC-EOI] is preserved throughout.
No direct agent-to-agent communication is introduced.

Stigmergic Feedback Mechanism
------------------------------
In the minimal simulation, stigmergy_read() returns the trace but does not
influence agent state. In this extended simulation:

    1. Agent writes its current state to the environment (as before)
    2. Agent reads the recent trace (last `window` signals)
    3. Agent computes mean of recent signals as environmental feedback
    4. Environmental feedback is blended into agent state:
           state = (state + env_mean) / 2  [stigmergy modulation]
    5. HiveSync pull toward invariant (as before)
    6. DCE memory integration (as before)

Canonical References (from CANONICAL.md)
-----------------------------------------
[SEMANTIC-3SYNC]     : tri-axis coherence architecture
[SEMANTIC-STIGMERGY] : indirect coordination via shared environment signals
[SEMANTIC-HIVESYNC]  : convergence toward shared structural attractor
[SEMANTIC-DCE]       : temporal continuity via weighted memory integration
[SEMANTIC-EOI]       : identity boundary — never dissolved

Source: Extends Section 4, Listing 1 — DCE Foundation Series · Paper 8
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import statistics


# ── Environment with Feedback ─────────────────────────────────────────────────

class FeedbackEnvironment:
    """
    Extended shared environment with active stigmergic feedback.

    [SEMANTIC-STIGMERGY]: Agents read and write signals here.
    Unlike the minimal simulation's passive trace, this environment
    computes a feedback signal (mean of recent signals) that actively
    modulates agent state — completing the stigmergic feedback loop
    described in Figure 1 [SEMANTIC-3SYNC-DIAGRAM].

    Attributes
    ----------
    trace : list of float
        Full accumulated history of all deposited signals.
    window : int or None
        Number of recent signals used to compute feedback mean.
        If None, uses all signals in trace.
    """

    def __init__(self, window: Optional[int] = None) -> None:
        self.trace: List[float] = []
        self.window = window

    def write(self, signal: float) -> None:
        """
        Deposit a signal into the environment.

        [SEMANTIC-STIGMERGY]: Agent writes current state as environmental
        signal. This is the ONLY way agents influence each other.

        Parameters
        ----------
        signal : float
            Agent's current state value to deposit.
        """
        self.trace.append(signal)

    def read(self) -> List[float]:
        """
        Read all signals from the environment.

        Returns
        -------
        list of float
            Full accumulated trace.
        """
        return self.trace

    def feedback(self) -> Optional[float]:
        """
        Compute environmental feedback signal as mean of recent trace.

        [SEMANTIC-STIGMERGY]: The feedback loop completes the stigmergic
        cycle — signals deposited back into the environment modulate
        agent behavior. Returns None if trace is empty.

        Returns
        -------
        float or None
            Mean of recent `window` signals, or None if trace is empty.
        """
        if not self.trace:
            return None
        recent = self.trace[-self.window:] if self.window else self.trace
        return statistics.mean(recent)


# ── Extended Agent ────────────────────────────────────────────────────────────

class FeedbackAgent:
    """
    Agent with richer stigmergic feedback in the 3Sync architecture.

    [SEMANTIC-EOI]: Each agent maintains a unique identity boundary (id)
    that is never dissolved throughout the simulation.

    Extends the minimal Agent with stigmergy_modulate() — blends
    environmental feedback into agent state before HiveSync and DCE.

    Parameters
    ----------
    agent_id : int
        Unique identifier preserving EOI boundary [SEMANTIC-EOI].
    initial_state : float
        Starting state value.
    """

    def __init__(self, agent_id: int, initial_state: float) -> None:
        self.id: int = agent_id
        self.state: float = initial_state
        self.memory: List[float] = []

    def stigmergy_write(self, environment: FeedbackEnvironment) -> None:
        """
        Write current state as a signal to the shared environment.

        [SEMANTIC-STIGMERGY]: Identical to minimal simulation.
        This is the ONLY mechanism by which agents influence each other.

        Parameters
        ----------
        environment : FeedbackEnvironment
            The shared stigmergic environment.
        """
        environment.write(self.state)

    def stigmergy_read(self, environment: FeedbackEnvironment) -> List[float]:
        """
        Read all signals from the shared environment.

        [SEMANTIC-STIGMERGY]: Returns full trace for environmental awareness.

        Parameters
        ----------
        environment : FeedbackEnvironment
            The shared stigmergic environment.

        Returns
        -------
        list of float
            Full accumulated trace.
        """
        return environment.read()

    def stigmergy_modulate(self, environment: FeedbackEnvironment) -> None:
        """
        Modulate agent state based on environmental feedback signal.

        Extended stigmergic mechanism — blends environment mean into state:
            state = (state + env_mean) / 2

        [SEMANTIC-STIGMERGY]: Operationalizes the feedback loop from
        Figure 1 [SEMANTIC-3SYNC-DIAGRAM]. If trace is empty, no-op.

        Parameters
        ----------
        environment : FeedbackEnvironment
            The shared stigmergic environment with feedback capability.
        """
        fb = environment.feedback()
        if fb is not None:
            self.state = (self.state + fb) / 2

    def hivesync(self, invariant: float) -> None:
        """
        Converge toward the shared structural attractor.

        [SEMANTIC-HIVESYNC]: Identical to minimal simulation.
        state = (state + invariant) / 2

        Parameters
        ----------
        invariant : float
            The shared structural attractor value.
        """
        self.state = (self.state + invariant) / 2

    def dce(self) -> None:
        """
        Preserve temporal continuity across context boundaries.

        [SEMANTIC-DCE]: Identical to minimal simulation.
        Past states integrated via weighted continuity function.
        Memory creates path-dependence.
        """
        if self.memory:
            self.state = (self.state + self.memory[-1]) / 2
        self.memory.append(self.state)


# ── Simulation Result ─────────────────────────────────────────────────────────

@dataclass
class FeedbackSimulationResult:
    """
    Container for stigmergy feedback simulation output.

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
    feedback_signals : list of float
        Environmental feedback signal computed at each agent-step.
    invariant : float
        The HiveSync attractor value used [SEMANTIC-HIVESYNC].
    num_agents : int
        Number of agents in the simulation.
    steps : int
        Number of time steps executed.
    window : Optional[int]
        Feedback window size used for mean computation.
    """
    agent_ids: List[int]
    trajectories: List[List[float]]
    memories: List[List[float]]
    environment_trace: List[float]
    feedback_signals: List[float]
    invariant: float
    num_agents: int
    steps: int
    window: Optional[int]


def run_feedback_simulation(
    num_agents: int = 3,
    initial_states: List[float] = None,
    invariant: float = 50.0,
    steps: int = 5,
    window: Optional[int] = None,
) -> FeedbackSimulationResult:
    """
    Run the extended 3Sync simulation with stigmergic feedback modulation.

    Tri-axis structure [SEMANTIC-3SYNC]:
        Step 1a — Stigmergy write   : deposit state signal to environment
        Step 1b — Stigmergy read    : read accumulated trace
        Step 1c — Stigmergy modulate: blend env feedback into agent state
        Step 2  — HiveSync          : converge toward invariant attractor
        Step 3  — DCE               : integrate memory for temporal continuity

    Parameters
    ----------
    num_agents : int, optional
        Number of agents (default: 3).
    initial_states : list of float, optional
        Initial state for each agent. Defaults to [i*10 for i in range(n)].
    invariant : float, optional
        HiveSync structural attractor value (default: 50).
    steps : int, optional
        Number of simulation time steps (default: 5).
    window : int or None, optional
        Number of recent signals for feedback mean. None = all signals.

    Returns
    -------
    FeedbackSimulationResult
        Full simulation output including trajectories, memories,
        environment trace, feedback signals, and metadata.

    References
    ----------
    Paper 8 §4   — Minimal Simulation (base)
    CANONICAL.md — [SEMANTIC-STIGMERGY], [SEMANTIC-3SYNC-DIAGRAM]
    DOI: 10.5281/zenodo.20406312
    """
    if initial_states is None:
        initial_states = [i * 10.0 for i in range(num_agents)]

    env = FeedbackEnvironment(window=window)
    agents = [FeedbackAgent(agent_id=i, initial_state=initial_states[i])
              for i in range(num_agents)]
    trajectories: List[List[float]] = [[] for _ in range(num_agents)]
    feedback_signals: List[float] = []

    for _t in range(steps):
        for i, agent in enumerate(agents):
            agent.stigmergy_write(env)
            agent.stigmergy_read(env)
            fb = env.feedback()
            if fb is not None:
                feedback_signals.append(fb)
            agent.stigmergy_modulate(env)
            agent.hivesync(invariant)
            agent.dce()
            trajectories[i].append(agent.state)

    return FeedbackSimulationResult(
        agent_ids=[a.id for a in agents],
        trajectories=trajectories,
        memories=[list(a.memory) for a in agents],
        environment_trace=list(env.trace),
        feedback_signals=feedback_signals,
        invariant=invariant,
        num_agents=num_agents,
        steps=steps,
        window=window,
    )


# ── CLI Entry Point ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("3Sync Stigmergy Feedback Simulation — DCE Foundation Series · Paper 8")
    print("DOI: 10.5281/zenodo.20406312")
    print("Extension: Richer stigmergic feedback modulation")
    print("=" * 60)

    result = run_feedback_simulation(window=5)

    print(f"Invariant (HiveSync attractor): {result.invariant}")
    print(f"Agents: {result.num_agents} | Steps: {result.steps}")
    print(f"Feedback window: {result.window or 'all signals'}")
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
    print(f"Feedback signals recorded: {len(result.feedback_signals)}")
    print()
    print("Tri-Axis Structure Preserved [SEMANTIC-3SYNC]:")
    print("  Stigmergy : write + read + modulate (env feedback)")
    print("  HiveSync  : invariant attractor pull")
    print("  DCE       : temporal continuity via memory")
    print("  EOI       : identity boundaries preserved throughout")
