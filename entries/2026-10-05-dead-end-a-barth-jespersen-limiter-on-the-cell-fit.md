---
title: "Dead end: A Barth–Jespersen limiter on the cell fit"
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

**A Barth–Jespersen limiter on the cell fit** cured that but clipped true gradients (drag 7 to 15% low), because the cell's own arrivals are the wrong bound; the neighbour range, exchanged across seams, would be the right one. It stays in the code, off. Louis: "I don't much like these limiters."

Recorded on the wiki page [Particle to field projection](../topics/particle-to-field-projection.md) under "What did not work, and why"; the date is the commit that first carried it.
