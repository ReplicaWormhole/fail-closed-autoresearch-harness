# LOOP-0006 Coordinator Report

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_recorded: false
last_updated: 2026-06-03

## Executive summary

LOOP-0006 pursued a certified PCL/PAL proof or counterexample. It ran three main
lanes: a symbolic PCL certificate lane, a structured PCL counterexample lane, and
a PAL/PCL bridge lane.

No success condition was met. CLAIM-0001 remains open/fail-closed. LOOP-0006 did
not produce a proof, did not produce a certified rank-two positive-gap
counterexample, and did not find a bridge defect. It did sharpen the next
symbolic target: the crossed `2 x 2` principal minor of the PCL matrix and the
trace-coupled rank-one update structure.

Auditor verdict: `no_success_condition_met / fail_closed`.

## Artifacts

Main lanes:

- `pcl_symbolic_certificate_lane.md`
- `pcl_structured_counterexample_lane.md`
- `pal_pcl_bridge_lane.md`

Adversarial review:

- `skeptic.md`
- `auditor.md`

Executable/log artifacts:

- `research_harness/experiments/LOOP-0006_pcl_principal_minors.py`
- `research_harness/experiments/LOOP-0006_pcl_structured_search.py`
- `research_harness/logs/LOOP-0006_pcl_structured_seed6006.json`
- `research_harness/logs/LOOP-0006_pcl_structured_seed6006.stdout.log`

## What LOOP-0006 established

### Symbolic PCL certificate lane

The lane worked with

```text
M = -K = 2I_4 - A - B + (1/2)T.
```

It confirmed diagonal wedge/SOS certificates for the `1 x 1` principal minors
but did not find a full Hermitian Gram/SOS or all-principal-minor certificate.
It also blocked a tempting overstrong route:

```text
D = 2I - A - B >= 0
```

is false. In the product equality case `eig(D)=[-1,1,1,1]`; the trace rank-one
update is essential and repairs the bad direction so `eig(M)=[0,1,1,1]`.

The sharp next symbolic target isolated by the lane is the crossed `2 x 2`
principal minor

```text
Delta_cross = M_{11,11} M_{22,22} - |M_{11,22}|^2 >= 0
```

and its relabelings. This minor remains unproved and is not by itself sufficient
for full PCL.

### Structured counterexample lane

A corrected structured PCL search was run. The lane explicitly fixed an initial
partial-trace convention error; the corrected convention is

```text
tr_1(C)[a,b] = sum_i C[i,a,i,b]
tr_2(C)[i,j] = sum_a C[i,a,j,a]
```

Corrected results:

```text
product projection spectrum: [-1,-1,-1,0]
traceless diagonal spectrum: [-2,-2,-1,0]
structured support best lambda_max: -0.24830718408995792
eps=0.01 equality perturbation best lambda_max: -0.004606073165632001
eps=0.1 equality perturbation best lambda_max: -0.3137722327674509
BFGS best lambda_max: -5.20317946714477e-13
best overall lambda_max: 0.0
robust_positive: false
```

No robust positive compression eigenvalue and no positive original gap were
found.

### PAL/PCL bridge lane

The bridge lane clarified the quantifier-level relationship:

- PCL implies PAL by taking the SVD-diagonal `2 x 2` principal submatrix.
- PAL implies CLAIM-0001 via the rank-two SVD route.
- CLAIM-0001 implies PCL because each `C=PCQ` has rank at most two.

Thus universal PAL, CLAIM-0001, and PCL are equivalent formulations. However,
one fixed PAL block is only a principal slice of one fixed PCL matrix; it is not
a full fixed-basis `4 x 4` PSD certificate.

## Skeptic/auditor verdict

The skeptic and auditor both rejected promotion:

- no full PCL PSD/SOS/principal-minor certificate;
- no proof of PAL;
- no robust positive PCL eigenvalue or original gap;
- no accepted bridge defect.

## Updated bottleneck

Prove the equivalent PCL compression inequality

```text
M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0
```

on `Gr(2,16) x Gr(2,16)`, prove the universal phase-aware PAL two-frame
determinant inequality, or produce a certified rank-two positive-gap
counterexample.

More detailed immediate target: prove all `2 x 2` principal minors of `M`,
especially the crossed minor `Delta_cross`, then continue to `3 x 3` minors and
`det M`, or replace the principal-minor route by a direct Hermitian Gram/SOS
certificate for the full matrix.

## Recommended LOOP-0007 focus

Pursue a rigorous PCL/PAL certificate with primary emphasis on crossed `2 x 2`
principal minors and the trace-coupled rank-one-update structure. Maintain the
correct partial-trace convention and equality-family regressions. Avoid all known
false routes: fixed-gauge `H<=2I`, all-frame `m>=3` PSD promotion, independent
local Schmidt normalization of both support planes, and diagonal positivity as a
substitute for full PSD.
