---
title: "Viscoelastic stretch at large steps: the Jacobian spectrum at the wall, preconditioning and smoothers, the lagged-stretch dead end, \"linear\" at Courant 8 and 16, per-step switching, the accuracy accounting; linked from Home, the cylinder campaign, solvers and constitutive models"
date: "2026-10-16"
authors:
  - "Louis Moresi"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "viscoelastic-stretch-at-large-steps"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Cylinder-campaign-2026/52cceaec37ac150214c9f479dafad54a3db5f512"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`52cceaec`](https://github.com/underworldcode/underworld3/wiki/Cylinder-campaign-2026/52cceaec37ac150214c9f479dafad54a3db5f512) by Louis Moresi, 2026-10-16: **Viscoelastic stretch at large steps: the Jacobian spectrum at the wall, preconditioning and smoothers, the lagged-stretch dead end, "linear" at Courant 8 and 16, per-step switching, the accuracy accounting; linked from Home, the cylinder campaign, solvers and constitutive models**

Created the page [Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md); that text is on the page, not repeated here.

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Cylinder campaign 2026

The FENE-P record ([Constitutive models](https://github.com/underworldcode/underworld3/wiki/Constitutive-models)); the deficit fill and the limiter ([Particle-to-field projection](../topics/particle-to-field-projection.md)); St follows the velocity history, and lift collapses with resolution ([Transport histories](../topics/transport-histories.md)); the stall that looked like a hang ([Solvers and multigrid](../topics/solvers-and-multigrid.md)); the benchmarks and the next target ([Benchmarks](../benchmarks/benchmarks.md)); why the implicit stretch stalls at Courant 8 on the wall cell and how runs now get through it ([Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md)).

### Added to Solvers and multigrid

- **Preconditioning an indefinite viscoelastic velocity block** (confined cylinder, 2026-10): a stretch-free SPD preconditioning matrix tripled the inner iterations, GMRES + ASM smoothing stalled at the same step; the failure was the Newton problem. See [Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md).

### Added to Viscoelastic Constitutive models

The stress is stored as the logarithm of a conformation and stepped with an exponential (ETD) integrator at first order; the positive-definite update (the `deformation` convected step) adds the b² L Lᵀ term that makes the stretched target a product of two factors, and the cross-slot bifurcation appears only with it. Taken with the new velocity gradient, that step puts the stored stress into the momentum tangent; at a wall with $\Delta t\,|\boldsymbol{\sigma}^*|/\eta \sim 1$ Newton stalls, and `stretch_in_momentum` chooses how much of the stretch the momentum sees ([Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md)). For FENE-P the step is taken on the conformation at the lagged rate f*/λ, with f* carried as a nodal field so the matrix exponential of the record does not enter the compiled flux twice (inlined, it made the C-source generation take 85 s per step).
