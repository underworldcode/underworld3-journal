---
title: "Dead end: The first deficit fill was a diffusion"
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

**The first deficit fill was a diffusion.** Filling any shortfall pulled about half the cells toward the un-advected field every step; a rotating Gaussian lost 18% of its peak with the forward-nodes history and 6% with forward-IP. Every cylinder run looked stable throughout. Lesson: a regularisation that "only acts on empty cells" has to be checked on a moving smooth field against the unregularised baseline, not on a stable run. The fill now acts below 50% coverage; the runs that carried the bias are listed in the roadmap.

Recorded on the wiki page [Particle to field projection](../topics/particle-to-field-projection.md) under "What did not work, and why"; the date is the commit that first carried it.
