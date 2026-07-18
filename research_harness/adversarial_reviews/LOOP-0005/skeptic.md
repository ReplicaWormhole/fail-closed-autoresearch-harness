# LOOP-0005 Skeptic Review

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
pcl_status: exact_reformulation_open_unproved
success_verdict: no_success_condition_met
last_updated: 2026-06-03
reviewed:
  - research_harness/adversarial_reviews/LOOP-0005/pcl_normal_form_lane.md
  - research_harness/adversarial_reviews/LOOP-0005/pcl_numerical_eigen_lane.md
  - research_harness/adversarial_reviews/LOOP-0005/pcl_proof_sos_lane.md
  - research_harness/adversarial_reviews/LOOP-0004/auditor.md
  - research_harness/experiments/LOOP-0005_pcl_compression_search.py

## Executive verdict

Fail closed. LOOP-0005 did not prove PCL and did not produce a certified rank-two positive-gap counterexample.

The useful outcome is an exact and apparently consistent 4 x 4 compression formulation of the Projected Compression Lemma (PCL), plus numerical evidence that finds equality/near-equality rather than a violation. But all three lanes explicitly stop short of an actual universal certificate.

Final decision:

```text
complete proof of CLAIM-0001: no
complete proof of PCL: no
rank-two positive-gap counterexample: no
accepted bridge-defect: no
PCL status: exact equivalent support-compression reformulation; open/unproved
CLAIM-0001 status: open/fail-closed
```

## 1. PCL status: proved or only reformulated/tested?

Only reformulated and tested.

The PCL statement is the same support-compression restatement accepted in LOOP-0004:

```text
For all rank-two projections P,Q on H=C^4 tensor C^4,
Phi|_{Hom(QH,PH)} <= 0,
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I.
```

This is equivalent to CLAIM-0001 because every `C=PCQ` has ordinary operator rank at most two, and every rank-at-most-two `C` has range/co-range supports of dimension at most two, enlarged if needed.

LOOP-0005 did not add a proof of the universal negativity. It produced:

1. a coordinate/compression formula for the 4 x 4 Hermitian matrix `K`;
2. normal-form warnings about limited local-unitary covariance;
3. numerical searches that found no positive compression eigenvalue;
4. partial diagonal SOS identities and a proposed Plucker/SOS target.

None of these is a certificate for all pairs `(P,Q)`.

## 2. Normal-form/covariance review

The normal-form lane is conservative and largely correct. In particular, it correctly identifies a hidden trap: PCL is not covariant under arbitrary independent left/right local unitaries on the range and co-range planes. For

```text
C' = U C V^*,      U=U_A tensor U_B,      V=V_A tensor V_B,
```

the partial traces only conjugate simply when the left and right unitaries match on the subsystem being traced. Therefore the safe ambient covariance is simultaneous local conjugation

```text
P -> W P W^*,      Q -> W Q W^*,      W=W_A tensor W_B,
```

not independent local normalization of `P` and `Q`.

Skeptic checks:

- The compression entry formula

```text
K_{alpha beta,gamma delta}
 = <tr_1 E_{alpha beta}, tr_1 E_{gamma delta}>
 + <tr_2 E_{alpha beta}, tr_2 E_{gamma delta}>
 - (1/2) conjugate(tr E_{alpha beta}) tr E_{gamma delta}
 - 2 delta_{alpha gamma} delta_{beta delta}
```

matches the convention `K_ab=<E_a,Phi(E_b)>` with Hilbert-Schmidt inner product linear in the second argument, as used by NumPy `vdot` in the numerical lane.

- The component formulas

```text
tr_1 |p_alpha><q_beta| [a,b] = sum_i p_alpha[i,a] conjugate(q_beta[i,b])
tr_2 |p_alpha><q_beta| [i,j] = sum_a p_alpha[i,a] conjugate(q_beta[j,a])
tr |p_alpha><q_beta| = <q_beta,p_alpha>
```

are consistent with row-major vectorization and with the implementation in `LOOP-0005_pcl_compression_search.py`.

- The lane does not claim a full canonical normal form. That is appropriate. A false proof could arise if one Schmidt-normalized both two-planes independently; the lane explicitly avoids that.

Remaining caveat: any later Plucker/normal-form proof must also account for the independent `U(2)` basis changes inside each support plane. Those change the displayed 4 x 4 matrix by a unitary congruence/representation on `Hom(QH,PH)`, so eigenvalues/minors of the full compression are invariant, but individual entries are gauge-dependent.

## 3. Numerical/eigenvalue lane review

The numerical lane did not find a robust positive compression eigenvalue. It found equality and negative evidence only.

Reported main run:

```text
random_samples: 5000
random_positive_count_tol_1e_10: 0
random_best_lambda_max: -1.047205640060712
optimization_restarts: 8
optimization_maxiter: 200
optimization_best_lambda_max: -8.4668383415476e-14
optimization_best_reconstructed_gap: -8.504308368628699e-14
best_overall_lambda_max: 0.0
best_overall_reconstructed_gap: 0.0
positive_robust_tol_1e_8: false
```

Equality regressions were reproduced:

```text
traceless diagonal:       eigvals [-2, -2, -1, 0]
product projection:       eigvals [-1, -1, -1, 0]
LOOP-0002 equality case:  eigvals [-1, -1, -1, 0]
```

The implementation contains useful internal checks:

- adjoint/quadratic self-check errors are roundoff-scale (`~1e-14` to `~1e-13`);
- the reconstructed top-eigenvector operator satisfies `gap(C) ~= lambda_max(K)`;
- reconstructed rank is at most two because the operator is built from `Hom(QH,PH)`.

Skeptic limitations:

1. Random Grassmannian sampling and BFGS over QR-orthonormalized frames are not exhaustive and not certified.
2. The BFGS best has `optimizer_success: false` and reports precision loss. It should be read only as a near-equality probe.
3. The best overall value `0.0` comes from known equality regressions, not from discovery of a positive gap.
4. No interval/rational certificate was produced for either positivity or global nonpositivity.

Conclusion: numerical lane supports “no counterexample found,” not “PCL proved.”

## 4. Proof/SOS lane review

The proof/SOS lane does not contain an actual SOS certificate or PSD factorization.

Accepted useful content:

- The formulas

```text
tr_1 |vec(U)><vec(V)| = U^T conjugate(V)
tr_2 |vec(U)><vec(V)| = U V^*
tr |vec(U)><vec(V)| = tr(V^* U)
```

are consistent with the stated vectorization.

- The reduced target

```text
M(U,V) = 2I_4 - A(U,V) - B(U,V) + (1/2)T(U,V) >= 0
```

on `Gr(2,16) x Gr(2,16)` is a valid exact algebraic target.

- The lane correctly rejects two invalid/overstrong proof routes inherited from earlier loops:
  - a naive all-frame PSD kernel for `m >= 3`, already contradicted by the LOOP-0004 matrix-unit obstruction;
  - the fixed-gauge `H <= 2I` route, which is not the full support-compression statement.

What is missing:

1. No Gram/SOS certificate is displayed.
2. No principal-minor nonnegativity proof is given.
3. The diagonal Lagrange/wedge SOS identities prove only diagonal entries of `M=-K` are nonnegative. Diagonal nonnegativity is far weaker than `M >= 0`.
4. The route “prove `det M >= 0`” is not by itself decisive unless all lower principal minors are also proved nonnegative. The lane says this in places, but any future proof must not treat the determinant alone as sufficient.
5. The proposed Plucker-coordinate certificate remains a task description, not a result.

Conclusion: proof/SOS lane isolates the right-looking algebraic subproblem but leaves PCL open.

## 5. Hidden assumptions and overclaim risks

The main risks to guard against in future loops are:

1. False covariance/gauge fixing.
   Do not independently Schmidt-normalize both `P` and `Q` using separate local unitaries unless the effect on partial traces is explicitly preserved.

2. Entrywise or diagonal positivity mistaken for compression PSD.
   PCL requires the full 4 x 4 Hermitian matrix `K <= 0`, equivalently `M=-K >= 0`.

3. Determinant-only proof.
   For a 4 x 4 Hermitian matrix, PSD needs all principal minors or another equivalent PSD certificate. `det M >= 0` alone is insufficient.

4. All-frame kernel promotion.
   LOOP-0004 already found an `m=3` obstruction. Any proof must use the exact two-plane/two-plane structure of `Hom(QH,PH)`.

5. Numerical equality mistaken for proof.
   The optimizer reached values around `-1e-13`, with precision-loss messages. This is consistent with sharp equality families but gives no global certificate.

6. Basis-gauge dependence.
   Compression entries depend on chosen orthonormal frames of `ran P` and `ran Q`; only the compression operator/eigenvalues/PSD status are intrinsic.

## 6. Next blockers

PCL remains blocked on one of the following:

1. A genuine analytic proof that

```text
M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0
```

for all orthonormal two-frames `U,V in C^{16 x 2}`.

2. A certified Plucker/SOS certificate for all principal minors of `M`, or a direct Hermitian Gram factorization of `M` in the coordinate ring of `Gr(2,16) x Gr(2,16)`.

3. A robust counterexample: explicit rank-at-most-two `C` with direct verified

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2 - 2||C||_F^2 > 0
```

preferably with rational/interval certification, not just floating-point output.

4. A smaller valid normal form that preserves the actual covariance group and all support-plane gauge freedoms.

## Final skeptic decision

```text
LOOP-0005 status: fail_closed
PCL proved: no
PCL refuted: no
robust positive compression eigenvalue found: no
equality/near-equality evidence found: yes
actual SOS/PSD certificate found: no
CLAIM-0001 remains: open / fail_closed
```
