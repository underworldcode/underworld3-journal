---
title: "Dead end: Preconditioning an indefinite viscoelastic velocity block"
date: "2026-10-16"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "solvers-and-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Solvers-and-multigrid"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**Preconditioning an indefinite viscoelastic velocity block** (confined cylinder, 2026-10): a stretch-free SPD preconditioning matrix tripled the inner iterations, GMRES + ASM smoothing stalled at the same step; the failure was the Newton problem. See [Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md).

Recorded on the wiki page [Solvers and multigrid](../topics/solvers-and-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
