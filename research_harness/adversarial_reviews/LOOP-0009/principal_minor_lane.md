# LOOP-0009 principal-minor / rank-one-update lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: full-PCL principal minors and determinant-lemma diagnostics
success_condition_met: none

## Executive verdict

I repaired the missing principal-minor lane by writing and running a deterministic probe for all principal minors of the full `4 x 4` PCL matrix

```text
M = 2I - A - B + (1/2)T = D + (1/2) conjugate(t) t^T.
```

No negative principal minor was found in the coordinate two-plane scan or in `2000` random frame pairs.  The script also verifies the rank-one trace-update determinant identity for every principal subset:

```text
det(D_S + (1/2) conjugate(t_S) t_S^T)
 = det(D_S) + (1/2) t_S^T adj(D_S) conjugate(t_S).
```

The largest checked identity error was `4.440892108477151e-15`.

## Real run output

Command:

```text
python3 research_harness/experiments/LOOP-0009_principal_minor_lane.py \
  --seed 9009 --random-trials 2000 \
  --out research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.json \
  > research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.stdout.log
python3 -m py_compile research_harness/experiments/LOOP-0009_principal_minor_lane.py
```

Summary:

```text
control min eigs: {'product_projection_support_00_10': 0.0, 'diagonal_traceless_support_00_11': 0.0, 'right_product_support_00_01': 0.0}
coordinate negative-pair counts by minor size: {'1': 0, '2': 0, '3': 0, '4': 0}
random negative-frame counts by minor size: {'1': 0, '2': 0, '3': 0, '4': 0}
random min det(M_S) by size: {'1': 1.2084680308569111, '2': 1.6516027614966962, '3': 2.4529810081740915, '4': 3.7146661736564064}
max rank-one-update identity error: 4.440892108477151e-15
```

## What this adds

The rank-one-update identity is exact algebraically and numerically regression-tested, including singular `D_S` cases by using the adjugate polynomial formula rather than `D_S^-1`.  It gives the right certificate shape for every principal-minor route: each minor needs the coupled determinant

```text
det(D_S) + (1/2) t_S^T adj(D_S) conjugate(t_S) >= 0,
```

not a false proof that `D_S >= 0` or `det(D_S) >= 0`.

The coordinate scan retains the equality guardrail: all equality controls have `min_eig(M)=0`, and no coordinate principal minor becomes negative.

## Fail-closed caveats

- This is numerical evidence plus an identity, not a proof of principal-minor nonnegativity.
- Proving all `1x1`, `2x2`, `3x3`, and `4x4` principal minors remains open.
- The crossed scalar/PAL minor is only one subcase; scalar success alone would not prove full PCL.

Artifacts:

- `research_harness/experiments/LOOP-0009_principal_minor_lane.py`
- `research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.json`
- `research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.stdout.log`
