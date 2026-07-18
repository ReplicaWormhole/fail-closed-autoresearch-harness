# LOOP-0009 mixed Plucker identity lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: scalar PAL / crossed-PCL mixed two-frame Plucker ansatz
success_condition_met: none

## Executive verdict

I attacked the scalar crossed PAL/PCL determinant

```text
D_1 D_2 - |a + conjugate(b)|^2 >= 0,
```

equivalently `det M[{(1,1),(2,2)}] >= 0`, with the trace rank-one update retained.

Outcome: no proof, no scalar counterexample, and no promotion to full PCL/CLAIM.  The useful new output is an exact mixed two-frame off-diagonal Plucker identity, plus a precise obstruction to the most direct mixed-Gram/Cauchy proof built from that identity.

In short: the crossed off-diagonal entry is not produced by same-pair wedge polarization (LOOP-0008 obstruction), but it is produced exactly by genuinely mixed wedges `(X_1,Y_2)` paired with `(X_2,Y_1)`, modulo the explicit orthonormality constraints.  However, the norms of those mixed wedge vectors are not bounded by the target diagonal defects `D_1,D_2`; the margin can be as low as `-1.5` already on coordinate orthonormal frames.  Therefore the simple mixed Plucker Gram ansatz fails.

Fail-closed verdict remains: this is an obstruction/diagnostic, not a certificate.

## 1. Setup and non-assumptions

No Hermitian, normal, positive, or commutative assumption is made.  Work with Hilbert-Schmidt orthonormal two-frames

```text
<X_i, X_j>_F = delta_ij,
<Y_i, Y_j>_F = delta_ij,
X_i,Y_i in M_4(C).
```

For the crossed PCL block `S={(1,1),(2,2)}`, write

```text
M_S = [[D_1, m], [conjugate(m), D_2]],
det M_S = D_1 D_2 - |m|^2.
```

The trace update is included in `M = D + (1/2)T`, where `D=2I-A-B` and `T_{pq}=conjugate(t_p)t_q`.  On this crossed block,

```text
t_1 = tr(Y_1^* X_1),
t_2 = tr(Y_2^* X_2),
m = M_{(1,1),(2,2)}.
```

## 2. Exact mixed Plucker identity found

For vectors `a,b,c,d`, use the complex wedge inner product

```text
<a wedge b, c wedge d>
  = <a,c><b,d> - <a,d><b,c>.
```

Define row and column mixed Plucker contractions

```text
R_mix = sum_{r,s}
  < X_1[r,*] wedge Y_2[s,*], X_2[r,*] wedge Y_1[s,*] >,

C_mix = sum_{r,s}
  < X_1[*,r] wedge Y_2[*,s], X_2[*,r] wedge Y_1[*,s] >.
```

Expanding gives the off-manifold identity with explicit orthonormality multipliers:

```text
R_mix = <X_1,X_2>_F <Y_2,Y_1>_F - A_{(1,1),(2,2)},
C_mix = <X_1,X_2>_F <Y_2,Y_1>_F - B_{(1,1),(2,2)},
```

up to the convention-equivalent conjugation of the displayed scalar product.  Therefore, on the frame constraint manifold where

```text
<X_1,X_2>_F = 0,
<Y_1,Y_2>_F = 0,
```

the crossed off-diagonal entry satisfies

```text
m = R_mix + C_mix + (1/2) conjugate(t_1) t_2.        (2.1)
```

The LOOP-0009 script checked (2.1) to roundoff:

```text
random samples: 5000
max mixed offdiag identity error: 8.441528768080324e-17
sparse coordinate max identity error: 0.0
optimized near-equality identity error: 2.2887833992611187e-16
```

This is the genuinely mixed replacement for the failed LOOP-0008 same-pair polarization.  For comparison, the same-pair wedge polarization mismatch reached

```text
max same-pair polarization mismatch: 0.47081642102929433
```

in this run.

## 3. Failed mixed-Gram/Cauchy ansatz

The tempting next step is to treat (2.1) as an inner product of mixed Plucker vectors and apply Cauchy-Schwarz.  Define the mixed squared norms

```text
N_12 = sum ||X_1 row wedge Y_2 row||^2
     + sum ||X_1 col wedge Y_2 col||^2
     + (1/2)|tr(Y_2^*X_1)|^2,

N_21 = sum ||X_2 row wedge Y_1 row||^2
     + sum ||X_2 col wedge Y_1 col||^2
     + (1/2)|tr(Y_1^*X_2)|^2.
```

Then Cauchy would give

```text
|m|^2 <= N_12 N_21.
```

To imply the target determinant by this direct Gram route one would need, at minimum,

```text
N_12 <= D_1,
N_21 <= D_2,
```

or some trace-coupled correction that replaces these inequalities.  The direct inequalities are false on the actual orthonormal frame constraint manifold.

Regression data:

```text
random min(D_1 - N_12): -0.41194477765578674
random min(D_2 - N_21): -0.4054262460823934
sparse coordinate min(D_1 - N_12): -1.5
sparse coordinate min(D_2 - N_21): -1.5
sparse negative D_1-N_12 count: 5260 / 14400
sparse negative D_2-N_21 count: 5260 / 14400
optimized best D_1-N_12: -1.499999999999748
optimized best D_2-N_21: -1.4999999999998226
```

Because these negative margins occur with `<X_1,X_2>=<Y_1,Y_2>=0`, adding orthonormality multipliers alone cannot repair this simple norm-domination subclaim on the constraint manifold.  A valid certificate would need extra mixed trace/Plucker cancellations at determinant level, not merely Cauchy on the mixed vectors from (2.1).

## 4. Equality guardrails

The product equality control still shows why the trace update cannot be removed:

```text
product example X_1=Y_1=E_00, X_2=Y_2=E_01:
D_1 = D_2 = 0.5
m = -0.5
det M_S = 0
det D_S = -1.0
eig(D_S) = [-1, 1]
eig(M_S) = [0, 1]
N_12 = N_21 = 1.0
D_1-N_12 = D_2-N_21 = -0.5
same-pair offdiag gives +0.5, the wrong sign
mixed identity error = 0.0
```

The traceless diagonal equality control gives an even sharper obstruction to mixed norm domination:

```text
traceless example X_1=Y_1=E_00, X_2=Y_2=E_11:
D_1 = D_2 = 0.5
m = 0.5
det M_S = 0
det D_S = 0.0
eig(M_S) = [0, 1]
N_12 = N_21 = 2.0
D_1-N_12 = D_2-N_21 = -1.5
mixed identity error = 0.0
```

Thus the mixed off-diagonal identity is correct, but its natural mixed-vector norms are far too large at equality.  Any SOS certificate must vanish at these equality controls despite the nonzero mixed wedge norms.

## 5. Script and log artifacts

Created and ran:

```text
research_harness/experiments/LOOP-0009_mixed_plucker_probe.py
```

Run command from repository root:

```text
python3 research_harness/experiments/LOOP-0009_mixed_plucker_probe.py \
  --seed 9009 --samples 5000 --opt-starts 6 --maxiter 120 \
  | tee research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.stdout.log
```

JSON log:

```text
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.json
```

Stdout log:

```text
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.stdout.log
```

Actual run summary:

```text
status: mixed_identity_found_but_simple_cauchy_ansatz_obstructed_not_proof
random samples: 5000
max mixed offdiag identity error: 8.441528768080324e-17
max same-pair polarization mismatch: 0.47081642102929433
random min delta: 1.6516027614966962
random min D1-N12: -0.41194477765578674
random min D2-N21: -0.4054262460823934
sparse coordinate total: 14400
sparse min delta: 0.0
sparse min D1-N12: -1.5
sparse min D2-N21: -1.5
sparse negative D1-N12 count: 5260
sparse negative D2-N21 count: 5260
local optimized best delta: 6.034130765841868e-13
local optimized best D1-N12: -1.499999999999748
local optimized best D2-N21: -1.4999999999998226
```

The local optimized `delta` is near zero/equality and is not a counterexample.  No negative scalar determinant was found.

## 6. What was established vs. what remains open

Established in LOOP-0009:

1. The crossed PAL/PCL off-diagonal entry has an exact mixed two-frame Plucker representation, with explicit orthonormality multipliers.
2. This representation fixes the LOOP-0008 same-pair polarization mismatch at the off-diagonal level.
3. The direct mixed-vector Cauchy/SOS ansatz fails because its natural mixed norms are not bounded by the target diagonal defects, even on exact coordinate orthonormal frames.
4. Sparse and random regressions found no scalar violation; this is only evidence, not proof.

Not established:

1. Universal scalar nonnegativity `det M_S >= 0`.
2. A valid trace-coupled Plucker/SOS/Gram certificate for the scalar defect.
3. Full `4 x 4` PCL PSD.
4. CLAIM-0001.
5. Any certified rank-two positive-gap counterexample.

## 7. Next subtarget

The next scalar proof attempt should not try to dominate the mixed Plucker norms by `D_1,D_2`.  That subclaim is false.  A viable next ansatz must work directly at determinant level, using cancellations among

```text
D_1D_2,
|R_mix + C_mix + (1/2)conjugate(t_1)t_2|^2,
<X_1,X_2>, <Y_1,Y_2> multipliers,
```

and must vanish on both product and traceless equality mechanisms.  Concretely, the next subtarget is a determinant-level SOS/Gram identity whose elementary degree-four features are mixed Plucker contractions but whose Gram matrix has null directions enforcing the equality controls.  If that cannot be found, shift to full-PCL principal-minor/Schur certificates with the same mixed identity as the off-diagonal building block.
