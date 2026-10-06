"""
simulations/stigmergy_feedback.py
==================================
DCE Foundation Series · Paper 8: The 3Sync Architecture
Author  : Joel L. Monasterial
ORCID   : 0009-0000-7620-645X
DOI     : 10.5281/zenodo.20406311
GitHub  : https://github.com/jmusashi/paper-8-substrate
Version : 1.3
Date    : October 1, 2026

Reference implementation of the extended environmental-feedback realization.

This extension closes the environmental modulation loop within the Stigmergy
axis. Environmental traces influence subsequent agent state through a mean of
recent signals. Environmental feedback is not a fourth operational axis.

The three operational axes remain:
    Stigmergy  : environment-mediated coordination, including feedback here
    HiveSync   : invariant-directed convergence
    DCE        : temporal continuity

The combined operation remains subject to the EOI identity constraint.

Implementation boundary
-----------------------
This program is a reference realization through which selected Paper 8
properties can be observed and tested. It is not the definition of 3Sync.
The published Paper 8 v1.3 specification remains authoritative.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import statistics


class FeedbackEnvironment:
    """Shared trace medium with active feedback for the Stigmergy axis."""

    def __init__(self, window: Optional[int] = None) -> None:
        if window is not None and window <= 0:
            raise ValueError("window must be a positive integer or None")
        self.trace: List[float] = []
        self.window = window

    def write(self, signal: float) -> None:
        """Deposit an agent signal into the environmental trace."""
        self.trace.append(signal)

    def read(self) -> List[float]:
        """Return the accumulated environmental trace."""
        return self.trace

    def feedback(self) -> Optional[float]:
        """Return the mean of the applicable environmental feedback window."""
        if not self.trace:
            return None
        recent = self.trace[-self.window:] if self.window is not None else self.trace
        return statistics.mean(recent)


class FeedbackAgent:
    """Agent state used by the extended reference realization.

    ``id`` is an implementation identifier. ``memory`` is an observable
    temporal record. Neither field creates identity; the architecture operates
    subject to the EOI identity constraint.
    """

    def __init__(self, agent_id: int, initial_state: float) -> None:
        self.id: int = agent_id
        self.state: float = initial_state
        self.memory: List[float] = []

    def stigmergy_write(self, environment: FeedbackEnvironment) -> None:
        environment.write(self.state)

    def stigmergy_read(self, environment: FeedbackEnvironment) -> List[float]:
        return environment.read()

    def stigmergy_modulate(self, environment: FeedbackEnvironment) -> None:
        """Blend environmental feedback into state within the Stigmergy axis."""
        feedback = environment.feedback()
        if feedback is not None:
            self.state = (self.state + feedback) / 2

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
class FeedbackSimulationResult:
    """Observable output of the extended environmental-feedback realization."""

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
    initial_states: Optional[List[float]] = None,
    invariant: float = 50.0,
    steps: int = 5,
    window: Optional[int] = None,
) -> FeedbackSimulationResult:
    """Run the extended Paper 8 environmental-feedback realization.

    Per agent-step:
      1. Stigmergy deposits state into the environment.
      2. Stigmergy reads the accumulated trace.
      3. Stigmergy feedback modulates state using the trace mean.
      4. HiveSync applies invariant-directed convergence.
      5. DCE applies the reference temporal-continuity update.

    No direct agent-to-agent communication is required by this realization.
    """
    if initial_states is None:
        initial_states = [i * 10.0 for i in range(num_agents)]

    if len(initial_states) != num_agents:
        raise ValueError("initial_states length must equal num_agents")

    env = FeedbackEnvironment(window=window)
    agents = [
        FeedbackAgent(agent_id=i, initial_state=initial_states[i])
        for i in range(num_agents)
    ]
    trajectories: List[List[float]] = [[] for _ in range(num_agents)]
    feedback_signals: List[float] = []

    for _t in range(steps):
        for i, agent in enumerate(agents):
            agent.stigmergy_write(env)
            agent.stigmergy_read(env)
            feedback = env.feedback()
            if feedback is not None:
                feedback_signals.append(feedback)
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


if __name__ == "__main__":
    result = run_feedback_simulation(window=5)

    print("3Sync Extended Environmental-Feedback Reference Simulation · Paper 8 v1.3")
    print("DOI: 10.5281/zenodo.20406311")
    print("=" * 70)
    print(f"Invariant (HiveSync attractor): {result.invariant}")
    print(f"Agents: {result.num_agents} | Steps: {result.steps}")
    print(f"Feedback window: {result.window if result.window is not None else 'all signals'}")
    print("-" * 70)

    for t in range(result.steps):
        states = [
            round(result.trajectories[i][t], 4)
            for i in range(result.num_agents)
        ]
        print(f"t={t + 1} | Agent states: {states}")

    print("-" * 70)
    print(f"Environment trace length: {len(result.environment_trace)}")
    print(f"Feedback signals recorded: {len(result.feedback_signals)}")
    print()
    print("Observable properties:")
    print("  P1: Asymptotic convergence toward the structural attractor")
    print("  P2: Distinguishable trajectories remain observable")
    print("  P3: No direct agent-to-agent communication is required")
    print("  P4: Environmental history accumulates")
    print("  P5: Environmental feedback modulation is active")
    print("  P6: The configured feedback window is applied")
    print("  P7: The three-axis structure remains preserved")
    print()
    print("EOI remains the identity constraint, not a fourth operational axis.")
    print("These observations are implementation evidence under tested conditions;")
    print("this program is not the definition of 3Sync.")
