# WS-literature-and-related-inequalities incremental report

Initialized in co-mathematician migration at 2026-06-03T20:01:29+02:00.

## LOOP-0012 update (2026-06-03T20:11:48+02:00)

Concrete actions:

- Checked local CLAIM-0001 hypotheses and prior loop summaries in `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`.
- Checked local bridge/source text in `kronecker_sum_singular_value_note.tex`, especially projection formula, Eckart--Young bridge, corrected rank-one inequality, Rico--Wolf fallback bound, and bibliography lines.
- Attempted network retrieval of arXiv source `2507.18278`; blocked by `No route to host`, so external theorem statements beyond local repository text are marked as requiring later verification.
- Created `related_inequality_map_LOOP-0012.md` with a source-backed applicability table for partial-trace, ordinary-rank-vs-operator-Schmidt, singular-value/projection/compression, and quantum-information inequality families.

Current summary:

The safe related-inequality map is now explicit. Locally checked sources support the following: Rico--Wolf is recorded in the repo as giving the weaker rank-two bound `||tr_1 C||_F^2+||tr_2 C||_F^2 <= 3||C||_F^2`, yielding only the fallback singular-value constant `3/4`; the sharp CLAIM-0001 inequality is still open/fail-closed. Normal-matrix results, positivity/density-matrix results, CP/data-processing inequalities, and operator-Schmidt-rank shortcuts have stronger or different hypotheses and must not be imported as proofs for arbitrary non-Hermitian ordinary-rank-two `C`.

Reviewer status:

No promotion. This workstream now has a usable literature guardrail map, but it does not prove CLAIM-0001 and does not reduce fail-closed status.

## LOOP-0013 update (2026-06-03T21:00:55+02:00)

Artifacts:

- `research_harness/adversarial_reviews/LOOP-0013/literature_related_inequalities_lane.md`
- `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex`
- `research_harness/workstreams/WS-literature-and-related-inequalities/related_inequality_map_LOOP-0013.md`

Concrete actions:

- Retried external retrieval of arXiv `2507.18278`; abs, PDF, and e-print retrieval succeeded.
- Stored durable source and e-print copies with SHA256 hashes in the LOOP-0013 adversarial-review directory.
- Verified exact statements/hypotheses in Costa Rico--Wolf source: normal rank-`r` trace-corrected inequality; arbitrary-rank low-rank Schatten fallback; rank-one trace-corrected inequality; rank-two dilation; Werner-state application.
- Produced a source-backed applicability map distinguishing importable weaker context from non-importable stronger-hypothesis results.

Current summary:

External verification resolves the LOOP-0012 network blocker. The source confirms that the sharp trace-corrected inequality with coefficient `r` plus `1/r |tr M|^2` is only stated for normal matrices, and the beyond-normal rank-two case is explicitly open. The arbitrary rank-two result available from the source gives only `||tr_1 M||_2^2+||tr_2 M||_2^2 <= 3||M||_2^2`, which is too weak for CLAIM-0001. Rank-one, Werner-state, positivity, and operator-Schmidt-rank results cannot be imported as proofs under CLAIM-0001 hypotheses.

Reviewer status:

No promotion / fail-closed. U-0004 is materially advanced by source-backed verification, but no accepted proof, counterexample, or bridge defect was found.
