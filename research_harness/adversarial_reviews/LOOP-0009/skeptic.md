# LOOP-0009 skeptic review

status: FAIL-CLOSED / REJECT LOOP SUCCESS
claim_focus: CLAIM-0001-rank-two-partial-trace
role: skeptic / adversarial review
reviewed_artifacts:
- `research_harness/adversarial_reviews/LOOP-0009/mixed_plucker_lane.md`
- `research_harness/adversarial_reviews/LOOP-0009/zero_mode_lane.md`
- `research_harness/adversarial_reviews/LOOP-0009/principal_minor_lane.md`
- `research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.stdout.log`
- `research_harness/logs/LOOP-0009_zero_mode_classification.stdout.log`
- `research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.stdout.log`
- prior context: `research_harness/adversarial_reviews/LOOP-0008/coordinator.md`

## Executive verdict

LOOP-0009 does not prove CLAIM-0001 and must not be promoted.

The loop produced useful diagnostics:

1. an exact mixed two-frame Plucker identity for the crossed scalar off-diagonal, checked numerically to roundoff;
2. a concrete obstruction to the naive mixed-vector Cauchy/Gram norm-domination proof;
3. repaired zero-mode diagnostics at the equality controls;
4. a deterministic principal-minor/rank-one-update probe for the full `4 x 4` PCL matrix.

But every proof gate remains open.  No scalar determinant certificate, no full PCL PSD certificate, no global equality classification, and no certified positive-gap rank-two counterexample were produced.  The correct adversarial status is therefore:

```text
FAIL-CLOSED / REJECT LOOP SUCCESS / CLAIM-0001 REMAINS OPEN
```

## Claim under review

Target claim:

```text
rank(C) <= 2 in M_4(C) tensor M_4(C)
  implies

gap(C) = ||tr1 C||_F^2 + ||tr2 C||_F^2
         - 2||C||_F^2 - (1/2)|tr C|^2 <= 0,
```

with the corrected partial traces.

Skeptic standard: do not accept arguments that silently assume Hermitian, normal, positive, commuting, or real structure; do not treat scalar PAL as full PCL; do not treat local tangent evidence as a global proof; do not claim `D >= 0` or `det(D) >= 0`; do not use uncoupled Cauchy/Plucker norm bounds unless the required domination inequalities are actually true on the constrained frame manifold.

## PASS/FAIL gates

### Gate A: certified rank-two counterexample

Status: FAIL.

No artifact reports an explicit rank-at-most-two `C` with certified positive corrected `gap(C)`.  The reported near-equality positives/zeros remain numerical roundoff or equality controls, not counterexamples.

Relevant LOOP-0008 guardrail remains active: the converted full-PCL search had worst converted original normalized gap `2.2204460492503126e-16`, explicitly treated as roundoff/equality evidence in `LOOP-0008/coordinator.md`, not as a violation.

### Gate B: scalar crossed PAL/PCL determinant proof

Status: FAIL, with useful obstruction.

The scalar target was

```text
D_1 D_2 - |m|^2 >= 0,
```

equivalently `det M[{(1,1),(2,2)}] >= 0`, with the trace rank-one update retained.

What survived:

- `mixed_plucker_lane.md` reports an exact mixed off-diagonal identity on the orthonormal frame constraint manifold:

```text
m = R_mix + C_mix + (1/2) conjugate(t_1) t_2.
```

- The stdout log confirms the mixed identity was checked to roundoff:

```text
max_mixed_offdiag_identity_error: 8.441528768080324e-17
sparse max identity error: 0.0
optimized near-equality identity error: 2.2887833992611187e-16
```

- This repairs the LOOP-0008 same-pair polarization obstruction at the off-diagonal identity level.  LOOP-0009 still measured same-pair mismatch, with stdout reporting:

```text
max_same_pair_polarization_mismatch: 0.47081642102929433
```

What did not survive:

- The direct mixed Plucker/Cauchy proof route fails.  The natural mixed norms `N_12,N_21` are not bounded by the diagonal defects `D_1,D_2`.
- The log reports negative margins on actual orthonormal frames:

```text
random min(D_1 - N_12): -0.41194477765578674
random min(D_2 - N_21): -0.4054262460823934
sparse min(D_1 - N_12): -1.5
sparse min(D_2 - N_21): -1.5
sparse negative D_1-N_12 count: 5260 / 14400
sparse negative D_2-N_21 count: 5260 / 14400
```

Therefore any proof based on the uncoupled chain

```text
|m|^2 <= N_12 N_21,
N_12 <= D_1,
N_21 <= D_2
```

is rejected as false.  Orthogonality multipliers alone cannot fix this particular subclaim because the negative margins already occur on the exact constraint manifold.

### Gate C: scalar evidence promoted to full PCL or CLAIM

Status: FAIL.

Even if the scalar crossed determinant were proven, LOOP-0009 does not establish a valid bridge from scalar PAL/crossed-PCL to the full `4 x 4` PCL PSD condition, nor from scalar PAL alone to CLAIM-0001 with all quantifiers.  The current scalar lane is a subproblem, not a complete claim proof.

### Gate D: full `4 x 4` PCL principal-minor proof

Status: FAIL, with useful guardrail.

What survived:

- `principal_minor_lane.md` gives the correct coupled rank-one-update shape for principal minors:

```text
det(D_S + (1/2) conjugate(t_S) t_S^T)
 = det(D_S) + (1/2) t_S^T adj(D_S) conjugate(t_S).
```

- The stdout log reports:

```text
coordinate negative-pair counts by minor size: {'1': 0, '2': 0, '3': 0, '4': 0}
random negative-frame counts by minor size: {'1': 0, '2': 0, '3': 0, '4': 0}
random min det(M_S) by size: {'1': 1.2084680308569111, '2': 1.6516027614966962, '3': 2.4529810081740915, '4': 3.7146661736564064}
max rank-one-update identity error: 4.440892108477151e-15
```

- Equality controls retained `min_eig(M)=0`:

```text
product_projection_support_00_10: 0.0
diagonal_traceless_support_00_11: 0.0
right_product_support_00_01: 0.0
```

What did not survive:

- The principal-minor lane is numerical search plus a determinant identity, not nonnegativity proof for all frames.
- It does not prove all `1 x 1`, `2 x 2`, `3 x 3`, and `4 x 4` principal minors.
- It correctly avoids, and the skeptic rejects, any shortcut claiming `D_S >= 0` or `det(D_S) >= 0`.  LOOP-0008 already recorded the trace-update obstruction: product support can have `eig(D)=[-1,1,1,1]` while the update repairs `M` to `eig(M)=[0,1,1,1]`.

### Gate E: tangent/equality classification as proof

Status: FAIL, with useful local evidence.

What survived:

- `zero_mode_lane.md` reports the repaired zero-mode run:

```text
diag_difference: zero_count=9, positive_count=0, eigmax=0.0
product_projection: zero_count=13, positive_count=0, eigmax=0.0
```

- This is consistent with LOOP-0008 tangent evidence: the equality controls appear stationary and have no observed positive Hessian directions on the real Frobenius unit sphere.

What did not survive:

- No exact equality-manifold classification was produced.
- No symbolic orbit/tangent parametrization was certified.
- No compactness, patching, or global maximality argument was supplied.

Therefore tangent evidence remains local numerical support only.  It cannot replace a scalar certificate, full PCL proof, or counterexample.

## Rejected overclaims

The following interpretations are explicitly rejected:

1. `Mixed Plucker identity found` => `scalar determinant proven`.
   False.  The identity is useful, but the direct Cauchy norm domination needed for the obvious proof route is false.

2. `No random/sparse negative principal minors` => `full PCL PSD proven`.
   False.  Random and coordinate scans are regression tests, not universal quantifier elimination.

3. `Rank-one-update formula verified` => `principal minors nonnegative`.
   False.  The formula gives the right coupled object to prove; it does not prove its sign.

4. `D` or `D_S` is nonnegative.
   False/not established and contradicted by prior controls.  The trace term must remain coupled.

5. `Scalar PAL/crossed minor` => `full PCL` => `CLAIM-0001`.
   Not established.  This bridge remains a major missing step.

6. `Zero Hessian modes look like equality directions` => `global proof`.
   False.  The zero-mode lane has no certified global classification.

7. Any hidden assumption that frame matrices are Hermitian, normal, positive, diagonal, commuting, or real.
   Rejected.  The target is over general complex matrices; proof attempts must preserve that setting.

## What LOOP-0009 actually establishes

Accepted as useful, but not sufficient:

- The LOOP-0008 same-pair polarization obstruction has a more precise replacement: a genuine mixed two-frame Plucker identity gives the crossed off-diagonal entry, modulo explicit orthonormality constraints.
- The simplest mixed-vector Cauchy/SOS route is blocked by explicit negative `D_i - N_ij` margins, including sparse coordinate frames with margin `-1.5`.
- Equality controls continue to behave as sharp controls: local Hessian diagnostics show no positive eigenvalues and the principal-minor controls have `min_eig(M)=0`.
- The principal-minor route should use the coupled adjugate/rank-one-update expression, not an uncoupled determinant of `D`.

## What remains unproved

- Universal scalar nonnegativity of `det M[{(1,1),(2,2)}]`.
- Full `4 x 4` PCL PSD for all orthonormal two-frames.
- Nonnegativity of all full-PCL principal minors.
- A bridge from scalar PAL/crossed-PCL evidence to CLAIM-0001.
- Exact equality-manifold classification and a global argument from it.
- A certified rank-at-most-two positive-gap counterexample.

## Next precise attacks

1. Determinant-level mixed Plucker SOS.
   Do not try to prove `N_12 <= D_1` and `N_21 <= D_2`; that subclaim is falsified.  Instead attack

```text
D_1D_2 - |R_mix + C_mix + (1/2)conjugate(t_1)t_2|^2
```

directly with orthonormality multipliers and equality null directions forced into the Gram ansatz.

2. Equality-forced Gram constraints.
   Any scalar or principal-minor SOS must vanish at both product and traceless equality controls even though the mixed wedge norms can be large.  Build these null constraints into the ansatz before solving.

3. Full principal-minor certificates.
   For each principal subset `S`, prove or refute

```text
det(D_S) + (1/2) t_S^T adj(D_S) conjugate(t_S) >= 0
```

on the complex orthonormal frame manifold.  Prioritize `2 x 2` minors beyond the crossed scalar block, then `3 x 3` Schur/adjugate patterns.

4. Exact zero-mode classification.
   Replace numerical zero-mode bases by symbolic orbit/equality-family parametrizations at the `diag_difference` and `product_projection` controls.  A local theorem still needs a global patching argument.

5. Bridge audit.
   If scalar PAL is proven, immediately audit the quantifier bridge to full PCL/CLAIM.  Do not declare CLAIM-0001 from a scalar minor alone.

6. Counterexample route.
   If proof stalls, continue targeted search for a certified rank-at-most-two `C` with positive corrected gap.  Any candidate must include exact rank verification and corrected partial-trace recomputation.

## Final skeptic decision

```text
LOOP-0009: FAIL-CLOSED
CLAIM-0001: NOT PROVED
COUNTEREXAMPLE: NOT FOUND
PROMOTION: REJECTED
```

LOOP-0009 made real progress in identifying the correct mixed off-diagonal algebra and in killing a tempting false Cauchy/Plucker proof route.  It did not close the claim.
