---
title: "Dead end: Nearest-node injection for orphan columns"
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

**Nearest-node injection for orphan columns.** Not correct in serial either: on the ladder's two-mid chain four orphans injected onto fine rows that already carried a weight-1 entry gave duplicate columns, a singular coarse operator and NaN, split and unsplit finest alike; in parallel 512 of 618 orphans duplicated. Dropping the unknowns is the rule on every hierarchy now; the repair is gone.

Recorded on the wiki page [Fault multigrid](../topics/fault-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
