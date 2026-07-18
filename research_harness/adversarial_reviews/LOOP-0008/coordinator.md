# LOOP-0008 Coordinator Report

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_recorded: false
last_updated: 2026-06-03

## Executive summary

LOOP-0008 continued the adversarial attack on the rank-two partial-trace
inequality. It ran three main lanes:

1. a scalar certificate lane for the coupled PAL/crossed-PCL determinant;
2. a tangent/equality lane around the known sharp equality controls;
3. a full `4 x 4` PCL search lane beyond the scalar crossed minor.

No success condition was met. LOOP-0008 did not produce a complete proof, did not
produce a certified rank-two positive-gap counterexample, and did not identify a
bridge defect. CLAIM-0001 remains open/fail-closed.

Skeptic/auditor verdict: `FAIL-CLOSED / REJECT LOOP SUCCESS`.

## Artifacts

Main lanes:

- `scalar_certificate_lane.md`
- `tangent_equality_lane.md`
- `full_pcl_search_lane.md`

Adversarial review:

- `skeptic.md`
- `auditor.md`

Executable/log artifacts:

- `research_harness/experiments/LOOP-0008_scalar_certificate_probe.py`
- `research_harness/logs/LOOP-0008_scalar_certificate_probe_seed8008.json`
- `research_harness/logs/LOOP-0008_scalar_certificate_probe_seed8008.stdout.log`
- `research_harness/experiments/LOOP-0008_tangent_equality_lane.py`
- `research_harness/logs/LOOP-0008_tangent_equality_seed8008.json`
- `research_harness/logs/LOOP-0008_tangent_equality_seed8008.stdout.log`
- `research_harness/experiments/LOOP-0008_full_pcl_search.py`
- `research_harness/logs/LOOP-0008_full_pcl_search_seed8008.json`
- `research_harness/logs/LOOP-0008_full_pcl_search_seed8008.stdout.log`
- `research_harness/logs/LOOP-0008_full_pcl_rank_one_update_controls.stdout.log`

## What LOOP-0008 established

### 1. Scalar certificate lane

The scalar lane attacked the immediate PAL/crossed-PCL target

```text
D_1 D_2 - |a + conjugate(b)|^2 >= 0,
```

equivalently `det M[{(1,1),(2,2)}] >= 0`, retaining the trace rank-one update.
It did not find a complete scalar certificate, but it established two useful
constraints on future proofs.

First, the trace-update determinant expansion and one-pair diagonal wedge/SOS
identities were verified to roundoff:

```text
random samples = 5000
random min_delta = 1.7774468279460423
random min_det_D = 1.552491745021106
max trace-update formula error = 8.881784197001252e-16
max one-pair wedge diagonal error = 1.5543122344752192e-15
```

Second, the lane found a concrete obstruction to a naive polarization route:

the one-pair row/column wedge SOS identities do not polarize directly into the
crossed off-diagonal PAL/PCL entry. The measured mismatch was

```text
max naive wedge bilinear mismatch = 0.295153648209067
```

Coordinate enumeration again confirmed the contraction-defect-only determinant
route is false:

```text
coordinate pairs = 14400
coordinate min_delta = 0.0
coordinate min_det_D = -1.0
coordinate negative_det_D_count = 48
local optimization best_delta = 6.455059043026971e-13
```

No scalar proof or scalar counterexample was found.

### 2. Tangent/equality lane

The tangent lane parameterized the rank-two tangent space at two sharp equality
controls using

```text
T_C rank<=2 = { D : (I-P)D(I-Q)=0 }
```

and computed first/second variation evidence for the original corrected
`gap(C)` on the unit-Frobenius sphere.

For both equality controls, the projected first variation vanished to floating
point precision and the tangent second variation was numerically negative
semidefinite:

```text
diag_difference:
  complex tangent dimension = 60
  real sphere tangent dimension = 119
  projected first variation l2 = 0.0
  second variation max eigenvalue = 0.0
  positive second-variation eigenvalue count = 0
  near-zero count = 9
  best random exact-tangent normalized gap = -1.1286354329006127e-06
  best random ambient-retracted normalized gap = -7.802594210527474e-08

product_projection:
  complex tangent dimension = 60
  real sphere tangent dimension = 119
  projected first variation l2 = 0.0
  second variation max eigenvalue = 0.0
  positive second-variation eigenvalue count = 0
  near-zero count = 13
  best random exact-tangent normalized gap = -1.0783607031772395e-06
  best random ambient-retracted normalized gap = -8.329051037758715e-08
```

No positive tangent direction was found. This is local numerical evidence only,
not a global proof and not an equality classification.

### 3. Full PCL/search lane

The full PCL lane attacked the full compression matrix

```text
M(U,V) = 2I_4 - A(U,V) - B(U,V) + (1/2)T(U,V) >= 0,
```

not only the scalar crossed minor. For dangerous compression eigenvectors it
converted back to original `C=PCQ` and checked the corrected original `gap(C)`.

Key output:

```text
coordinate pairs checked = 14400
coordinate negative min-eigenvalue count = 0
coordinate worst lambda_min(M) = 0.0
coordinate worst converted original normalized gap = 2.2204460492503126e-16
random trials = 3000
random worst lambda_min(M) = 1.060359499717052
random positive original gap count = 0
max gap/rayleigh identity error = 2.6645352591003757e-15
optimized worst lambda_min(M) = 3.2507330161017243e-13
optimized converted original normalized gap = -3.2427069109517103e-13
worst overall lambda_min(M) = 0.0
worst overall converted original normalized gap = 2.2204460492503126e-16
robust_pcl_violation_found = False
```

No full PCL proof/certificate was found. No robust PCL violation or certified
positive original-gap counterexample was found. The tiny positive converted gap
`2.22e-16` is roundoff/equality evidence, not a counterexample.

The lane also reconfirmed the known trace-update obstruction: `D=2I-A-B` can be
indefinite, e.g. product support has `eig(D)=[-1,1,1,1]`, while the trace update
repairs `M` to `eig(M)=[0,1,1,1]`.

## Skeptic/auditor verdict

The skeptic and auditor both reject promotion. The auditor initially raced with
the skeptic file creation, but controller verification confirmed `skeptic.md` is
present and agrees with the fail-closed verdict.

Reasons for rejection:

- no complete scalar PAL/crossed-minor certificate;
- scalar crossed-minor work was not extended to full `4 x 4` PCL PSD;
- tangent/equality evidence is local and numerical;
- full PCL searches found no robust violation but no proof;
- no explicit certified rank-at-most-two positive-gap `C` was produced;
- no bridge defect was identified.

Therefore CLAIM-0001 remains open/fail-closed.

## Updated bottleneck

The sharpest bottleneck is now a trace-coupled full-PCL certificate. The scalar
PAL/crossed-PCL determinant remains an important subtarget, but a scalar proof
alone is not enough unless it is extended with all quantifiers to PAL/PCL/CLAIM.

A successful next loop should produce one of:

1. a direct mixed two-frame Plucker/SOS/Gram certificate for the scalar defect,
   together with a route from scalar PAL to CLAIM or full PCL;
2. a direct full `4 x 4` PCL Hermitian Gram/SOS/Schur/principal-minor certificate
   retaining the trace rank-one update;
3. a rigorous tangent/equality classification showing local/global maximality of
   all equality components plus a compactness/patching argument;
4. an explicit certified rank-at-most-two `C` with positive original `gap(C)`.

## Recommended LOOP-0009 focus

Prioritize exact algebra over broader random search:

1. **Mixed Plucker identity lane:** derive candidate mixed wedge/Plucker terms for
   the scalar defect and include orthonormality multipliers explicitly. The
   naive diagonal-wedge polarization route is blocked by LOOP-0008's mismatch.
2. **Zero-mode/equality classification lane:** classify the tangent zero modes
   found at the two equality controls (`9` and `13` near-zero real modes) and
   decide whether they correspond to symmetry/equality-manifold directions.
3. **Full PCL principal-minor lane:** compute symbolic/numeric patterns for all
   `2 x 2`, `3 x 3`, and `4 x 4` principal minors of `M`, looking for Schur or
   rank-one-update certificates that keep the trace term coupled.
