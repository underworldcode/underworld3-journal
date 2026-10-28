---
title: "Dead end: Smoother and hierarchy changes against the mechanism mode"
date: "2026-10-05"
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

**Smoother and hierarchy changes against the mechanism mode** (SOR ×4/×8, Richardson, Chebyshev, deeper hierarchies, GAMG, three settings): 0.99 per cycle throughout. The mode needs Krylov space, not a better smoother.

Recorded on the wiki page [Solvers and multigrid](../topics/solvers-and-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
