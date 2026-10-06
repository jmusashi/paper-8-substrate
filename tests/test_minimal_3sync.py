"""Tests for the minimal Paper 8 v1.3 reference realization.

These assertions test observable implementation properties. They do not define
3Sync and do not treat implementation IDs, state equality, or memory records as
proof of identity. Published Paper 8 v1.3 remains authoritative.
DOI: 10.5281/zenodo.20406311
"""
import inspect
import pytest
from simulations.minimal_3sync import Agent, Environment, run_simulation

@pytest.fixture
def result():
    return run_simulation(num_agents=3, initial_states=[0.0,10.0,20.0], invariant=50.0, steps=5)

def test_p1_observed_convergence(result):
    initial=[0.0,10.0,20.0]
    for i,x0 in enumerate(initial):
        assert abs(result.trajectories[i][-1]-result.invariant) < abs(x0-result.invariant)

def test_p1_distance_nonincreasing():
    r=run_simulation(num_agents=3, invariant=50.0, steps=20)
    for tr in r.trajectories:
        d=[abs(x-r.invariant) for x in tr]
        assert all(b <= a for a,b in zip(d,d[1:]))

def test_p2_implementation_ids_unique_and_stable(result):
    assert result.agent_ids == list(range(result.num_agents))
    assert len(set(result.agent_ids)) == result.num_agents

def test_p2_histories_distinguishable_under_test_conditions(result):
    assert len({tuple(x) for x in result.trajectories}) == result.num_agents
    assert len({tuple(x) for x in result.memories}) == result.num_agents
    assert all(len(m)==result.steps for m in result.memories)

def test_p3_agent_api_has_no_agent_parameter():
    for name in ("stigmergy_write","stigmergy_read","hivesync","dce"):
        sig=inspect.signature(getattr(Agent,name))
        for p in sig.parameters.values():
            assert p.annotation is not Agent

def test_p3_stigmergy_interfaces_use_environment():
    for name in ("stigmergy_write","stigmergy_read"):
        params=list(inspect.signature(getattr(Agent,name)).parameters.values())
        assert [p.name for p in params] == ["self","environment"]

def test_p4_environment_history_accumulates(result):
    assert len(result.environment_trace)==result.num_agents*result.steps
    assert all(isinstance(x,(int,float)) for x in result.environment_trace)

def test_minimal_read_does_not_modulate_state():
    env=Environment(); a=Agent(0,25.0); env.write(100.0)
    before=a.state; a.stigmergy_read(env)
    assert a.state==before

def test_invalid_initial_state_length_rejected():
    with pytest.raises(ValueError):
        run_simulation(num_agents=3, initial_states=[0.0,10.0])
