# LOOP-0004 Skeptic Report

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
pal_status: unproved_not_refuted
pcl_status: exact_reformulation_unproved
reviewed:
  - research_harness/adversarial_reviews/LOOP-0004/pal_proof_lane.md
  - research_harness/adversarial_reviews/LOOP-0004/pal_refutation_search.md
  - research_harness/adversarial_reviews/LOOP-0004/alternative_derivation_lane.md
  - research_harness/adversarial_reviews/LOOP-0003/skeptic.md
  - research_harness/adversarial_reviews/LOOP-0003/auditor.md

## Executive verdict

Fail closed.

LOOP-0004 did not prove CLAIM-0001 and did not refute it. The proof lane correctly tracks the right-singular-vector phase law and gives a useful exact determinant formulation of PAL, but that formulation is only a reduction: the remaining statement is precisely the unproved PAL determinant inequality. The refutation/search lane found no robust PAL violation; it found exact sparse equality cases and floating-point near-equality, which are negative evidence only. The alternative projected-compression lemma (PCL) is a clean and, subject to the stated rank/support conventions, exact restatement of CLAIM-0001, but it is not a proof because the required compression negativity is still open.

Current status:

```text
CLAIM-0001: open / fail_closed / no proof / no counterexample
PAL: exact phase-aware SVD bottleneck; unproved; not numerically refuted
PCL: exact support-compression reformulation of CLAIM-0001; unproved
Fixed-gauge H <= 2I style matrix lemma: still refuted/obsolete
```

## 1. PAL proof lane audit

### 1.1 Phase and conjugation bookkeeping

The phase law in the proof lane is consistent with the convention

```text
<A,B>_F = tr(A^*B)
```

and with right singular-vector phase changes `Y_i -> eta_i Y_i`:

```text
L_i = X_iY_i^*       -> conjugate(eta_i)L_i
R_i = X_i^*Y_i       -> eta_i R_i
t_i = tr(X_i^*Y_i)  -> eta_i t_i
```

Thus, for

```text
a = <L_1,L_2>_F,
b = <R_1,R_2>_F - (1/2)conjugate(t_1)t_2,
```

one gets

```text
H_12' = e^{i delta} a + e^{-i delta} b,
max_delta Re(H_12') = |a + conjugate(b)|.
```

I do not see a sign or conjugation error in this derivation. In particular, the PAL cross term is not the refuted fixed-gauge quantity `a+b`; it is the phase-optimized quantity `a+conjugate(b)`.

### 1.2 Determinant-defect formulation

The lane defines

```text
z = a + conjugate(b)
  = <L_1,L_2>_F + conjugate(<R_1,R_2>_F) - (1/2)t_1 conjugate(t_2)
```

and

```text
K^PAL_ij = 2 delta_ij
           - <L_i,L_j>_F
           - conjugate(<R_i,R_j>_F)
           + (1/2)t_i conjugate(t_j).
```

This gives

```text
K^PAL = [[D_1, -z],[-conjugate(z), D_2]],
det K^PAL = D_1D_2 - |z|^2.
```

The diagonal terms are nonnegative by the one-pair contraction estimates
`||XY^*||_F <= 1` and `||X^*Y||_F <= 1` for unit Frobenius `X,Y`. Therefore, for this 2 by 2 matrix, PAL is equivalent to `K^PAL >= 0`.

This is a correct reformulation of PAL. It is not a proof of PAL. The missing step is still exactly the global assertion that this 2 by 2 phase-aware kernel is PSD for all Hilbert-Schmidt orthonormal two-frames.

### 1.3 Hidden assumptions / overclaims

Accepted:

- No Hermitian, normal, positive, or diagonal assumption on `C` is used in the PAL statement.
- The phase-aware replacement is the right way to avoid the LOOP-0002 fixed-gauge failure.
- The 3-frame matrix-unit obstruction is a useful warning that a naive all-frame PSD kernel proof is false.

Caveats:

- Any language suggesting the proof lane proves PAL should be rejected. It proves an exact equivalence/reduction: PAL iff the displayed 2 by 2 determinant is nonnegative.
- The obstruction to an `m >= 3` PSD kernel does not itself prove the 2-frame case; it only rules out one overstrong route.
- Matrix-unit equality checks are regression tests, not certificates for arbitrary non-sparse complex frames.

## 2. PAL refutation/search lane audit

The search lane reports:

```text
matrix-unit cases checked: 57600
equality cases: 528
best matrix-unit violation: 0.0
random trials: 8000
best random violation: -1.549087158428483
best optimized violation: -6.211697822777751e-14
```

I inspected the script and the recorded JSON/stdout logs. The implementation uses the same PAL definitions as the proof lane:

```text
violation = |a + conjugate(b)|^2 - D_1D_2.
```

Skeptical interpretation:

- No robust positive PAL violation was found.
- The matrix-unit sweep found equality, not a counterexample.
- The BFGS result `-6.2e-14` is roundoff-scale negative and should be read as near-equality, not as a violation or certification.
- The optimizer did not report success for the best restart, so the optimized point should be treated only as heuristic evidence.
- The random search is finite and local/noncertifying; it cannot prove PAL.
- The coarse original-gap conversion scan for the best PAL near-equality frame is not a proof and is not needed for a no-refutation conclusion.

Conclusion: the refutation lane supplies useful negative evidence and equality data, but no robust violation of PAL and no rank-two positive-gap counterexample to CLAIM-0001.

## 3. Alternative projected-compression lemma audit

### 3.1 Equivalence check

The alternative lane defines

```text
q(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
       - (1/2)|tr C|^2 - 2||C||_F^2,
```

so `q(C)` is the original CLAIM-0001 gap. It then defines PCL as:

```text
For every rank-two pair of orthogonal projections P,Q on H = C^4 tensor C^4,
q(C) <= 0 for every C with C = P C Q.
```

This is exactly equivalent to CLAIM-0001 as a support-compression statement:

- If PCL holds and `rank(C) <= 2`, take `P` as the range projection of `C` and `Q` as the range projection of `C^*`; enlarge either support to rank two if necessary. Then `C=PCQ`, so PCL gives `q(C)<=0`.
- If CLAIM-0001 holds and `C=PCQ` with `rank(P)=rank(Q)=2`, then the ordinary matrix rank of `C` is at most two, so CLAIM-0001 gives `q(C)<=0` on the whole block `Hom(QH,PH)`.

Thus PCL is neither weaker nor stronger than the original rank-two claim; it is an exact reformulation.

### 3.2 What PCL proves and does not prove

PCL currently proves no new inequality unless the universal compression negativity is established. It replaces the scalar PAL bottleneck by a 4 by 4 Hermitian compression matrix over pairs of two-planes in `Gr(2,16)`, which is cleaner and phase-free, but still open.

Useful aspects:

- It removes SVD coefficient-cone and right-phase bookkeeping.
- It tests the full block `Hom(QH,PH)`, so it is naturally invariant under support-basis changes.
- It gives a directly checkable finite-dimensional matrix condition for each fixed pair `(P,Q)`.

Caveats:

- The statement depends on the same unnormalized partial-trace conventions as CLAIM-0001; any normalization change would change `Phi`.
- The adjoint formulas `tr_1^*(A)=I_4 tensor A`, `tr_2^*(B)=B tensor I_4`, and `tr^*(z)=zI_16` are convention-dependent but acceptable under the stated unnormalized convention.
- The numerical PCL smoke check is only a sanity check. Random negative largest eigenvalues and the LOOP-0002 example eigenvalues `[-1,-1,-1,0]` do not certify all pairs of planes.
- Equality examples imply that any proof must allow nontrivial kernel; strict negativity is false.

## 4. Relationship between PAL, PCL, and CLAIM-0001

PAL is the natural phase-aware scalar condition arising from a two-term SVD route. PCL is a phase-free support-compression restatement of the original rank condition. PCL is exactly equivalent to CLAIM-0001. PAL appears to be an exact universal bottleneck for the SVD route and would imply CLAIM-0001, but LOOP-0004 does not prove PAL.

For repository status purposes, neither PAL nor PCL should be promoted to theorem status. They are open targets:

```text
Proving PAL would close CLAIM-0001 via the SVD route.
Proving PCL would close CLAIM-0001 directly.
Refuting either with a robust positive witness would likely refute CLAIM-0001, but would still require reconstructing C and checking the original gap.
```

## 5. Blockers and next actions

Main blockers before any promotion:

1. Prove the exact PAL determinant inequality

```text
D_1D_2 - |a+conjugate(b)|^2 >= 0
```

for arbitrary Hilbert-Schmidt orthonormal two-frames in `M_4(C)`, or produce a robust violation.

2. If using PCL, prove that the compression of

```text
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I
```

to every `Hom(QH,PH)` with `rank(P)=rank(Q)=2` is negative semidefinite.

3. Avoid overstrong routes already known to fail: fixed-gauge complex PSD conditions and naive `m >= 3` all-frame PSD kernels.

4. Treat all numerical searches as heuristic unless they produce either interval/rational certification or a robust reconstructable original `C` with positive gap well above tolerance.

5. Preserve the equality cases as regression tests: product-projection equality, traceless two-product-atom equality, and the LOOP-0002 phase-absorbed equality case.

## Final fail-closed status

No LOOP-0004 artifact proves CLAIM-0001/PAL. No LOOP-0004 artifact refutes CLAIM-0001/PAL. The strongest outcomes are two useful open reformulations:

```text
PAL determinant form: exact phase-aware 2 by 2 scalar bottleneck, unproved.
PCL: exact Grassmannian/support-compression restatement of CLAIM-0001, unproved.
```

Final verdict: `fail_closed; CLAIM-0001 remains open`.
