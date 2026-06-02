"""
simulations — DCE Foundation Series · Paper 8: The 3Sync Architecture
======================================================================
DOI    : 10.5281/zenodo.20406312
GitHub : https://github.com/jmusashi/paper-8-substrate
ORCID  : 0009-0000-7620-645X

Modules
-------
minimal_3sync       : Canonical minimal simulation (Paper 8 §4, Listing 1)
                      Three agents, stigmergy trace, HiveSync toward
                      invariant = 50, DCE memory. [SEMANTIC-3SYNC]

stigmergy_feedback  : Extended simulation with active stigmergic feedback
                      modulation. Environment computes mean of recent signals
                      and modulates agent state. Tri-axis structure preserved.
                      [SEMANTIC-STIGMERGY], [SEMANTIC-3SYNC-DIAGRAM]

Canonical References
--------------------
[SEMANTIC-3SYNC]     : tri-axis coherence architecture
[SEMANTIC-HIVESYNC]  : synchronization invariant / shared attractor
[SEMANTIC-DCE]       : decision continuity via weighted memory integration
[SEMANTIC-STIGMERGY] : indirect coordination via shared environment
[SEMANTIC-EOI]       : identity boundary — preserved throughout simulation
"""

from simulations.minimal_3sync import Agent, Environment, run_simulation, SimulationResult
from simulations.stigmergy_feedback import (
    FeedbackAgent,
    FeedbackEnvironment,
    run_feedback_simulation,
    FeedbackSimulationResult,
)

__all__ = [
    "Agent",
    "Environment",
    "run_simulation",
    "SimulationResult",
    "FeedbackAgent",
    "FeedbackEnvironment",
    "run_feedback_simulation",
    "FeedbackSimulationResult",
]