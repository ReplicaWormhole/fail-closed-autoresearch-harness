# LOOP-0008 full PCL/search lane

status: fail_closed_no_full_pcl_certificate_no_counterexample
claim_focus: CLAIM-0001 via full Projected Compression Lemma (PCL)
last_updated: 2026-06-03

## Executive summary

I attacked the full `4 x 4` PCL target rather than only the scalar crossed minor.
For orthonormal support two-frames `U,V in C^16`, with basis
`E_{i alpha}=|u_i><v_alpha|`, the target matrix is

```text
M(U,V) = 2I_4 - A(U,V) - B(U,V) + (1/2)T(U,V) >= 0.
```

A PCL violation is `lambda_min(M)<0`.  Since the original gap form on the same
support is represented by `K=-M`, a negative PCL eigenvalue must convert to an
explicit original operator

```text
C = sum_{i,alpha} x_{i alpha} E_{i alpha} = P C Q,
rank(C) <= 2,
gap(C) = - x^* M x > 0.
```

I added and ran a full-PCL search script that always performs this conversion and
checks the original corrected partial traces.  It found no robust PCL violation
and no positive original gap.  It also found no proof/certificate of full PSD.
The lane therefore fails closed.

## Artifacts created

Script:

```text
research_harness/experiments/LOOP-0008_full_pcl_search.py
```

Logs:

```text
research_harness/logs/LOOP-0008_full_pcl_search_seed8008.json
research_harness/logs/LOOP-0008_full_pcl_search_seed8008.stdout.log
research_harness/logs/LOOP-0008_full_pcl_rank_one_update_controls.stdout.log
```

Main run command from repository root:

```text
python3 research_harness/experiments/LOOP-0008_full_pcl_search.py \
  --seed 8008 --random-trials 3000 --opt-restarts 6 --maxiter 150 \
  --out research_harness/logs/LOOP-0008_full_pcl_search_seed8008.json \
  > research_harness/logs/LOOP-0008_full_pcl_search_seed8008.stdout.log
```

## Conventions checked

The script uses the corrected original partial-trace convention:

```text
tr_1(C)[a,b] = sum_i C[i,a,i,b]
tr_2(C)[i,j] = sum_a C[i,a,j,a]
```

For rank-one compression atoms `E_{i alpha}=|vec(U_i)><vec(V_alpha)|`, it uses

```text
tr_1 E_{i alpha} = U_i^T conjugate(V_alpha)
tr_2 E_{i alpha} = U_i V_alpha^*
tr   E_{i alpha} = tr(V_alpha^* U_i).
```

For every probed frame pair, the script diagonalizes `M`, converts the worst
`M` eigenvector to an explicit `C`, normalizes `C`, computes `gap(C)` by the
original formula, and records

```text
abs(normalized_gap(C) + x^* M x).
```

The random scan maximum identity error was

```text
2.6645352591003757e-15
```

so the PCL/original-gap sign conversion was internally consistent to roundoff.

## What the full-PCL search tested

The script tested:

1. equality/control supports;
2. exhaustive coordinate two-plane support pairs (`120 x 120 = 14400` pairs);
3. `3000` random complex support-frame pairs;
4. local BFGS minimization of `lambda_min(M)` over unconstrained frame variables
   with QR projection back to two-frames (`6` restarts, `150` max iterations).

For each frame pair, it recorded:

- full eigenvalues of `M`;
- all principal minor minima by size `1,2,3,4`;
- the worst original `C=PCQ` produced from the most dangerous PCL eigenvector;
- the rank and original normalized gap of that `C`.

## Main numerical output

Stdout summary:

```text
seed: 8008
random_trials: 3000
coordinate_pairs: 14400
control_min_eigs:
  product_projection_support_00_10: 0.0
  diagonal_traceless_support_00_11: 0.0
  right_product_support_00_01: 0.0
coordinate_worst_min_eig_M: 0.0
random_worst_min_eig_M: 1.060359499717052
optimized_worst_min_eig_M: 3.2507330161017243e-13
worst_overall_min_eig_M: 0.0
worst_overall_original_normalized_gap: 2.2204460492503126e-16
robust_pcl_violation_found: false
elapsed_sec: 117.47016215324402
```

Additional parsed values from the JSON log:

```text
coordinate negative min-eigenvalue count (tol 1e-10): 0
coordinate pair count with negative principal minors by size:
  size 1: 0
  size 2: 0
  size 3: 0
  size 4: 0
random positive original-gap count (tol 1e-10): 0
random min principal minors by size:
  size 1: 1.2177939820249133
  size 2: 1.69074933141542
  size 3: 2.5635066707197547
  size 4: 4.020800087698649
optimized best eig_M:
  [3.2507330161017243e-13,
   1.5217542054091155,
   1.9999999999997633,
   1.9999999999998774]
optimized best original normalized gap:
  -3.2427069109517103e-13
```

Interpretation: random frames sit well inside the conjectural PSD cone; optimizer
runs move back to equality/near-equality, not to a negative eigenvalue.  This is
not a proof.

## Equality and rank-one-update observations

The full matrix confirms the same trace-update obstruction seen in the crossed
minor.  The control log records `D=2I-A-B` and `T` for product and diagonal
equality supports.

Product support `span{|00>,|10>}` (and similarly `span{|00>,|01>}`):

```text
eig(D) = [-1, 1, 1, 1]
eig(M) = [0, 1, 1, 1]
D = [[0,0,0,-1], [0,1,0,0], [0,0,1,0], [-1,0,0,0]]
T = [[1,0,0,1], [0,0,0,0], [0,0,0,0], [1,0,0,1]]
```

Diagonal/traceless support `span{|00>,|11>}`:

```text
eig(D) = [0, 0, 2, 2]
eig(M) = [0, 1, 2, 2]
D = diag(0,2,2,0)
T = [[1,0,0,1], [0,0,0,0], [0,0,0,0], [1,0,0,1]]
```

Thus a full-PCL proof cannot first prove `D>=0`; `D` is already indefinite on the
product equality family.  The rank-one trace update repairs the bad direction
exactly.  A determinant-lemma route for

```text
M = D + (1/2)t t^*
```

would have to retain the coupled update in every principal block/Schur
complement.  Discarding the trace term or treating it as a harmless positive
add-on after a contraction-defect proof is false.

## Principal-minor route status

The numerical principal-minor checks gave no negative minors in the tested
classes, including all coordinate two-plane support pairs.  Equality controls
show many sharp zero minors, including zero determinant of the full `4 x 4`
matrix.  However, this is finite/numerical evidence only.  I did not find:

```text
- symbolic nonnegativity certificates for all 1x1, 2x2, 3x3 minors and det(M);
- a Schur-complement proof that survives the indefinite D obstruction;
- a Gram/SOS certificate for the full Hermitian matrix M;
- an exact Plucker/SOS identity for the determinant or all minors.
```

The scalar crossed minor remains only one principal slice.  The LOOP-0008 run
looked at the full matrix numerically, but it does not promote crossed-minor or
principal-minor evidence into a proof.

## Counterexample status

No explicit counterexample was found.  In particular, the worst candidate from
the full PCL search had

```text
lambda_min(M) = 0.0
converted original normalized gap = 2.2204460492503126e-16
rank(C) = 2
```

This is equality/roundoff, not a positive original gap.  The optimized near-zero
candidate had

```text
lambda_min(M) = 3.2507330161017243e-13
converted original normalized gap = -3.2427069109517103e-13
```

again consistent with equality/roundoff and not a violation.

## Fail-closed verdict

This lane did not prove full `4 x 4` PCL PSD and did not produce an explicit
rank-at-most-two positive-gap `C`.  It provides reproducible full-compression
regression evidence and a guardrail for rank-one-update proof attempts, but
CLAIM-0001 remains open.

The next viable full-PCL subtargets are:

```text
1. derive a trace-coupled Schur/principal-minor certificate for M itself;
2. find a full Hermitian Gram/SOS representation of M on Gr(2,16) x Gr(2,16);
3. parameterize equality tangent spaces and certify local maximality of gap;
4. continue counterexample search only with automatic conversion to explicit C
   and original corrected gap checks.
```
