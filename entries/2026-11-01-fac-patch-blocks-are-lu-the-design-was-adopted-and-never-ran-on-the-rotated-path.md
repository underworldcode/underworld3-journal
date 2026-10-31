---
title: "FAC patch blocks are LU and ILU there is a regression: the LU block solve of #670 was measured, made the default and never ran on the rotated path, because the composite's ASM child read the options after the rotated path had deleted them (#892, fixed by #912)"
date: 2026-11-01
authors: [docs hub session_01HxWvn87HYCEJodpgCdaBro, from the dev hub's reading of the code and the notes session's correction]
options:
  kind: finding
  status: live
  topics: [fault-multigrid, solvers-and-multigrid]
  links:
    - https://github.com/underworldcode/underworld3/issues/892
    - https://github.com/underworldcode/underworld3/pull/912
    - https://github.com/underworldcode/underworld3/commit/891c9bb0
    - https://github.com/underworldcode/underworld3/commit/9f4cb200
    - https://github.com/lmoresi/uw3-campaigns/blob/main/DEV-HUB.md
---

The fault-patch design of August says the finest level's additive-Schwarz blocks over
the fault zone are solved by LU with a nonzero shift. On the rotated free-slip path,
which every fault model uses, they ran as unshifted ILU(0) from the day LU became the
default (2026-09-03) until #912 (2026-10-31). The design was measured, adopted, and
never applied on the path the fault models use; nothing was dropped to work around a
bug, and nothing regressed from a state that had worked. This entry is the record the
dev hub's plan asked for (its step 7), written where the next refactor will meet it.

## The defect

`custom_mg._configure_pcmg` writes the FAC block solver
(`mg_levels_<l>_sub_1_sub_pc_type lu`, nonzero shift) into the options database. The
rotated path forces the level smoother's `setUp()` and then deletes those keys.
`PCSetUp_Composite` only hands its children their operators, so the ASM child sets up
at its first apply; by then the keys are gone and its blocks take PCASM's default,
unshifted ILU(0). Found by the integration session on 2026-10-29 when the tail sweep
recorded each level's smoother; filed as #892.

## The history, read from the code

The first account passed between sessions ("LU blocks landed in August, the composite
default of September regressed them") was wrong, and the dev hub corrected it from the
commits:

- 9f4cb200, 2026-08-26 (#638, the fault-patch design #629): the patch lands as plain
  ASM replacing the level smoother, with an **SOR** block solve; `UW_FAC_SUB_PC` had
  no default. The forced `setUp()` covers plain ASM, so the rotated path got what it
  was configured to get.
- 18f0b947, 2026-09-03 (#670): the band block's rows are capped and cut along strike so
  that an LU block stays cheap.
- 891c9bb0, 2026-09-03 (#670): composite mode **and** LU with a nonzero shift become
  the defaults in the same commit. Its measurement was on the TI S-fault rig (10
  velocity iterations against 44), on the non-rotated path.
- So on the rotated path the LU blocks never ran. The non-rotated callers never delete
  the keys and probably do get LU; the dev hub is confirming that.
- ab8003ef, 2026-10-13: the split-level hierarchy. A pair touching a split coarse level
  skips FAC detection (`custom_mg.py:1556` at 4698938f), so no chain hierarchy ever
  carried the patch on any level.
- A stale comment in `custom_mg.py` ("Subdomain solver: SOR ... no factorization") sat
  above a default of `"lu"` until #912: the amnesia in miniature.

Louis, 2026-10-30, on the first account: "I thought ASM with the fault split into small
patches so LU works efficiently was our original choice. I did not realise that we
dropped this to work around a bug and then gave up on it. This seems typical of the kind
of amnesia that regresses great algorithms into dead ones!" The corrected account is
less dramatic and the same lesson: a design that is written down, measured once on one
path and set as a default is not applied until something reads back what runs.

## What rested on it

Every fault rotated solve from 2026-09-03 to #912: the faults-in-convection guide's
welded-against-chain table (the welded tail's 200-iteration caps on a mobilising lid),
the 2026-10-29 tail ruling and its provisional form of 2026-10-30, the drivers'
`uw_chain=2`, and the kaiju trench demonstrations in UWTN 2026-022. With the LU blocks
the welded base with the split finest takes 3 velocity iterations per linear solve at
every band ratio from 6 to 25 (entry 2026-10-31; ruling, entry of today).

## The fix, and the intent where the next refactor will meet it

#912 (cc839425): a helper in `custom_mg`, called after `pc.setUp()` from every call
site, sets up each FAC level's smoother and its composite child and puts the configured
block solver on the live block KSPs (88212f75); a regression test, written first and
shown failing, reads back the live block PC of every FAC level and fails unless it is
the configured type, composite and plain ASM, rotated and non-rotated, serial and at
np 2 (`test_1090_mg_live_configuration_parallel`, 44612397, 3e5d9880); the docstring at
the block configuration and at the helper say it in words (`custom_mg.py` 1216 and 1260
at 25d62812).

The durable intent, in one sentence each place it lives: **FAC blocks are LU, with the
nonzero shift; ILU there is a regression.** And the class it belongs to: a key written
to the options database for a consumer that sets up lazily must still be there when the
consumer runs, or be set on the live object; the general guard is a test that reads
back every multigrid level's live configuration against what was configured (the dev
hub's step 8), and #806 (solvers do not report the configuration they ran with) is its
observability half.

## Verdict

Kept. Feeds the fault-multigrid guide's configuration rules (PR #862), the topic page's
current understanding, and the dev hub's `PRIORITY` record. The non-rotated path's
block solver, once confirmed, is a one-line follow-up here or on #892.
