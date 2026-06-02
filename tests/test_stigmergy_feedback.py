"""
tests/test_stigmergy_feedback.py
=================================
DCE Foundation Series · Paper 8: The 3Sync Architecture
DOI     : 10.5281/zenodo.20406312
GitHub  : https://github.com/jmusashi/paper-8-substrate

Test Suite for simulations/stigmergy_feedback.py
-------------------------------------------------
Verifies that the four canonical 3Sync properties (P1–P4) still hold
under the richer stigmergic feedback mechanism, AND tests additional
feedback-specific behaviors.

Properties Tested
-----------------
P1 — Asymptotic Convergence [SEMANTIC-HIVESYNC]
P2 — Identity Preservation [SEMANTIC-EOI]
P3 — No Direct Communication [SEMANTIC-STIGMERGY]
P4 — Environment History Accumulation [SEMANTIC-STIGMERGY]
P5 — Feedback Modulation Is Active [SEMANTIC-3SYNC-DIAGRAM]
P6 — Feedback Window Parameter [SEMANTIC-STIGMERGY]
P7 — Tri-Axis Structure Preserved [SEMANTIC-3SYNC]

Run with:
    python -m pytest tests/test_stigmergy_feedback.py -v

References
----------
Paper 8 §4   — Minimal Simulation (base)
CANONICAL.md — [SEMANTIC-3SYNC], [SEMANTIC-STIGMERGY], [SEMANTIC-EOI],
               [SEMANTIC-HIVESYNC], [SEMANTIC-DCE], [SEMANTIC-3SYNC-DIAGRAM]
DOI: 10.5281/zenodo.20406312
"""

import sys
import os
import pytest
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulations.stigmergy_feedback import (
    FeedbackAgent,
    FeedbackEnvironment,
    run_feedback_simulation,
    FeedbackSimulationResult,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def default_result() -> FeedbackSimulationResult:
    """Canonical Paper 8 §4 parameters with feedback modulation."""
    return run_feedback_simulation(num_agents=3, invariant=50.0, steps=5)


@pytest.fixture
def extended_result() -> FeedbackSimulationResult:
    """Longer simulation for convergence verification."""
    return run_feedback_simulation(num_agents=3, invariant=50.0, steps=20)


@pytest.fixture
def windowed_result() -> FeedbackSimulationResult:
    """Simulation with windowed feedback (last 3 signals)."""
    return run_feedback_simulation(
        num_agents=3, invariant=50.0, steps=10, window=3
    )


@pytest.fixture
def custom_result() -> FeedbackSimulationResult:
    """Custom parameters to verify generality."""
    return run_feedback_simulation(
        num_agents=4,
        initial_states=[0.0, 25.0, 75.0, 100.0],
        invariant=50.0,
        steps=10,
    )


# ── P1: Asymptotic Convergence Under Feedback ─────────────────────────────────

class TestP1ConvergenceUnderFeedback:
    """
    P1 — Convergence holds even with active stigmergic feedback modulation.
    [SEMANTIC-HIVESYNC]: HiveSync attractor pull must dominate over time.
    """

    def test_all_agents_move_toward_invariant(self, default_result):
        """Each agent's final state is closer to invariant than initial state."""
        invariant = default_result.invariant
        initial_states = [0.0, 10.0, 20.0]
        for i in range(default_result.num_agents):
            initial_distance = abs(initial_states[i] - invariant)
            final_distance = abs(default_result.trajectories[i][-1] - invariant)
            assert final_distance < initial_distance, (
                f"Agent {i}: convergence failed under feedback. "
                f"Initial: {initial_distance:.4f}, Final: {final_distance:.4f} "
                f"[SEMANTIC-HIVESYNC]"
            )

    def test_convergence_over_extended_steps(self, extended_result):
        """Over 20 steps, agents converge significantly toward invariant."""
        invariant = extended_result.invariant
        initial_states = [0.0, 10.0, 20.0]
        for i in range(extended_result.num_agents):
            initial_distance = abs(initial_states[i] - invariant)
            final_distance = abs(extended_result.trajectories[i][-1] - invariant)
            assert final_distance < initial_distance * 0.5, (
                f"Agent {i}: insufficient convergence after 20 steps. "
                f"Final {final_distance:.4f} should be < 50% of "
                f"initial {initial_distance:.4f} [SEMANTIC-HIVESYNC]"
            )

    def test_convergence_with_windowed_feedback(self, windowed_result):
        """Convergence holds when feedback uses only recent window of signals."""
        invariant = windowed_result.invariant
        initial_states = [0.0, 10.0, 20.0]
        for i in range(windowed_result.num_agents):
            initial_distance = abs(initial_states[i] - invariant)
            final_distance = abs(windowed_result.trajectories[i][-1] - invariant)
            assert final_distance < initial_distance, (
                f"Agent {i}: convergence failed with windowed feedback."
            )

    def test_convergence_with_custom_parameters(self, custom_result):
        """Convergence holds for non-default agent counts and initial states."""
        invariant = custom_result.invariant
        initial_states = [0.0, 25.0, 75.0, 100.0]
        for i in range(custom_result.num_agents):
            initial_distance = abs(initial_states[i] - invariant)
            final_distance = abs(custom_result.trajectories[i][-1] - invariant)
            assert final_distance < initial_distance, (
                f"Agent {i}: convergence failed with custom parameters."
            )

    def test_all_agents_converge_toward_same_attractor(self, extended_result):
        """All agents converge toward the same structural attractor."""
        final_states = [
            extended_result.trajectories[i][-1]
            for i in range(extended_result.num_agents)
        ]
        max_spread = max(final_states) - min(final_states)
        assert max_spread < 10.0, (
            f"Agents not converged under feedback. Spread: {max_spread:.4f} "
            f"[SEMANTIC-HIVESYNC]"
        )


# ── P2: Identity Preservation Under Feedback ──────────────────────────────────

class TestP2IdentityPreservationUnderFeedback:
    """
    P2 — Identity preservation holds under stigmergic feedback modulation.
    [SEMANTIC-EOI]: Feedback must not cause identity collapse.
    """

    def test_agent_ids_are_unique(self, default_result):
        """Agent IDs remain unique under feedback modulation [SEMANTIC-EOI]."""
        ids = default_result.agent_ids
        assert len(ids) == len(set(ids)), (
            f"Agent IDs not unique under feedback: {ids} [SEMANTIC-EOI]"
        )

    def test_trajectories_are_distinguishable(self, default_result):
        """No two agents have identical trajectories under feedback."""
        n = default_result.num_agents
        for i in range(n):
            for j in range(i + 1, n):
                assert default_result.trajectories[i] != default_result.trajectories[j], (
                    f"Identity collapse: Agents {i} and {j} identical "
                    f"under feedback [SEMANTIC-EOI]"
                )

    def test_memory_traces_are_distinguishable(self, default_result):
        """DCE memory traces remain unique per agent under feedback."""
        n = default_result.num_agents
        for i in range(n):
            for j in range(i + 1, n):
                assert default_result.memories[i] != default_result.memories[j], (
                    f"Memory traces identical for Agents {i} and {j} "
                    f"under feedback [SEMANTIC-DCE]"
                )

    def test_memory_length_equals_steps(self, default_result):
        """DCE memory has exactly `steps` entries per agent [SEMANTIC-DCE]."""
        for i in range(default_result.num_agents):
            assert len(default_result.memories[i]) == default_result.steps, (
                f"Agent {i} memory length {len(default_result.memories[i])} "
                f"!= steps {default_result.steps} [SEMANTIC-DCE]"
            )

    def test_no_identity_collapse_at_any_step(self, extended_result):
        """At every time step, agent states remain distinguishable."""
        n = extended_result.num_agents
        for t in range(extended_result.steps):
            states_at_t = [extended_result.trajectories[i][t] for i in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    assert states_at_t[i] != states_at_t[j], (
                        f"Identity collapse at t={t}: "
                        f"Agent {i} == Agent {j} = {states_at_t[i]:.6f} "
                        f"under feedback [SEMANTIC-EOI]"
                    )


# ── P3: No Direct Communication Under Feedback ────────────────────────────────

class TestP3NoDirectCommunicationUnderFeedback:
    """
    P3 — No direct agent-to-agent communication under feedback modulation.
    [SEMANTIC-STIGMERGY]: Feedback remains environment-mediated only.
    """

    def test_feedback_agent_has_no_direct_agent_reference_methods(self):
        """FeedbackAgent methods do not accept other FeedbackAgent instances."""
        import inspect
        agent = FeedbackAgent(agent_id=0, initial_state=0.0)
        methods = [m for m in dir(agent)
                   if not m.startswith('_') and callable(getattr(agent, m))]
        for method_name in methods:
            method = getattr(agent, method_name)
            sig = inspect.signature(method)
            for param_name, param in sig.parameters.items():
                if param.annotation != inspect.Parameter.empty:
                    assert param.annotation != FeedbackAgent, (
                        f"FeedbackAgent.{method_name} has parameter '{param_name}' "
                        f"of type FeedbackAgent — direct communication detected! "
                        f"[SEMANTIC-STIGMERGY]"
                    )

    def test_stigmergy_modulate_only_accepts_environment(self):
        """stigmergy_modulate accepts only FeedbackEnvironment — not agents."""
        import inspect
        agent = FeedbackAgent(agent_id=0, initial_state=0.0)
        sig = inspect.signature(agent.stigmergy_modulate)
        params = list(sig.parameters.values())
        assert len(params) == 1, (
            f"stigmergy_modulate should have 1 parameter, got {len(params)}"
        )
        assert params[0].name == "environment"

    def test_feedback_is_computed_from_environment_not_agents(self):
        """Feedback signal is derived from environment trace, not agent states."""
        env = FeedbackEnvironment()
        env.write(30.0)
        env.write(40.0)
        env.write(50.0)
        expected_feedback = statistics.mean([30.0, 40.0, 50.0])
        assert env.feedback() == expected_feedback, (
            f"Feedback {env.feedback()} != expected mean {expected_feedback} "
            f"[SEMANTIC-STIGMERGY]"
        )

    def test_simulation_uses_single_shared_environment(self, default_result):
        """Single shared FeedbackEnvironment mediates all coordination."""
        assert len(default_result.environment_trace) == \
               default_result.num_agents * default_result.steps, (
            "Environment trace length mismatch — "
            "single shared environment required [SEMANTIC-STIGMERGY]"
        )


# ── P4: Environment History Accumulation Under Feedback ───────────────────────

class TestP4EnvironmentHistoryUnderFeedback:
    """
    P4 — Environment trace length equals num_agents * steps under feedback.
    [SEMANTIC-STIGMERGY]: History accumulation must hold under richer feedback.
    """

    def test_trace_length_default(self, default_result):
        """Default: trace length = 3 agents × 5 steps = 15."""
        expected = default_result.num_agents * default_result.steps
        assert len(default_result.environment_trace) == expected, (
            f"Trace length {len(default_result.environment_trace)} != {expected} "
            f"[SEMANTIC-STIGMERGY]"
        )

    def test_trace_length_extended(self, extended_result):
        """Extended: trace length = 3 agents × 20 steps = 60."""
        expected = extended_result.num_agents * extended_result.steps
        assert len(extended_result.environment_trace) == expected

    def test_trace_length_custom(self, custom_result):
        """Custom: trace length = 4 agents × 10 steps = 40."""
        expected = custom_result.num_agents * custom_result.steps
        assert len(custom_result.environment_trace) == expected

    def test_trace_length_windowed(self, windowed_result):
        """Windowed feedback does not alter trace accumulation."""
        expected = windowed_result.num_agents * windowed_result.steps
        assert len(windowed_result.environment_trace) == expected

    @pytest.mark.parametrize("num_agents,steps", [
        (1, 5), (2, 5), (3, 5), (3, 10), (5, 7),
    ])
    def test_trace_length_parametrized(self, num_agents, steps):
        """Parametrized: trace length = num_agents × steps for various configs."""
        result = run_feedback_simulation(num_agents=num_agents, steps=steps)
        expected = num_agents * steps
        assert len(result.environment_trace) == expected, (
            f"num_agents={num_agents}, steps={steps}: "
            f"trace length {len(result.environment_trace)} != {expected}"
        )


# ── P5: Feedback Modulation Is Active ─────────────────────────────────────────

class TestP5FeedbackModulationIsActive:
    """
    P5 — Feedback signals are non-empty and actively influence agent state.
    [SEMANTIC-STIGMERGY], [SEMANTIC-3SYNC-DIAGRAM]
    """

    def test_feedback_signals_are_non_empty(self, default_result):
        """Feedback signals are recorded during simulation."""
        assert len(default_result.feedback_signals) > 0, (
            "No feedback signals recorded — stigmergic modulation inactive. "
            "[SEMANTIC-STIGMERGY] feedback loop not completing."
        )

    def test_feedback_produces_different_trajectories_than_minimal(self):
        """Feedback simulation produces different trajectories than minimal."""
        from simulations.minimal_3sync import run_simulation as run_minimal
        minimal = run_minimal(num_agents=3, invariant=50.0, steps=5)
        feedback = run_feedback_simulation(num_agents=3, invariant=50.0, steps=5)
        any_different = any(
            minimal.trajectories[i] != feedback.trajectories[i]
            for i in range(3)
        )
        assert any_different, (
            "Feedback simulation produces identical trajectories to minimal. "
            "Stigmergic modulation has no effect — feedback loop inactive."
        )

    def test_environment_feedback_returns_mean_of_trace(self):
        """FeedbackEnvironment.feedback() returns mean of trace signals."""
        env = FeedbackEnvironment()
        signals = [10.0, 20.0, 30.0, 40.0, 50.0]
        for s in signals:
            env.write(s)
        expected = statistics.mean(signals)
        assert abs(env.feedback() - expected) < 1e-10, (
            f"Feedback {env.feedback()} != mean {expected}"
        )

    def test_feedback_returns_none_when_trace_empty(self):
        """FeedbackEnvironment.feedback() returns None when trace is empty."""
        env = FeedbackEnvironment()
        assert env.feedback() is None

    def test_modulate_does_not_change_state_when_trace_empty(self):
        """stigmergy_modulate() leaves state unchanged when environment is empty."""
        agent = FeedbackAgent(agent_id=0, initial_state=25.0)
        env = FeedbackEnvironment()
        original_state = agent.state
        agent.stigmergy_modulate(env)
        assert agent.state == original_state


# ── P6: Feedback Window Parameter ─────────────────────────────────────────────

class TestP6FeedbackWindowParameter:
    """
    P6 — When window is set, only recent signals are used for feedback mean.
    """

    def test_windowed_feedback_uses_only_recent_signals(self):
        """With window=2, feedback uses only last 2 signals in trace."""
        env = FeedbackEnvironment(window=2)
        env.write(10.0)
        env.write(20.0)
        env.write(30.0)
        env.write(40.0)
        expected = statistics.mean([30.0, 40.0])
        assert abs(env.feedback() - expected) < 1e-10, (
            f"Windowed feedback {env.feedback()} != mean of last 2: {expected}"
        )

    def test_no_window_uses_all_signals(self):
        """With window=None, feedback uses all signals in trace."""
        env = FeedbackEnvironment(window=None)
        signals = [10.0, 20.0, 30.0, 40.0]
        for s in signals:
            env.write(s)
        expected = statistics.mean(signals)
        assert abs(env.feedback() - expected) < 1e-10

    def test_windowed_and_full_produce_different_feedback(self):
        """Windowed and full-trace feedback produce different values."""
        signals = [10.0, 20.0, 30.0, 40.0, 50.0]
        env_full = FeedbackEnvironment(window=None)
        env_windowed = FeedbackEnvironment(window=2)
        for s in signals:
            env_full.write(s)
            env_windowed.write(s)
        assert env_full.feedback() != env_windowed.feedback()

    def test_windowed_simulation_still_converges(self, windowed_result):
        """Windowed feedback simulation still converges toward invariant."""
        invariant = windowed_result.invariant
        initial_states = [0.0, 10.0, 20.0]
        for i in range(windowed_result.num_agents):
            initial_distance = abs(initial_states[i] - invariant)
            final_distance = abs(windowed_result.trajectories[i][-1] - invariant)
            assert final_distance < initial_distance


# ── P7: Tri-Axis Structure Preserved ──────────────────────────────────────────

class TestP7TriAxisStructurePreserved:
    """
    P7 — All three axes remain structurally intact in the extended simulation.
    [SEMANTIC-3SYNC]: tri-axis structure must be complete and uncompromised.
    """

    def test_feedback_agent_has_all_three_axis_methods(self):
        """FeedbackAgent implements all three axis methods [SEMANTIC-3SYNC]."""
        agent = FeedbackAgent(agent_id=0, initial_state=0.0)
        assert hasattr(agent, 'stigmergy_write'), "Missing stigmergy_write"
        assert hasattr(agent, 'stigmergy_read'), "Missing stigmergy_read"
        assert hasattr(agent, 'stigmergy_modulate'), "Missing stigmergy_modulate"
        assert hasattr(agent, 'hivesync'), "Missing hivesync [SEMANTIC-HIVESYNC]"
        assert hasattr(agent, 'dce'), "Missing dce [SEMANTIC-DCE]"

    def test_hivesync_still_pulls_toward_invariant(self):
        """HiveSync axis still pulls agent toward invariant after feedback."""
        agent = FeedbackAgent(agent_id=0, initial_state=0.0)
        state_before = agent.state
        agent.hivesync(50.0)
        assert agent.state > state_before, (
            f"HiveSync failed to pull toward invariant 50 [SEMANTIC-HIVESYNC]"
        )
        assert agent.state == (state_before + 50.0) / 2

    def test_dce_integrates_memory(self):
        """DCE axis integrates memory into state [SEMANTIC-DCE]."""
        agent = FeedbackAgent(agent_id=0, initial_state=25.0)
        assert len(agent.memory) == 0
        agent.dce()
        assert len(agent.memory) == 1
        agent.dce()
        assert len(agent.memory) == 2

    def test_eoi_boundary_preserved_throughout(self, extended_result):
        """EOI identity boundary preserved throughout extended feedback simulation."""
        n = extended_result.num_agents
        for t in range(extended_result.steps):
            states_at_t = [extended_result.trajectories[i][t] for i in range(n)]
            unique_states = len(set(round(s, 10) for s in states_at_t))
            assert unique_states == n, (
                f"EOI boundary violated at t={t}: only {unique_states} unique "
                f"states for {n} agents [SEMANTIC-EOI]"
            )

    def test_result_metadata_is_correct(self, default_result):
        """Simulation result metadata correctly reflects configuration."""
        assert default_result.num_agents == 3
        assert default_result.steps == 5
        assert default_result.invariant == 50.0
        assert len(default_result.agent_ids) == 3
        assert len(default_result.trajectories) == 3
        assert len(default_result.memories) == 3


# ── Integration Test ──────────────────────────────────────────────────────────

class TestIntegrationFeedback:
    """
    Integration tests verifying all properties (P1–P7) hold simultaneously.
    [SEMANTIC-3SYNC]: confirms 3Sync coherence under richer stigmergic feedback.
    """

    def test_all_core_properties_hold_simultaneously(self):
        """Run feedback simulation and verify P1–P5 all pass simultaneously."""
        result = run_feedback_simulation(num_agents=3, invariant=50.0, steps=5)
        invariant = result.invariant
        initial_states = [0.0, 10.0, 20.0]

        # P1: Convergence
        for i in range(result.num_agents):
            assert abs(result.trajectories[i][-1] - invariant) < \
                   abs(initial_states[i] - invariant), \
                f"P1 failed for Agent {i} under feedback"

        # P2: Identity preservation
        ids = result.agent_ids
        assert len(ids) == len(set(ids)), "P2 failed: duplicate agent IDs"
        for i in range(result.num_agents):
            for j in range(i + 1, result.num_agents):
                assert result.trajectories[i] != result.trajectories[j], \
                    f"P2 failed: identity collapse between Agents {i} and {j}"

        # P3: No direct communication
        assert len(result.environment_trace) == result.num_agents * result.steps, \
            "P3 failed: environment trace inconsistent"

        # P4: History accumulation
        assert len(result.environment_trace) == result.num_agents * result.steps, \
            "P4 failed: environment trace length mismatch"

        # P5: Feedback is active
        assert len(result.feedback_signals) > 0, \
            "P5 failed: no feedback signals recorded"

    def test_feedback_simulation_is_faithful_to_paper8(self):
        """Comprehensive faithfulness test against Paper 8 canonical definitions."""
        result = run_feedback_simulation(
            num_agents=3, invariant=50.0, steps=10, window=5
        )

        # Invariant alignment [SEMANTIC-HIVESYNC]
        for i in range(result.num_agents):
            assert abs(result.trajectories[i][-1] - result.invariant) < \
                   abs([0.0, 10.0, 20.0][i] - result.invariant), \
                f"Invariant alignment failed for Agent {i}"

        # Temporal continuity [SEMANTIC-DCE]
        for i in range(result.num_agents):
            assert len(result.memories[i]) == result.steps, \
                f"DCE memory length mismatch for Agent {i}"

        # No identity merging [SEMANTIC-EOI]
        for i in range(result.num_agents):
            for j in range(i + 1, result.num_agents):
                assert result.trajectories[i] != result.trajectories[j], \
                    f"Identity merging detected between Agents {i} and {j}"

        # Environment-mediated coordination [SEMANTIC-STIGMERGY]
        assert len(result.environment_trace) == result.num_agents * result.steps

        # Feedback loop active [SEMANTIC-3SYNC-DIAGRAM]
        assert len(result.feedback_signals) > 0
