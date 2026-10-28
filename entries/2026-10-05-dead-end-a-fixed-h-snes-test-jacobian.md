---
title: "Dead end: A fixed-h `-snes_test_jacobian`"
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

**A fixed-h `-snes_test_jacobian`** on a power-law rheology reported 1.5e-3 and looked like a tangent error; the central-difference h-sweep converged as h² to 1e-6 in every case. Truncation error, not the Jacobian.

Recorded on the wiki page [Solvers and multigrid](../topics/solvers-and-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
