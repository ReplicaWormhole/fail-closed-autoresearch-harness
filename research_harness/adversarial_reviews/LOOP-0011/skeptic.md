# LOOP-0011 skeptic review

status: FAIL-CLOSED / REJECT LOOP SUCCESS
claim_focus: CLAIM-0001-rank-two-partial-trace
role: skeptic / adversarial review
reviewed_artifacts:
- `research_harness/adversarial_reviews/LOOP-0011/scalar_slack_domination_lane.md`
- `research_harness/adversarial_reviews/LOOP-0011/full_pcl_lift_lane.md`
- `research_harness/adversarial_reviews/LOOP-0011/diagonal_zero_modes_lane.md`
- `research_harness/experiments/LOOP-0011_scalar_slack_domination_lane.py`
- `research_harness/experiments/LOOP-0011_full_pcl_schur_diagnostics.py`
- `research_harness/experiments/LOOP-0011_diagonal_zero_modes_lane.py`
- `research_harness/logs/LOOP-0011_scalar_slack_domination_lane_seed11011.stdout.log`
- `research_harness/logs/LOOP-0011_scalar_slack_domination_lane_seed11011.json`
- `research_harness/logs/LOOP-0011_full_pcl_schur_diagnostics_seed11011.stdout.log`
- `research_harness/logs/LOOP-0011_full_pcl_schur_diagnostics_seed11011.json`
- `research_harness/logs/LOOP-0011_diagonal_zero_modes_lane.json`

## Executive verdict

LOOP-0011 does not prove CLAIM-0001 and must not be promoted.

The loop made useful fail-closed progress:

1. it sharpened the scalar crossed PAL/PCL determinant into the ratio/slack-domination form
   `q := D1D2/(N12N21) >= rho := |m|^2/(N12N21)` when `N12N21 > 0`;
2. it confirmed that equality controls can have exchange penalty equal to mixed Gram slack, so scalar proofs must encode cancellation rather than delete the penalty;
3. it produced a reproducible full-PCL Schur/principal-minor diagnostic which again shows that `D = 2I-A-B` is not a valid certificate object by itself;
4. it numerically classified the four LOOP-0010 diagonal-difference residual zero modes by adding active support-plane directions.

None of these closes the claim.  The correct adversarial status remains:

```text
LOOP-0011: FAIL-CLOSED
CLAIM-0001: NOT PROVED
COUNTEREXAMPLE: NOT FOUND
BRIDGE DEFECT: NOT FOUND
PROMOTION: REJECTED
```

## Claim and skeptic standard

Target claim:

```text
rank(C) <= 2 in M_4(C) tensor M_4(C)
  implies

gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2||C||_F^2 - (1/2)|tr C|^2 <= 0.
```

Skeptic standard for LOOP-0011:

- no hidden Hermitian, normal, positive, diagonal, commuting, real, or coordinate-support assumptions;
- no promotion of a scalar crossed minor to full PCL or CLAIM-0001 without the missing full-matrix/quantifier bridge;
- no treatment of finite coordinate scans, Schur diagnostics, or random Haar probes as symbolic proof;
- no treatment of local zero-mode classification as global equality classification or global inequality proof;
- no certificate route based on `D >= 0`, `det(D_S) >= 0`, or D-only Schur complements after repeated coordinate obstructions.

## PASS/FAIL gates

### Gate A: certified rank-two positive-gap counterexample

Status: FAIL.

No LOOP-0011 artifact exports an explicit rank-at-most-two matrix `C` with rigorously certified positive corrected partial-trace gap.  The scalar lane reports no scalar violation; the full-PCL lane reports no negative tested `M`; the zero-mode lane reports sampled equality/roundoff zero-gap rays, not positive-gap counterexamples.

Roundoff-scale values remain rejected unless backed by exact, interval, or high-precision certification of `rank(C) <= 2` and `gap(C) > 0` with the corrected partial traces.

### Gate B: scalar crossed PAL/PCL determinant proof

Status: FAIL, with surviving reduction.

The scalar lane studies

```text
Delta = D1 D2 - |m|^2
      = GramSlack - ExchangePenalty,
GramSlack       = N12 N21 - |m|^2,
ExchangePenalty = N12 N21 - D1 D2.
```

When `N12N21 > 0`, this becomes the ratio target

```text
q := D1D2/(N12N21) >= rho := |m|^2/(N12N21).
```

What survives from the real run:

```text
coordinate_equality_count = 264
coordinate_equality_signature_count = 3
coordinate_max_ratio = 1.0
coordinate_min_delta = 0.0
random_min_delta = 1.8042001266381489 at sample 1251
random_max_ratio = 0.3025637369333136 at sample 1490
random_min_normalized_gap = 0.6968995627087884 at sample 1490
local_min_delta_objective = 1.4531204332359976e-08
local_max_penalty_ratio_objective = -0.9999970379320856
local_min_normalized_gap_objective = 3.899191214726261e-06
```

The negative objective value for `local_max_penalty_ratio_objective` is a maximization convention: it corresponds to a penalty/slack ratio near `0.9999970379320856`, i.e. near equality, not a violation.

The sharp equality controls remain:

```text
product_LOOP9:   delta=0.0, slack=0.75, penalty=0.75, ratio=1.0
traceless_LOOP9: delta=0.0, slack=3.75, penalty=3.75, ratio=1.0
```

What does not survive:

- `Delta = GramSlack - ExchangePenalty` is not a proof of `Delta >= 0`.
- A Cauchy proof of `GramSlack >= 0` alone is insufficient; the whole difficulty is proving it dominates the exchange penalty.
- Any route that makes the exchange penalty vanish, nonpositive, or separately bounded by a false diagonal defect is rejected.
- The finite coordinate and random/local numerical probes are not a symbolic scalar certificate.

Skeptic verdict for Gate B: useful scalar bottleneck sharpening, no scalar proof.

### Gate C: scalar result promoted to full PCL or CLAIM-0001

Status: FAIL.

Even a future proof of this scalar crossed determinant would not, by itself, prove full PCL or CLAIM-0001.  LOOP-0011 provides no bridge from one scalar crossed minor to all principal minors or to PSD of the full `4 x 4` compression matrix for every pair of complex two-planes.  A scalar PAL/crossed-minor result remains a necessary subtarget/regression, not a complete proof of the original rank-two inequality.

### Gate D: full PCL Schur/principal-minor certificate

Status: FAIL, with strong guardrails.

The full-PCL lane probes

```text
M = 2I - A - B + (1/2)T
  = D + (1/2)conjugate(t)t^T.
```

It checks principal-minor update identities, Schur complements over principal pivots, and all unpivoted one-by-one pivot permutations for coordinate controls and random frames.

What survives from the real run:

```text
trials = 250
negative_min_eig_M = 0
negative_principal_detM_cases = 0
random_min_eig_M_min = 1.1697749192794171
random_schur_M_negative_splits = 0
random_pivot_M_negative_sequences = 0
coordinate_negative_min_eig_M = 0
coordinate_M_schur_negative_splits = 0
max_update_identity_error = 3.552715515154371e-15
```

The same run again rejects D-only certificate routes on coordinate supports:

```text
coordinate_negative_min_eig_D = 48
coordinate_negative_detD_by_size = {"1": 0, "2": 48, "3": 96, "4": 48}
coordinate_repaired_negative_D_by_size = {"1": 0, "2": 48, "3": 96, "4": 48}
coordinate_D_schur_negative_splits = 144
```

What does not survive:

- Random frames in this run are far from the boundary and cannot certify universal PSD.
- Coordinate support pairs are a finite diagnostic set, not a cover of `Gr(2,16) x Gr(2,16)`.
- Schur complements checked numerically over finite cases are not symbolic nonnegativity proofs.
- Positivity of tested Schur pivots is not a globally valid pivot strategy unless a symbolic positive pivot/minor selection theorem is supplied.
- D-only Schur or determinant routes are explicitly false on coordinate equality/boundary cases.

Skeptic verdict for Gate D: useful diagnostic and false-route rejection, no full PCL proof.

### Gate E: diagonal-difference zero-mode classification as proof

Status: FAIL, with improved local classification.

LOOP-0011 repairs the LOOP-0010 local zero-mode gap at the diagonal-difference control by adding active support-plane candidates in the `2 x 2` atom plane:

```text
span{i C0, A tensor P, i A tensor P, P tensor B, i P tensor B for A,B in {E01,E10}}.
```

What survives from the JSON log:

```text
zero_count_tol = 9
negative_count_tol = 110
positive_count_tol = 0
eigenvalue_min = -2.0
eigenvalue_max = 0.0

LOOP0010_prior_candidates:
  classified = 5, unclassified = 4, contains_zero_space = false,
  max residual = 0.7071067811865475, min principal cosine = 0.0

expanded_support_plane_only:
  candidate_rank = 9, classified = 9, unclassified = 0,
  contains_zero_space = true, max residual = 1.5700924586837752e-16,
  min principal cosine = 1.0

prior_plus_expanded_support_plane:
  classified = 9, unclassified = 0,
  contains_zero_space = true, max residual = 3.188872858294072e-16

four_dim_prior_residual_target_vs_expanded:
  classified = 4, unclassified = 0,
  contains_zero_space = true, max residual = 7.850462293418876e-17
```

The sampled one-parameter rays along expanded directions stayed rank <= 2 and had zero or roundoff-zero gap in the log.

What does not survive:

- This is a local floating-point Hessian/tangent-space classification at one equality control.
- It is not an exact symbolic tangent-kernel theorem.
- It is not a proof that these directions integrate to all nearby equality families beyond the sampled rays.
- It is not a global equality classification and does not exclude remote positive-gap rank-two matrices.
- Local negative-semidefinite second variation plus zero-mode classification is not a global proof of CLAIM-0001.

Skeptic verdict for Gate E: LOOP-0010 local gap repaired numerically, but still no global proof.

## Rejected overclaims and invalid routes

The following promotions are explicitly rejected:

1. `GramSlack - ExchangePenalty` proves scalar nonnegativity.
   False.  LOOP-0011 identifies the needed domination inequality; it does not prove it.

2. Equality/near-equality local optimization proves scalar PAL.
   False.  Local optimization approached equality ratios near `1`, but no symbolic proof or certified exhaustive search was produced.

3. Scalar crossed-minor success proves full PCL or CLAIM-0001.
   False unless a separate bridge proves all full-PCL PSD requirements or an equivalent direct rank-two inequality with all quantifiers.

4. Coordinate equality signatures are a finite normal form for arbitrary frames.
   Not established.  Coordinate supports are regression tests and obstruction examples only.

5. Schur diagnostics are a proof.
   False.  Finite/random Schur checks do not supply a universal pivot rule or symbolic nonnegative Schur complement formula.

6. `D >= 0`, `det(D_S) >= 0`, or D-only Schur complements.
   False/rejected.  LOOP-0011 reports coordinate negative `D` eigen/minor/Schur behavior repaired only by the trace update.

7. The trace rank-one update can be added after proving a D-only fact.
   False in the sharp cases.  The update must be retained throughout the certificate because it cancels defects in equality/boundary strata.

8. Local zero-mode classification proves the inequality.
   False.  It is local, numerical, and tied to visible equality controls; global proof requires compactness/patching or an independent certificate.

9. Hidden structural assumptions on `C` or the support frames.
   Rejected.  CLAIM-0001 is for arbitrary complex rank-at-most-two operators, not only Hermitian, normal, positive, diagonal, coordinate, real, or commuting cases.

## Surviving reductions and useful facts

Accepted as useful but insufficient:

- The scalar crossed determinant is now sharply framed as a cancellation problem:

```text
D1D2 - |m|^2
= (N12N21 - |m|^2) - (N12N21 - D1D2).
```

- Equality controls force any scalar certificate to vanish where exchange penalty equals Gram slack; a proof must encode this null structure.

- The ratio form `q >= rho` is a useful diagnostic when `N12N21 > 0`, but singular/zero cases still need polynomial handling in any exact proof.

- Full PCL must be attacked through the trace-coupled matrix

```text
M = D + (1/2)conjugate(t)t^T,
```

and principal minors through the coupled adjugate/rank-one-update expression, not through `D` alone.

- Coordinate support pairs and known equality controls are valuable regression tests: any proposed certificate that fails them is invalid.

- The added active support-plane directions plausibly explain the previously unclassified diagonal-difference local zero modes, but only as local numerical evidence.

## What remains unproved

- Universal scalar nonnegativity of the crossed determinant `D1D2 - |m|^2 >= 0`.
- A non-circular proof that mixed Gram slack dominates exchange penalty on the complex two-frame constraint manifold.
- Full `4 x 4` PCL PSD for all rank-two support projections.
- Nonnegativity of all full-PCL principal minors for arbitrary complex frames.
- A symbolic Schur/Gram/SOS certificate retaining the trace rank-one update at every step.
- A globally valid pivot/minor selection theorem if using Schur complements.
- Exact equality-manifold classification and a global patching/compactness argument.
- A certified rank-at-most-two positive-gap counterexample.

## Next precise attacks

1. Coupled scalar SOS with equality null constraints.
   Attack `D1D2 - |m|^2` directly on the complex orthonormal two-frame manifold.  Build product and traceless equality null conditions into the Gram/SOS ansatz so the certificate vanishes when exchange penalty equals Gram slack.

2. Exchange-penalty domination, not removal.
   Decompose `N12N21 - D1D2` against the actual mixed Gram slack.  Do not attempt to prove it is nonpositive or separately dominated by false diagonal defects.

3. Polynomial treatment of zero mixed-norm cases.
   The ratio diagnostic is useful only when `N12N21 > 0`.  Any exact scalar proof must handle `N12N21 = 0` by polynomial identities or limiting arguments, not by dividing without justification.

4. Full trace-coupled Schur certificates.
   Derive symbolic formulas for Schur complements of `M`, not `D`, under pivots whose positivity is itself proven.  Test every formula on coordinate equality controls where D-only Schur complements go negative.

5. All-principal-minor adjugate attack.
   For every principal subset `S`, prove or refute

```text
det(D_S) + (1/2)t_S^T adj(D_S)conjugate(t_S) >= 0
```

on `Gr(2,16) x Gr(2,16)`, including singular `D_S` cases.

6. Exact zero-mode/equality-family theorem.
   Replace numerical Hessian eigenspaces by exact tangent-kernel calculations at the diagonal-difference and product-projection controls.  Then prove which zero directions integrate to equality families and whether these local families exhaust the equality set.

7. Scalar-to-full bridge audit.
   If scalar PAL/crossed-minor is proven, immediately audit whether it supplies full PCL PSD, all relevant principal minors, or a direct CLAIM-0001 proof.  Do not declare success from one scalar minor alone.

8. Counterexample certification route.
   Continue direct rank-two searches; if any positive gap appears, export the explicit matrix and certify `rank(C) <= 2` and corrected `gap(C) > 0` using exact/high-precision/interval arithmetic.

## Final skeptic decision

```text
LOOP-0011: FAIL-CLOSED
CLAIM-0001: NOT PROVED
COUNTEREXAMPLE: NOT FOUND
BRIDGE DEFECT: NOT FOUND
PROMOTION: REJECTED
```

LOOP-0011 usefully sharpened the scalar slack-domination target, strengthened the full-PCL trace-coupled Schur guardrails, and numerically closed the LOOP-0010 diagonal-difference local zero-mode residual.  It did not produce a proof, a certified counterexample, or a valid scalar-to-full-PCL bridge.  CLAIM-0001 remains open.
