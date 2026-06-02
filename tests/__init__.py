"""
tests — DCE Foundation Series · Paper 8: The 3Sync Architecture
================================================================
DOI    : 10.5281/zenodo.20406312
GitHub : https://github.com/jmusashi/paper-8-substrate
ORCID  : 0009-0000-7620-645X

Test Modules
------------
test_minimal_3sync      : 27 tests for simulations/minimal_3sync.py
                          Encodes P1–P4 as assertions:
                          P1 — Asymptotic Convergence   [SEMANTIC-HIVESYNC]
                          P2 — Identity Preservation    [SEMANTIC-EOI]
                          P3 — No Direct Communication  [SEMANTIC-STIGMERGY]
                          P4 — Environment History      [SEMANTIC-STIGMERGY]

test_stigmergy_feedback : 39 tests for simulations/stigmergy_feedback.py
                          Verifies P1–P4 hold under richer feedback, plus:
                          P5 — Feedback Modulation Active  [SEMANTIC-3SYNC-DIAGRAM]
                          P6 — Feedback Window Parameter   [SEMANTIC-STIGMERGY]
                          P7 — Tri-Axis Structure Preserved [SEMANTIC-3SYNC]

Run All Tests
-------------
    python -m pytest tests/ -v

Run Individual Suites
---------------------
    python -m pytest tests/test_minimal_3sync.py -v
    python -m pytest tests/test_stigmergy_feedback.py -v

Total: 66 tests — 0 failures expected on faithful implementation.
See VALIDATION.md for full interpretation guide.
"""