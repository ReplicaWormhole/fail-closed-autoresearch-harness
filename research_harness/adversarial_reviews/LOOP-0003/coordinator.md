# LOOP-0003 Coordinator Report

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_recorded: false
last_updated: 2026-06-03

## Executive summary

LOOP-0003 ran the required adversarial lanes after LOOP-0002 refuted the
fixed-gauge Lemma M. The loop did not prove or refute CLAIM-0001. It sharpened
the active bottleneck to a phase-aware scalar lemma (PAL) for the rank-two SVD
route and produced additional negative numerical evidence against direct
rank-two positive-gap counterexamples.

Auditor verdict: `completed_fail_closed; no_success_condition_met`.

## Artifacts

Proposer / search / classifier lanes:

- `phase_aware_lemma_proposer.md`
- `direct_gap_counterexample.md`
- `equality_family_classifier.md`

Adversarial review:

- `skeptic.md`
- `auditor.md`

Executable/log artifacts:

- `research_harness/experiments/LOOP-0003_direct_gap_search.py`
- `research_harness/logs/LOOP-0003_smoke.json`
- `research_harness/logs/LOOP-0003_direct_gap_search_seed3003_rank2.json`
- `research_harness/logs/LOOP-0003_direct_gap_search_seed4003_rank1.json`
- matching `.stdout.log` and `_best.npz` files in `research_harness/logs/`.

## Lane outcomes

### Phase-aware lemma proposer

The proposer replaced the false fixed-gauge target `H <= 2I` by the
phase-aware scalar candidate PAL. With

```text
L_i = X_iY_i^*,
R_i = X_i^*Y_i,
t_i = tr(X_i^*Y_i),
a = <L_1,L_2>_F,
b = <R_1,R_2>_F - (1/2) conjugate(t_1)t_2,
D_i = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2,
```

the proposed bottleneck is

```text
|a + conjugate(b)|^2 <= D_1 D_2.
```

If PAL is true, it would imply CLAIM-0001 by the rank-two SVD route. LOOP-0003
found no violation in sanity tests, but no proof.

### Direct gap counterexample search

The counterexample lane optimized the original gap directly over normalized
rank-constrained factorizations `C=UV^*`, not the refuted surrogate Lemma M.
The rank-two run used 96 restarts and reported:

```text
max final gap: 8.881784094140483e-16
positivity threshold: 1e-10
positive restarts above threshold: 0
best numerical rank: 2
```

This is roundoff-scale equality evidence, not a positive-gap counterexample.
The rank-one run peaked near `-0.5`.

### Equality-family classifier

The classifier found partial equality-family structure:

- product-type rank-two equality with one factor rank one and the other a scalar
  rank-two projection;
- traceless two-product-atom diagonal equality with opposite coefficients;
- the LOOP-0002 phase-absorbed example belongs to the product-type equality
  family.

The classification is partial and not promoted to a complete equality theorem.

## Skeptic and auditor verdict

The skeptic found no sign/gauge error in the PAL derivation and no robust
positive-gap counterexample, but rejected promotion because PAL is still
unproved and numerical search is not certification.

The auditor rejected all success conditions:

- complete proof: not met;
- verified rank-two positive-gap counterexample: not met;
- accepted bridge-defect closing/replacing the target: not met.

## Updated bottleneck

Prove or refute PAL, or bypass it with an alternative complete proof of
CLAIM-0001 or a robust certified rank-two positive-gap counterexample.

Recommended LOOP-0004 target: attack PAL directly by real Gram/SOS or
structured sparse/support-pattern searches that can be converted back into
original-gap checks.
