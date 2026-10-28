---
title: "Dead end: The particle (Lagrangian) history"
date: "2026-10-05"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "transport-histories"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Transport-histories"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**The particle (Lagrangian) history** read unrelated rows after a removal (PETSc's swap-with-last on repopulation); the proxy hid an error of order one at the particle level. Look at particle-level error before blaming a method.

Recorded on the wiki page [Transport histories](../topics/transport-histories.md) under "What did not work, and why"; the date is the commit that first carried it.
