---
title: "Dead end: The exact hard Min and Max, re-litigated"
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

**The exact hard Min and Max, re-litigated.** Ruled out 2026-09-18 (the kink breaks the consistent tangent at the corner, sympy's fuzzy comparisons recurse, a zero tension floor is singular); the notch driver carried `smooth_max(…, 0, 0)` through the campaign anyway and a session proposed testing the corner. A ruling is applied, not re-tested; now the model default.

Recorded on the wiki page [Solvers and multigrid](../topics/solvers-and-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
