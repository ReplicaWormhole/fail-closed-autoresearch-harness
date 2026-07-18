# LOOP-0009 auditor review for CLAIM-0001

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
role: auditor
success_condition_met: none
verdict: no accepted proof, no certified rank-two positive-gap counterexample, no accepted bridge defect

## Executive verdict

LOOP-0009 is fail-closed.

The reviewed LOOP-0009 artifacts compile and their recorded logs exist. They add useful diagnostics:

1. a mixed two-frame Plucker identity for the crossed PAL/PCL off-diagonal entry, verified numerically to roundoff;
2. a concrete obstruction to the direct mixed-vector Cauchy/SOS norm-domination route;
3. repaired zero-mode diagnostics at the known equality controls;
4. a principal-minor/rank-one-update diagnostic lane for the full `4 x 4` PCL matrix.

However, none of these artifacts satisfies a promotion gate for CLAIM-0001. There is no complete proof of the rank-two partial-trace inequality, no certified positive original rank-two gap, and no accepted bridge defect showing that CLAIM-0001 can be bypassed or is not needed.

The loop should therefore be recorded as completed but unsuccessful. The current bottleneck remains a trace-coupled full-PCL certificate, a universal PAL/crossed-minor proof together with a complete extension to CLAIM/PCL, or a certified rank-two positive-gap counterexample.

## Exact commands and checks performed by auditor

Repository root:

```text
.
```

Compile check run by auditor:

```text
python3 -m py_compile \
  research_harness/experiments/LOOP-0009_mixed_plucker_probe.py \
  research_harness/experiments/LOOP-0009_zero_mode_classification.py \
  research_harness/experiments/LOOP-0009_principal_minor_lane.py
```

Result: exit code `0` with no output. All three LOOP-0009 experiment scripts compile.

Artifacts and logs read by auditor:

```text
research_harness/adversarial_reviews/LOOP-0009/mixed_plucker_lane.md
research_harness/adversarial_reviews/LOOP-0009/zero_mode_lane.md
research_harness/adversarial_reviews/LOOP-0009/principal_minor_lane.md
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.stdout.log
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.json
research_harness/logs/LOOP-0009_zero_mode_classification.stdout.log
research_harness/logs/LOOP-0009_zero_mode_classification.json
research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.stdout.log
research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.json
research_harness/status.json
research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
```

Note: the delegated context named `research_harness/claim_cards/CLAIM-0001.md`, but the repository claim card present on disk is `CLAIM-0001-rank-two-partial-trace.md`; that file was reviewed.

## Lane audit

### 1. Mixed Plucker lane

Reviewed report:

```text
research_harness/adversarial_reviews/LOOP-0009/mixed_plucker_lane.md
```

Reviewed run artifacts:

```text
research_harness/experiments/LOOP-0009_mixed_plucker_probe.py
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.stdout.log
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.json
```

Reported command:

```text
python3 research_harness/experiments/LOOP-0009_mixed_plucker_probe.py \
  --seed 9009 --samples 5000 --opt-starts 6 --maxiter 120 \
  | tee research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.stdout.log
```

Key log values reviewed:

```text
status: mixed_identity_found_but_simple_cauchy_ansatz_obstructed_not_proof
random samples: 5000
max mixed offdiag identity error: 8.441528768080324e-17
max same-pair polarization mismatch: 0.47081642102929433
random min delta: 1.6516027614966962
sparse coordinate total: 14400
sparse min delta: 0.0
local optimized best delta: 6.034130765841868e-13
random min D1-N12: -0.41194477765578674
random min D2-N21: -0.4054262460823934
sparse min D1-N12: -1.5
sparse min D2-N21: -1.5
sparse negative D1-N12 count: 5260
sparse negative D2-N21 count: 5260
```

Audit conclusion: the mixed off-diagonal identity is a useful diagnostic and appears numerically consistent. But the same lane explicitly refutes the simple mixed-Gram/Cauchy norm-domination subclaim by negative margins on the actual orthonormal constraint manifold. This is not a scalar PAL proof, not a full PCL proof, and not a counterexample to CLAIM-0001. The near-zero optimized scalar determinant is equality/roundoff, not a positive-gap certificate.

### 2. Zero-mode classification lane

Reviewed report:

```text
research_harness/adversarial_reviews/LOOP-0009/zero_mode_lane.md
```

Reviewed run artifacts:

```text
research_harness/experiments/LOOP-0009_zero_mode_classification.py
research_harness/logs/LOOP-0009_zero_mode_classification.stdout.log
research_harness/logs/LOOP-0009_zero_mode_classification.json
```

Reported command:

```text
python3 research_harness/experiments/LOOP-0009_zero_mode_classification.py \
  --out research_harness/logs/LOOP-0009_zero_mode_classification.json \
  > research_harness/logs/LOOP-0009_zero_mode_classification.stdout.log
python3 -m py_compile research_harness/experiments/LOOP-0009_zero_mode_classification.py
```

Key log values reviewed:

```text
diag_difference: zero_count=9, positive_count=0, eigmax=0.0
product_projection: zero_count=13, positive_count=0, eigmax=0.0
success_condition_met: false
caveat: Numerical tangent-zero diagnostics only; not an equality classification proof.
```

Audit conclusion: this lane supports the previous numerical observation that the known equality controls are stationary and have no positive Hessian directions in the sampled/constructed tangent model. It is local numerical evidence only. It does not classify equality manifolds exactly, prove global nonpositivity, or certify a counterexample.

### 3. Principal-minor / rank-one-update lane

Reviewed report:

```text
research_harness/adversarial_reviews/LOOP-0009/principal_minor_lane.md
```

Reviewed run artifacts:

```text
research_harness/experiments/LOOP-0009_principal_minor_lane.py
research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.stdout.log
research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.json
```

Reported command:

```text
python3 research_harness/experiments/LOOP-0009_principal_minor_lane.py \
  --seed 9009 --random-trials 2000 \
  --out research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.json \
  > research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.stdout.log
python3 -m py_compile research_harness/experiments/LOOP-0009_principal_minor_lane.py
```

Key log values reviewed:

```text
control min eigs: {'product_projection_support_00_10': 0.0, 'diagonal_traceless_support_00_11': 0.0, 'right_product_support_00_01': 0.0}
coordinate negative-pair counts by minor size: {'1': 0, '2': 0, '3': 0, '4': 0}
random negative-frame counts by minor size: {'1': 0, '2': 0, '3': 0, '4': 0}
random min det(M_S) by size: {'1': 1.2084680308569111, '2': 1.6516027614966962, '3': 2.4529810081740915, '4': 3.7146661736564064}
max rank-one-update identity error: 4.440892108477151e-15
success_condition_met: false
caveat: All results are numerical diagnostics/regressions; no principal-minor proof or certified counterexample.
```

Audit conclusion: this lane verifies the correct rank-one trace-update determinant identity numerically and confirms that tested coordinate/random principal minors did not go negative. It also preserves the guardrail that `D` alone can have negative determinants while the trace update repairs equality cases. But no all-principal-minor certificate is supplied. Numerical absence of negative minors is not a proof of full PCL/CLAIM.

## Promotion gates

### Gate A: Complete proof of CLAIM-0001

Required: a proof with all quantifiers intact for arbitrary complex rank-at-most-two `C in M_4(C) tensor M_4(C)`, with no hidden Hermitian, positive, normal, commuting, vector-state, or convexity assumptions; or an equivalent universal proof of PCL/PAL together with a complete derivation to CLAIM-0001.

Result: failed.

Reason: LOOP-0009 provides identities and diagnostics, but no global proof. The mixed Plucker route explicitly reports that its simplest Cauchy/SOS norm-domination subclaim is false. The principal-minor lane gives a determinant-lemma shape and numerical regressions but no universal principal-minor proof. The zero-mode lane is local and numerical.

### Gate B: Certified rank-two positive-gap counterexample

Required: an explicit rank-at-most-two operator `C`, with independently checkable exact or certified interval arithmetic, such that

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2
  - 2 ||C||_F^2 - (1/2)|tr C|^2 > 0
```

by a positive margin exceeding numerical error.

Result: failed.

Reason: no LOOP-0009 lane reports a positive original rank-two gap. The mixed Plucker optimized scalar value is near equality (`best_delta = 6.034130765841868e-13`, with `delta` being the nonnegative determinant-side quantity), not a positive-gap counterexample. Principal-minor and zero-mode logs report no robust violations.

### Gate C: Accepted bridge defect

Required: a demonstrated defect in the bridge/reduction status sufficient to close or redirect CLAIM-0001, e.g. showing that CLAIM-0001 is not needed for the downstream target, that an asserted equivalence is false in a consequential way, or that a weaker replacement has been proved and accepted.

Result: failed.

Reason: LOOP-0009 found a defect in a proposed proof ansatz (simple mixed-vector Cauchy norm domination), not a defect in the CLAIM-0001 bridge itself. Prior status still records CLAIM-0001/PAL/PCL as the active bottleneck/equivalent formulations. No accepted bypass or weaker bridge replacement is supplied.

## Artifact list

Reports reviewed:

```text
research_harness/adversarial_reviews/LOOP-0009/mixed_plucker_lane.md
research_harness/adversarial_reviews/LOOP-0009/zero_mode_lane.md
research_harness/adversarial_reviews/LOOP-0009/principal_minor_lane.md
```

Experiment scripts verified to compile:

```text
research_harness/experiments/LOOP-0009_mixed_plucker_probe.py
research_harness/experiments/LOOP-0009_zero_mode_classification.py
research_harness/experiments/LOOP-0009_principal_minor_lane.py
```

Logs reviewed:

```text
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.stdout.log
research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.json
research_harness/logs/LOOP-0009_zero_mode_classification.stdout.log
research_harness/logs/LOOP-0009_zero_mode_classification.json
research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.stdout.log
research_harness/logs/LOOP-0009_principal_minor_lane_seed9009.json
```

Context reviewed:

```text
research_harness/status.json
research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
```

Auditor-created artifact:

```text
research_harness/adversarial_reviews/LOOP-0009/auditor.md
```

## Final fail-closed decision

Do not mark CLAIM-0001 successful from LOOP-0009.

Accepted outcomes:

```text
complete proof: no
certified rank-two positive-gap counterexample: no
accepted bridge defect: no
```

Recommended next bottleneck statement:

```text
Produce a trace-coupled full-PCL certificate, an all-quantifier PAL/crossed-minor proof extended to CLAIM/PCL, or a certified rank-two positive-gap counterexample. The simple mixed Plucker Cauchy norm-domination route is now blocked and should not be reused as a proof route.
```
