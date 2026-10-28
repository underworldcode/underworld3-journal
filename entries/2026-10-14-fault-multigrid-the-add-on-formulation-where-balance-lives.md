---
title: "Fault multigrid: the add-on formulation, where balance lives"
date: "2026-10-14"
authors:
  - "Louis Moresi"
options:
  kind: "finding"
  status: "live"
  topics:
    - "fault-multigrid"
  links:
    - "https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/1ce9b4692e7dfa7ea81eb9552cd354aa9b5c8d6b"
  origin: "wiki commit, migrated 2026-10-27"
---

Wiki commit [`1ce9b469`](https://github.com/underworldcode/underworld3/wiki/Fault-multigrid/1ce9b4692e7dfa7ea81eb9552cd354aa9b5c8d6b) by Louis Moresi, 2026-10-14: **Fault multigrid: the add-on formulation, where balance lives**

Underworld development team with AI support from Claude Code

The text this commit added, as written that day (the integrated version is on the topic page):

### Added to Fault multigrid

## The add-on formulation: where balance lives
The add-on has two goals, an accurate representation of the fault and rapid set-up and tear-down, and the balance of the whole system is a property of the add-on formulation alone: every cell outside the band is a copy of the base and inherits the base's balance. The two levers are fewer band cells and moved band cells; nothing else changes the ratio.
- **Minimal add-on degrees of freedom, no rebalance.** A split-node fault is an exact discontinuity at any resolution, so the leanest add-on is the cut (or the ladder at the base's spacing) on a clone of the base's finest level: the new unknowns are the duplicated spine nodes and the crossing vertices, and the only imbalance is the gathered star, two cell layers along the trace. For a plate-scale model that is a few percent on one rank. A TI band cannot be that lean, since it needs about two elements across its width, so the width sets the refinement. With a band of area fraction $f$ refined $k$ halvings on $P$ ranks, a fault of length $L$ in a domain of width $D$ loads the busiest rank by roughly $f\,4^{k}\sqrt{P}\,D/L$ above the mean: it grows with $\sqrt P$, so the cap moves out but never disappears, and it is dominated by $4^{k}$, which is the case for keeping the band at the base's resolution or one halving below it. The large case on this page refines three halvings across most of the box; those are a toy's proportions.
- **Non-conforming (composite) multigrid.** The fault-patch design already in the library for the finest level, extended to the ladder levels: the band is the only add-on, with no copy of the base, and the levels at $S, 2S, 4S$ live on the band and couple to the base at its rim. It removes the duplicated base from set-up and tear-down and from memory. It does not change the balance, because the band's cells are still on the band's ranks.
- **Partition the add-on levels for themselves.** The transfers are partition-agnostic and the co-location step already pays one redistribution per level per rebuild; a geometric partition of each add-on level weighted by its star costs the same and lifts the cap. The prize on the large case is the 16-rank solve going from about 67 s toward 25 to 30 s. Segmenting one fault's star across ranks is the expensive version, since it puts a pair on a rank seam and breaks the communication-free contact block; not now.
Position (2026-10-14): keep the band lean by realisation; never touch the base; the composite grid is the proper form of the add-on and the ladder its patch; the one cheap partitioning step on the add-on levels is tried and measured against the no-move case before it is kept. The ribbon replay is the prerequisite for all three.
