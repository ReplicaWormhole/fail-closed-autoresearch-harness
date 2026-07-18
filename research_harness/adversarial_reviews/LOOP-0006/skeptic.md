# LOOP-0006 Skeptic Review

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_verdict: no_success_condition_met
pcl_status: open_unproved_not_refuted
pal_status: open_unproved_not_refuted
last_updated: 2026-06-03

reviewed:
  - research_harness/adversarial_reviews/LOOP-0006/pcl_symbolic_certificate_lane.md
  - research_harness/adversarial_reviews/LOOP-0006/pcl_structured_counterexample_lane.md
  - research_harness/adversarial_reviews/LOOP-0006/pal_pcl_bridge_lane.md
  - research_harness/adversarial_reviews/LOOP-0005/auditor.md
  - research_harness/logs/LOOP-0006_pcl_structured_seed6006.json
  - research_harness/experiments/LOOP-0006_pcl_principal_minors.py
  - research_harness/experiments/LOOP-0006_pcl_structured_search.py

## Executive verdict

Fail closed. LOOP-0006 does not prove or refute CLAIM-0001.

No stop/success condition is met:

```text
complete proof found: no
rank-two positive-gap counterexample found: no
accepted bridge-defect found: no
PCL: exact reformulation remains open; no PSD certificate; no refutation
PAL: logically aligned with PCL/CLAIM at universal quantifier level, but still unproved
CLAIM-0001: open / fail_closed
```

The three LOOP-0006 lanes made useful progress in narrowing the proof target and
correcting implementation conventions, but they do not supply an auditor-acceptable
proof, counterexample, or bridge defect.

## 1. Convention and sign audit

The PCL sign convention is internally consistent with LOOP-0005:

```text
q(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2 - 2||C||_F^2
K = compression matrix for q
PCL asks K <= 0
M := -K = 2I - A - B + (1/2)T asks M >= 0
```

The partial-trace convention used in the symbolic and bridge lanes is also
consistent with the corrected structured script:

```text
tr_1 |vec(U)><vec(V)| = U^T conjugate(V)
tr_2 |vec(U)><vec(V)| = U V^*
tr   |vec(U)><vec(V)| = tr(V^* U)
```

The structured search explicitly reports that an earlier implementation summed
the wrong tensor indices and produced spurious positives. The corrected code uses

```python
tr_1(C)[a,b] = sum_i C[i,a,i,b]  via np.einsum('iaib->ab', T)
tr_2(C)[i,j] = sum_a C[i,a,j,a]  via np.einsum('iaja->ij', T)
```

and the corrected controls reproduce the expected LOOP-0005 equality spectra:

```text
product projection K eigenvalues:  [-1, -1, -1, 0]
traceless diagonal K eigenvalues:  [-2, -2, -1, 0]
```

I do not see a remaining sign flip in the reported `K <= 0` / `M >= 0` usage.
The major risk is not a sign error in LOOP-0006; it is overinterpreting numerical
or principal-slice evidence as a full proof.

## 2. Symbolic certificate lane audit

The symbolic lane did not find an actual certificate. It found:

1. valid-looking diagonal/wedge SOS identities for the `1 x 1` principal minors;
2. an important negative regression showing `D=2I-A-B` is not PSD;
3. a narrowed principal-minor target, especially the crossed `2 x 2` minor.

This is useful but not a proof of PCL.

### 2.1 Diagonal SOS is insufficient

The diagonal Lagrange identities certify only

```text
M_{i alpha, i alpha} >= 0.
```

They do not imply Hermitian PSD of the full `4 x 4` matrix. The lane correctly
states this, and no hidden diagonal-to-PSD inference appears to be made.

### 2.2 `D=2I-A-B` route is correctly rejected

The product equality case has

```text
eig(D) = [-1, 1, 1, 1]
eig((1/2)T) = [0, 0, 0, 1]
eig(M) = [0, 1, 1, 1]
```

so any proof that first establishes `D >= 0` is impossible. Future proof attempts
must retain the trace rank-one update globally or prove a precise rank-one-update
inertia domination statement. The symbolic lane does not prove such a statement.

### 2.3 Is the crossed `2 x 2` minor really the next target?

Skeptic answer: it is a plausible and important next target, but not a solved or
exclusive bottleneck.

For a principal-minor proof of a `4 x 4` Hermitian matrix, after the diagonal
minors the next layer is all `2 x 2` principal minors. The crossed minor

```text
Delta_cross = det M[{(1,1),(2,2)}]
```

is especially sharp because it vanishes in the known equality regressions while
its diagonal entries are positive. That makes it a good stress target and shows
that diagonal positivity alone cannot close the argument.

However:

- no SOS/Gram/principal-minor certificate for this crossed minor is supplied;
- shared-index `2 x 2` minors are described as easier but are not actually
  certified in this lane;
- even proving the crossed `2 x 2` minors would not prove PCL by itself; the
  remaining `2 x 2`, `3 x 3`, and `4 x 4` principal minors, or an equivalent full
  PSD certificate, would still be needed;
- the phrase “smallest unresolved object” should be read as “smallest sharp
  unresolved object along the chosen principal-minor route,” not as a complete
  reduction of PCL to that single determinant.

Therefore the symbolic lane advances the map of the proof problem, but it does
not produce an actual certificate.

## 3. Structured counterexample lane audit

The corrected structured search found no counterexample. The reported results
are consistent with the logs:

```text
best overall lambda_max: 0.0
robust_positive: false
structured support best lambda_max: -0.24830718408995792
perturb eps=0.01 best lambda_max: -0.004606073165632001
perturb eps=0.1 best lambda_max: -0.3137722327674509
local optimization best lambda_max: -5.20317946714477e-13
```

The near-zero optimizer value is negative at floating-point scale and is best
interpreted as convergence to an equality/roundoff regime, not as a positive-gap
candidate. There is no robust positive eigenvalue, no reconstructed positive
original gap, and no rational/interval certificate.

The partial-trace correction matters. The lane explicitly admits that the earlier
wrong Einstein sums produced spurious positives even on a control case. After the
correction, those positives disappear. This supports the corrected convention and
removes the apparent counterexample signal; it does not prove PCL.

Remaining limitations:

- finite support-pattern search is not exhaustive over `Gr(2,16) x Gr(2,16)`;
- equality perturbation sampling is local and random;
- BFGS is local and floating-point;
- no interval, rational, or independent exact certification was attempted because
  no positive candidate survived;
- the product-control basis in the script is a product-plane representative that
  is equivalent to the reported product equality under relabeling, but future
  regression comments should avoid ambiguity about whether the second factor or
  first factor is being held fixed.

Conclusion: no structured counterexample was found, and no robust positive
eigenvalue remains after the partial-trace correction.

## 4. PAL-PCL bridge audit

The bridge lane is conceptually useful and mostly conservative. It correctly
distinguishes two different statements:

```text
one fixed PAL/SVD diagonal block in one support basis  !=  full fixed-basis PCL
universal PAL over all two-frames                      == enough to cover PCL directions by re-SVD
```

### 4.1 Principal-slice identification

With the stated vectorization convention,

```text
tr_1 E_ii = conjugate(X_i^* Y_i)
tr_2 E_ii = X_i Y_i^*
```

so the PAL off-diagonal must use the phase-aware term

```text
z = <X_1Y_1^*, X_2Y_2^*> + conjugate(<X_1^*Y_1, X_2^*Y_2>)
    - (1/2)t_1 conjugate(t_2).
```

This avoids the known false fixed-gauge replacement using `a+b`. I do not see a
remaining conjugation error in the bridge formula as written.

### 4.2 Logical equivalence caveat

The implication diagram is acceptable only at the level of universal statements:

```text
PCL => PAL
PAL => CLAIM-0001
CLAIM-0001 => PCL
```

The caveat is essential. PAL for one fixed SVD basis checks only the diagonal
slice `span{E_11,E_22}`. It does not check fixed-basis directions involving
`E_12`, `E_21`, mixed minors, or the full determinant of `M(U,V)`. PAL covers
those directions only by changing to the SVD basis of the particular coefficient
matrix `Z` being tested. Thus it is a moving-basis argument, not a fixed block
diagonalization of the `4 x 4` PCL matrix.

This means the bridge lane closes a conceptual relation, not the inequality. It
must not be cited as a proof that the full fixed `M(U,V)` has been certified by a
single PAL block.

## 5. Hidden assumptions and overclaim risks

The main assumptions that must remain explicit are:

1. Universal quantification is required. PAL implies PCL only if PAL is proved for
   all Hilbert-Schmidt orthonormal two-frames, not just for a chosen support basis.

2. The SVD basis moves with the coefficient matrix. This is valid for proving the
   universal inequality for each `C`, but it does not yield a fixed-basis
   `4 x 4` PSD/SOS certificate.

3. Principal-minor targets are not interchangeable with a full proof. Crossed
   `2 x 2` minors are sharp next tests, but PCL still requires all principal
   minors or an equivalent PSD certificate.

4. Equality regressions with zero eigenvalues/minors are not counterexamples.
   They are sharp constraints for any proposed certificate.

5. Numerical nonpositivity is not proof. The structured search is useful
   regression evidence only.

6. No independent local Schmidt normalization of both support planes is justified
   unless covariance of the partial-trace quadratic form is proved. LOOP-0006
   appears to respect this guardrail.

7. The trace rank-one update cannot be separated after proving `D >= 0`, because
   `D >= 0` is false.

## 6. Current blockers

The next accepted success must provide one of the following:

1. A complete proof of PCL:

```text
M(U,V) = 2I_4 - A(U,V) - B(U,V) + (1/2)T(U,V) >= 0
```

for all orthonormal two-frames `U,V in C^16`, with a full Hermitian Gram/SOS,
all-principal-minor, interval-certified symbolic, or otherwise rigorous
certificate.

2. A complete proof of universal PAL, with the phase-aware off-diagonal and
universal quantification over all Hilbert-Schmidt orthonormal two-frames.

3. A certified rank-at-most-two counterexample `C` with

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2 - 2||C||_F^2 > 0
```

verified by rational, interval, or another independently checkable certificate.

Immediate technical sub-blockers:

- produce an actual certificate for all `2 x 2` principal minors of `M`, not only
  diagonal minors;
- in particular, attack the sharp crossed minor, but do not treat it as sufficient
  by itself;
- then certify the relevant `3 x 3` minors and `det M`, or replace the
  principal-minor route with a direct full-matrix PSD certificate;
- maintain the corrected partial-trace convention in all scripts and symbolic
  formulas;
- use the equality families as mandatory regressions for any proposed proof.

## Final decision

```text
LOOP-0006 status: fail_closed
CLAIM-0001 status: open / fail_closed
PCL proved: no
PAL proved: no
PCL refuted: no
rank-two positive-gap counterexample: no
bridge defect accepted: no
```

LOOP-0006 sharpened the proof landscape and corrected a numerical convention
error, but it did not close CLAIM-0001. The current bottleneck remains: prove PCL
or universal PAL rigorously, or produce a certified rank-two positive-gap
counterexample.
