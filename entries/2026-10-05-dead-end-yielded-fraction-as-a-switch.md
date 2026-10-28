---
title: "Dead end: Yielded fraction as a switch"
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

**Yielded fraction as a switch** between tangents (ruled out earlier) and any cheap local test for the Schur sign: the coupling is $O(\sin\varphi)$ in every yielding cell at every state; the sign flip is global. The velocity block's mechanism, by contrast, is element-local (the modulus along $\mathbf n$) and could be a pre-solve check; the Ritz values of the outer Krylov are the free by-product that would say which failure a stall is.

Recorded on the wiki page [Solvers and multigrid](../topics/solvers-and-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
