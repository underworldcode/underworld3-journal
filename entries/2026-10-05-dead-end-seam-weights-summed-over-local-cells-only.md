---
title: "Dead end: Seam weights summed over local cells only"
date: "2026-10-05"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "particle-to-field-projection"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Particle-to-field-projection"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**Seam weights summed over local cells only** half-weighted the nodes on partition seams, so three ranks differed from serial. They are summed across seams now.

Recorded on the wiki page [Particle to field projection](../topics/particle-to-field-projection.md) under "What did not work, and why"; the date is the commit that first carried it.
