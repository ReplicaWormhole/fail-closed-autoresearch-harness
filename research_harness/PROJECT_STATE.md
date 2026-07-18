# Project state: rank-two partial-trace inequality

Last migrated: 2026-06-03T20:01:29+02:00
Mode: co-mathematician workspace
Active claim: `CLAIM-0001`
Claim card: `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`
Machine status: `research_harness/status.json`

## Research question

For `C in M_4(C) tensor M_4(C)` with ordinary matrix rank `rank(C) <= 2`, prove or refute

```text
gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2||C||_F^2 - (1/2)|tr C|^2 <= 0.
```

The corrected partial trace convention for executable checks is:

```text
tr_1(C)[a,b] = sum_i C[i,a,i,b]
tr_2(C)[i,j] = sum_a C[i,a,j,a]
```

## Current mathematical state after LOOP-0013

Status: open / fail-closed / human steering requested.

The fixed-gauge complex-coefficient lemma route is refuted.  Universal PAL, PCL, and the original claim are tracked as equivalent formulations at the quantifier level, but none has been proved or refuted.

Current bottleneck:

1. Scalar crossed PAL/PCL minor: prove exactly `GramSlack >= ExchangePenalty`; LOOP-0013 provides restricted equality-family guardrails but no universal certificate.
2. Full PCL: prove PSD of the trace-coupled `4 x 4` matrix `M`, not the false D-only surrogate; LOOP-0013 isolates the determinant-update target but no PSD proof.
3. Equality geometry: turn restricted/local equality-family evidence into a global theorem useful for a proof.
4. Human steering: `ESC-0001` is open because the central symbolic certificate bottleneck survived LOOP-0012/0013.

## Coordinator policy

Before each loop, the project coordinator must:

1. read `status.json`, `GOALS.md`, `dashboard.md`, `uncertainty_ledger.md`, and active workstream states;
2. choose workstream actions that reduce a named uncertainty;
3. write incremental updates into affected workstreams;
4. run skeptic/auditor review;
5. update dashboard, status, and claim card;
6. escalate if no material progress is made on the same bottleneck.
