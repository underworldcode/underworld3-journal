---
title: "Dead end: Nonlinear remedies for a linear failure"
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

**Nonlinear remedies for a linear failure.** Three weeks of line searches (bt kills Picard, l2 accepts uphill steps, nleqerr, cp, Anderson, NGMRES, damping, Eisenstat–Walker caps) against a solve that was failing inside Newton's linear solve. Diagnose the linear solve with −F(x) before touching the nonlinear loop.

Recorded on the wiki page [Solvers and multigrid](../topics/solvers-and-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
