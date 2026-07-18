# LOOP-0008 auditor report

claim: CLAIM-0001-rank-two-partial-trace
role: LOOP-0008 auditor
verdict: FAIL-CLOSED / REJECT LOOP SUCCESS
success_condition_met: false

## Exact verdict

LOOP-0008 is not accepted as a success for CLAIM-0001.

I found no complete proof of `rank(C) <= 2 => gap(C) <= 0`, no certified positive-gap rank-two counterexample, and no accepted bridge defect. The LOOP-0008 artifacts provide useful numerical/regression evidence and identify further obstructions, but they do not close the claim.

Therefore the conservative auditor verdict is fail-closed.

## Artifacts reviewed

Repository root used:

```text
.
```

Reviewed claim/status context:

```text
research_harness/status.json
research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
```

Reviewed LOOP-0008 lane reports:

```text
research_harness/adversarial_reviews/LOOP-0008/scalar_certificate_lane.md
research_harness/adversarial_reviews/LOOP-0008/tangent_equality_lane.md
research_harness/adversarial_reviews/LOOP-0008/full_pcl_search_lane.md
research_harness/adversarial_reviews/LOOP-0008/certificate_lane.md
```

`research_harness/adversarial_reviews/LOOP-0008/skeptic.md` was not present at the auditor's first read because the skeptic/auditor were dispatched concurrently. Controller post-run verification confirms `skeptic.md` is present, nonempty, and agrees with the fail-closed verdict. This race note does not change the audit verdict.

Reviewed scripts/logs:

```text
research_harness/experiments/LOOP-0008_scalar_certificate_probe.py
research_harness/experiments/LOOP-0008_tangent_equality_lane.py
research_harness/experiments/LOOP-0008_full_pcl_search.py
research_harness/logs/LOOP-0008_scalar_certificate_probe_seed8008.json
research_harness/logs/LOOP-0008_scalar_certificate_probe_seed8008.stdout.log
research_harness/logs/LOOP-0008_tangent_equality_seed8008.json
research_harness/logs/LOOP-0008_tangent_equality_seed8008.stdout.log
research_harness/logs/LOOP-0008_full_pcl_search_seed8008.json
research_harness/logs/LOOP-0008_full_pcl_search_seed8008.stdout.log
research_harness/logs/LOOP-0008_full_pcl_rank_one_update_controls.stdout.log
```

## Independent re-run / verification performed

From the repository root I re-ran the key LOOP-0008 scripts with the reported seed/parameters:

```text
python3 research_harness/experiments/LOOP-0008_scalar_certificate_probe.py
python3 research_harness/experiments/LOOP-0008_tangent_equality_lane.py --seed 8008 --random-dirs 5000 --out /tmp/LOOP-0008_tangent_audit.json
python3 research_harness/experiments/LOOP-0008_full_pcl_search.py --seed 8008 --random-trials 3000 --opt-restarts 6 --maxiter 150 --out /tmp/LOOP-0008_full_pcl_audit.json
```

The re-run completed with exit code 0. Summary values matched the reported logs in the material quantities:

```text
scalar:
  status = probe_not_proof
  random samples = 5000
  random min_delta = 1.7774468279460423
  max_trace_update_formula_error = 8.881784197001252e-16
  sparse total = 14400
  sparse min_delta = 0.0
  sparse min_det_D = -1.0
  best optimized delta = 6.455059043026971e-13

tangent/equality:
  success_condition_met = false
  robust_positive_direction_or_gap_found_tol_1e-10 = false
  diag_difference: rank = 2, normalized_gap = 0.0, first variation l2 = 0.0, max q = 0.0, positive second-variation count = 0
  product_projection: rank = 2, normalized_gap = -2.2204460492503136e-16, first variation l2 = 0.0, max q = 0.0, positive second-variation count = 0

full PCL search:
  success_condition_met = false
  robust_pcl_violation_found = false
  coordinate total = 14400
  coordinate negative min-eigenvalue count = 0
  random trials = 3000
  random positive original-gap count = 0
  max gap/rayleigh identity error = 2.6645352591003757e-15
  worst overall min_eig(M) = 0.0
  worst overall original normalized gap = 2.2204460492503126e-16
  optimized best min_eig(M) = 3.2507330161017243e-13
```

The `2.2204460492503126e-16` positive-looking worst original normalized gap is machine roundoff at an equality control, not a certified positive-gap counterexample. It is far below any robust positivity threshold and is not accompanied by exact/interval certification.

## Assessment by success gate

### 1. Complete proof

Not present.

The scalar certificate lane records exact/reproducible identities and a failed natural certificate route, but explicitly does not prove universal scalar nonnegativity `det M_S >= 0`, full PCL PSD, or CLAIM-0001.

The full PCL lane numerically tests `M(U,V) = 2I - A - B + (1/2)T` and checks conversion to original `gap(C)`, but supplies no Hermitian Gram/SOS, Schur-complement, principal-minor, Plucker, or exact certificate proving `M >= 0` for all support planes.

The tangent/equality lane gives floating-point local evidence at two equality controls only. It cannot establish the global rank-two inequality.

### 2. Certified rank-two positive-gap counterexample

Not present.

The scalar and full PCL searches found no robust violation. The full PCL script converts the worst compression eigenvector to an explicit rank-at-most-two `C` and checks original corrected partial traces, but the worst value is equality/roundoff:

```text
rank(C) = 2
normalized_gap(C) = 2.2204460492503126e-16
```

This is not a certified positive gap.

### 3. Accepted bridge defect

Not present.

The lanes identify important guardrails: the trace rank-one update is essential, `D=2I-A-B` can be indefinite on product equality supports, and naive diagonal-wedge polarization does not reproduce the crossed PAL/PCL off-diagonal terms. These are useful obstructions to proof strategies, not an accepted bridge defect that resolves the target claim or invalidates the needed equivalence in a way that satisfies the success condition.

## Auditor conclusion

LOOP-0008 should be recorded as completed but not successful. CLAIM-0001 remains open/fail-closed.

Updated bottleneck:

```text
Prove the trace-coupled scalar PAL / crossed-PCL-minor determinant with the rank-one trace update retained and extend it to a full 4x4 PCL certificate; or produce a full Hermitian Gram/SOS, Schur/principal-minor, Plucker/rank-one-update certificate for universal PCL PSD; or provide an explicit rank-at-most-two C with positive original gap certified beyond floating-point roundoff.
```


## Controller post-run verification

After both reviewer subagents returned, the controller verified `research_harness/adversarial_reviews/LOOP-0008/skeptic.md` exists and rejects all success conditions. Auditor verdict remains `FAIL-CLOSED / REJECT LOOP SUCCESS`.
