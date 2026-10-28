---
title: "Dead end: GAMG as the coarse-level solve"
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

**GAMG as the coarse-level solve.** It leaves the multigrid's convergence unchanged, but it is weak on the coupled block, which it treats as one scalar system. On a 6,067-tet base it took three times as long as native LU.

Recorded on the wiki page [Shear band length scales](../topics/shear-band-length-scales.md) under "What did not work, and why"; the date is the commit that first carried it.
