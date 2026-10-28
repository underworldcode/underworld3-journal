---
title: "Dead end: Node-cloud transfers to a split coarse level"
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

**Node-cloud transfers to a split coarse level.** Coincident coarse nodes degenerate the Delaunay triangulation of the cloud; the faulted thick layer's multigrid returned NaN on its first cycle for this reason, which was first misread as a failure of geometric multigrid on the rotated 3-D operator.

Recorded on the wiki page [Fault multigrid](../topics/fault-multigrid.md) under "What did not work, and why"; the date is the commit that first carried it.
