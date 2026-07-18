# LOOP-0010 auditor review for CLAIM-0001

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
role: auditor
success_condition_met: none
verdict: no accepted proof, no certified rank-two positive-gap counterexample, no accepted bridge defect

## Executive verdict

LOOP-0010 is fail-closed.

I verified that the three LOOP-0010 experiment scripts compile and that their referenced stdout/JSON logs exist. The artifacts record useful negative/diagnostic information:

1. the scalar crossed-minor lane records the exact mixed-Gram/Cauchy-minus-exchange bookkeeping identity and obstructs the simple determinant-level ansatz `D1 D2 >= N12 N21`;
2. the full PCL coordinate-orbit lane checks a finite coordinate-support principal-minor atlas and shows the trace rank-one update repairs coordinate cases where the defect matrix `D` alone has negative determinants;
3. the zero-mode symbolic lane classifies all numerical zero modes at the product-projection control but leaves 4 zero dimensions unclassified at the diagonal-difference control.

None of these reaches a promotion gate for CLAIM-0001. There is no complete global proof of the rank-two partial-trace inequality, no certified positive original rank-two gap counterexample, and no accepted bridge defect replacing or bypassing the active claim.

## Exact commands and checks performed by auditor

Repository root:

```text
.
```

Compile check run by auditor:

```text
python3 -m py_compile research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py
```

Result: exit code `0` with no output. All three LOOP-0010 experiment scripts compile.

Artifacts and logs read by auditor:

```text
research_harness/adversarial_reviews/LOOP-0010/scalar_trace_coupled_sos_lane.md
research_harness/adversarial_reviews/LOOP-0010/full_pcl_certificate_lane.md
research_harness/adversarial_reviews/LOOP-0010/zero_mode_symbolic_lane.md
research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py
research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py
research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py
research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.stdout.log
research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.json
research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.stdout.log
research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.json
research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.stdout.log
research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.json
research_harness/AUTOLOOP.md
```

Note: the scalar report is named `scalar_trace_coupled_sos_lane.md` in the task context. Its actual contents title the lane as the LOOP-0010 scalar crossed-minor certificate lane.

## Lane audit

### 1. Scalar trace-coupled / crossed-minor SOS lane

Reviewed report:

```text
research_harness/adversarial_reviews/LOOP-0010/scalar_trace_coupled_sos_lane.md
```

Reviewed run artifacts:

```text
research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py
research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.stdout.log
research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.json
```

Reported command in the lane report:

```text
python research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py --samples 3000 --opt-starts 6 --maxiter 120 2>&1 | tee research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.stdout.log
```

Key reviewed log values:

```text
status: exact_cauchy_minus_exchange_identity_recorded; determinant_level_simple_exchange_product_ansatz_obstructed; no proof_or_counterexample
coordinate_min_delta: 0.0
coordinate_min_exchange_product_margin: -3.75
coordinate_positive_exchange_penalty_count: 6848
random_min_delta: 1.8376015909653387 at sample 1989
random_min_exchange_product_margin: -0.9634774182502084 at sample 2226
random_max_penalty_minus_slack: -1.837601590965339 at sample 1989
local min_delta: 3.9613078512756795e-13
local min_exchange_product_margin: -3.7499999999888525
local max_penalty_minus_slack objective value: 8.313350008393172e-13
```

Audit conclusion: this lane is internally consistent as a diagnostic. It records the determinant-level split

```text
Delta = (N12 N21 - |<W12,W21>|^2) - (N12 N21 - D1 D2)
```

and gives coordinate obstructions to the simple strengthening `D1 D2 >= N12 N21`, including the `traceless_LOOP9` control with margin `-3.75` and exact `Delta = 0.0`. That obstruction is useful, but it is not a proof of the scalar crossed minor, not a full PCL certificate, and not a rank-two original-gap counterexample. The local value `max_penalty_minus_slack = 8.313350008393172e-13` is roundoff/equality-scale and is not certified as a violation.

### 2. Full PCL coordinate-orbit / principal-minor lane

Reviewed report:

```text
research_harness/adversarial_reviews/LOOP-0010/full_pcl_certificate_lane.md
```

Reviewed run artifacts:

```text
research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py
research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.stdout.log
research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.json
```

Reported commands in the lane report:

```text
python3 research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py   > research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.stdout.log
python3 -m py_compile research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py
```

Key reviewed log values:

```text
max_update_identity_error: 8.881784197001252e-16
size 1: total=57600, negative_detM=0, negative_detD=0, min_detM=0.5, min_detD=0.0
size 2: total=86400, negative_detM=0, negative_detD=48, min_detM=0.0, min_detD=-1.0
size 3: total=57600, negative_detM=0, negative_detD=96, min_detM=0.0, min_detD=-1.0
size 4: total=14400, negative_detM=0, negative_detD=48, min_detM=0.0, min_detD=-1.0
```

Audit conclusion: this lane verifies a finite coordinate-support atlas and the determinant rank-one-update identity to roundoff. It also gives a clear guardrail: `D` alone is not a valid certificate target, since coordinate cases have negative `det(D_S)` for minor sizes 2, 3, and 4. But the lane explicitly states it is a finite coordinate-support diagnostic only. It does not cover arbitrary complex two-frames and therefore does not prove full PCL or CLAIM-0001.

### 3. Zero-mode symbolic classification lane

Reviewed report:

```text
research_harness/adversarial_reviews/LOOP-0010/zero_mode_symbolic_lane.md
```

Reviewed run artifacts:

```text
research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py
research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.stdout.log
research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.json
```

Reported commands in the lane report:

```text
python3 -m py_compile research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py
python3 research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py \
  --out research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.json \
  > research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.stdout.log
```

Key reviewed log values:

```text
diag_difference: zero_count=9, positive_count=0, all_candidate_contains_zero_space=false, classified_dim=5, unclassified_dim=4, max_residual=0.7071067811865475, min_principal_cosine=0.0
product_projection: zero_count=13, positive_count=0, all_candidate_contains_zero_space=true, classified_dim=13, unclassified_dim=0, max_residual=2.220446049250313e-16, min_principal_cosine=1.0
```

Audit conclusion: this is useful local evidence about equality controls. It fully explains the product-projection numerical zero space by the explicit candidate span, but it does not fully classify the diagonal-difference zero space. More importantly, it is a local floating-point Hessian/tangent-space diagnostic, not a global inequality proof and not a counterexample certificate.

## Promotion gates

### Gate A: Complete proof of CLAIM-0001

Required: a proof for arbitrary complex rank-at-most-two `C` of the original rank-two partial-trace inequality, with all quantifiers intact and without hidden Hermitian, normal, positive, commuting, fixed-gauge, convexity, or density assumptions; or an equivalent universal PCL/PAL proof plus a complete derivation back to CLAIM-0001.

Result: failed.

Reason: LOOP-0010 provides identities, finite atlases, and local classifications only. The scalar lane explicitly says it is not a proof and found no SOS/Gram sub-slack decomposition. The full PCL lane is finite coordinate support only. The zero-mode lane is local and partly unclassified.

### Gate B: Certified rank-two positive-gap counterexample

Required: an explicit reconstructable rank-at-most-two operator `C`, independently checked with exact or certified interval arithmetic, satisfying

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 - 2 ||C||_F^2 - (1/2)|tr C|^2 > 0
```

by a positive margin exceeding numerical error.

Result: failed.

Reason: no LOOP-0010 artifact reports a positive original rank-two gap. The scalar/local near-zero values are equality/roundoff-scale diagnostics, not certified original-gap counterexamples. The PCL coordinate atlas reports no negative coordinate principal minors of `M`, and the zero-mode lane reports no positive Hessian directions at the tested controls.

### Gate C: Accepted bridge defect

Required: a precise mathematical defect in the active bridge/reduction sufficient to replace, bypass, or close CLAIM-0001, accepted by the auditor.

Result: failed.

Reason: LOOP-0010 identifies defects in proof ansatzes (`D1D2 >= N12N21`, and `D`-alone principal-minor positivity), not a defect in the active CLAIM-0001 bridge itself. No accepted replacement target or bypass is supplied.

## Artifact list

Reports reviewed:

```text
research_harness/adversarial_reviews/LOOP-0010/scalar_trace_coupled_sos_lane.md
research_harness/adversarial_reviews/LOOP-0010/full_pcl_certificate_lane.md
research_harness/adversarial_reviews/LOOP-0010/zero_mode_symbolic_lane.md
```

Experiment scripts checked:

```text
research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py
research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py
research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py
```

Logs reviewed:

```text
research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.stdout.log
research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.json
research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.stdout.log
research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.json
research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.stdout.log
research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.json
```

New artifact written by auditor:

```text
research_harness/adversarial_reviews/LOOP-0010/auditor.md
```

## Final decision

Do not promote LOOP-0010 to success.

Record LOOP-0010 as `completed_fail_closed` for CLAIM-0001. The active claim remains open/fail-closed. The next useful work should target either a genuinely universal trace-coupled PCL/principal-minor certificate, a scalar crossed-minor proof with a non-circular sub-slack decomposition and a valid bridge to the original claim, an exact classification of remaining equality zero modes, or a certified rank-two positive-gap counterexample.
