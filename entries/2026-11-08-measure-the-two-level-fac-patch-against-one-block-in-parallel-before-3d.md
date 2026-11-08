---
title: "Measure the two-level FAC patch against #934's one block in parallel, by wall time and memory, before any 3-D work: the serial iteration comparison that held it could not show its case (Louis, 2026-11-08)"
date: 2026-11-08
authors: ["Louis Moresi", "docs hub session_01HxWvn87HYCEJodpgCdaBro"]
options:
  kind: decision
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/pull/934
    - https://github.com/underworldcode/underworld3/issues/895
    - https://github.com/underworldcode/underworld3/tree/feature/fault-slip-coarse-space
    - entries/2026-11-02-the-add-on-is-the-line-for-split-faults-the-fault-carries-its-own-resolution-and-split-coarse-levels-are-not-developed-further.md
---

Louis asked on 2026-11-08 whether #934 unwinds the parallel distribution of the fault
work, and what became of the blocks-plus-coarse-slip design. Both have short answers.
The distribution of the add-on (its partition, load balance, rank-interior stars and
transfers) is intact. What #934 changed is the finest level's FAC patch: to fix #925, the
blocks are now cut from every rank's rows and sent whole to one rank, and with no zone
keyed the structural rows of every fault form one block. So a single fault, already on
one rank under the gather placement, loses nothing, but a network's faults no longer
factorise in parallel. The two-level form, bounded ASM pieces plus one global slip coarse
problem factorised redundantly on every rank, exists on `feature/fault-slip-coarse-space`
and handles any number of faults with one coarse solve. It was held on 2026-11-02 because
it lost to one block in 2-D, on a comparison of iterations, mostly serial (79-87 against
67), where the exact block always wins. Its case, parallel wall time and memory, was never
measured.

## What was decided

Louis, 2026-11-08, on the docs hub's recommendation: "OK - let's go with your
recommendation". Before any 3-D work, compare in 2-D on kaiju:

- fixtures: UWTN 2026-022's linear fixture at band ratios 24 and 48; a two-fault network
  whose faults land on different ranks; a fault placed with conforming seams where one
  can be;
- arms: #934's one block; the two-level form at `fac_block_rows` 2000 and at one rung;
  per-rank pieces with no coarse space, as the control;
- np 1, 4, 8 and 16;
- measured: velocity iterations, velocity-solve wall time, patch set-up and
  factorisation time, peak memory per rank, coarse-problem size, and the answer.

## Closure

- **Preferred**: decide the patch's form from parallel time and memory, not serial
  iterations. Until the table is in, #934's one block stays the default.
- **Allowed**: the two-level form as an opt-in on its branch, for the comparison.
- **Where enforced**: the dev hub's queue under #895 (brief in `DOCS-HUB.md`, "For the
  other hubs", 2026-11-08; sending it directly was refused, so it waits there); the
  fault-multigrid guide's parallel section, which already says a network's patch is one
  LU on one rank and its cost is unmeasured.

## Verdict

Open until the table is in; the entry that reports it carries Louis's ruling on the
default for networks and for 3-D.
