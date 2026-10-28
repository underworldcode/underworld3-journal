---
title: "Updated Constitutive models (markdown)"
date: "2026-10-05"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "viscoelastic-constitutive-models"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Viscoelastic-Constitutive-models/11af23f6ae5ee8b3aca43e852a5e24277c4dadbf"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`11af23f6`](https://github.com/underworldcode/underworld3/wiki/Viscoelastic-Constitutive-models/11af23f6ae5ee8b3aca43e852a5e24277c4dadbf) by Louis Moresi, 2026-10-05: **Updated Constitutive models (markdown)**

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Viscoelastic Constitutive models

# Constitutive models
What we understand about the viscoelastic constitutive models and their time integration. Usage: `docs/developer/subsystems/stress-transport.md`. Argument: [Discussion #815](https://github.com/underworldcode/underworld3/discussions/815).
## The library
A model is named by three independent choices on `ViscoElasticPlasticFlowModel`: the **element** (maxwell, or jeffreys with a parallel solvent dashpot), the **relaxation law** (linear, or FENE-P with extensibility L²) and the **objective rate**. UCM, Oldroyd-B and FENE-P are three points in that space, and a Burgers element would be a second history. We treat this as a library of methods rather than one scheme, as a code carries several turbulence models, and we use domain-neutral names because the same machinery describes transient mantle rheology.
The stress is stored as the logarithm of a conformation and stepped with an exponential (ETD) integrator at first order; the positive-definite update (the `deformation` convected step) adds the b² L Lᵀ term that makes the stretched target a product of two factors, and the cross-slot bifurcation appears only with it. For FENE-P the step is taken on the conformation at the lagged rate f*/λ, with f* carried as a nodal field so the matrix exponential of the record does not enter the compiled flux twice (inlined, it made the C-source generation take 85 s per step).
## FENE-P: the record is log(f c)
The record for FENE-P is log(σ/G + I), the same record Oldroyd-B keeps, which for FENE-P is log(f c) rather than log c. The conformation is recovered through the trace, f* = 1 + (tr e^ψ − d)/L², c* = e^ψ/f*. Every SPD record then decodes to an admissible conformation, whatever the projection that commits it did. The relaxation rate, the strain source and the deformation term read the lagged f*; the stress decode has no lag. Against the closed-form steady shear the scheme is first order in dt/λ with errors that halve cleanly (+0.0068, +0.0034, +0.0018 in shear stress at dt 0.1, 0.05, 0.025).
Two derivation traps, both found by the shear-box test: the stretching source acts on G(c − I), not on σ (they differ for FENE-P), and the f* on the rate cancels the f* on the stress for every source, so the source weights keep their Oldroyd-B form.
## What did not work, and why
- **Storing log c for FENE-P.** The conformation is bounded by L²; the nodal Galerkin projection that commits the record is not. At a cylinder wall, where log c jumps by 4 across one cell, the projection overshot by a factor 1.5 in c and committed a record with trace 105 of L² 100 from a stress whose own conformation had 70. The spring factor hit its floor, the wall layer alternated between saturated and free, and the velocity multigrid ground to the guard's hang limit. Lesson: a bounded variable is not the one to project.
- **Our first two diagnoses were wrong.** We blamed saturation (the snapshots said the spring factor was 4.65 against a floor of 100) and then the lagged rate, and encoded the record with the exact factor of the stress, f = 1 + tr σ/(G L²). That made it worse: the stress a step produces is not a FENE-P stress on 50 to 80 wall nodes (its trace fell to −11 where −2 is the physical minimum), so f went toward zero and amplified the conformation 400-fold in one step. A floor on that f left the real cause in place. The per-step diagnostic that printed the record's trace at the nodes against the stress's own closed-form trace is what settled it, after three attempts.
- **Naming the FENE-P fields by `id(self)`** gave different names on different ranks and deadlocked the first snapshot in parallel. Names come from a counter now.
- **Rewiring the smoothing expression unconditionally** forced a C-source regeneration every step for every history commit; comparing the value first cut the Oldroyd-B shear-box step from 7.5 to 1.2 s.
- **Infinite extensibility** gave 0/0 in the spring factor; it is refused, and L² at or below the dimension is refused too (the trace decode would divide by zero).
## Open
Second order for the positive-definite path (the second-order schemes combine levels with negative weights, which does not preserve positivity). A Burgers element as a second history. FENE-P at Re 100 against Richter et al. 2010 as a trend comparison.
## History
