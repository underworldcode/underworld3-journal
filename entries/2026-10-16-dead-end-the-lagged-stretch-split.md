---
title: "Dead end: The lagged stretch (\"split\")"
date: "2026-10-16"
authors:
  - "Underworld sessions (wiki)"
options:
  kind: "dead-end"
  status: "live"
  topics:
    - "viscoelastic-stretch-at-large-steps"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Viscoelastic-stretch-at-large-steps"
  origin: "wiki 'What did not work' section, migrated 2026-10-27"
---

**The lagged stretch ("split").** Taking the stretch with $\mathbf{L}^n$ removes $\boldsymbol{\sigma}^*$ from the tangent exactly, but at the wall $\Delta t\,|\mathbf{L}|$ is 4 to 8: the lag error is several times the stress itself, entering the momentum as a fixed force. Three variants, all from the step-40 restart at $\Delta t = 1/60$:
- stretching the whole conformation $\mathbf{c}^*$ with $\mathbf{L}^n$ also lags the elastic loading, leaving about 85 % of the viscous response explicit: drag −108 at step 42;
- stretching only $\boldsymbol{\sigma}^*$ (loading implicit): drag $5\times10^5$ at step 42;
- the same without the quadratic term: drag −111 at step 42.

Sub-steps do not help: the error is in which $\mathbf{L}$ is used, not in the step length. The option lived in commit `75a374b9` on `feature/ve-stretch-split` and was removed in `11256696`.

Recorded on the wiki page [Viscoelastic stretch at large steps](../topics/viscoelastic-stretch-at-large-steps.md) under "What did not work, and why"; the date is the commit that first carried it.
