---
title: "The ladder is equant: its half-width is one cell and its rungs are about one cell apart, so recipe v2 stands, and the fault-division design goes to a plate-boundaries module (Louis, 2026-11-03)"
date: 2026-11-03
authors: ["Louis Moresi", "science hub session_013CgVT1Gx9WTvaZVqU58HsQ (kaiju), which recorded it", "notes session session_011S876ckjYqqth1aPyojrhh on wombat", "recorded by the docs hub"]
options:
  kind: decision
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/lmoresi/uw3-campaigns/blob/017b84d/zg95_lid_regimes/DECISIONS.md
    - https://github.com/lmoresi/uw3-campaigns/blob/1575048/HUB.md
    - entries/2026-11-03-the-faults-division-and-the-bands-width-are-not-knobs-the-ladder-is-built-from-the-faults-own-points-and-the-width-is-the-local-mesh-size.md
    - entries/2026-11-02-the-add-on-is-the-line-for-split-faults-the-fault-carries-its-own-resolution-and-split-coarse-levels-are-not-developed-further.md
---

The earlier 2026-11-03 entry recorded Louis's principle that the band's width is set by
the local mesh size. It read that as a band one local cell wide, half the width of recipe
v2's band. That reading was kaiju's and the hubs'; the notes session carried it into the
entry, and it was not Louis's. Kaiju drafted a driver change on that reading: every
locator divides the fault at the local cell size, the band is a whole number of cells
wide, and the division used is recorded. It placed the draft offline on 80 stored faults
(f393fd7 on `kaiju/fault-division-draft`, page UANqhA82AfRoh7fjgrPwYG) and never ran it.
Louis's answer on the design page, the same day:

> This is a lot of design for what is, actually, a simple driver to test a concept. If we
> implement this, then we should consider it part of a plate-boundaries module. I'd say -
> make the ladder equant if given the choice. The half-width is one cell (I think) and so
> the discretisation along the length would be similar.

## What was decided

- The ladder is equant. Its half-width is one local cell, so the band is two cells wide,
  and its rungs are about one cell apart. This replaces the earlier entry's "one local
  cell wide". Its principle stands: the fault's own points are the rungs, and neither
  the division nor the width is a knob.
- Recipe v2 stands as accepted. `uw_spacing 0` derives the rung spacing as one base cell
  (0.0156 at refinement 5), and the width is $2S$. The setting remains in the driver only
  as an override of that derivation.
- Kaiju's division design is shelved. It is input for a library plate-boundaries module,
  for the dev hub to weigh, and is not driver code.
- The first v2 baselines, TAf-v2 and Earth run 2, are launched on kaiju from the pinned
  clone.

## What it does not say

- Louis's "(I think)" leaves the half-width open to measurement. No run has compared an
  equant band with a narrower one.
- The library's ladder takes any width. Only the drivers and the guides' recipes are bound
  by this ruling.
- UWTN 2026-022's runs have equant ladders finer than the cells: $S = 0.0052$ on a base of
  $h_b = 1/32$ in the recipe, and $S = 0.004$ on $h_b = 0.0156$ in the annulus models.
  Each band is $2S$ wide. They are kept, and the note says so.

## Closure

- **Preferred**: the equant ladder. The fault's own points are the rungs, about one local
  cell $h$ apart. The band is $2h$ wide, given as `width` to
  `place_fault_ribbon_2d(base, [(name, points)], width, split=True, mesher="ladder")`.
- **Allowed**: a ladder finer than the cells, with the width still twice the rung
  spacing, for comparison with the measurements already made (UWTN 2026-022, the
  band-ratio sweep, the spacing arms).
- **Where enforced**:
  - the drivers' ledger, principle row and `uw_spacing` row
    (`zg95_lid_regimes/DECISIONS.md`, uw3-campaigns main 017b84d); the drivers as they
    stand (recipe v2, a7792cd);
  - the fault-multigrid and faults-in-convection guides (PR #862, docs hub): ruling 4,
    the production paragraph and the convection recipe give the equant form with this
    entry;
  - UWTN 2026-022: its recipe says the width argument is $2S$, so the ladder is equant
    (notes session, on the workbench, not yet pushed);
  - the topic page (docs hub; done with this entry).

This entry supersedes the earlier 2026-11-03 entry, whose width reading was wrong. That
entry's principle, the fault's own points are the rungs and neither the division nor the
width is a knob, is carried here unchanged, and its quotation of Louis's morning message
remains the record of the principle.

## Verdict

Kept. Feeds the guides, the topic page, UWTN 2026-022 and the dev hub's plate-boundaries
module.
