# LOOP-0013 full-PCL trace-coupled certificate lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace / U-0002 full PCL PSD
lane: WS-full-pcl-certificate / Schur-Gram-SOS-rank-one-update
success_condition_met: none

## Executive verdict

No complete proof and no counterexample were obtained.  The lane made a durable
advance by separating the part that is now algebraically proved from the part
that remains a genuine symbolic certificate problem.

The only admissible target is the full trace-coupled matrix

```text
M = 2I_4 - A - B + (1/2)T
  = D + (1/2) conjugate(t) t^T,      D = 2I_4 - A - B,
```

where `t` is the four-entry trace vector in the `E_{ia}` compression basis.
D-only pivots, D-only minors, and Schur complements of `D` are explicitly
rejected: they are false on coordinate controls and cannot be used as a PCL
certificate.

## Artifacts and reproducible run

Created executable diagnostic script:

```text
./research_harness/experiments/LOOP-0013_full_pcl_rank_update_diagnostics.py
```

Commands run from repository root `.`:

```text
python3.12 -m py_compile research_harness/experiments/LOOP-0013_full_pcl_rank_update_diagnostics.py
python3.12 research_harness/experiments/LOOP-0013_full_pcl_rank_update_diagnostics.py --trials 500 --seed 13013 > research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.stdout.log
```

Logs written:

```text
./research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.stdout.log
./research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.json
```

Stdout summary:

```json
{
  "loop": "LOOP-0013",
  "seed": 13013,
  "trials": 500,
  "coordinate_total_pairs": 14400,
  "coordinate_M_negative_eig_count": 0,
  "coordinate_D_negative_eig_count": 48,
  "coordinate_M_no_nonnegative_pivot_order_count": 0,
  "coordinate_D_no_nonnegative_pivot_order_count": 120,
  "coordinate_good_fixed_M_pivot_orders": [
    "[0, 1, 2, 3]",
    "[0, 2, 1, 3]",
    "[1, 0, 2, 3]",
    "[1, 2, 0, 3]",
    "[1, 2, 3, 0]",
    "[1, 3, 2, 0]",
    "[2, 0, 1, 3]",
    "[2, 1, 0, 3]",
    "[2, 1, 3, 0]",
    "[2, 3, 1, 0]",
    "[3, 1, 2, 0]",
    "[3, 2, 1, 0]"
  ],
  "coordinate_size4_min_detM": {
    "value": 0.0,
    "case": {"P": [0, 1], "Q": [0, 1], "S": [0, 1, 2, 3], "detD": -1.0, "update_q": 2.0, "detM": 0.0, "identity_abs_residual": 0.0}
  },
  "coordinate_size4_min_detD": {
    "value": -1.0,
    "case": {"P": [0, 1], "Q": [0, 1], "S": [0, 1, 2, 3], "detD": -1.0, "update_q": 2.0, "detM": 0.0, "identity_abs_residual": 0.0}
  },
  "coordinate_max_det_identity_residual_size4": 8.881784197001252e-16,
  "random_M_negative_eig_count": 0,
  "random_D_negative_eig_count": 0,
  "random_worst_M_min_eig": {"value": 1.1348538922391722, "case": {"trial": 63, "eig_M": [1.1348538922391722, 1.5173396400099186, 1.6218261006699703, 1.7546788477858934]}},
  "random_size4_min_detM": {"value": 3.8843571701982333, "case": {"trial": 489, "S": [0, 1, 2, 3], "detD": 3.5541875591725542, "update_q": 0.6603392220513565, "detM": 3.8843571701982333, "identity_abs_residual": 8.88243222559818e-16}},
  "random_size4_min_update_q": {"value": 0.08447634668938439, "case": {"trial": 289, "S": [0, 1, 2, 3], "detD": 5.121850081091066, "update_q": 0.08447634668938439, "detM": 5.164088254435758, "identity_abs_residual": 3.5540186783472804e-18}},
  "log": "./research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.json"
}
```

## Algebraic part proved: trace-coupled determinant update identity

For every principal subset `S`, write

```text
M_S = D_S + (1/2) conjugate(t_S) t_S^T.
```

The determinant update identity is the adjugate-polynomial form of the matrix
determinant lemma:

```text
det(M_S) = det(D_S) + (1/2) t_S^T adj(D_S) conjugate(t_S).
```

This proof does not require `D_S` to be invertible.  When `D_S` is invertible,
`det(D_S + u v^T)=det(D_S)(1+v^T D_S^{-1}u)` with
`u=(1/2)conjugate(t_S)` and `v=t_S`; multiplying by the inverse gives the
adjugate expression.  Both sides are polynomial in the entries of `D_S` and
`t_S`, so the identity extends through singular `D_S` by continuity/polynomial
identity.  This is an identity for `M`, not a certificate for `D`.

The LOOP-0013 script checks this identity for every principal subset in all
`14400` coordinate plane pairs and in `500` random full-frame trials.  The worst
recorded residual was floating-point roundoff (`4.44e-15` in random size 4;
`8.88e-16` in coordinate size 4).

## What remains unproved

PCL needs all principal minors of `M` nonnegative, or equivalently a full
Hermitian Schur/Gram/SOS certificate.  After the identity above, the exact
remaining target is

```text
det(D_S) + (1/2) q_S >= 0,
q_S := t_S^T adj(D_S) conjugate(t_S),       for every principal S.
```

The diagnostics found no negative `q_S` in the coordinate atlas or in the random
sample, suggesting `q_S` may itself have a Gram/SOS representation.  This is only
evidence: no symbolic Gram for `q_S` or for `det(M_S)` was found.

Coordinate summary by subset size:

| size | negative det(M_S) | negative det(D_S) | negative q_S | zero det(M_S) | min det(M_S) | min det(D_S) | min q_S |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 | 0 | 0.5 | 0.0 | 0.0 |
| 2 | 0 | 48 | 0 | 264 | 0.0 | -1.0 | 0.0 |
| 3 | 0 | 96 | 0 | 528 | 0.0 | -1.0 | 0.0 |
| 4 | 0 | 48 | 0 | 264 | 0.0 | -1.0 | 0.0 |

Random sample summary (`seed=13013`, `trials=500`):

| size | negative det(M_S) | negative det(D_S) | negative q_S | min det(M_S) | min det(D_S) | min q_S |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0 | 0 | 0 | 1.2221637806130328 | 1.159951983284349 | 0.00005554618024678745 |
| 2 | 0 | 0 | 0 | 1.7428944074173878 | 1.5935313185956037 | 0.001756922702195725 |
| 3 | 0 | 0 | 0 | 2.4900043723247083 | 2.3180767411268706 | 0.008421265048441786 |
| 4 | 0 | 0 | 0 | 3.8843571701982333 | 3.5541875591725542 | 0.08447634668938439 |

## D-only routes explicitly rejected

The coordinate atlas again refutes D-only minors and D-only pivots:

```text
coordinate_D_negative_eig_count = 48
coordinate_D_no_nonnegative_pivot_order_count = 120
negative det(D_S) counts: size 2 -> 48, size 3 -> 96, size 4 -> 48
```

The sharp coordinate repair example for the full determinant is

```text
P = [0,1], Q = [0,1], S = [0,1,2,3]
det(D_S) = -1,     q_S = 2,     det(M_S) = -1 + (1/2)*2 = 0.
```

This example is a compact regression guardrail: any certificate that first tries
to prove `det(D_S) >= 0` or `D >= 0` fails exactly where the trace update is
needed.

## Pivot / Schur exploration

For full `M`, the coordinate atlas had no negative eigenvalue and no case with
zero available nonnegative pivot order:

```text
coordinate_M_negative_eig_count = 0
coordinate_M_no_nonnegative_pivot_order_count = 0
```

Moreover, `12` fixed pivot permutations worked across all coordinate support
pairs.  However, this is not a proof for arbitrary two-frames.  It only suggests
a possible Schur route: choose one of the coordinate-good orders and derive a
symbolic trace-coupled LDL certificate in that order.  The Schur complement must
be

```text
S_R(M) = M_RR - c c^*/m,
m = M_ii = D_ii + (1/2)|t_i|^2,
c = M_Ri = D_Ri + (1/2)conjugate(t_R)t_i,
```

with the update carried inside `c` and `m`.  Replacing this by a Schur complement
of `D` is invalid.

## Fail-closed conclusion

LOOP-0013 proves and regression-tests the determinant update identity and gives a
more precise certificate target:

```text
Find a Gram/SOS representation of q_S and/or det(D_S)+(1/2)q_S for all principal
S, or prove a fixed/full-M trace-coupled Schur order symbolically.
```

No accepted proof of `M >= 0`, no counterexample, and no bridge defect were
found.  U-0002 remains open.
