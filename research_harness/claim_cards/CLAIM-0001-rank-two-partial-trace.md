# CLAIM-0001: Rank-Two Partial-Trace Inequality

status: proof_gap_found
last_updated: 2026-06-03

## Statement

Let `C in M_4(C) tensor M_4(C)` and assume `rank(C) <= 2`. Then

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2
  <= 2 ||C||_F^2 + (1/2) |tr C|^2.
```

Equivalently, `gap(C) <= 0`, where

```text
gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2 ||C||_F^2 - (1/2) |tr C|^2.
```

## Mathematical context

This claim is recorded in the existing repo as the missing bridge for the Kronecker-sum singular-value problem.

Existing file pointers:

- `problem_statement_aristotle/co_mathematician/COORDINATOR_REPORT_2026-05-09.md`
- `problem_statement_aristotle/co_mathematician/workstreams/05_partial_trace_inequality.md`
- `problem_statement_aristotle/co_mathematician/scripts/check_partial_trace_ineq.py`
- `partial_trace_inequality_needed_for_sv_bound.tex`
- `trace_inequality/rank_two_partial_trace_proof.tex`

## Assumptions

- Complex matrices.
- Tensor factors are both dimension 4.
- `C` is an arbitrary rank-at-most-two operator on `C^4 tensor C^4`.
- Frobenius/Hilbert-Schmidt norm.
- Standard, unnormalized partial traces.

## Explicit non-assumptions

- `C` need not be Hermitian.
- `C` need not be normal.
- `C` need not be positive semidefinite.
- `C` is not assumed to be a vector state.
- The rank constraint is not convex and must not be handled via naive convexity.

## Known sharpness/equality witness

```text
C = (1/sqrt(2)) ( |0,0><0,0| - |1,1><1,1| ).
```

Then

```text
rank(C) = 2,
||C||_F^2 = 1,
tr(C) = 0,
tr_1(C) = tr_2(C) = (1/sqrt(2)) diag(1, -1, 0, 0),
gap(C) = 0.
```

Therefore the constant is sharp for this formulation if the inequality is true.

LOOP-0001 found a second sharp rank-two equality family:

```text
C = (P_2 tensor |0><0|)/sqrt(2),    P_2 = diag(1,1,0,0).
```

Then

```text
rank(C) = 2,
||C||_F^2 = 1,
||tr_1 C||_F^2 = 2,
||tr_2 C||_F^2 = 1,
|tr C|^2 = 2,
gap(C) = 0.
```

## Existing evidence

Numerical evidence from the existing workstream:

- Random rank-one/rank-two sampling found no positive gap.
- Local optimization over `C = U V^*` converged to equality within roundoff.
- Seeds 1, 2, and 3 optimized to gaps around `-4e-15` to `-7e-15`.

Evidence level: numerical support only, not proof.

LOOP-0001 evidence:

- Corrected the ordinary-rank SVD/vector-factorization reduction. Writing
  `C=sum_i s_i |x_i><y_i|` with `i <= 2` and reshaping `x_i,y_i` into matrices
  `X_i,Y_i`, the partial traces become `tr_2(|x_i><y_i|)=X_iY_i^*` and
  `tr_1(|x_i><y_i|)=X_i^*Y_i`.
- The claim was first reduced to a proposed two-pair contraction lemma for the
  reshaped singular-vector matrices, called `Lemma M` in
  `research_harness/adversarial_reviews/LOOP-0001/proposer_factorization.md`.
- LOOP-0002 refuted Lemma M as stated: `X_1=Y_1=E_00`, `X_2=E_01`,
  `Y_2=iE_01` gives `H=[[3/2,-3i/2],[3i/2,3/2]]` and `eig(H)=[0,3]`, so
  the fixed-gauge matrix claim `H <= 2I_2` is false.
- The Lemma M refutation does not refute CLAIM-0001: after SVD phase absorption,
  the associated rank-two operator is an equality case to numerical precision,
  not a positive-gap counterexample.
- Exact stronger-variant refutations were found: coefficient `alpha < 1/2` is
  false at rank 2, and the same `alpha=1/2` inequality is false at rank 3.

## Current proof status

No accepted proof.

LOOP-0001 status: proof gap was localized to a proposed two-pair contraction
lemma called Lemma M.

LOOP-0002 status: Lemma M as stated is refuted. The refutation does not refute
CLAIM-0001, because the false statement controlled arbitrary complex
coefficients in a fixed SVD gauge, whereas the original SVD reduction uses
nonnegative real singular coefficients with phase freedom in the singular
vectors. Therefore CLAIM-0001 remains open with no accepted proof and no known
counterexample from LOOP-0002.

Known rejected/incomplete routes:

- Normal-matrix density route is false.
- Corrected polarization calculation does not prove this claim.
- Main Lean theorem still has `sorry`.

## Open attack surfaces

1. Rank-factorization proof via `C = U V^*`, `U,V in C^{16 x r}`, `r <= 2`.
2. SVD proof via `C = s_1 |x_1><y_1| + s_2 |x_2><y_2|`.
3. Operator-Schmidt analysis of `x_i` and `y_i`.
4. Equality-family classification.
5. Refutation of stronger variants to identify why the exact constants/rank matter.
6. Determine whether the Kronecker-sum target needs this full inequality or only a weaker projected form.
7. Formulate and prove/disprove a phase-aware replacement for the refuted
   LOOP-0001 Lemma M / determinant bound, using nonnegative singular
   coefficients and SVD gauge freedom.
8. Search directly for positive `gap(C)` over rank-two `C`, independently of the
   refuted fixed-gauge matrix inequality.

## Promotion gates

To promote beyond `conjectural`, require:

- a written proof attempt with no hidden Hermitian/positive/normal assumptions;
- a skeptic report identifying and resolving all nontrivial gaps;
- numerical checks of any intermediate strengthened lemmas;
- a derivation note if the proof survives;
- formalization targets for stable algebraic lemmas.

## Adversarial history

- LOOP-0001 completed: `research_harness/adversarial_reviews/LOOP-0001/`.
- LOOP-0002 completed: `research_harness/adversarial_reviews/LOOP-0002/`.
  Lemma M as stated was refuted; CLAIM-0001 remains open/fail-closed.
- LOOP-0003 completed: `research_harness/adversarial_reviews/LOOP-0003/`.
  PAL was isolated as the current unproved phase-aware bottleneck; direct search found no robust positive gap.
- LOOP-0004 completed: `research_harness/adversarial_reviews/LOOP-0004/`.
  PAL was sharpened to a determinant target, no PAL violation was found, and PCL was introduced as an equivalent support-compression formulation.
- LOOP-0005 completed: `research_harness/adversarial_reviews/LOOP-0005/`.
  PCL was expressed as an explicit 4-by-4 compression matrix; numerical eigenvalue searches found no robust positive eigenvalue; proof/SOS remains open.
- LOOP-0006 completed: `research_harness/adversarial_reviews/LOOP-0006/`.
  The crossed 2-by-2 PCL minor was isolated as the next sharp symbolic target; PAL/PCL/CLAIM equivalence was clarified; corrected structured search found no robust positive eigenvalue.
- LOOP-0007 completed: `research_harness/adversarial_reviews/LOOP-0007/`.
  The crossed PCL minor was identified exactly with the phase-aware PAL determinant slice; the trace rank-one update determinant identity was recorded; corrected original-gap searches found no positive counterexample.
- LOOP-0008 completed: `research_harness/adversarial_reviews/LOOP-0008/`.
  Scalar certificate, tangent/equality, and full-PCL search lanes produced no proof or counterexample; naive diagonal-wedge polarization was blocked, equality controls were numerically stationary with negative-semidefinite tangent second variation, and full PCL searches found no robust violation.


## LOOP-0003 update

LOOP-0003 did not prove or refute CLAIM-0001. A direct numerical search over
rank-constrained factorizations `C=UV^*`, `U,V in C^{16xr}`, found no robust
positive gap: the best rank-two value was `8.881784094140483e-16`, below the
`1e-10` positivity threshold and consistent with equality-roundoff. The rank-one
search peaked at approximately `-0.5`.

The loop replaced the refuted fixed-gauge Lemma M target with the phase-aware
scalar candidate PAL. For SVD data `X_i,Y_i` with Hilbert-Schmidt orthonormal
two-frames, define `L_i=X_iY_i^*`, `R_i=X_i^*Y_i`, `t_i=tr(X_i^*Y_i)`,
`a=<L_1,L_2>`, `b=<R_1,R_2>-(1/2)conjugate(t_1)t_2`, and
`D_i=2-||L_i||_F^2-||R_i||_F^2+(1/2)|t_i|^2`. The candidate lemma is
`|a+conjugate(b)|^2 <= D_1D_2`. PAL would imply CLAIM-0001 by the rank-two SVD
route, and it survived LOOP-0003 random/sparse numerical tests, but it remains
unproved.

LOOP-0003 also recorded partial equality-family information: product-type
rank-two equality and traceless two-product-atom equality are distinct visible
mechanisms; the LOOP-0002 phase-absorbed example belongs to the product-type
equality family. This is not a complete classification.

Current bottleneck: prove or refute PAL, or supply an alternative complete proof
of CLAIM-0001 / robust rank-two positive-gap counterexample.


## LOOP-0004 update

LOOP-0004 did not prove or refute CLAIM-0001. The phase-aware scalar PAL target
from LOOP-0003 was sharpened to an exact determinant formulation. For
orthonormal two-frames `X_i,Y_i`, PAL is equivalent to positivity of the
2-by-2 Hermitian matrix

```text
K^PAL = [[D_1, -z],[-conjugate(z), D_2]],
z = <X_1Y_1^*,X_2Y_2^*> + conjugate(<X_1^*Y_1,X_2^*Y_2>)
    - (1/2)tr(X_1^*Y_1)conjugate(tr(X_2^*Y_2)).
```

The determinant inequality `D_1D_2-|z|^2 >= 0` remains unproved. Sparse
matrix-unit enumeration and floating-point random/BFGS searches found no PAL
violation, only equality or near-equality. The proof lane also found that a
natural all-frame `m>=3` PSD kernel extension is false, so any proof must use
two-frame/determinant-specific structure.

LOOP-0004 also introduced the Projected Compression Lemma (PCL): for every pair
of rank-two support projections `P,Q` on `C^4 tensor C^4`, the quadratic-form
operator

```text
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I
```

should be negative semidefinite on `Hom(QH,PH)={C:C=PCQ}`. PCL is exactly
equivalent to CLAIM-0001, not a proof or a strengthening. Its universal
compression negativity remains open.

Fail-closed verdict remains: no accepted proof and no accepted rank-two
positive-gap counterexample. Current bottleneck: prove PAL or PCL, or produce a
certified rank-two positive-gap counterexample.


## LOOP-0005 update

LOOP-0005 did not prove or refute CLAIM-0001. It attacked the Projected
Compression Lemma (PCL), the exact support-compression reformulation introduced
in LOOP-0004.

For orthonormal two-frames `p_alpha,q_beta` in `H=C^4 tensor C^4`, with
`E_{alpha beta}=|p_alpha><q_beta|`, the PCL compression matrix is

```text
K_{alpha beta,gamma delta}
 = <tr_1 E_{alpha beta}, tr_1 E_{gamma delta}>
 + <tr_2 E_{alpha beta}, tr_2 E_{gamma delta}>
 - (1/2)conjugate(tr E_{alpha beta}) tr E_{gamma delta}
 - 2 delta_{alpha gamma} delta_{beta delta}.
```

Equivalently, `K = Gram({A_ab}) + Gram({B_ij}) - (1/2)vec(T)vec(T)^* - 2I_4`,
and PCL asks for `K <= 0` for every pair of rank-two support planes.

Numerical PCL compression searches found no robust positive eigenvalue. Equality
regressions reproduced the known sharp spectra `[-2,-2,-1,0]` and
`[-1,-1,-1,0]`; the main random/BFGS run had
`random_positive_count_tol_1e_10=0`, best optimized `lambda_max=-8.47e-14`, and
`positive_robust_tol_1e_8=false`.

The proof/SOS lane isolated the exact algebraic target
`M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0` on
`Gr(2,16) x Gr(2,16)`, but supplied no complete PSD/SOS certificate. Diagonal
wedge/SOS identities are useful but do not imply full `4 x 4` PSD. PCL remains
open/unproved and not refuted.

Fail-closed verdict remains: no accepted proof, no accepted rank-two
positive-gap counterexample, and no accepted bridge-defect. Current bottleneck:
prove PCL via a full Hermitian Gram/SOS or principal-minor certificate, prove the
PAL two-frame determinant inequality, or produce a certified rank-two
positive-gap counterexample.


## LOOP-0006 update

LOOP-0006 did not prove or refute CLAIM-0001. It attacked the equivalent PCL
formulation by symbolic certificate search, structured counterexample search,
and a PAL/PCL bridge audit.

The symbolic PCL lane confirmed diagonal wedge/SOS certificates for the `1 x 1`
principal minors of `M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V)`, but found no full
Hermitian Gram/SOS or all-principal-minor certificate. It also showed that the
overstrong contraction-defect route `D=2I-A-B >= 0` is false: in the product
equality case `eig(D)=[-1,1,1,1]`, while the trace rank-one update repairs the
bad direction and `eig(M)=[0,1,1,1]`. The sharp next symbolic target is the
crossed `2 x 2` principal minor `M_{11,11}M_{22,22}-|M_{11,22}|^2 >= 0`, but
this minor remains unproved and is not by itself sufficient for full PCL.

The structured PCL counterexample lane corrected a partial-trace convention error
that had produced spurious positives. With the corrected convention, equality
controls reproduced the known `K` spectra `[-1,-1,-1,0]` and `[-2,-2,-1,0]`;
structured search, equality perturbations, and BFGS optimization found no robust
positive eigenvalue. The main corrected run had `best overall lambda_max=0.0`,
`robust_positive=false`, and local optimization
`best lambda_max=-5.20317946714477e-13`, consistent with equality/roundoff. No
certified positive-gap rank-two counterexample was produced.

The PAL/PCL bridge lane identified the exact quantifier-level relation: PCL
implies PAL by taking the SVD-diagonal `2 x 2` principal submatrix, PAL implies
CLAIM-0001 by the rank-two SVD route, and CLAIM-0001 implies PCL by support
compression. Thus universal PAL, CLAIM-0001, and PCL are equivalent
formulations. However, one fixed PAL block is only a principal slice of a fixed
PCL matrix; it is not a full fixed-basis `4 x 4` PSD certificate.

Fail-closed verdict remains: no accepted proof, no accepted rank-two
positive-gap counterexample, and no accepted bridge-defect. Current bottleneck:
prove PCL via a full Hermitian Gram/SOS, rank-one-update, or all-principal-minor
certificate; prove universal phase-aware PAL; or produce a certified rank-two
positive-gap counterexample.


## LOOP-0007 update

LOOP-0007 did not prove or refute CLAIM-0001. It sharpened the LOOP-0006 crossed
PCL minor into an exact equivalence with the phase-aware PAL determinant slice and
confirmed that the trace rank-one update is essential already at this scalar
level.

The PCL crossed-minor lane derived the exact rank-one-update determinant identity
`det M_S = det D_S + (1/2) u_S^* adj(D_S) u_S`, where `D=2I-A-B`. The product
equality family has `det D_S=-1` while the trace update repairs the block to
`det M_S=0`, so contraction-defect-only proofs are false.

The PAL determinant lane decomposed `K^PAL = K_L + K_R + T_T` and reduced the
problem to `det(K_L+K_R+T_T) >= 0`. This is useful structure but not a proof.
It also reinforced the false-route guardrails: separated left/right
Cauchy-Schwarz routes fail, all-frame `m>=3` PSD promotion is false, and
fixed-gauge arbitrary-complex-coefficient strengthening remains false.

The certified search lane used the original corrected partial-trace convention
and found no positive original normalized gap: `20000` random rank-two samples had
best normalized gap `-1.2143877928448128`, coordinate two-unit scan best was
`0.0`, equality perturbation best was `-7.779413143726018e-10`, and
`robust_positive_gap_found=false`.

Fail-closed verdict remains: no accepted proof, no accepted rank-two positive-gap
counterexample, and no accepted bridge-defect. Current immediate bottleneck:
prove the coupled scalar PAL/crossed-PCL-minor defect with the trace update
retained, then extend to full PCL, or produce a certified positive-gap rank-two
counterexample.


## LOOP-0008 update

LOOP-0008 did not prove or refute CLAIM-0001. It attacked three subtargets: the
coupled scalar PAL/crossed-PCL determinant, tangent/equality behavior at two
sharp equality controls, and the full `4 x 4` PCL compression matrix.

The scalar certificate lane verified trace-update determinant bookkeeping and
one-pair diagonal wedge/SOS identities to roundoff, but found no scalar proof. It
also found that naive polarization of the one-pair diagonal wedge identities does
not reproduce the crossed off-diagonal PAL/PCL entries; the maximum mismatch in
the probe was `0.295153648209067`. Coordinate enumeration again confirmed that
`det D_S >= 0` is false: `min_det_D=-1.0`, with `48` negative coordinate cases,
while the trace update repairs equality cases.

The tangent/equality lane found both known equality controls stationary for the
original corrected gap on the rank-two/unit-Frobenius tangent space. The projected
first variation was `0.0` for both controls, the maximum tangent second-variation
eigenvalue was `0.0` for both controls, and positive second-variation eigenvalue
counts were zero. Near-zero real tangent mode counts were `9` for the diagonal
difference control and `13` for the product-projection control. This is local
numerical evidence only, not an equality classification or proof.

The full PCL lane attacked the full matrix `M=2I_4-A-B+(1/2)T`, converted
dangerous compression eigenvectors back to original `C=PCQ`, and checked the
original gap. It found no robust violation: coordinate worst `lambda_min(M)=0.0`,
random worst `lambda_min(M)=1.060359499717052`, optimized worst
`lambda_min(M)=3.2507330161017243e-13`, worst converted original normalized gap
`2.2204460492503126e-16` (roundoff/equality), and
`robust_pcl_violation_found=false`. No full PCL certificate was found.

Fail-closed verdict remains: no accepted proof, no accepted rank-two positive-gap
counterexample, and no accepted bridge defect. The current bottleneck is a
trace-coupled full-PCL certificate. A scalar PAL/crossed-minor proof remains a
key subtarget but is insufficient for CLAIM-0001 unless extended to full
PAL/PCL/CLAIM with all quantifiers intact.

## LOOP-0009 update

LOOP-0009 did not prove or refute CLAIM-0001. It continued the automatic
adversarial loop with three repaired/completed lanes: mixed Plucker identity,
zero-mode classification diagnostics, and principal-minor/rank-one-update
diagnostics.

The mixed Plucker lane found a genuinely mixed two-frame identity for the crossed
PAL/PCL off-diagonal entry, checked to roundoff with maximum random identity error
`8.441528768080324e-17`. This repairs the LOOP-0008 same-pair polarization
obstruction at the off-diagonal bookkeeping level. However, the direct mixed
Cauchy/Gram norm-domination route fails on the actual orthonormal frame
constraint manifold: the lane found `min(D_1-N_12)=-1.5` and
`min(D_2-N_21)=-1.5` in sparse coordinate tests. Thus the simplest mixed-vector
SOS route is rejected.

The zero-mode lane confirmed the LOOP-0008 local tangent diagnostics at the known
equality controls: diagonal-difference zero-mode count `9`, product-projection
zero-mode count `13`, and no positive Hessian directions in the numerical real
unit-sphere tangent model. This remains local numerical evidence only, not an
exact equality-manifold classification or global proof.

The principal-minor lane verified the correct trace rank-one-update determinant
shape for every principal subset,

```text
det(D_S + (1/2)conjugate(t_S)t_S^T)
 = det(D_S) + (1/2)t_S^T adj(D_S)conjugate(t_S),
```

with maximum checked identity error `4.440892108477151e-15`. Coordinate two-plane
and 2000-random-frame tests found no negative principal minors, but this is not a
universal nonnegativity proof. The lane reinforces that future principal-minor
proofs must retain the trace-coupled update; `D_S >= 0` or `det(D_S) >= 0`
shortcuts remain false/rejected.

Skeptic and auditor reviews both recorded LOOP-0009 as fail-closed: no complete
proof, no certified rank-two positive-gap counterexample, and no accepted bridge
defect. The current bottleneck remains a trace-coupled full-PCL certificate, a
scalar PAL/crossed-minor proof plus complete extension to CLAIM/PCL, or a
certified rank-two positive-gap counterexample.

## LOOP-0010 update

LOOP-0010 did not prove or refute CLAIM-0001. It attacked the post-LOOP-0009
bottleneck through scalar crossed-minor determinant bookkeeping, a full-PCL
coordinate principal-minor atlas, and local equality zero-mode classification.

The scalar lane recorded the determinant split

```text
Delta = D1 D2 - |m|^2
      = (N12 N21 - |m|^2) - (N12 N21 - D1 D2),
```

where the first term is mixed Gram/Cauchy slack and the second is the exchange
penalty from comparing mixed off-diagonal Plucker vectors with same-pair diagonal
defects. The natural refined shortcut `D1D2 >= N12N21` is false: coordinate tests
found `min(D1D2-N12N21)=-3.75`, with `6848` coordinate cases having positive
exchange penalty. No scalar violation was found (`coordinate_min_delta=0.0`,
random minimum `1.8376015909653387`, local minimum about `3.96e-13`).

The full-PCL coordinate atlas checked all coordinate rank-two support pairs and
all principal minors. No coordinate `det(M_S)` was negative, but `D` alone again
failed as a certificate target: negative `det(D_S)` counts were `48`, `96`, and
`48` for minor sizes `2`, `3`, and `4`, each with minimum `-1.0`. The trace
rank-one update repaired these finite coordinate cases. This is a finite atlas,
not a proof over arbitrary Grassmannian frames.

The zero-mode lane compared numerical Hessian zero spaces with explicit
phase/product-unitary/equality candidate directions. Product-projection zero
modes were fully classified numerically (`13/13`), but the diagonal-difference
control retained `4` unclassified zero dimensions out of `9`. Equality analysis
therefore remains incomplete and local.

Skeptic and auditor reviews both recorded LOOP-0010 as fail-closed: no complete
proof, no certified positive-gap rank-two counterexample, and no accepted bridge
defect.

## LOOP-0011 update

LOOP-0011 did not prove or refute CLAIM-0001. It continued from the LOOP-0010
scalar slack/exchange formulation, full-PCL coordinate atlas, and incomplete
diagonal-difference zero-mode classification.

The scalar lane organized the crossed minor as

```text
Delta = GramSlack - ExchangePenalty,
GramSlack = N12 N21 - |m|^2,
ExchangePenalty = N12 N21 - D1D2,
```

or, when `N12N21>0`, as the ratio inequality
`q=D1D2/(N12N21) >= rho=|m|^2/(N12N21)`. Coordinate equality cases reach
penalty/slack ratio `1`, with `264` coordinate equality cases in `3` signatures;
random tests were away from the boundary (`random_max_ratio=0.3025637369333136`),
and local optimization moved back toward equality (`ratio≈0.999997`) without a
violation. This sharpens the scalar target but gives no proof.

The full-PCL Schur lane found no negative `M` eigenvalue, principal minor, or
Schur split in the tested coordinate/random diagnostics, but again showed that
D-only Schur/determinant routes are false: coordinate `D` had `48` negative
minimum-eigenvalue cases, negative `det(D_S)` counts `48,96,48` for sizes
`2,3,4`, and `144` negative D-Schur splits, all requiring the trace update.

The diagonal-difference zero-mode lane resolved the four LOOP-0010 residual local
zero modes numerically: expanded active support-plane candidates classified all
`9/9` diagonal-difference zero modes with residual about `3.19e-16`; the prior
four-dimensional residual lay in this expanded span with residual about
`7.85e-17`. Together with the earlier product-projection result, the two main
local equality controls now have numerical zero-mode classifications. This is
still local floating-point tangent evidence, not a global proof or complete
equality theorem.

Skeptic and auditor reviews both recorded LOOP-0011 as fail-closed: no complete
proof, no certified positive-gap rank-two counterexample, and no accepted bridge
defect.


## Co-mathematician mode migration

After LOOP-0011, the research harness was migrated from a bare adversarial
cron-loop into a co-mathematician-style workspace inspired by arXiv:2605.06651.
The active state is now split across `PROJECT_STATE.md`, `GOALS.md`,
`dashboard.md`, `uncertainty_ledger.md`, `failed_explorations.md`, persistent
workstreams under `research_harness/workstreams/`, and a scaffolded working
paper under `research_harness/working_paper/`.

This migration does not change the mathematical verdict. CLAIM-0001 remains
open/fail-closed. The migration changes loop organization: future loops should
advance named workstreams, update uncertainty and failed-route ledgers, preserve
progressive-disclosure dashboard state, and escalate repeated stalls to the user
instead of silently grinding fixed lanes.

## LOOP-0012 update

LOOP-0012 did not prove or refute CLAIM-0001. It ran as the first full
co-mathematician workspace loop after migration and advanced scalar, full-PCL,
equality, literature, and working-paper workstreams.

The scalar/equality lane re-ran the scalar slack diagnostics with seed `12012` and
organized coordinate ratio-1/equality cases into three exact finite signatures:
same row/column identical supports (`48` cases), same-row/same-column parallel
disjoint translates (`144` cases), and diagonal identical supports (`72` cases).
The run again found no scalar violation (`local_min_delta≈6.63e-12`) and showed
local optimization approaching equality (`ratio≈0.9999999898468404`). The key
lesson is that equality can have positive `GramSlack` exactly matched by positive
`ExchangePenalty`, so product-domination shortcuts remain false.

The full-PCL lane created `LOOP-0012_trace_coupled_pivot_candidate.py` and logs.
It isolated the admissible trace-coupled Schur/rank-one-update object
`S_R(M)=M_RR-c c^*/m` with `m=M_ii=D_ii+(1/2)|t_i|^2` and
`c=M_Ri=D_Ri+(1/2)conj(t_R)t_i`. Coordinate diagnostics over `14400` support
pairs had no negative `M` eigenvalue and no no-pivot-order case for `M`, while
`D` had `48` negative-eigenvalue cases and `120` no-nonnegative-pivot-order cases.
Thus D-only pivots are refuted as a proof route, but no full certificate was
found.

The literature lane produced a local-source related-inequality guardrail map and
found no importable external theorem with exact hypotheses. Network retrieval was
unavailable, so external bibliographic anchors still require verification. The
working-paper scaffold was updated with provenance-rich literature guardrail text.

Skeptic and auditor reviews recorded LOOP-0012 as fail-closed: no complete proof,
no certified positive-gap rank-two counterexample, and no accepted bridge defect.

## Current verdict

Fail-closed: no accepted proof and no accepted counterexample for CLAIM-0001.
The LOOP-0001 bottleneck Lemma M is refuted as stated. Universal PAL, CLAIM-0001,
and PCL are now understood as equivalent formulations, but no formulation is
proved. LOOP-0012 sharpened the scalar bottleneck with exact coordinate
ratio-1/equality signatures and sharpened the full-PCL bottleneck to a
trace-coupled Schur/rank-one-update certificate target, while reinforcing that
full-PCL proofs must retain the trace rank-one update and cannot use D-only
pivots, determinant, or Schur routes. The current proof gap is a symbolic mixed
Plucker/Gram/SOS certificate for `GramSlack >= ExchangePenalty`, a full-PCL
Hermitian Gram/SOS/Schur/rank-one-update/all-principal-minor certificate for `M`,
an exact global equality-family analysis that can be used in a proof, verified
literature with exact hypotheses, or a certified rank-two positive-gap
counterexample.
## LOOP-0013 update

LOOP-0013 did not prove or refute CLAIM-0001. It advanced scalar/equality, full-PCL, literature, and working-paper workstreams and then opened a human-steering escalation because the central symbolic certificate bottleneck persists.

The scalar/equality lane promoted the LOOP-0012 coordinate ratio-1 signatures into exact restricted parametrized equality families. On representative row/column/diagonal charts it verified `Delta=0` with positive `GramSlack=ExchangePenalty` (constants `3/4`, `3`, and `15/4`). This materially sharpens equality guardrails but is not a global equality theorem and not a universal mixed Plucker/Gram/SOS certificate.

The full-PCL lane separated the proved algebraic determinant-update identity

```text
det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S)
```

from the still-missing nonnegativity proof. Coordinate/random diagnostics again found no `M` violation and again refuted D-only routes (`D_negative_eig_count=48`, `D_no_nonnegative_pivot_order_count=120`), but no PSD certificate for the full trace-coupled `M` was produced.

The literature lane successfully retrieved arXiv `2507.18278` and verified source hypotheses. The closest sharp trace-corrected theorem is normal-only, and the source explicitly leaves the beyond-normal rank-two case open; the arbitrary-rank-two theorem gives only the weaker `3||C||_F^2` fallback. Thus no external theorem was imported as a proof and no bridge defect was found.

Skeptic and auditor reviews recorded LOOP-0013 as fail-closed: no complete proof, no certified positive-gap rank-two counterexample, and no accepted bridge defect. Autonomous work is now paused pending `ESC-0001` human steering.
