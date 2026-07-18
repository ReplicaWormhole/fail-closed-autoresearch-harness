# LOOP-0009 coordinator report

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
completed_at: 2026-06-03T17:59:08+02:00
success_condition_met: none
verdict: no accepted proof, no certified rank-two positive-gap counterexample, no accepted bridge defect

## Executive summary

LOOP-0009 continued the automatic adversarial loop on the rank-two partial-trace inequality. The loop completed the mixed-Plucker, zero-mode, and principal-minor lanes, then ran skeptic and auditor review.

The loop produced useful structure but no promotion result:

1. The mixed-Plucker lane found and regression-tested a genuinely mixed two-frame identity for the crossed PAL/PCL off-diagonal entry.
2. The same lane showed that the direct mixed-vector Cauchy/Gram norm-domination route is false on the actual orthonormal frame constraint manifold.
3. The repaired zero-mode lane confirmed local numerical nonpositivity at the known equality controls, with zero-mode counts `9` and `13`, but did not classify equality manifolds.
4. The repaired principal-minor lane verified the correct trace rank-one-update determinant-lemma shape for every principal subset of the full `4 x 4` PCL matrix and found no negative minors in coordinate/random tests, but did not prove nonnegativity universally.
5. Skeptic and auditor both rejected promotion and recorded fail-closed status.

## Lanes completed

### 1. Mixed Plucker lane

Report:

```text
research_harness/adversarial_reviews/LOOP-0009/mixed_plucker_lane.md
```

Executable/log artifacts:

```text
research_harness/experiments/LOOP-0009_mixed_plucker_probe.py
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.json
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.stdout.log
```

Key values:

```text
random samples: 5000
max mixed offdiag identity error: 8.441528768080324e-17
sparse coordinate max identity error: 0.0
optimized near-equality identity error: 2.2887833992611187e-16
max same-pair polarization mismatch: 0.47081642102929433
sparse min(D_1-N_12): -1.5
sparse min(D_2-N_21): -1.5
```

Coordinator interpretation: the identity repairs the LOOP-0008 same-pair polarization obstruction at the off-diagonal bookkeeping level. But the direct Cauchy route using `N_12 <= D_1` and `N_21 <= D_2` is rejected because those inequalities are false on constrained frames.

### 2. Zero-mode lane

Report:

```text
research_harness/adversarial_reviews/LOOP-0009/zero_mode_lane.md
```

Executable/log artifacts:

```text
research_harness/experiments/LOOP-0009_zero_mode_classification.py
research_harness/logs/LOOP-0009_zero_mode_classification.json
research_harness/logs/LOOP-0009_zero_mode_classification.stdout.log
```

Key values:

```text
diag_difference: zero_count=9, positive_count=0, eigmax=0.0
product_projection: zero_count=13, positive_count=0, eigmax=0.0
```

Coordinator interpretation: this supports the working hypothesis that observed zero modes are equality/symmetry directions, but it is numerical local evidence only. It is not a global proof and not an exact equality classification.

### 3. Principal-minor / rank-one-update lane

Report:

```text
research_harness/adversarial_reviews/LOOP-0009/principal_minor_lane.md
```

Executable/log artifacts:

```text
research_harness/experiments/LOOP-0009_principal_minor_lane.py
research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.json
research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.stdout.log
```

Key values:

```text
control min eigs: product/right/diagonal equality controls all 0.0
coordinate negative-pair counts by minor size: {'1': 0, '2': 0, '3': 0, '4': 0}
random negative-frame counts by minor size: {'1': 0, '2': 0, '3': 0, '4': 0}
random min det(M_S) by size: {'1': 1.2084680308569111, '2': 1.6516027614966962, '3': 2.4529810081740915, '4': 3.7146661736564064}
max rank-one-update identity error: 4.440892108477151e-15
```

Coordinator interpretation: the useful exact shape for every principal-minor route is

```text
det(D_S + (1/2) conjugate(t_S) t_S^T)
 = det(D_S) + (1/2) t_S^T adj(D_S) conjugate(t_S) >= 0.
```

This must retain the trace-coupled update. Attempts to prove `D_S >= 0` or `det(D_S) >= 0` remain rejected.

## Adversarial reviews

Skeptic report:

```text
research_harness/adversarial_reviews/LOOP-0009/skeptic.md
```

Auditor report:

```text
research_harness/adversarial_reviews/LOOP-0009/auditor.md
```

Both reviews reject LOOP-0009 success. The auditor compile check exited `0` for all three LOOP-0009 scripts:

```text
python3 -m py_compile   research_harness/experiments/LOOP-0009_mixed_plucker_probe.py   research_harness/experiments/LOOP-0009_zero_mode_classification.py   research_harness/experiments/LOOP-0009_principal_minor_lane.py
```

## Fail-closed promotion gates

- Complete proof of CLAIM-0001: failed.
- Certified rank-two positive-gap counterexample: failed.
- Accepted bridge defect/bypass: failed.
- Scalar PAL/crossed-minor proof: failed.
- Full `4 x 4` PCL principal-minor or Gram/SOS proof: failed.
- Exact equality-manifold classification: failed.

## Updated bottleneck

The active bottleneck remains a trace-coupled full-PCL certificate. The next loop should not repeat broad random search as the main effort. It should attack one of these precise subtargets:

1. Derive an exact determinant-level SOS/Gram certificate for the crossed scalar PAL/PCL minor that uses the mixed off-diagonal identity but cancels the false mixed-norm domination terms.
2. Attack all principal minors through the coupled adjugate formula `det(D_S)+(1/2)t_S^T adj(D_S)conjugate(t_S)`; start with all `2 x 2` minor orbits, then `3 x 3` and `4 x 4`.
3. Construct an explicit trace-coupled Schur-complement or Hermitian Gram certificate for the full `4 x 4` matrix `M` directly.
4. Symbolically classify the zero modes at product and diagonal equality controls to decide whether they are exactly equality/symmetry directions.

## Coordinator verdict

Fail-closed. CLAIM-0001 remains open/unproved and not refuted. LOOP-0009 should be counted as completed, but not successful.
