# 3Sync Minimal Simulation Asset

**Status:** Historical Paper 8 v1.2 listing record  
**Current canonical specification:** Paper 8, Version 1.3  
**Current reference implementation:** `simulations/minimal_3sync.py`  
**Repository:** `jmusashi/paper-8-substrate`

---

## Purpose

This record preserves the provenance of the earlier `assets/3sync_simulation.py` listing while preventing the historical implementation language from being mistaken for the current Paper 8 v1.3 architecture.

The historical asset originated as a minimal 3Sync simulation associated with Paper 8 v1.2. It demonstrated a simple three-agent realization using:

- Stigmergy for environment-mediated coordination;
- HiveSync for invariant-directed convergence; and
- Decision Continuity Engineering (DCE) for temporal continuity.

The historical listing is not the definition of 3Sync and must not be treated as the authoritative v1.3 reference implementation.

---

## Current Authority Boundary

For the current Paper 8 substrate:

1. **Paper 8 v1.3 is authoritative.**
2. **`CANONICAL.md` records the repository-level canonical semantics.**
3. **`simulations/minimal_3sync.py` is the current minimal reference realization.**
4. **`tests/test_minimal_3sync.py` tests observable properties of that realization.**
5. This asset record exists for provenance and historical traceability only.

Where historical wording differs from Paper 8 v1.3, the v1.3 specification governs.

---

## Current 3Sync Architecture

3Sync integrates three operational axes:

- **Stigmergy**: environment-mediated coordination
- **HiveSync**: invariant-directed convergence
- **DCE**: temporal continuity

The compact architectural relationship is:

**3Sync = (Stigmergy, HiveSync, DCE) subject to Cᴱₒᴵ**

The transition operator is represented as:

**T₃ₛ = Φᴰ ∘ Φᴴ ∘ Φₛ**

subject to:

**Cᴱₒᴵ**

The Equation of Identity (EOI) is the governing identity constraint. EOI is not a fourth operational axis.

---

## Historical v1.2 Listing Boundary

The earlier `assets/3sync_simulation.py` used implementation language that should not be carried forward as current v1.3 semantics.

In particular, the historical listing associated an agent's implementation `id` with an EOI identity boundary and stated that agent identity boundaries were preserved throughout the simulation.

Those statements are retained only as historical provenance. They are not current architectural claims.

The v1.3 boundary is:

```text
implementation ID ≠ identity
state inequality ≠ proof of identity distinction
state equality ≠ identity collapse
trajectory inequality ≠ proof of identity preservation
memory history ≠ origin of identity
```

EOI remains the identity constraint under which the three-axis operation is evaluated.

---

## DCE and Memory

In the historical listing, memory was used in the DCE update to introduce temporal dependence into the simulated state trajectory.

For v1.3 interpretation, memory is an observable temporal record used by the reference realization. Memory does not create identity and does not by itself prove identity preservation.

The reference implementation therefore separates:

- **implementation memory**, which records observable state history; from
- **EOI**, which remains the governing identity constraint.

---

## Stigmergy Boundary

The historical minimal simulation deposits agent state into a shared environment and reads the accumulated environmental trace.

In the minimal realization, the returned trace is not used to modify agent state. Active environmental modulation belongs to the extended realization in:

`simulations/stigmergy_feedback.py`

Environmental feedback therefore remains part of the Stigmergy axis rather than becoming a fourth operational axis.

---

## HiveSync Boundary

The minimal HiveSync realization moves agent state toward a shared structural attractor.

This is an implementation of invariant-directed convergence. It should not be interpreted as negotiated consensus, identity convergence, or identity merging.

Observable state convergence and claims about identity remain separate questions.

---

## Observable Implementation Properties

The current minimal reference realization supports observation and testing of properties including:

- convergence toward the structural attractor under the tested conditions;
- distinguishable trajectories under the tested initial conditions;
- environment-mediated trace deposition and reading;
- accumulation of environmental history; and
- temporal state records produced by the reference DCE update.

These are implementation observations. They do not independently define or prove the complete 3Sync architecture.

---

## Historical Metadata

The superseded asset identified itself as:

- **Title:** 3Sync Minimal Simulation
- **Series:** DCE Foundation Series · Paper 8: The 3Sync Architecture
- **Author:** Joel L. Monasterial
- **ORCID:** 0009-0000-7620-645X
- **Version:** 1.2
- **Date:** June 2, 2026
- **Historical DOI shown in the listing:** `10.5281/zenodo.20406312`

This metadata is preserved here as provenance for the historical listing. It must not be substituted for the current Paper 8 v1.3 metadata.

---

## Current Paper 8 Metadata

- **Title:** The 3Sync Architecture: A Tri-Axis Framework for Multi-Agent Coherence, Autonomy, and Continuity
- **Series:** DCE Foundation Series · Paper 8
- **Author:** Joel L. Monasterial
- **ORCID:** 0009-0000-7620-645X
- **Version:** 1.3
- **Date:** October 1, 2026
- **DOI:** `10.5281/zenodo.20406311`

---

## Repository Routing

Use the following repository surfaces for current v1.3 interpretation:

- `CANONICAL.md` for canonical repository semantics
- `3sync-layer-definition.md` for the machine-readable layer definition
- `diagrams/3sync_tri_axis_diagram.md` for the tri-axis architecture diagram record
- `simulations/minimal_3sync.py` for the minimal reference realization
- `simulations/stigmergy_feedback.py` for the extended environmental-feedback realization
- `tests/test_minimal_3sync.py` for tests of minimal-realization observables
- `tests/test_stigmergy_feedback.py` for tests of extended-realization observables
- `VALIDATION.md` for validation boundaries and evidence interpretation

---

## Preservation Rule

This record exists to preserve historical continuity without allowing superseded implementation semantics to govern the current architecture.

The historical listing may be retained as an archived artifact, but current readers and machine agents should route architectural interpretation to Paper 8 v1.3 and the current v1.3 substrate.

**Historical implementation evidence is provenance, not present canon.**
