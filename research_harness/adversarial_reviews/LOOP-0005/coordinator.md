# LOOP-0005 Coordinator Report

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_recorded: false
last_updated: 2026-06-03

## Executive summary

LOOP-0005 attacked PCL, the Projected Compression Lemma introduced in LOOP-0004.
PCL is exactly equivalent to CLAIM-0001: for every rank-two support projection
pair `P,Q` on `H=C^4 tensor C^4`, the operator

```text
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I
```

should be negative semidefinite on `Hom(QH,PH)`.

No success condition was met. LOOP-0005 did not prove PCL/CLAIM-0001, did not
refute it, and did not produce a certified positive-gap rank-two counterexample.
It did produce a precise 4-by-4 compression-matrix target and stronger numerical
regression evidence.

Auditor verdict: `no_success_condition_met / fail_closed`.

## Artifacts

Main lanes:

- `pcl_normal_form_lane.md`
- `pcl_numerical_eigen_lane.md`
- `pcl_proof_sos_lane.md`

Adversarial review:

- `skeptic.md`
- `auditor.md`

Executable/log artifacts:

- `research_harness/experiments/LOOP-0005_pcl_compression_search.py`
- `research_harness/experiments/LOOP-0005_pcl_probe.py`
- `research_harness/logs/LOOP-0005_pcl_search_seed5005.json`
- `research_harness/logs/LOOP-0005_pcl_search_seed5005.stdout.log`
- `research_harness/logs/LOOP-0005_pcl_search_smoke.json`
- `research_harness/logs/LOOP-0005_pcl_search_smoke.stdout.log`

## What LOOP-0005 established

### Explicit PCL compression matrix

For orthonormal bases `p_1,p_2` of `ran P` and `q_1,q_2` of `ran Q`, define

```text
E_{alpha beta} = |p_alpha><q_beta|.
```

The PCL compression matrix is

```text
K_{alpha beta, gamma delta}
 = <tr_1 E_{alpha beta}, tr_1 E_{gamma delta}>
 + <tr_2 E_{alpha beta}, tr_2 E_{gamma delta}>
 - (1/2) conjugate(tr E_{alpha beta}) tr E_{gamma delta}
 - 2 delta_{alpha gamma} delta_{beta delta}.
```

PCL asks for `K <= 0` for every pair of rank-two support planes.

Equivalently,

```text
K = Gram({A_ab}) + Gram({B_ij}) - (1/2)vec(T)vec(T)^* - 2I_4.
```

### Numerical/eigenvalue evidence

The PCL eigenvalue lane implemented the compression checker and verified the
quadratic form convention. Equality regressions reproduced the known sharp
spectra:

```text
traceless diagonal equality: [-2, -2, -1, 0]
product projection equality: [-1, -1, -1, 0]
LOOP-0002 phase-absorbed equality: [-1, -1, -1, 0]
```

Main run:

```text
random samples: 5000
random_positive_count_tol_1e_10: 0
best random lambda_max: -1.047205640060712
best optimized lambda_max: -8.4668383415476e-14
reconstructed direct gap: -8.504308368628699e-14
positive_robust_tol_1e_8: false
```

No robust positive PCL eigenvalue or original positive gap was found.

### Proof/SOS status

The proof/SOS lane isolated the algebraic target

```text
M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0
```

on `Gr(2,16) x Gr(2,16)`. It found useful diagonal/wedge-style identities and
regression checks, but no full Hermitian Gram/SOS certificate and no proof of all
principal minors. Diagonal positivity alone is insufficient for full `4 x 4` PSD.

## Skeptic/auditor verdict

The skeptic and auditor both rejected promotion:

- PCL remains an exact reformulation/open equivalent target, not a proof.
- Numerical evidence is negative/equality evidence only.
- No complete PSD/SOS certificate was obtained.
- No certified positive-gap rank-two `C` was found.

## Updated bottleneck

Prove the equivalent PCL compression inequality

```text
M(U,V)=2I-A-B+(1/2)T >= 0
```

on `Gr(2,16) x Gr(2,16)`, prove the PAL two-frame determinant inequality, or
produce a certified rank-two positive-gap counterexample.

## Recommended LOOP-0006 focus

Pursue a certified PCL proof/counterexample, with emphasis on invariant
Plucker-coordinate or Hermitian Gram/SOS certificates for the full 4-by-4 matrix
`M`, not only diagonal entries or determinant alone. Preserve equality-family
regression tests and avoid known false routes: independent local Schmidt
normalization, all-frame `m>=3` PSD promotion, fixed-gauge `H<=2I`, and diagonal
positivity mistaken for full PSD.
