# LOOP-0007 Auditor Report

claim: CLAIM-0001-rank-two-partial-trace
role: LOOP-0007 auditor
verdict: FAIL-CLOSED / NOT ACCEPTED
success_condition_met: no
last_updated: 2026-06-03

## Success verdict

LOOP-0007 is not accepted as a success for CLAIM-0001.

I found no complete proof of `rank(C)<=2 => gap(C)<=0`, no certified positive-gap rank-two counterexample, and no accepted bridge defect. The loop produced useful algebraic reductions, guardrail examples, and reproducible numerical regressions, but all lanes explicitly remain incomplete or numerical-only.

Therefore the conservative auditor decision is:

```text
FAIL-CLOSED: CLAIM-0001 remains open/unproved/unrefuted.
```

## Artifacts reviewed

Required top-level/context artifacts:

- `research_harness/status.json`
  - Reports `active_claim: CLAIM-0001`, `success: false`, `last_completed_loop: LOOP-0006`, `next_loop_number: 7`.
  - Current bottleneck before LOOP-0007: prove PCL compression PSD, prove PAL determinant inequality, or certify positive-gap rank-two counterexample.
- `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`
  - Confirms current status is proof gap/open through LOOP-0006.
  - Defines target inequality and success gates.

Required LOOP-0007 review artifacts:

- `research_harness/adversarial_reviews/LOOP-0007/pcl_crossed_minor_lane.md`
- `research_harness/adversarial_reviews/LOOP-0007/pal_determinant_lane.md`
- `research_harness/adversarial_reviews/LOOP-0007/certified_search_lane.md`
- `research_harness/adversarial_reviews/LOOP-0007/skeptic.md`
  - Present after the concurrent skeptic/auditor run. Controller verification confirms the skeptic report also rejects all success conditions and identifies the same coupled PAL/crossed-PCL-minor bottleneck. The original audit was already fail-closed; this post-run verification removes the process deficiency without changing the verdict.

LOOP-0007 scripts/logs inspected:

- `research_harness/experiments/LOOP-0007_pal_determinant_identities.py`
- `research_harness/logs/LOOP-0007_pal_determinant_identities.json`
- `research_harness/experiments/LOOP-0007_pcl_crossed_minor_probe.py`
- `research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.json`
- `research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.stdout.log`
- `research_harness/experiments/LOOP-0007_certified_search.py`
- `research_harness/logs/LOOP-0007_certified_search_seed7007.json`
- `research_harness/logs/LOOP-0007_certified_search_seed7007.stdout.log`
- `research_harness/experiments/LOOP-0004_pal_search.py` as used by LOOP-0007
- `research_harness/logs/LOOP-0007_pal_search_seed7007.json`
- `research_harness/logs/LOOP-0007_pal_search_seed7007.stdout.log`

## Re-run checks performed

I re-ran the key LOOP-0007 scripts from the repository root `.`.

### PAL determinant identity script

Command re-run:

```text
python3 research_harness/experiments/LOOP-0007_pal_determinant_identities.py
```

Key reproduced values:

```text
identity_random_m2.max_identity_residual = 4.440892098500626e-16
identity_random_m2.min_det_slack_m2 = 1.7189848517707407
identity_random_m3.max_identity_residual = 2.220446049250313e-16
m3_all_frame_obstruction eig(K) = [-0.5000000000000001, 1.0, 1.0]
loop0002_fixed_gauge_witness eig(fixed_gauge_K) = [-1.0, 2.0]
```

Audit interpretation: the identity/regression data are reproducible and support the reported algebraic bookkeeping/guardrails. They do not prove the universal two-frame determinant inequality.

### PCL crossed-minor probe

Command re-run:

```text
python3 research_harness/experiments/LOOP-0007_pcl_crossed_minor_probe.py
```

Key reproduced values:

```text
random samples = 2000
min_delta_cross = 1.7189848517707407 at sample 137
min_det_D2 = 1.5892325445991295 at sample 137
max_rank_one_update_identity_error = 8.881784197001252e-16
max_pal_block_identity_error = 8.881784197001252e-16
coordinate two-plane pairs = 14400
coordinate min_delta_cross = 0.0
coordinate min_det_D2 = -1.0
coordinate negative_D2_count = 48
```

Audit interpretation: the rank-one-update and PAL-slice identities are numerically verified to roundoff in the script. The coordinate examples also verify that the contraction-defect-only determinant route is false (`det D2 = -1.0`). This is useful obstruction/reduction evidence, but it is not a proof of `Delta_cross >= 0`, and even one crossed minor would not be a full PCL certificate.

### Certified original-gap search

Command re-run:

```text
python3 research_harness/experiments/LOOP-0007_certified_search.py \
  --seed 7007 --random-trials 20000 --perturb-trials 2000 \
  --out /tmp/LOOP-0007_certified_search_rerun.json
```

Key reproduced values:

```text
equality normalized gaps:
  diag_difference = 0.0
  product_projection = -2.2204460492503136e-16
  phase_sparse_control = -0.5
random_rank2 trials = 20000
random best normalized gap = -1.2143877928448128
random positive count tol 1e-10 = 0
coordinate best normalized gap = 0.0
coordinate positive count tol 1e-10 = 0
best perturbation normalized gap = -7.779413143726018e-10
robust_positive_gap_found = false
```

Audit interpretation: the search was reproducible and found no positive rank-two gap. It is explicitly a numerical/regression search, not a certificate that no counterexample exists.

### PAL search regression log

Inspected existing log:

```text
research_harness/logs/LOOP-0007_pal_search_seed7007.json
```

Key recorded values:

```text
matrix-unit best violation = 0.0
random best violation = -1.6873856119785282
optimized best violation = -1.1268763699945339e-13
optimizer_success = false
```

Audit interpretation: no robust PAL violation is recorded. The near-zero optimized value is consistent with equality/roundoff. The legacy field `max_original_gap_grid = 0.7984793214128977` is not accepted as evidence for a counterexample because the LOOP-0007 PAL lane itself warns that this field predates the corrected LOOP-0006 partial-trace convention and was not used as success evidence.

## Lane-by-lane audit decision

### PCL crossed-minor lane

Accepted only as a partial reduction/guardrail lane.

Verified useful outputs:

- Crossed PCL minor is identified with the PAL determinant slice.
- Exact rank-one-update determinant identity is regression-checked to roundoff.
- The separated contraction-defect route is blocked by exact sparse examples (`det D2=-1`, repaired to `det M2=0`).

Not accepted as success:

- No proof of `Delta_cross >= 0` for all frames.
- No proof of all `2 x 2`, `3 x 3`, or full `4 x 4` PCL PSD conditions.
- No counterexample.

### PAL determinant lane

Accepted only as an identity/guardrail lane.

Verified useful outputs:

- `K^PAL = KL + KR + TT` decomposition is implemented and regression-checked.
- Guardrails show separated left/right Cauchy-Schwarz routes and all-frame `m>=3` PSD promotion are false.
- LOOP-0002 fixed-gauge obstruction remains a false strengthening, while the phase-aware block is sharp.

Not accepted as success:

- No proof of `det(KL+KR+TT) >= 0` for all orthonormal two-frames.
- No SOS certificate.
- No counterexample.

### Certified search lane

Accepted only as reproducible negative numerical evidence.

Verified useful outputs:

- Equality controls reproduce zero/nonpositive gaps.
- Random rank-two, equality perturbation, and coordinate scans found no robust positive gap.

Not accepted as success:

- Search is not exhaustive or certified in interval/rational/high-precision arithmetic.
- No explicit positive-gap `16 x 16` rank-at-most-two matrix was produced.

## Conservative conclusion

The success condition for LOOP-0007 required one of:

1. a complete proof of CLAIM-0001;
2. a certified positive-gap rank-two counterexample;
3. an accepted bridge defect.

None is present. The reviewed artifacts themselves repeatedly state fail-closed/no proof/no counterexample, and my re-runs reproduce only regression/identity values, not a certificate.

Final auditor verdict:

```text
LOOP-0007_FAIL_CLOSED_NOT_ACCEPTED
```

## Updated bottleneck

The updated bottleneck remains essentially the same but sharper:

```text
Prove the coupled phase-aware PAL two-frame determinant inequality
D1*D2 - |z|^2 >= 0, equivalently certify the crossed PCL 2x2 minor with the trace rank-one update included; then extend/translate to a complete route for CLAIM-0001, either via universal PAL/SVD or via full PCL PSD. Alternatively, produce a certified original-convention rank-at-most-two positive-gap counterexample.
```

More concretely, the next fail-closed subtargets are:

1. Find a direct two-frame SOS/mixed-discriminant certificate for the coupled determinant `det(KL+KR+TT) >= 0`, using the orthogonality constraints rather than separated `KL`/`KR` PSD claims.
2. In PCL language, certify not only the crossed `2 x 2` block but a full Hermitian `4 x 4` PSD certificate for `M(U,V)=2I_4-A-B+(1/2)T` on `Gr(2,16) x Gr(2,16)`.
3. If searching numerically, record an explicit candidate `C` and verify rank/gap with independent high-precision or exact arithmetic before claiming counterexample success.


## Controller post-run verification

The concurrently dispatched skeptic report exists and was verified after the auditor write. It agrees that LOOP-0007 has no proof, no certified counterexample, and no bridge-defect success. Auditor verdict remains `FAIL-CLOSED / NOT ACCEPTED`.
