---
title: "Dead end: Random-solution and random-RHS tests of the velocity multigrid"
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

**Random-solution and random-RHS tests of the velocity multigrid.** The first showed 0.909/cycle on an operator the fieldsplit could not solve at all; the second gave 1.000 even on the Picard block. Neither is the Newton right-hand side.

Recorded on the wiki page [Solvers and multigrid](../topics/solvers-and-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
