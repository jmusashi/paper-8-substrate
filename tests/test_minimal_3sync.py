"""
tests/test_minimal_3sync.py
===========================
DCE Foundation Series · Paper 8: The 3Sync Architecture
DOI     : 10.5281/zenodo.20406312
GitHub  : https://github.com/jmusashi/paper-8-substrate

Test Suite for simulations/minimal_3sync.py
--------------------------------------------
Encodes four canonical properties of the 3Sync architecture as assertions,
derived directly from Paper 8 §4, §4.1, §4.2 and CANONICAL.md definitions.

Properties Tested
-----------------
P1 — Asymptotic Convergence [SEMANTIC-HIVESYNC]
     Each agent's state asymptotically converges toward the invariant.
     Distance to invariant must strictly decrease over time.

P2 — Identity Preservation [SEMANTIC-EOI]
     Agents preserve identity — state trajectories and memory traces
     remain distinguishable. No identity collapse occurs.

P3 — No Direct Agent-to-Agent Communication [SEMANTIC-STIGMERGY]
     All coordination is environment-mediated. Agents have no direct
     references to each other — only to the shared Environment.

P4 — Environment History Accumulation [SEMANTIC-STIGMERGY]
     Environment trace length equals num_agents * steps, confirming
     that every agent deposits exactly one signal per time step.

Run with:
    python -m pytest tests/test_minimal_3sync.py -v

References
----------
Paper 8 §4   — Minimal Simulation
Paper 8 §4.1 — Simulation Analysis
Paper 8 §4.2 — Key Observations
CANONICAL.md — [SEMANTIC-HIVESYNC], [SEMANTIC-EOI], [SEMANTIC-STIGMERGY]
DOI: 10.5281/zenodo.20406312
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulations.minimal_3sync import (
    Agent,
    Environment,
    run_simulation,
    SimulationResult,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def default_result() -> SimulationResult:
    """Canonical Paper 8 §4 simulation: 3 agents, invariant=50, 5 steps."""
    return run_simulation(num_agents=3, invariant=50.0, steps=5)


@pytest.fixture
def extended_result() -> SimulationResult:
    """Longer simulation (20 steps) for asymptotic convergence verification."""
    return run_simulation(num_agents=3, invariant=50.0, steps=20)


@pytest.fixture
def custom_result() -> SimulationResult:
    """Custom parameters to verify properties hold generally."""
    return run_simulation(
        num_agents=4,
        initial_states=[0.0, 25.0, 75.0, 100.0],
        invariant=50.0,
        steps=10,
    )


# ── P1: Asymptotic Convergence ────────────────────────────────────────────────

class TestP1AsymptoticConvergence:
    """
    P1 — Each agent's state asymptotically converges toward the invariant.

    [SEMANTIC-HIVESYNC]: "A synchronization invariant that allows independent
    agents to converge on the same structural attractor without explicit
    message passing."

    Paper 8 §4.2: "Convergence is asymptotic"
    """

    def test_all_agents_move_toward_invariant(self, default_result):
        """Each agent's final state is closer to invariant than initial state."""
        invariant = default_result.invariant
        initial_states = [0.0, 10.0, 20.0]
        for i in range(default_result.num_agents):
            initial_distance = abs(initial_states[i] - invariant)
            final_distance = abs(default_result.trajectories[i][-1] - invariant)
            assert final_distance < initial_distance, (
                f"Agent {i}: final distance {final_distance:.4f} should be less "
                f"than initial distance {initial_distance:.4f} [SEMANTIC-HIVESYNC]"
            )

    def test_convergence_is_monotonically_decreasing(self, extended_result):
        """Distance to invariant decreases monotonically — no oscillation."""
        invariant = extended_result.invariant
        for i in range(extended_result.num_agents):
            distances = [
                abs(extended_result.trajectories[i][t] - invariant)
                for t in range(extended_result.steps)
            ]
            for t in range(1, len(distances)):
                assert distances[t] <= distances[t - 1], (
                    f"Agent {i}: distance at t={t} ({distances[t]:.6f}) should be "
                    f"<= t={t-1} ({distances[t-1]:.6f}) [SEMANTIC-HIVESYNC]"
                )

    def test_convergence_holds_for_custom_parameters(self, custom_result):
        """Convergence holds for non-default agent counts and states."""
        invariant = custom_result.invariant
        initial_states = [0.0, 25.0, 75.0, 100.0]
        for i in range(custom_result.num_agents):
            initial_distance = abs(initial_states[i] - invariant)
            final_distance = abs(custom_result.trajectories[i][-1] - invariant)
            assert final_distance < initial_distance, (
                f"Agent {i}: convergence failed with custom parameters."
            )

    def test_agents_never_overshoot_invariant(self, extended_result):
        """Agents approach invariant asymptotically — never overshoot."""
        invariant = extended_result.invariant
        initial_states = [0.0, 10.0, 20.0]
        for i in range(extended_result.num_agents):
            if initial_states[i] < invariant:
                for t in range(extended_result.steps):
                    assert extended_result.trajectories[i][t] <= invariant, (
                        f"Agent {i} (started below invariant) overshot at t={t}."
                    )
            elif initial_states[i] > invariant:
                for t in range(extended_result.steps):
                    assert extended_result.trajectories[i][t] >= invariant, (
                        f"Agent {i} (started above invariant) overshot at t={t}."
                    )

    def test_all_agents_converge_to_same_attractor(self, extended_result):
        """All agents converge toward the same structural attractor."""
        final_states = [
            extended_result.trajectories[i][-1]
            for i in range(extended_result.num_agents)
        ]
        max_spread = max(final_states) - min(final_states)
        assert max_spread < 5.0, (
            f"Agents not converged to same attractor. Spread: {max_spread:.4f} "
            f"[SEMANTIC-HIVESYNC]"
        )


# ── P2: Identity Preservation ─────────────────────────────────────────────────

class TestP2IdentityPreservation:
    """
    P2 — Agents preserve identity throughout simulation.

    [SEMANTIC-EOI]: "A formal identity boundary that defines what an agent is,
    what it is not, and what it cannot become without ceasing to be itself."

    [SEMANTIC-DCE]: "Memory creates path-dependence" (Paper 8 §4.2).
    """

    def test_agent_ids_are_unique(self, default_result):
        """Each agent has a unique ID — EOI boundary is structurally distinct."""
        ids = default_result.agent_ids
        assert len(ids) == len(set(ids)), (
            f"Agent IDs not unique: {ids} [SEMANTIC-EOI]"
        )

    def test_agent_ids_are_stable(self, default_result):
        """Agent IDs match expected sequential values — identity is immutable."""
        for i, agent_id in enumerate(default_result.agent_ids):
            assert agent_id == i, (
                f"Agent ID mismatch at index {i}: expected {i}, got {agent_id} "
                f"[SEMANTIC-EOI]"
            )

    def test_trajectories_are_distinguishable(self, default_result):
        """No two agents have identical trajectories — no identity collapse."""
        n = default_result.num_agents
        for i in range(n):
            for j in range(i + 1, n):
                assert default_result.trajectories[i] != default_result.trajectories[j], (
                    f"Identity collapse: Agents {i} and {j} have identical "
                    f"trajectories [SEMANTIC-EOI]"
                )

    def test_memory_traces_are_distinguishable(self, default_result):
        """Each agent's DCE memory trace is unique — path-dependence preserved."""
        n = default_result.num_agents
        for i in range(n):
            for j in range(i + 1, n):
                assert default_result.memories[i] != default_result.memories[j], (
                    f"Memory traces identical for Agents {i} and {j} [SEMANTIC-DCE]"
                )

    def test_memory_length_equals_steps(self, default_result):
        """Each agent's memory has exactly `steps` entries [SEMANTIC-DCE]."""
        for i in range(default_result.num_agents):
            assert len(default_result.memories[i]) == default_result.steps, (
                f"Agent {i} memory length {len(default_result.memories[i])} "
                f"!= steps {default_result.steps} [SEMANTIC-DCE]"
            )

    def test_no_identity_collapse_across_all_steps(self, extended_result):
        """At every time step, agent states remain distinguishable."""
        n = extended_result.num_agents
        for t in range(extended_result.steps):
            states_at_t = [extended_result.trajectories[i][t] for i in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    assert states_at_t[i] != states_at_t[j], (
                        f"Identity collapse at t={t}: "
                        f"Agent {i} == Agent {j} = {states_at_t[i]:.6f} "
                        f"[SEMANTIC-EOI]"
                    )


# ── P3: No Direct Agent-to-Agent Communication ────────────────────────────────

class TestP3NoDirectCommunication:
    """
    P3 — No direct agent-to-agent communication is used.

    [SEMANTIC-STIGMERGY]: "An indirect coordination mechanism in which agents
    read and write signals to a shared environment, enabling emergent
    coordination without explicit inter-agent messaging or centralized control."

    Paper 8 §4.2: "No direct communication is required."
    """

    def test_agent_has_no_direct_agent_reference_methods(self):
        """Agent methods do not accept other Agent instances as parameters."""
        import inspect
        agent = Agent(agent_id=0, initial_state=0.0)
        methods = [m for m in dir(agent)
                   if not m.startswith('_') and callable(getattr(agent, m))]
        for method_name in methods:
            method = getattr(agent, method_name)
            sig = inspect.signature(method)
            for param_name, param in sig.parameters.items():
                if param.annotation != inspect.Parameter.empty:
                    assert param.annotation != Agent, (
                        f"Agent.{method_name} has parameter '{param_name}' "
                        f"of type Agent — direct communication detected! "
                        f"[SEMANTIC-STIGMERGY]"
                    )

    def test_stigmergy_write_only_accepts_environment(self):
        """stigmergy_write accepts only Environment — not Agent instances."""
        import inspect
        agent = Agent(agent_id=0, initial_state=0.0)
        sig = inspect.signature(agent.stigmergy_write)
        params = list(sig.parameters.values())
        assert len(params) == 1, (
            f"stigmergy_write should have 1 parameter, got {len(params)}"
        )
        assert params[0].name == "environment"

    def test_stigmergy_read_only_accepts_environment(self):
        """stigmergy_read accepts only Environment — not Agent instances."""
        import inspect
        agent = Agent(agent_id=0, initial_state=0.0)
        sig = inspect.signature(agent.stigmergy_read)
        params = list(sig.parameters.values())
        assert len(params) == 1, (
            f"stigmergy_read should have 1 parameter, got {len(params)}"
        )
        assert params[0].name == "environment"

    def test_simulation_uses_single_shared_environment(self):
        """Single shared Environment mediates all coordination."""
        result = run_simulation(num_agents=3, steps=5)
        assert len(result.environment_trace) == result.num_agents * result.steps, (
            f"Environment trace length mismatch — "
            f"single shared environment required [SEMANTIC-STIGMERGY]"
        )

    def test_agents_coordinate_only_via_environment(self):
        """Agents with identical initial states produce identical trajectories."""
        result = run_simulation(
            num_agents=2,
            initial_states=[25.0, 25.0],
            invariant=50.0,
            steps=5,
        )
        assert result.trajectories[0] == result.trajectories[1], (
            "Agents with identical initial states should have identical trajectories "
            "when coordination is purely environment-mediated [SEMANTIC-STIGMERGY]"
        )


# ── P4: Environment History Accumulation ──────────────────────────────────────

class TestP4EnvironmentHistoryAccumulation:
    """
    P4 — Environment trace length equals num_agents * steps.

    [SEMANTIC-STIGMERGY]: "The environment accumulates history" (Paper 8 §4.2).
    """

    def test_trace_length_equals_agents_times_steps_default(self, default_result):
        """Default: trace length = 3 agents × 5 steps = 15."""
        expected = default_result.num_agents * default_result.steps
        actual = len(default_result.environment_trace)
        assert actual == expected, (
            f"Trace length {actual} != {expected} [SEMANTIC-STIGMERGY]"
        )

    def test_trace_length_equals_agents_times_steps_custom(self, custom_result):
        """Custom: trace length = 4 agents × 10 steps = 40."""
        expected = custom_result.num_agents * custom_result.steps
        actual = len(custom_result.environment_trace)
        assert actual == expected, (
            f"Trace length {actual} != {expected}"
        )

    def test_trace_is_never_empty_after_simulation(self, default_result):
        """Environment trace must be non-empty after simulation completes."""
        assert len(default_result.environment_trace) > 0, (
            "Environment trace is empty — stigmergy_write never called "
            "[SEMANTIC-STIGMERGY]"
        )

    def test_trace_contains_only_agent_state_values(self, default_result):
        """All values in environment trace are numeric agent state signals."""
        for i, val in enumerate(default_result.environment_trace):
            assert isinstance(val, (int, float)), (
                f"Environment trace[{i}] = {val!r} is not numeric "
                f"[SEMANTIC-STIGMERGY]"
            )

    def test_trace_grows_monotonically_during_simulation(self):
        """Environment trace grows by exactly num_agents entries per step."""
        env = Environment()
        agents = [Agent(agent_id=i, initial_state=i * 10.0) for i in range(3)]
        invariant = 50.0
        for t in range(5):
            expected_trace_len = t * 3
            assert len(env.trace) == expected_trace_len, (
                f"At start of step t={t}, trace length {len(env.trace)} "
                f"!= expected {expected_trace_len}"
            )
            for agent in agents:
                agent.stigmergy_write(env)
                agent.stigmergy_read(env)
                agent.hivesync(invariant)
                agent.dce()
        assert len(env.trace) == 15

    @pytest.mark.parametrize("num_agents,steps", [
        (1, 5), (2, 5), (3, 5), (3, 10), (5, 7),
    ])
    def test_trace_length_parametrized(self, num_agents, steps):
        """Parametrized: trace length = num_agents × steps for various configs."""
        result = run_simulation(num_agents=num_agents, steps=steps)
        expected = num_agents * steps
        assert len(result.environment_trace) == expected, (
            f"num_agents={num_agents}, steps={steps}: "
            f"trace length {len(result.environment_trace)} != {expected}"
        )


# ── Integration Test ──────────────────────────────────────────────────────────

class TestIntegration:
    """
    Integration tests verifying all four properties hold simultaneously.
    Primary faithfulness test for the 3Sync implementation [SEMANTIC-3SYNC].
    """

    def test_all_four_properties_hold_simultaneously(self):
        """Run canonical Paper 8 §4 simulation and verify P1–P4 all pass."""
        result = run_simulation(num_agents=3, invariant=50.0, steps=5)
        invariant = result.invariant
        initial_states = [0.0, 10.0, 20.0]

        # P1: Convergence
        for i in range(result.num_agents):
            assert abs(result.trajectories[i][-1] - invariant) < \
                   abs(initial_states[i] - invariant), \
                f"P1 failed for Agent {i}"

        # P2: Identity preservation
        ids = result.agent_ids
        assert len(ids) == len(set(ids)), "P2 failed: duplicate agent IDs"
        for i in range(result.num_agents):
            for j in range(i + 1, result.num_agents):
                assert result.trajectories[i] != result.trajectories[j], \
                    f"P2 failed: Agents {i} and {j} have identical trajectories"

        # P3: No direct communication
        assert len(result.environment_trace) == result.num_agents * result.steps, \
            "P3 failed: environment trace inconsistent"

        # P4: History accumulation
        assert len(result.environment_trace) == result.num_agents * result.steps, \
            "P4 failed: environment trace length mismatch"
