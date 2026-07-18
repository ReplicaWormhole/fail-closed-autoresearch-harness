# LOOP-0001 Coordinator Report

status: completed
claim_focus:
  - `CLAIM-0001-rank-two-partial-trace.md`
  - `CLAIM-0002-kronecker-weaker-than-bridge.md`

## Goal

Run the first adversarial loop on the rank-two partial-trace bottleneck.

## Artifacts produced

- `proposer_factorization.md`
- `proposer_counterexample.md`
- `repo_audit.md`
- `skeptic.md`
- `auditor.md`

Numerical/log artifacts from the counterexample lane:

- `research_harness/logs/loop_0001_existing_script_seed1001.log`
- `research_harness/logs/loop_0001_counterexample_search.py`
- `research_harness/logs/loop_0001_counterexample_search_seed1001.json`
- `research_harness/logs/loop_0001_counterexample_search_seed1001.stdout.log`
- `research_harness/logs/loop_0001_exact_witnesses.log`

## Main mathematical outcome

CLAIM-0001 is not proved and not refuted.

The useful progress is localization of the proof gap. The corrected route uses ordinary-rank SVD

```text
C = sum_i s_i |x_i><y_i|,    i <= 2,
```

with reshaped vectors `X_i,Y_i in M_4(C)`. The partial traces are

```text
tr_2(|x_i><y_i|) = X_i Y_i^*,
tr_1(|x_i><y_i|) = X_i^* Y_i.
```

The remaining bottleneck is Lemma M, a two-pair contraction inequality for `X_1,X_2,Y_1,Y_2` with Hilbert-Schmidt orthonormality constraints. In the auditor's formulation, define

```text
L_i = X_i Y_i^*,
R_i = X_i^* Y_i,
t_i = tr(X_i^*Y_i),
H_ij = <L_i,L_j>_F + <R_i,R_j>_F - (1/2) overline(t_i)t_j.
```

The missing claim is roughly

```text
H <= 2 I_2,
```

or the equivalent determinant/off-diagonal bound in the proposer/skeptic reports. This is not yet proved.

## Counterexample/stronger-variant outcome

No rank-two counterexample to CLAIM-0001 was found.

But stronger variants were exactly refuted:

1. Coefficient `alpha < 1/2` is false already at rank 2.
2. The `alpha = 1/2` inequality is false at rank 3.
3. Overly sharp one-partial-trace variants fail on product-projection examples.

Important equality families now tracked in CLAIM-0001:

```text
(|00><00| - |11><11|)/sqrt(2)
(P_2 tensor |0><0|)/sqrt(2),    P_2 = diag(1,1,0,0)
```

## Repository audit outcome

The old proof route in `trace_inequality/rank_two_partial_trace_proof.tex` is invalid because it confuses ordinary matrix rank with operator-Schmidt rank and uses a false scalar inequality.

The Aristotle partial-trace proof is circular for the intended goal because it assumes the Kronecker-sum singular-value bound to recover the partial-trace bridge.

The bridge note `partial_trace_inequality_needed_for_sv_bound.tex` is the strongest reusable artifact: it supports equivalence between the Kronecker-sum singular-value bound and the rank-two partial-trace/projection estimate.

## Claim-card updates applied

- `CLAIM-0001` status changed from `conjectural` to `proof_gap_found`.
- `CLAIM-0001` updated with:
  - Lemma M as the localized proof gap;
  - second equality family;
  - exact stronger-variant refutations;
  - LOOP-0001 adversarial history.
- `CLAIM-0002` status changed from `conjectural` to `refuted` as currently worded, because the bridge note supports equivalence with the full rank-two estimate rather than a weaker restricted-image target.

## Next loop recommendation

LOOP-0002 should focus narrowly on Lemma M.

Recommended parallel lanes:

1. Sum-of-squares/Gram proposer:
   Find a Gram, wedge-product, or SOS representation of `K = 2I - H` under the two Hilbert-Schmidt orthonormality constraints.

2. Determinant-bound proposer:
   Attack the scalar determinant form `|H_12|^2 <= D_1 D_2` directly.

3. Lemma M counterexample hunter:
   Search for exact or high-precision numerical violations of Lemma M, then test whether they produce positive-gap rank-two `C` or only refute an overstrong matrix formulation.

4. Bridge formalization/audit lane:
   Turn `partial_trace_inequality_needed_for_sv_bound.tex` into a stable derivation note or formalization target, so CLAIM-0002 remains retired unless a specific defect is found.

## Coordinator verdict

LOOP-0001 made real progress but did not solve the open problem. The central bottleneck is now sharper: prove or disprove Lemma M.
