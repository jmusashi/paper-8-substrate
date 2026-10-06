"""Tests for the extended Paper 8 v1.3 environmental-feedback realization.

P1-P7 below are observable properties of this reference implementation. The
tests do not equate implementation IDs, state inequality, or trajectory
inequality with EOI identity. EOI remains the governing identity constraint.
DOI: 10.5281/zenodo.20406311
"""
import inspect
import statistics
import pytest
from simulations.minimal_3sync import run_simulation
from simulations.stigmergy_feedback import FeedbackAgent, FeedbackEnvironment, run_feedback_simulation

@pytest.fixture
def result():
    return run_feedback_simulation(num_agents=3, initial_states=[0.0,10.0,20.0], invariant=50.0, steps=5)

def test_p1_observed_convergence(result):
    for i,x0 in enumerate([0.0,10.0,20.0]):
        assert abs(result.trajectories[i][-1]-result.invariant) < abs(x0-result.invariant)

def test_p2_distinguishable_histories_under_test_conditions(result):
    assert result.agent_ids == list(range(result.num_agents))
    assert len({tuple(x) for x in result.trajectories})==result.num_agents
    assert len({tuple(x) for x in result.memories})==result.num_agents
    assert all(len(m)==result.steps for m in result.memories)

def test_p3_no_direct_agent_parameter():
    for name in ("stigmergy_write","stigmergy_read","stigmergy_modulate","hivesync","dce"):
        for p in inspect.signature(getattr(FeedbackAgent,name)).parameters.values():
            assert p.annotation is not FeedbackAgent

def test_p4_environment_history_accumulates(result):
    assert len(result.environment_trace)==result.num_agents*result.steps

def test_p5_feedback_is_active_and_changes_realization(result):
    assert result.feedback_signals
    minimal=run_simulation(num_agents=3, initial_states=[0.0,10.0,20.0], invariant=50.0, steps=5)
    assert any(a != b for a,b in zip(minimal.trajectories,result.trajectories))

def test_p5_feedback_mean():
    env=FeedbackEnvironment()
    for x in [10.0,20.0,30.0]: env.write(x)
    assert env.feedback()==statistics.mean([10.0,20.0,30.0])

def test_p6_window_applied():
    env=FeedbackEnvironment(window=2)
    for x in [10.0,20.0,30.0,40.0]: env.write(x)
    assert env.feedback()==statistics.mean([30.0,40.0])

def test_p6_invalid_window_rejected():
    with pytest.raises(ValueError): FeedbackEnvironment(window=0)

def test_p7_three_axis_methods_present():
    a=FeedbackAgent(0,0.0)
    for name in ("stigmergy_write","stigmergy_read","stigmergy_modulate","hivesync","dce"):
        assert callable(getattr(a,name))

def test_p7_feedback_remains_stigmergic_extension():
    a=FeedbackAgent(0,0.0); env=FeedbackEnvironment(); env.write(20.0)
    a.stigmergy_modulate(env)
    assert a.state==10.0

def test_invalid_initial_state_length_rejected():
    with pytest.raises(ValueError):
        run_feedback_simulation(num_agents=3, initial_states=[0.0,10.0])
