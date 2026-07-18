# LOOP-0008 skeptic report

claim_focus: CLAIM-0001-rank-two-partial-trace
role: skeptic / adversarial review
verdict: fail_closed_no_success_condition_survives
reviewed:
- research_harness/status.json
- research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
- research_harness/adversarial_reviews/LOOP-0008/scalar_certificate_lane.md
- research_harness/adversarial_reviews/LOOP-0008/tangent_equality_lane.md
- research_harness/adversarial_reviews/LOOP-0008/full_pcl_search_lane.md
- research_harness/experiments/LOOP-0008_scalar_certificate_probe.py
- research_harness/experiments/LOOP-0008_tangent_equality_lane.py
- research_harness/experiments/LOOP-0008_full_pcl_search.py
- LOOP-0008 JSON/stdout logs

## Executive verdict

No LOOP-0008 success condition survives skeptical review.

LOOP-0008 produced useful guardrails, regressions, and negative evidence against several false proof routes, but it did not produce any of the required outcomes:

1. Complete proof of CLAIM-0001: no.
2. Certified rank-two positive-gap counterexample: no.
3. Accepted bridge defect showing that the current formulation/reduction is wrong: no.

The fail-closed status in the lane reports is appropriate. The current status should remain open/fail-closed.

The sharpest next bottleneck is no longer just the scalar crossed minor in isolation. The scalar PAL/crossed-PCL determinant is still a necessary immediate target, but success for CLAIM-0001 requires either:

- a trace-coupled certificate that extends from the crossed 2x2 slice to full 4x4 PCL PSD, or
- a direct full-PCL Hermitian Gram/SOS/Schur/principal-minor certificate retaining the trace rank-one update, or
- an explicit rank-at-most-two matrix C with rigorously certified positive original gap.

A scalar crossed-minor proof alone must not be promoted as a proof of CLAIM-0001 unless the extension to universal PAL/full PCL/CLAIM is also completed with all quantifiers intact.

## Global adversarial checks

### Partial-trace convention

The LOOP-0008 scripts state and implement the corrected convention

```text
tr_1(C)[a,b] = sum_i C[i,a,i,b]
tr_2(C)[i,j] = sum_a C[i,a,j,a].
```

For rank-one atoms `|vec(U)><vec(V)|`, the full-PCL script uses

```text
tr_1 = U^T conjugate(V)
tr_2 = U V^*
tr   = tr(V^* U),
```

which is consistent with row-major vectorization and the stated partial traces. The full-PCL script also converts worst compression eigenvectors back to explicit original matrices C and checks the identity `normalized_gap(C) + x^* M x = 0` to roundoff. This is a good convention regression.

Skeptical limitation: this is a floating-point consistency check, not an exact derivation certificate. It prevents an obvious convention leak in LOOP-0008, but it cannot certify the universal inequality.

### Trace rank-one update

LOOP-0008 correctly keeps the trace update in the scalar and full-PCL targets:

```text
M = D + (1/2) T,  D = 2I - A - B.
```

The product equality controls show `D` can be indefinite while `M` is repaired to PSD/equality. Therefore any proof route that drops the trace term, proves `D >= 0`, proves `det D_S >= 0`, or treats the trace term as an afterthought is invalid. LOOP-0008 did not make that promotion error.

Skeptical limitation: retaining the trace update in numerical probes is not a proof that every Schur complement/principal block remains repaired.

### Numerical evidence vs proof

All three lanes explicitly mark their evidence as numerical/probe/fail-closed. None of the lane writeups claims a complete proof. The reported positive-looking quantities near `1e-16` or `1e-13` are roundoff/equality scale and do not qualify as counterexamples.

No candidate matrix with robust positive original gap was exported and certified in high precision, interval arithmetic, or exact arithmetic. Therefore there is no counterexample success.

## Lane-by-lane skeptical review

## 1. Scalar certificate lane

Reviewed target:

```text
D_1 D_2 - |a + conjugate(b)|^2 >= 0,
```

equivalently the crossed PCL principal minor

```text
det M[{(1,1),(2,2)}] >= 0.
```

### What survives

The lane usefully records the exact determinant update form

```text
det(D_S + (1/2)u_Su_S^*)
= det D_S + (1/2)u_S^* adj(D_S) u_S,
```

and emphasizes that the mixed trace term is essential. The coordinate/product equality controls correctly expose the false route `det D_S >= 0` / `D_S >= 0`.

The lane also identifies a real obstruction to a tempting proof strategy: the one-pair row/column wedge SOS identities do not naively polarize into the crossed PAL/PCL off-diagonal entries. That is a useful negative result about a proof route.

### What does not survive promotion

The scalar inequality itself remains unproved. The lane found no Plucker, SOS, Gram, determinant, or exact algebraic certificate.

The random/local checks are not proof evidence. In particular:

- `5000` random samples are finite and floating-point.
- BFGS over a QR-projected parametrization is a heuristic and can miss boundary/structured cases.
- Coordinate two-plane enumeration is exact only for coordinate planes, not for all `Gr(2,16) x Gr(2,16)`.
- A large random positive margin for generic frames says little about sharp boundary/equality strata.

The negative result about naive diagonal-wedge polarization is not a bridge defect. It refutes one certificate route only; it does not refute PAL, PCL, or CLAIM-0001.

### Skeptic verdict for scalar lane

Fail closed. Useful guardrails and obstruction only. No scalar proof, no counterexample, no bridge defect.

## 2. Tangent/equality lane

Reviewed target: local analysis of the original gap near two known equality controls:

```text
C_diag = (|00><00| - |11><11|)/sqrt(2)
C_prod = (|00><00| + |10><10|)/sqrt(2).
```

### What survives

The lane checks the original gap, rank, partial traces, projected first variation, tangent quadratic spectrum, and finite-difference rank-two-retracted perturbations at two important sharp equality controls. It finds no positive first/second-order numerical direction and no random rank-two-retracted positive-gap candidate.

The tangent dimension count is consistent with the smooth rank-two matrix variety: complex dimension `2*16 + 16*2 - 2*2 = 60`; real unit-sphere tangent dimension `119` after removing the real radial direction.

### What does not survive promotion

This lane is local, floating-point, and limited to two visible equality controls. It does not prove CLAIM-0001 and does not even prove exact local maximality.

Specific limitations:

- The Hessian matrix is computed numerically; no exact eigenvalue certificate is supplied.
- Second-order constrained analysis on a curved rank-two variety can require control of second-order retraction/curvature terms, especially along zero modes. The finite-difference SVD retraction checks are useful regressions but not exact algebra.
- Zero modes are not classified. They may correspond to equality families, gauge/symmetry directions, numerical degeneracy, or directions requiring higher-order analysis.
- Local maximality at two equality families would not rule out positive gap elsewhere on the rank-two variety.
- The equality-family classification remains incomplete.

### Skeptic verdict for tangent lane

Fail closed. The lane provides evidence that the two known sharp controls are not obviously unstable, but it gives no global proof and no certified counterexample.

## 3. Full PCL/search lane

Reviewed target:

```text
M(U,V) = 2I_4 - A(U,V) - B(U,V) + (1/2)T(U,V) >= 0
```

for all two-dimensional support frames `U,V in C^16`.

### What survives

This is the strongest LOOP-0008 numerical regression lane because it attacks the full 4x4 PCL compression rather than only the crossed scalar slice. It also performs the right sign/convention check: a negative eigenvalue of `M` would be converted to an explicit `C = PCQ`, and the original corrected partial traces would be evaluated directly.

The lane reports no robust PCL violation in:

- equality/control supports,
- all coordinate two-plane support pairs,
- 3000 random frame pairs,
- 6 BFGS restarts.

The conversion identity error is reported at roundoff scale, so the implementation is internally consistent.

### What does not survive promotion

The full PCL PSD statement remains unproved. The lane supplies no symbolic certificate for:

- all 1x1, 2x2, 3x3 principal minors and the 4x4 determinant,
- a full Hermitian Gram/SOS representation,
- a Schur complement argument surviving indefinite `D`,
- a rank-one-update determinant proof for every principal block,
- an exact algebraic treatment on `Gr(2,16) x Gr(2,16)`.

The numerical search has the usual coverage limits:

- Coordinate planes are a tiny structured subset of the Grassmannian.
- Random frames mostly probe the interior and may miss sharp low-dimensional strata.
- QR-projected BFGS is nonconvex and not exhaustive.
- Principal-minor checks are numerical and finite; they are not symbolic nonnegativity certificates.
- Equality-scale values such as `2.2204460492503126e-16` positive normalized gap are roundoff, not certified violations.

### Skeptic verdict for full PCL/search lane

Fail closed. No full-PCL proof and no certified positive-gap rank-two matrix.

## Rejected promotion routes / guardrails

The following routes must remain rejected unless substantially repaired:

1. Fixed-gauge arbitrary-complex-coefficient strengthening.
   LOOP-0002 already refuted this. LOOP-0008 does not repair it.

2. All-frame PSD promotion.
   Prior loops found `m >= 3` all-frame PSD extensions false. LOOP-0008 does not provide a valid all-frame theorem.

3. Dropping or postponing the trace rank-one update.
   Product equality controls make `D=2I-A-B` indefinite. The trace update is not optional.

4. Diagonal wedge SOS polarization.
   LOOP-0008 found the naive polarization does not reproduce the crossed off-diagonal entries. This proof route is obstructed.

5. Scalar crossed-minor positivity promoted to full PCL.
   Even if the crossed 2x2 minor were proved, a full 4x4 Hermitian PSD proof requires all relevant principal minors or an equivalent full-matrix certificate. The scalar slice alone is not enough.

6. Tangent/local evidence promoted to global inequality.
   Local numerical stationarity/negative second variation at known equality controls does not exclude remote positive-gap examples.

7. Roundoff-scale positive gap promoted to counterexample.
   Values around `1e-16` are equality/roundoff and fail the certification threshold.

## Success-condition audit

### Complete proof?

No. No lane supplies a complete proof of PAL, full PCL, or the original rank-two inequality.

### Certified positive-gap rank-two counterexample?

No. No explicit matrix C with rank(C) <= 2 and rigorously positive original gap was produced. The full-PCL lane's worst reported positive value is roundoff-scale and explicitly classified as non-robust.

### Accepted bridge defect?

No. LOOP-0008 finds obstructions to proof strategies but no defect in the equivalence between CLAIM-0001, universal PAL, and PCL, and no defect in the corrected partial-trace convention.

## Sharpest next bottleneck

The sharpest bottleneck is a trace-coupled full-PCL certificate. The immediate scalar crossed PAL/PCL minor is still important, but it should be treated as a sub-bottleneck, not as sufficient for final success.

A viable next proof attempt should target one of the following fail-closed deliverables:

1. Full matrix certificate:
   derive an exact Hermitian Gram/SOS representation for
   `M(U,V)=2I-A-B+(1/2)T` on `Gr(2,16) x Gr(2,16)`.

2. Principal-minor certificate:
   prove all principal minors of the 4x4 Hermitian `M` are nonnegative, retaining the trace update in every principal block and Schur complement.

3. Trace-aware rank-one-update proof:
   use `M=D+(1/2)tt^*` without assuming `D>=0`, and handle the product equality case where `D` has eigenvalue `-1` but `M` is repaired to zero.

4. Counterexample certification path:
   if numerics find `gap(C)>0`, export the explicit 16x16 C and certify rank <= 2 and positive original gap using high precision, interval arithmetic, or exact algebra.

Until one of these is completed, CLAIM-0001 remains open/fail-closed.
