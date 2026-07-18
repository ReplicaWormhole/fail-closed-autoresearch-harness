# LOOP-0003 Auditor Report

status: completed_fail_closed
claim_focus:
  - `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`
claim_0001_status: fail_closed_proof_gap_found_open
success_verdict: no_success_condition_met
last_updated: 2026-06-03

## Executive verdict

Fail closed.

LOOP-0003 does not prove CLAIM-0001 and does not refute it. The loop usefully
moves the proof state from the refuted fixed-gauge LOOP-0001/LOOP-0002 matrix
lemma toward a sharper phase-aware scalar bottleneck, but that bottleneck is
still unproved. The direct rank-two search found no robust positive-gap
counterexample; its best positive value is `8.881784094140483e-16`, which is
roundoff-scale and below the lane's own `1e-10` positivity threshold.

Therefore none of the success conditions is met:

- Complete proof of CLAIM-0001: not met.
- Verified rank-two positive-gap counterexample: not met.
- Accepted bridge-defect sufficient to close or redirect the target: not met.

Exact success verdict: `no_success_condition_met / fail_closed`.

## Inputs reviewed

Required LOOP-0003 artifacts reviewed:

1. `research_harness/status.json`
2. `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`
3. `research_harness/adversarial_reviews/LOOP-0003/phase_aware_lemma_proposer.md`
4. `research_harness/adversarial_reviews/LOOP-0003/direct_gap_counterexample.md`
5. `research_harness/adversarial_reviews/LOOP-0003/equality_family_classifier.md`
6. `research_harness/adversarial_reviews/LOOP-0003/skeptic.md`

I also performed a lightweight independent audit of the direct-search JSON logs:

- `research_harness/logs/LOOP-0003_direct_gap_search_seed3003_rank2.json`
- `research_harness/logs/LOOP-0003_direct_gap_search_seed4003_rank1.json`

The log summaries matched the direct-search and skeptic reports.

## What LOOP-0003 actually established

### 1. The prior fixed-gauge matrix bottleneck is replaced by a sharper candidate

The phase-aware lemma proposer correctly distinguishes the refuted fixed-gauge
complex-coefficient statement from the real nonnegative singular-value condition
needed by an ordinary rank-two SVD. For

```text
C = s_1 |x_1><y_1| + s_2 |x_2><y_2|,     s_i >= 0,
```

with reshaped singular vectors `X_i,Y_i`, the relevant diagonal defects and
off-diagonal quantities are

```text
L_i = X_iY_i^*,
R_i = X_i^*Y_i,
t_i = tr(X_i^*Y_i),
a = <L_1,L_2>_F,
b = <R_1,R_2>_F - (1/2) conjugate(t_1)t_2,
D_i = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2.
```

The proposed replacement bottleneck is the phase-aware scalar lemma PAL:

```text
|a + conjugate(b)|^2 <= D_1 D_2.
```

If PAL is true, it would supply a clean SVD-route proof of CLAIM-0001. LOOP-0003
provided sign/phase analysis and numerical sanity checks supporting PAL, but no
proof. Thus PAL is an unproved candidate lemma, not an accepted theorem.

### 2. No direct rank-two positive-gap counterexample was found

The direct-search lane optimized the original claim gap over rank-constrained
factorizations

```text
C = U V^*,     U,V in C^{16 x r},     r in {1,2},
```

with Frobenius normalization. This is a valid numerical attack on the original
claim rather than on the refuted Lemma M surrogate.

Independent log audit for the rank-two run gave:

```text
restarts: 96
max final gap: 8.881784094140483e-16
min final gap: -3.8503533766171515e-08
positive restarts at threshold 1e-10: 0
near-zero restarts with gap > -1e-8: 95
best rank tol 1e-10: 2
best rank tol 1e-8: 2
best leading singular values:
  [0.7071067811896656, 0.7071067811834296, 9.633198289182102e-17, ...]
```

The controls included the known rank-two equality witness with exactly reported
`gap = 0.0`, so the implementation can reach the boundary. The rank-two best
candidate is therefore best interpreted as equality to double-precision
roundoff, not as a robust counterexample.

Independent log audit for the rank-one run gave:

```text
restarts: 48
max final gap: -0.49999999999999956
min final gap: -0.500000000489244
positive restarts at threshold 1e-10: 0
best rank tol 1e-10: 1
```

This supports the lane's conclusion but remains numerical evidence only.

### 3. Equality-family information was expanded, but not completed

The equality-family classifier establishes useful visible families:

- product-type equality, e.g. a rank-one factor tensored with a scalar rank-two
  projection factor;
- traceless two-product-atom equality, e.g.
  `(|00><00| - |11><11|)/sqrt(2)`;
- the LOOP-0002 phase-absorbed example belongs to the product-type equality
  mechanism rather than to a positive-gap violation family.

The classifier is correctly scoped as partial. It does not rule out other
nonnormal, non-diagonal, or entangled-singular-vector equality cases, and it
must not be used as a proof of the universal claim.

## Success-condition audit

### Complete proof

Rejected. PAL is not proved, and no alternative proof of CLAIM-0001 is supplied.
The reports explicitly leave the main scalar inequality open.

### Verified rank-two positive-gap counterexample

Rejected. The direct search found no gap above `1e-10`; the maximum recorded
rank-two gap is `8.881784094140483e-16`, consistent with floating-point
roundoff at an equality point. No reconstructable robust positive-gap `C` is
available.

### Accepted bridge-defect

Rejected. LOOP-0003 identifies a better bridge/proof bottleneck, but it does not
establish a defect in the original claim or in the Kronecker-sum bridge that
would satisfy a stopping condition. The accepted defect from prior loops remains
that fixed-gauge `H <= 2I` / Lemma M is false as stated; LOOP-0003's new PAL
formulation is plausible but unproved.

## Current bottleneck

Updated current bottleneck:

```text
Prove or refute the phase-aware scalar PAL inequality for Hilbert-Schmidt
orthonormal two-frames in M_4(C):

| <X_1Y_1^*, X_2Y_2^*>_F
  + conjugate(<X_1^*Y_1, X_2^*Y_2>_F
              - (1/2) conjugate(t_1)t_2) |^2
<= D_1 D_2,

where t_i = tr(X_i^*Y_i) and
D_i = 2 - ||X_iY_i^*||_F^2 - ||X_i^*Y_i||_F^2 + (1/2)|t_i|^2.
```

This replaces the obsolete bottleneck `H <= 2I`, which was refuted in LOOP-0002.

## Next loop recommendation

Recommended LOOP-0004 target: attack PAL directly.

Priority options:

1. Try to prove PAL by a real Gram/SOS or determinant-defect identity for
   `D_1D_2 - |a + conjugate(b)|^2`. The construction must encode the right-vector
   phase law or real nonnegative singular coefficients, and must not revert to
   the refuted Hermitian PSD kernel `2I-H`.

2. Try to refute PAL with structured searches beyond random frames: sparse
   matrix-unit combinations, low-dimensional reductions, diagonal/support-pattern
   ansatzes, and optimized non-sparse two-frames. Any PAL violation should be
   converted by phase choice into a candidate rank-two `C` and then checked
   against the original gap.

3. Continue direct original-gap search only if it adds certification or new
   structure: e.g. interval/rational reconstruction near equality, constrained
   symbolic ansatzes, or a reproducible robust positive gap well above numerical
   tolerance.

4. Preserve equality regression tests for both visible mechanisms:

```text
(|00><00| - |11><11|)/sqrt(2),
(P_2 tensor |0><0|)/sqrt(2),
rank-one-factor tensor scalar rank-two projection,
LOOP-0002 phase-absorbed matrix-unit equality.
```

## Claim-card patch suggestion

Suggested patch language for
`research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`:

```text
## LOOP-0003 update

LOOP-0003 did not prove or refute CLAIM-0001. A direct numerical search over
rank-constrained factorizations `C=UV^*`, `U,V in C^{16xr}`, found no robust
positive gap: the best rank-two value was `8.881784094140483e-16`, below the
`1e-10` positivity threshold and consistent with equality-roundoff. The rank-one
search peaked at approximately `-0.5`.

The loop replaced the refuted fixed-gauge Lemma M target with the phase-aware
scalar candidate PAL. For SVD data `X_i,Y_i` with Hilbert-Schmidt orthonormal
two-frames, define `L_i=X_iY_i^*`, `R_i=X_i^*Y_i`, `t_i=tr(X_i^*Y_i)`,
`a=<L_1,L_2>`, `b=<R_1,R_2>-(1/2)conjugate(t_1)t_2`, and
`D_i=2-||L_i||_F^2-||R_i||_F^2+(1/2)|t_i|^2`. The candidate lemma is
`|a+conjugate(b)|^2 <= D_1D_2`. PAL would imply CLAIM-0001 by the rank-two SVD
route, and it survived LOOP-0003 random/sparse numerical tests, but it remains
unproved.

LOOP-0003 also recorded partial equality-family information: product-type
rank-two equality and traceless two-product-atom equality are distinct visible
mechanisms; the LOOP-0002 phase-absorbed example belongs to the product-type
equality family. This is not a complete classification.

Current bottleneck: prove or refute PAL, or supply an alternative complete proof
of CLAIM-0001 / robust rank-two positive-gap counterexample.
```

Recommended status remains:

```text
status: proof_gap_found
current verdict: fail-closed / open
```

## Final auditor status

CLAIM-0001 remains open. LOOP-0003 provides a sharper, phase-aware formulation of
the likely SVD bottleneck and useful negative counterexample-search evidence, but
no promotable proof, no verified counterexample, and no accepted bridge-defect.

Final verdict: `completed_fail_closed; no_success_condition_met`.
