---
title: "Dead end: Extrapolated weights"
date: "2026-10-13"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**Extrapolated weights.** Non-nested levels near a pulled tip gave weights up to 5.4 and weakly reached coarse unknowns; a 5 % column-norm pruning heuristic worked but the clamp removes the need for it.

Recorded on the wiki page [Fault multigrid](../topics/fault-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
