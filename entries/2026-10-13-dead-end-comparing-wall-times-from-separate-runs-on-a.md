---
title: "Dead end: Comparing wall times from separate runs on a shared machine"
date: "2026-10-13"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "shear-band-length-scales"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Shear-band-length-scales"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**Comparing wall times from separate runs on a shared machine.** The machine runs over its physical cores, and the same run took 221 s one night and 371 s the next. An apparent 2.4× slowdown of the gmsh levels in 2-D was this, plus a different monitor setting; run side by side it was 9%. We now time only arms started together, with identical options, and read PETSc's `-log_view`.

Recorded on the wiki page [Shear band length scales](../topics/shear-band-length-scales.md) under "What did not work, and why"; the date is the commit that first carried it.
