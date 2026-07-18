# Current State: Kronecker-Sum Singular-Value Problem

Status: fail-closed; main theorem not proved.

## Problem family

The repository contains earlier attempts to prove a singular-value inequality for Kronecker sums. The current reduction identifies a rank-two partial-trace inequality as the missing bridge.

## Solid items from existing repository notes

From `problem_statement_aristotle/co_mathematician/COORDINATOR_REPORT_2026-05-09.md`:

- The Frobenius identity is proved in Lean as `frobenius_norm_kronecker_sum`.
- The normal case has a written proof in `worked_out_proof.tex`.
- The desired constant is sharp if true, witnessed by `A = (1/2) E_12`, `B = 0`.
- The projection reduction identifies the rank-two partial-trace inequality as the missing bridge.
- The main Lean theorem `kronecker_sum_sv_bound` still has `sorry`.
- The normal-matrix density argument is false.
- The corrected polarization calculation does not prove the needed rank-two partial-trace inequality.

## Current bottleneck

The central claim is `CLAIM-0001`: for `rank(C) <= 2`,

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2
  <= 2 ||C||_F^2 + (1/2) |tr C|^2.
```

## Existing numerical evidence

Existing checks found no violation and optimized to equality within roundoff. The exact equality witness recorded in the repo is

```text
C = (1/sqrt(2)) ( |0,0><0,0| - |1,1><1,1| ).
```

For this witness:

```text
rank(C) = 2,
||C||_F^2 = 1,
tr(C) = 0,
tr_1(C) = tr_2(C) = (1/sqrt(2)) diag(1, -1, 0, 0),
lhs = 2,
rhs = 2.
```

## Live possibilities

The harness should keep all three possibilities alive:

1. The rank-two partial-trace inequality is true and proves the singular-value inequality.
2. The rank-two partial-trace inequality is too strong, but the Kronecker-sum problem is true for a weaker reason.
3. The singular-value inequality is false, and the right counterexample family has not yet been found.

## Immediate research target

Run adversarial Loop 0001:

- Proposer A: analytic proof via rank-two factorization `C = U V^*`.
- Proposer B: counterexample/stronger-lemma hunter.
- Repo auditor: map all old attempts into proved/false/incomplete/numerical/formalized.
- Skeptic: attack the proposals.
- Auditor: assign fail-closed statuses and update claim cards.
