---
title: "Dead end: The sheet placement on a bisection-refined 3-D child"
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

**The sheet placement on a bisection-refined 3-D child.** Its volume guard refuses the two-level child at every clearance and sheet size tried (volume change $4\times10^{-6}$ to $5\times10^{-5}$ against a guard of $10^{-9}$); at one add-on level `clearance=0.9` works. General 3-D fault patches on add-on meshes wait on the placement.

Recorded on the wiki page [Fault multigrid](../topics/fault-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
