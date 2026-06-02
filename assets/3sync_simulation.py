"""
3Sync Minimal Simulation
========================
DCE Foundation Series · Paper 8: The 3Sync Architecture
Author: Joel L. Monasterial
ORCID: 0009-0000-7620-645X
DOI: 10.5281/zenodo.20406312
Version: 1.2
Date: June 2, 2026

Description:
    Minimal simulation of 3Sync behavior. Three agents with divergent
    initial states are subjected to all three axes simultaneously,
    demonstrating:
    - Convergence toward the HiveSync attractor
    - Continuity maintenance via Decision Continuity Engineering (DCE)
    - Environmental coordination via Stigmergy

Source: Listing 1 — DCE Foundation Series · Paper 8 · Section 4
"""

# ── Canonical References ──────────────────────────────────────────────────────
# [SEMANTIC-3SYNC]     : tri-axis coherence architecture
# [SEMANTIC-HIVESYNC]  : synchronization invariant / shared attractor
# [SEMANTIC-DCE]       : decision continuity via weighted memory integration
# [SEMANTIC-STIGMERGY] : indirect coordination via shared environment
# [SEMANTIC-EOI]       : identity boundary — preserved throughout simulation
# ─────────────────────────────────────────────────────────────────────────────


class Agent:
    """
    Represents a single agent in the 3Sync architecture.

    Each agent maintains:
    - A unique identity (id) — EOI boundary [SEMANTIC-EOI]
    - A current state — subject to HiveSync and DCE
    - A memory — enables Decision Continuity Engineering [SEMANTIC-DCE]
    """

    def __init__(self, id, state):
        self.id = id
        self.state = state
        self.memory = []

    def stigmergy_read(self, environment):
        """
        Read environmental signals [SEMANTIC-STIGMERGY].
        Agents coordinate indirectly through the shared environment.
        """
        return environment.trace

    def stigmergy_write(self, environment, signal):
        """
        Write signals to the shared environment [SEMANTIC-STIGMERGY].
        Enables emergent coordination without explicit inter-agent messaging.
        """
        environment.trace.append(signal)

    def hivesync(self, invariant):
        """
        Converge toward the shared structural attractor [SEMANTIC-HIVESYNC].
        The attractor is a structural property of the agent population,
        not a consensus value arrived at through negotiation.
        """
        self.state = (self.state + invariant) / 2

    def dce(self):
        """
        Preserve temporal continuity across context boundaries [SEMANTIC-DCE].
        Each context is treated as a continuation of a persistent identity thread.
        Past states are integrated into current state via weighted continuity function.
        """
        if self.memory:
            self.state = (self.state + self.memory[-1]) / 2
        self.memory.append(self.state)


class Environment:
    """
    Shared environment for stigmergic coordination [SEMANTIC-STIGMERGY].
    Agents read and write signals here — no direct inter-agent communication.
    """

    def __init__(self):
        self.trace = []


# ── Simulation Setup ──────────────────────────────────────────────────────────

env = Environment()

# Three agents with divergent initial states (0, 10, 20)
# EOI boundary preserved — each agent maintains distinct identity [SEMANTIC-EOI]
agents = [Agent(id=i, state=i * 10) for i in range(3)]

# Shared structural attractor [SEMANTIC-HIVESYNC]
invariant = 50

# ── Simulation Loop ───────────────────────────────────────────────────────────

print("3Sync Minimal Simulation — DCE Foundation Series · Paper 8")
print(f"DOI: 10.5281/zenodo.20406312")
print(f"Invariant (HiveSync attractor): {invariant}")
print(f"Initial states: {[a.state for a in agents]}")
print("-" * 60)

for t in range(5):
    for agent in agents:
        # Axis 1: Stigmergy — write/read environmental signals
        agent.stigmergy_write(env, agent.state)
        agent.stigmergy_read(env)

        # Axis 2: HiveSync — converge toward shared attractor
        agent.hivesync(invariant)

        # Axis 3: DCE — maintain temporal continuity via memory
        agent.dce()

    states = [round(a.state, 4) for a in agents]
    print(f"t={t+1} | Agent states: {states}")

# ── Results ───────────────────────────────────────────────────────────────────

print("-" * 60)
print("Final states:")
for agent in agents:
    print(f"  Agent {agent.id}: {round(agent.state, 6)}")

print()
print("Key Observations:")
print("  - Convergence is asymptotic toward invariant =", invariant)
print("  - Memory creates path-dependence [SEMANTIC-DCE]")
print("  - Environment accumulates history [SEMANTIC-STIGMERGY]")
print("  - No direct inter-agent communication required")
print("  - Agent identity boundaries preserved throughout [SEMANTIC-EOI]")

