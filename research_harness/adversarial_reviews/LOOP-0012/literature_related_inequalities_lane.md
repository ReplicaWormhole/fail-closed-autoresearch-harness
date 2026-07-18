# LOOP-0012 literature and related inequalities lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
workstream: WS-literature-and-related-inequalities
success_condition_met: none

## Executive verdict

The literature workstream produced a guardrail map but did not supply a proof, counterexample, or accepted bridge defect.  The map is durable at:

```text
research_harness/workstreams/WS-literature-and-related-inequalities/related_inequality_map_LOOP-0012.md
```

Network retrieval of external sources was unavailable during the lane (`No route to host`), so the report distinguishes locally checked repository sources from bibliographic anchors requiring later verification.

## Source-backed points from local repository text

1. CLAIM-0001 concerns ordinary matrix rank `<=2`, arbitrary complex `C`, and unnormalized partial traces.  It explicitly does not assume Hermitian, normal, positive, trace-one, density-matrix, or channel structure.
2. The safe reduction is the ordinary-rank SVD/reshaping formula:
   `C=sum_i s_i |x_i><y_i|`, with `tr_2(|x_i><y_i|)=X_iY_i^*` and `tr_1(|x_i><y_i|)=X_i^*Y_i`.
3. Operator-Schmidt-rank shortcuts are invalid: ordinary rank two does not imply a two-term tensor-product expansion `C=s_1 A_1 tensor B_1+s_2 A_2 tensor B_2`.
4. Locally recorded Rico--Wolf/Costa partial-trace material gives a weaker rank-two fallback bound `||tr_1 C||_F^2+||tr_2 C||_F^2 <= 3||C||_F^2`, enough only for a weaker singular-value constant, not CLAIM-0001.
5. Quantum information results using positivity, density matrices, CPTP maps, trace norm, entropy, or relative entropy do not directly apply to arbitrary non-Hermitian rank-two operators with Frobenius partial traces.
6. PCL and PAL are exact internal reformulations/bridges, not external theorems; they remain open.

## Applicability conclusion

The safe import list remains narrow: use ordinary-rank SVD/reshaping, finite-dimensional Hermitian compression facts after forming the exact PCL matrix, and the local projection/Eckart--Young bridge.  Do not import normal-matrix, positivity, operator-Schmidt-rank, or quantum-channel hypotheses as if they proved CLAIM-0001.

## Artifact

- `research_harness/workstreams/WS-literature-and-related-inequalities/related_inequality_map_LOOP-0012.md`

This reduces U-0004 by turning it from `not_started` into a source/hypothesis guardrail map, but it does not close U-0001/U-0002 or promote success.
