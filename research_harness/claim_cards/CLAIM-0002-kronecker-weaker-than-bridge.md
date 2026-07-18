# CLAIM-0002: Kronecker-Sum Target May Be Weaker Than Full Rank-Two Bridge

status: refuted
last_updated: 2026-06-03

## Statement

The Kronecker-sum singular-value inequality may require only a restricted/projected version of `CLAIM-0001`, not the full rank-two partial-trace inequality for arbitrary rank-two `C in M_4(C) tensor M_4(C)`.

## Motivation

The existing coordinator report recommends testing whether the Kronecker-sum problem is weaker than the full open rank-two inequality. This matters because `CLAIM-0001` may be true, false, or unnecessarily strong.

## Tasks

1. Identify the exact image of the projection/reduction from the Kronecker-sum singular-value problem into rank-two operators `C`.
2. Determine whether arbitrary rank-two `C` occur in that image.
3. If not, formulate the restricted partial-trace inequality actually needed.
4. Search for numerical violations of the full bridge that do not lie in the Kronecker-sum image.
5. If a restricted inequality is found, create a new claim card for it.

## Current status

LOOP-0001 audit recommends retiring this claim as currently worded. The bridge
note `partial_trace_inequality_needed_for_sv_bound.tex` gives an equivalence
between the Kronecker-sum singular-value bound and the full rank-two
projection/partial-trace estimate for arbitrary ordinary rank-two `C`. No
restricted-image formulation was identified.

## Refutation basis

The backward direction in the bridge note takes an arbitrary rank-two `C`,
projects it to the traceless Kronecker-sum subspace, and applies the
Kronecker-sum singular-value bound to recover the projection estimate for that
same arbitrary `C`. Via the centered partial-trace identity, this is exactly
`CLAIM-0001`.

## Possible replacement

Create a new claim only if a future loop identifies a different target
inequality, a different variational class, or a verified defect in the bridge
equivalence.

## Promotion criterion

Promote only after the reduction map and its image constraints are written explicitly and checked against the existing Kronecker-sum formulation.
