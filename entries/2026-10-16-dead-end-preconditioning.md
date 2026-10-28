---
title: "Dead end: Preconditioning"
date: "2026-10-16"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "viscoelastic-stretch-at-large-steps"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Viscoelastic-stretch-at-large-steps"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**Preconditioning.** The breakdown is in the Newton problem, not the linear solver. A positive-definite preconditioning matrix without the stretch is a poor approximation of an operator that is mostly stretch; a stronger smoother (GMRES + ASM) stalls at the same step. We also briefly believed the velocity block ran on GAMG with Chebyshev/Jacobi smoothing and that GMRES + SOR would fix it — it was already on geometric multigrid with GMRES + SOR; a run printing the resolved preconditioner settled it. Check what a run resolved to, not what the defaults table says.

Recorded on the wiki page [Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md) under "What did not work, and why"; the date is the commit that first carried it.
