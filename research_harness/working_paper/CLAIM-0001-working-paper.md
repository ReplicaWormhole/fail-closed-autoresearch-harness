# Working paper: rank-two partial-trace inequality

Status: working document, not a proof.

## Claim

For `C in M_4(C) tensor M_4(C)` with ordinary matrix rank at most two,

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 - 2||C||_F^2 - (1/2)|tr C|^2 <= 0.
```

## Provenance convention

Every substantive assertion in this document should eventually carry a provenance note pointing to a claim card, loop report, workstream report, script, log, or external source.

## Current sections to fill

1. Original inequality and conventions.
2. PAL formulation.
3. PCL formulation.
4. Equivalence/bridge audit.
5. Refuted fixed-gauge lemma.
6. Scalar GramSlack/ExchangePenalty bottleneck.
7. Full PCL trace-update bottleneck.
8. Equality controls and local tangent evidence.
9. Counterexample search status.
10. Open lemmas.

## Literature guardrail text proposed in LOOP-0012

The claim is an inequality for arbitrary complex operators of ordinary matrix rank at most two on `C^4 tensor C^4`; no Hermitian, normal, positive, density-matrix, or complete-positivity hypothesis is available [source: `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md:34-48`]. Consequently, literature results stated only for normal matrices, positive semidefinite density operators, CPTP maps, or bounded operator-Schmidt rank cannot be imported as proofs without an explicit reduction preserving the exact hypotheses.

The now source-verified external anchor is Costa Rico--Wolf, *Partial trace relations beyond normal matrices*, arXiv:2507.18278. LOOP-0013 retrieved the arXiv source and stored a durable copy at `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex` [lane report: `research_harness/adversarial_reviews/LOOP-0013/literature_related_inequalities_lane.md`]. The source states the trace-corrected inequality

```text
||Tr_A[M]||_2^2 + ||Tr_B[M]||_2^2 <= r ||M||_2^2 + (1/r)|tr M|^2
```

for **normal** matrices `M` of rank `r`, and explicitly says whether it holds beyond normal matrices is open, especially for `r=2` [source: `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex:163-171`]. Therefore this theorem cannot be imported as a proof of CLAIM-0001. The same source proves the weaker arbitrary-rank bound

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 <= 3 ||C||_F^2
```

for the rank-two Schatten-2 specialization [source: `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex:468-472,533-536`]. This weaker estimate is directly relevant but yields only the fallback singular-value constant `3/4`, not the conjectured `1/2` [local source: `kronecker_sum_singular_value_note.tex:224-236`].

The safe bridge to the Kronecker-sum singular-value problem is local and algebraic: the projection onto the traceless Kronecker-sum subspace is expressed in terms of the two unnormalized partial traces [source: `kronecker_sum_singular_value_note.tex:99-126`], and the Eckart--Young/Mirsky variational principle reduces the top-two singular-value bound to rank-two test matrices [source: `kronecker_sum_singular_value_note.tex:128-136`]. These steps do not prove CLAIM-0001; they identify why the missing partial-trace estimate is exactly the needed sharp bridge.

The ordinary-rank reduction must use the ordinary SVD/reshaping formula: `C=sum_i s_i |x_i><y_i|`, with `i<=2`, and after reshaping vectors into `4x4` matrices, `tr_2(|x_i><y_i|)=X_iY_i^*` and `tr_1(|x_i><y_i|)=X_i^*Y_i` [source: `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md:97-100`]. It is not valid to replace ordinary rank at most two by operator-Schmidt rank at most two; an earlier proof file made precisely that stronger assertion [source to avoid: `trace_inequality/rank_two_partial_trace_proof.tex:90-96`].

This scaffold exists to make the research state native to mathematical reading rather than hidden in chat logs.
