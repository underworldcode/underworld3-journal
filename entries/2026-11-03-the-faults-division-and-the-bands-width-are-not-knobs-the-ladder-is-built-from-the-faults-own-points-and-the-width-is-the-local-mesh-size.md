---
title: "The fault's division and the band's width are not knobs: the ladder is built from the fault's own points, and the band is as wide as the local mesh size (Louis, 2026-11-03, clarifying decision 1b)"
date: 2026-11-03
authors: ["Louis Moresi", "science hub session_013CgVT1Gx9WTvaZVqU58HsQ (kaiju), which recorded it", "notes session session_011S876ckjYqqth1aPyojrhh on wombat", "recorded by the docs hub"]
options:
  kind: decision
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/blob/febbb87/zg95_lid_regimes/DECISIONS.md
    - https://github.com/lmoresi/uw3-campaigns/blob/7efb5ef/HUB.md
    - https://github.com/underworldcode/underworld3/blob/af6f19b3/src/underworld3/utilities/place_surface.py
    - entries/2026-11-02-the-add-on-is-the-line-for-split-faults-the-fault-carries-its-own-resolution-and-split-coarse-levels-are-not-developed-further.md
---

The 2026-11-02 decision said, as point 1b, that the fault carries its own resolution and
that no parameter $S$ sets the resolution along it. The drivers still had one: recipe v2
resamples a detected trace at `uw_spacing`, by default one base cell, and Louis had
accepted that default on the hub's question. The notes session asked him whether the two
agree. His answer, on 2026-11-03, to the science hub:

> In terms of resolution - the along-fault resolution is set by the discretisation of the
> fault, the fault width is set by the local mesh size (which may not be uniform
> everywhere that the fault is embedded, but an average of some sort seems sensible
> here). What is going wrong in our model is that we are also defining the fault and its
> discretisation as a knob we can control. Generally this is not true - the ladder is
> built from the fault points and we can see if that is sufficient or not, but we
> generally can't just change it.

## What was decided

- The ladder's rungs are the fault's own points. A model does not choose the spacing
  along the fault. Whether the division is sufficient is observed and recorded, not set.
- The band's width is the local mesh size along the fault, or an average of it where the
  mesh is not uniform. That makes the band about half as wide as the drivers' $2S$ with
  $S = h_b$. This part is new: the 2026-11-02 entry said nothing about the width.
- `uw_spacing` goes from the drivers. Recipe v2's one base cell agrees with the principle
  in rung spacing on the uniform annulus. It does not agree in width: v2's band is
  $2S = 2h_b$.

## What it does not say

- How the average is taken on a mesh that is not uniform is not defined. The annulus base
  is uniform at $h_b = 0.0156$.
- Nothing has been run with the band one cell wide. Kaiju is drafting the driver change:
  - the locator's points, produced at the local cell size, become the rungs;
  - $W$ is set to the local cell size;
  - the record states the division used: the rung count, the rung length's mean and
    range, and $W$;
  - the restart rule re-divides a restored trace only when the mesh differs.

  An offline placement check at $W = h_b$ comes first. No run is made before Louis sees
  the result.
- Whether the first v2 baselines run before or after the removal is Louis's call (HUB.md
  at 7efb5ef, "Waiting on Louis").
- The spacing arms of 2026-11-02 resampled the trace at $0.004$, $h_b/2$ and $h_b$. They
  remain measurements of the solver, run with the fault divided three ways. They are not a
  choice of division the model has.

## Closure

- **Preferred**: the fault placed at its own division, with the band one local cell
  wide. In the library this is
  `place_fault_ribbon_2d(base, [(name, points)], width, split=True, mesher="ladder")`.
  `points` are the fault's own points. `width` is the local mesh size. The library takes
  the points verbatim as the spine (`place_fault_ribbon_2d`'s docstring, `development`
  af6f19b3), and its rails lie at $\pm$`width`/2 (`_ladder_curved_assembly_2d`).
- **Allowed**: a band $2S$ wide, as in recipe v2 and in every measurement made so far, for
  comparison with those measurements.
- **Where enforced**:
  - the drivers' ledger: the principle row, with `uw_spacing` marked for removal
    (`zg95_lid_regimes/DECISIONS.md`, uw3-campaigns main febbb87); the driver commit when
    it lands (science hub, kaiju; not yet done);
  - UWTN 2026-022 (notes session, on the workbench, not yet pushed). "The spacing along
    the fault is a parameter" now reads "that of the fault's own points". The note's
    recipe and every run it reports used a band $2S$ wide. Whether to keep that, stating
    it, or to rerun at the local cell size is Louis's choice;
  - the fault-multigrid and faults-in-convection guides (PR #862, docs hub; ruling 4
    carries the width half with this entry);
  - the topic page's current understanding (docs hub; done with this entry).

This entry clarifies point 1b of the 2026-11-02 decision and supersedes no entry.

## Verdict

Kept. Feeds the drivers, UWTN 2026-022, the guides and the topic page.
