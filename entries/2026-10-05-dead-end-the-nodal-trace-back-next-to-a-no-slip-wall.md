---
title: "Dead end: The nodal trace-back next to a no-slip wall"
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

**The nodal trace-back next to a no-slip wall** carries about 50% too much stress in the first two cells: it reads from where the wall value is pinned. Grid and integration-point histories converge together there.

Recorded on the wiki page [Transport histories](../topics/transport-histories.md) under "What did not work, and why"; the date is the commit that first carried it.
