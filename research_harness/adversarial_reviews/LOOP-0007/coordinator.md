# LOOP-0007 Coordinator Report

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_recorded: false
last_updated: 2026-06-03

## Executive summary

LOOP-0007 continued the PCL/PAL attack on the rank-two partial-trace inequality.
The loop focused on the sharp scalar bottleneck isolated in LOOP-0006: the crossed
`2 x 2` PCL principal minor, equivalently the phase-aware PAL two-frame
determinant, with the trace rank-one update retained.

No success condition was met. The loop did not produce a complete proof, did not
produce a certified rank-two positive-gap counterexample, and did not find a
bridge defect. CLAIM-0001 remains open/fail-closed.

Auditor verdict: `FAIL-CLOSED / NOT ACCEPTED`.

## Artifacts

Main lanes:

- `pcl_crossed_minor_lane.md`
- `pal_determinant_lane.md`
- `certified_search_lane.md`

Adversarial review:

- `skeptic.md`
- `auditor.md`

Executable/log artifacts:

- `research_harness/experiments/LOOP-0007_pcl_crossed_minor_probe.py`
- `research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.json`
- `research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.stdout.log`
- `research_harness/experiments/LOOP-0007_pal_determinant_identities.py`
- `research_harness/logs/LOOP-0007_pal_determinant_identities.json`
- `research_harness/logs/LOOP-0007_pal_search_seed7007.json`
- `research_harness/logs/LOOP-0007_pal_search_seed7007.stdout.log`
- `research_harness/experiments/LOOP-0007_certified_search.py`
- `research_harness/logs/LOOP-0007_certified_search_seed7007.json`
- `research_harness/logs/LOOP-0007_certified_search_seed7007.stdout.log`

## What LOOP-0007 established

### 1. Crossed PCL minor lane

The crossed minor lane established two useful exact reductions.

First, the crossed `2 x 2` PCL principal minor is exactly the phase-aware PAL
determinant slice for the pair `(U_1,V_1),(U_2,V_2)`. Thus the immediate crossed
PCL target and the PAL determinant target are the same scalar obstruction, not
merely analogous.

Second, the crossed block has the trace-coupled rank-one-update determinant form

```text
det M_S = det D_S + (1/2) u_S^* adj(D_S) u_S,
```

where `D=2I-A-B`. This keeps the trace update coupled instead of discarding it.
The product equality case blocks the contraction-defect-only route: `det D_S=-1`
there, but the trace update repairs the block to `det M_S=0`.

Verification/probe values from the log:

```text
max_rank_one_update_identity_error = see log
max_pal_block_identity_error = see log
min_delta_cross = see log
min_det_D2 = see log
negative_D2_count = see log
```

No complete proof of `Delta_cross >= 0` was found.

### 2. PAL determinant lane

The PAL lane decomposed the phase-aware PAL block as

```text
K^PAL = K_L + K_R + T_T,
```

where `K_L` and `K_R` are left/right partial-trace contraction-defect blocks and
`T_T` is the trace rank-one update. This gives the exact target
`det(K_L+K_R+T_T) >= 0`, but not a proof.

The lane also recorded guardrails:

- separated Cauchy-Schwarz routes fail because the left/right pieces can be
  indefinite on equality examples;
- all-frame `m>=3` PSD promotion is false, with a matrix-unit obstruction having
  eigenvalues `[-1/2,1,1]`;
- fixed-gauge arbitrary-complex-coefficient overstrengthening remains false.

Verification values from the identity script include roundoff-level residuals and
known obstruction/equality spectra; see `LOOP-0007_pal_determinant_identities.json`.
The PAL regression search found no violation, with optimized best violation near
roundoff (`-1.1268763699945339e-13` in the lane report).

No universal PAL proof was found.

### 3. Certified search lane

The search lane used the original `gap(C)` convention, not merely a compression
eigenvalue. It ran equality regressions, `20000` random rank-two samples, rank-two
SVD-truncated perturbations around equality/control families, and a coordinate
two-unit scan.

Key output:

```text
diag_difference normalized gap = 0.0
product_projection normalized gap = -2.2204460492503136e-16
phase_sparse_control normalized gap = -0.5
random trials = 20000
random best normalized gap = -1.2143877928448128
random positive count tol 1e-10 = 0
coordinate best normalized gap = 0.0
coordinate positive count tol 1e-10 = 0
best perturbation normalized gap = -7.779413143726018e-10
robust_positive_gap_found = False
```

No certified positive-gap rank-two counterexample was found.

## Skeptic/auditor verdict

The skeptic and auditor both reject promotion.

Reasons:

- crossed PCL minor/PAL determinant equivalence is a reduction, not a proof;
- the trace-coupled rank-one update is essential and no SOS/Plucker/Gram
  certificate for it was produced;
- no full `4 x 4` PCL PSD certificate or all-principal-minor certificate was
  produced;
- numerical searches found no positive original gap and cannot prove nonexistence;
- no bridge defect was identified.

Therefore CLAIM-0001 remains open/fail-closed.

## Updated bottleneck

The immediate scalar bottleneck is now sharply identified as the coupled
phase-aware PAL determinant / crossed PCL minor:

```text
D_1 D_2 - |a + conjugate(b)|^2 >= 0,
```

equivalently

```text
det M[{(1,1),(2,2)}] >= 0
```

with the trace rank-one update retained.

A successful next loop must either:

1. prove this coupled scalar inequality by a direct trace-coupled SOS/Plucker,
   Gram, or determinant-defect certificate, then extend it toward full PCL; or
2. bypass the scalar minor with a full `4 x 4` PCL PSD certificate; or
3. produce an explicit certified rank-at-most-two `C` with positive original
   `gap(C)`.

## Recommended LOOP-0008 focus

Run a two-pronged loop:

1. **Certificate lane:** expand the scalar PAL/crossed-minor defect
   `xy-|c|^2 + (1/2)(y|t_1|^2+x|t_2|^2-2 Re(c t_1 conjugate(t_2)))` and search
   for a trace-coupled Plucker/SOS identity under the two-frame orthonormality
   constraints.
2. **Tangent/equality lane:** parameterize the tangent space at the sharp equality
   manifolds, compute the second variation of the original `gap(C)` and/or PAL
   defect, and look for a rigorous local-maximality certificate or an unstable
   direction.

Maintain the corrected partial-trace convention and do not promote numerical
near-zero equality to proof.
