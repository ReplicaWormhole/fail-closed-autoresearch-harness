# LOOP-0013 source-backed related-inequality map for CLAIM-0001

Date: 2026-06-03T21:00:55+02:00

Primary lane report: `research_harness/adversarial_reviews/LOOP-0013/literature_related_inequalities_lane.md`.

Durable external source: `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex`.

## CLAIM-0001 target

`C in M_4(C) tensor M_4(C)`, ordinary matrix rank `<=2`, arbitrary complex non-Hermitian/non-positive matrix. Need

`||tr_1 C||_F^2 + ||tr_2 C||_F^2 <= 2||C||_F^2 + (1/2)|tr C|^2`.

Do not replace ordinary rank by operator-Schmidt rank; do not add normality, positivity, density-matrix, channel/CP, Hermitian, or trace-one hypotheses.

## Importability table

| Source/result | Exact hypotheses | What it gives in CLAIM notation | Verdict |
|---|---|---|---|
| Costa Rico--Wolf arXiv:2507.18278, related-work Eq. `Ricosineq` (`PTI.tex:163-171`) | `M` normal of rank `r`; Schatten-2/Frobenius; ordinary partial traces. | For `r=2`, exactly `<= 2||M||_2^2 + 1/2 |tr M|^2`. | Not importable for CLAIM-0001: normality exceeds target; source says beyond-normal case is open. |
| Costa Rico--Wolf Cor. `AudenR` (`PTI.tex:468-472`) | Arbitrary `M`; ordinary rank `r`; `n` tensor factors; Schatten `p`; exponent `gamma>=1`. | For `n=r=p=gamma=2`, `||M_A||_2^2+||M_B||_2^2 <= 3||M||_2^2` (`PTI.tex:533-536`). | Importable only as weaker fallback/context. It cannot prove target trace-corrected bound. |
| Costa Rico--Wolf rank-one proposition (`PTI.tex:506-521`) | Ordinary rank-one `M`; `gamma>=2`. | For `gamma=2`, `||A||_2^2+||B||_2^2 <= ||M||_2^2+|tr M|^2`. | Valid but insufficient: CLAIM-0001 needs rank `<=2`; rank-two cross terms are the unresolved gap. |
| Costa Rico--Wolf Kronecker-sum majorization (`PTI.tex:364-369`) | General local matrices `C_i`; weak singular-value submajorization for Kronecker sums. | Supports their norm-template inequality, not the trace-corrected rank-two inequality. | Context/tool only; no direct CLAIM proof. |
| Costa Rico--Wolf Werner criterion (`PTI.tex:529-541`) | Rank-two matrices in `M_{d tensor d}` tied to Werner-state 2-copy undistillability parameter `alpha`. | Source derives `alpha >= -1/3` via the weaker constant `3` bound; sharp trace term remains open. | Context only; do not import as proof. |
| Local Eckart--Young/Mirsky + projection bridge | Arbitrary complex matrices; rank-two test matrices; unnormalized partial traces; traceless Kronecker-sum subspace. | Reduces sharp top-two singular-value target to CLAIM-0001/PCL. | Safe bridge/reformulation, not external closure. |
| Operator-Schmidt-rank shortcuts | Assumes two-term tensor-product/operator-Schmidt expansion. | Would not cover ordinary rank-two `C`. | Reject. |
| Positivity/entropy/data-processing/QI textbook inequalities | Positive/density/Hermitian inputs, CP maps, entropy/trace norm. | Different objects and stronger assumptions. | Reject for CLAIM-0001 proof. |

## Workstream status after LOOP-0013

- LOOP-0012 network blocker is resolved for arXiv `2507.18278`.
- The exact external source confirms the arbitrary non-normal rank-two trace-corrected inequality is open in that paper.
- The only directly applicable arbitrary-rank-two theorem gives the weaker `3||C||_F^2` fallback.
- Literature workstream remains `fail_closed`: useful guardrails and source-backed context, no accepted proof/counterexample/bridge defect.
