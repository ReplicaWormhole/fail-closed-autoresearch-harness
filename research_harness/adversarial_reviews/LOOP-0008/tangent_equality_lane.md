# LOOP-0008 Tangent / Equality Lane

status: completed_fail_closed_numerical_evidence_only
claim_focus: CLAIM-0001-rank-two-partial-trace
last_updated: 2026-06-03
script: research_harness/experiments/LOOP-0008_tangent_equality_lane.py
log: research_harness/logs/LOOP-0008_tangent_equality_seed8008.json
stdout_log: research_harness/logs/LOOP-0008_tangent_equality_seed8008.stdout.log

## Scope

This lane parameterized the tangent space to the rank-two variety at the two
known sharp equality controls and computed first/second variation evidence for
the original gap

```text
gap(C)=||tr_1 C||_F^2+||tr_2 C||_F^2-2||C||_F^2-(1/2)|tr C|^2.
```

The implementation uses the corrected partial-trace convention:

```text
tr_1(C)[a,b] = sum_i C[i,a,i,b]
tr_2(C)[i,j] = sum_a C[i,a,j,a]
```

This is a numerical local analysis/regression lane. It is not a proof of
CLAIM-0001 and it does not certify local maximality in exact arithmetic.

## Equality controls tested

1. Diagonal difference:

```text
C_diag = (|00><00| - |11><11|)/sqrt(2).
```

2. Product projection:

```text
C_prod = (P_2 tensor |0><0|)/sqrt(2)
       = (|00><00| + |10><10|)/sqrt(2).
```

Both are rank-two controls with normalized gap zero up to roundoff.

## Tangent parameterization

For a rank-two equality point `C0=U S V^*`, with rank-two left/right support
planes `P=UU^*` and `Q=VV^*`, the script uses the standard tangent model for the
rank-two matrix variety:

```text
T_C0 {rank <= 2} = {D : (I-P) D (I-Q) = 0}
                 = P D Q + P D (I-Q) + (I-P) D Q.
```

Equivalently, a complex basis is formed from

```text
U_2 x V_2,   U_2 x V_perp,   U_perp x V_2.
```

For `16 x 16` matrices and rank `2`, this gives complex dimension
`2*16 + 16*2 - 2*2 = 60`.  The lane then forms the real tangent to the unit
Frobenius sphere by adjoining `iB` for each complex basis element and projecting
out the real radial direction `C0`; the resulting real dimension is `119`.

The quadratic form is implemented through its Hermitian polarization:

```text
B(X,Y) = <tr_1 X, tr_1 Y> + <tr_2 X, tr_2 Y>
         - 2 <X,Y> - (1/2) conjugate(tr X) tr Y,

gap(C) = B(C,C).
```

On the real unit-sphere tangent basis, the script computes:

- the projected first variation coefficients `2 Re B(C0,D)`;
- the real second-variation quadratic matrix `Re B(D_i,D_j)`;
- eigenvalues of that tangent quadratic matrix;
- finite-difference sweeps along extremal eigen-directions after rank-two SVD
  retraction and Frobenius renormalization;
- random exact-tangent and random ambient rank-two-retracted perturbation checks.

## Command actually run

From repository root `.`:

```text
python3 research_harness/experiments/LOOP-0008_tangent_equality_lane.py \
  --seed 8008 --random-dirs 5000 \
  --out research_harness/logs/LOOP-0008_tangent_equality_seed8008.json \
  2>&1 | tee research_harness/logs/LOOP-0008_tangent_equality_seed8008.stdout.log
```

Stdout summary:

```text
diag_difference:
  normalized_gap = 0.0
  projected first variation l2 = 0.0
  max tangent q(D) eigenvalue = 0.0
  positive second-variation eigenvalue count, tol 1e-10 = 0
  best random exact-tangent rank2-retracted normalized gap = -1.1286354329006127e-06
  best random ambient rank2-retracted normalized gap = -7.802594210527474e-08

product_projection:
  normalized_gap = -2.2204460492503136e-16
  projected first variation l2 = 0.0
  max tangent q(D) eigenvalue = 0.0
  positive second-variation eigenvalue count, tol 1e-10 = 0
  best random exact-tangent rank2-retracted normalized gap = -1.0783607031772395e-06
  best random ambient rank2-retracted normalized gap = -8.329051037758715e-08

robust_positive_direction_or_gap_found_tol_1e-10 = false
```

## Detailed numerical results

### Diagonal difference control

Regression values:

```text
rank = 2
fro2 = 0.9999999999999998
gap = 0.0
normalized_gap = 0.0
trace_abs2 = 0.0
tr1_fro2 = 0.9999999999999998
tr2_fro2 = 0.9999999999999998
complex_tangent_dim = 60
real_sphere_tangent_dim = 119
projected_first_variation_l2 = 0.0
projected_first_variation_linf = 0.0
```

Second-variation spectrum for `q(D)=gap(D)` on the real unit-sphere tangent:

```text
min eigenvalue = -2.0
max eigenvalue = 0.0
positive_count_tol_1e-10 = 0
near_zero_count_tol_1e-10 = 9
negative_count_tol_1e-10 = 110
top eigenvalues = 0.0 repeated 9 times, then -0.9999999999999998
bottom eigenvalues = -2.0 repeated at least 10 times
```

Finite differences along a zero-mode eigen-direction stayed at numerical zero;
along a most-negative eigen-direction the normalized gap behaved like a negative
quadratic.  For example:

```text
eps=1e-2: plus = minus = -1.9998000199983323e-4, central_second = -3.9996000399966647
eps=1e-3: plus = minus = -1.99999799987971e-6, central_second = -3.9999959997594203
eps=1e-4: plus = minus = -1.999999987845058e-8, central_second = -3.999999975690116
```

The factor of about `2` between `central_second` and the eigenvalue `q(D)=-2`
is expected because `f(t)=t^2 q(D)+O(t^3)` gives
`(f(t)+f(-t)-2f(0))/t^2 approx 2q(D)`.

### Product projection control

Regression values:

```text
rank = 2
fro2 = 0.9999999999999998
gap = -2.220446049250313e-16
normalized_gap = -2.2204460492503136e-16
trace_abs2 = 1.9999999999999996
tr1_fro2 = 1.9999999999999996
tr2_fro2 = 0.9999999999999998
complex_tangent_dim = 60
real_sphere_tangent_dim = 119
projected_first_variation_l2 = 0.0
projected_first_variation_linf = 0.0
```

Second-variation spectrum for `q(D)=gap(D)` on the real unit-sphere tangent:

```text
min eigenvalue = -2.0
max eigenvalue = 0.0
positive_count_tol_1e-10 = 0
near_zero_count_tol_1e-10 = 13
negative_count_tol_1e-10 = 106
top eigenvalues = 0.0 repeated at least 10 times
bottom eigenvalues = -2.0 repeated at least 10 times
```

Finite differences again showed no positive direction.  Along a most-negative
eigen-direction:

```text
eps=1e-2: plus = minus = -1.9998000199983323e-4, central_second = -3.999600039992224
eps=1e-3: plus = minus = -1.999997999768688e-6, central_second = -3.9999959990932865
eps=1e-4: plus = minus = -1.9999999656405972e-8, central_second = -3.9999998868722733
```

## Interpretation

The tested equality controls are stationary for the original gap restricted to
the smooth rank-two manifold and unit Frobenius sphere: the projected first
variation vanished to floating-point precision.

The computed tangent quadratic forms were negative semidefinite to numerical
precision:

```text
max tangent q(D) = 0.0
positive eigenvalue count above 1e-10 = 0
```

The zero eigenvalues are expected to include tangent directions along equality
families and symmetry/gauge-generated flat directions.  The product-projection
control had more numerical zero modes (`13`) than the diagonal-difference control
(`9`), consistent with a larger visible equality family/stabilizer, but this lane
did not classify those zero modes exactly.

Random rank-two-retracted perturbation checks found no positive original gap.
The best normalized gaps were small negative values, with the largest ambient
rank-two-retracted values around `-8e-8` for `eps=1e-3`, consistent with approach
to equality rather than an unstable positive direction.

## Counterexample handling

No positive direction was found.  Therefore this lane did not produce an explicit
rank-at-most-two positive-gap matrix `C` requiring certification.  The script does
record rank and original-convention gap for every best perturbation candidate in
the JSON log; all best candidates remained nonpositive.

If a future run finds `normalized_gap > 1e-10`, it should be promoted only after
exporting the explicit `16 x 16` matrix and independently verifying rank `<=2`
and positive original gap in high precision or exact/interval arithmetic.

## Caveats / fail-closed verdict

- This is floating-point evidence, not a proof.
- The tangent model is the standard rank-two variety tangent at smooth rank-two
  points, but numerical SVD support extraction and real Gram diagonalization are
  not exact certificates.
- Negative semidefinite second variation at these two equality controls does not
  rule out positive gap elsewhere on the rank-two variety.
- The zero-mode spaces were not exactly classified; they may contain both genuine
  equality-family directions and numerical/gauge degeneracies.
- SVD truncation used in finite-difference paths is a controlled rank-preserving
  heuristic, not an algebraic proof path.

Conclusion: this lane found local-maximality evidence at the two sharp equality
controls for the original corrected-convention gap, but no proof and no certified
rank-two counterexample. CLAIM-0001 remains open/fail-closed.
