---
title: "Dead end: Nested iteration (coarse solve, interpolate, fine Newton)"
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

**Nested iteration (coarse solve, interpolate, fine Newton).** Bands are one cell wide and mesh-dependent, so the coarse solution is far in residual (F₀ 0.32 vs 0.42 cold); fine Newton from it fails, the fine blend saves 30%, the coarse solve cost more than that. The same information is all a FAS coarse correction can carry.

Recorded on the wiki page [Solvers and multigrid](../topics/solvers-and-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
