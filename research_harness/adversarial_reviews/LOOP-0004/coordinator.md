# LOOP-0004 Coordinator Report

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_recorded: false
last_updated: 2026-06-03

## Executive summary

LOOP-0004 continued from LOOP-0003 by attacking the phase-aware scalar PAL
inequality directly and by looking for an alternative formulation of the original
rank-two partial-trace inequality.

No success condition was met. The loop did not prove CLAIM-0001, did not refute
CLAIM-0001, and did not produce a verified positive-gap rank-two counterexample.
It did, however, sharpen the proof state: PAL is now formulated as an exact
2-by-2 determinant/PSD target, and an equivalent support-compression formulation
called PCL was introduced.

Auditor verdict: `no_success_condition_met / fail_closed`.

## Artifacts

Main lanes:

- `pal_proof_lane.md`
- `pal_refutation_search.md`
- `alternative_derivation_lane.md`

Adversarial review:

- `skeptic.md`
- `auditor.md`

Executable/log artifacts:

- `research_harness/experiments/LOOP-0004_pal_search.py`
- `research_harness/logs/LOOP-0004_pal_search_seed4004.json`
- `research_harness/logs/LOOP-0004_pal_search_seed4004.stdout.log`

## What changed mathematically

### PAL status

PAL is the phase-aware two-frame determinant inequality

```text
D_1D_2 - |a+conjugate(b)|^2 >= 0.
```

The proof lane rewrote this as positivity of the Hermitian matrix

```text
K^PAL = [[D_1, -z],[-conjugate(z), D_2]],
z = a + conjugate(b).
```

Known equality mechanisms remain sharp for PAL. The proof lane also found an
important obstruction: the analogous natural kernel is not PSD for longer
`m >= 3` frames, so a successful proof must be genuinely two-frame or
determinant-level and must not resurrect an overstrong all-frame PSD statement.

PAL status: open / unproved / not refuted.

### PAL refutation/search status

The search lane checked:

- 57,600 sparse matrix-unit two-frame cases;
- 8,000 random complex two-frame samples;
- 8 SciPy/BFGS restarts over unconstrained parameters projected to two-frames.

Key outputs:

```text
matrix-unit best violation: 0.0
matrix-unit equality cases: 528
random best violation: -1.549087158428483
optimized best violation: -6.211697822777751e-14
```

No robust positive PAL violation was found. The optimized value is roundoff-scale
near equality, not a refutation.

### Alternative derivation / PCL

The alternative lane introduced the Projected Compression Lemma (PCL). Define

```text
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I.
```

PCL states that for every pair of rank-two support projections `P,Q` on
`C^4 tensor C^4`, the compression of `Phi` to

```text
Hom(QH,PH) = { C : C = P C Q }
```

is negative semidefinite.

PCL is exactly equivalent to CLAIM-0001: every rank-two `C` has rank-two range
and co-range support projections, and every `C=PCQ` for rank-two `P,Q` has rank
at most two. PCL avoids SVD phase bookkeeping but remains unproved.

## Skeptic/auditor verdict

The skeptic and auditor both rejected promotion:

- PAL proof lane gives a reduction, not a proof.
- PAL search gives negative evidence/equality tests, not a proof or refutation.
- PCL is an exact reformulation, not a theorem.
- No certified positive original `gap(C)` was found.

## Updated bottleneck

Prove either the phase-aware two-frame PAL determinant inequality or the
equivalent Projected Compression Lemma (PCL), or produce a certified rank-two
`C` with robust positive original gap.

## Recommended LOOP-0005 focus

Attack PCL as the primary lane while keeping PAL determinant equality cases as
regression tests. In particular:

1. Derive local-unitary/Grassmannian normal forms for pairs of two-planes `P,Q`.
2. Express the PCL compression matrix in that normal form.
3. Search for exact PSD/SOS decompositions of `-Phi|_{Hom(QH,PH)}` using
   support-plane constraints or Plucker coordinates.
4. Preserve equality regression tests and the LOOP-0004 `m>=3` obstruction to
   reject overstrong kernel proofs.
