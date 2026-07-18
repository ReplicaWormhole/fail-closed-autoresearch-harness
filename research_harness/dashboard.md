# Research dashboard

Active claim: `CLAIM-0001-rank-two-partial-trace`
Status: open / fail-closed / human steering requested
Last completed loop: `LOOP-0013`
Next loop: `LOOP-0014` (paused until escalation is resolved)
Mode: co-mathematician workspace

## High-level bottlenecks

1. Scalar certificate: exact restricted equality families now show `GramSlack=ExchangePenalty>0`, but the universal symbolic mixed Plucker/Gram/SOS certificate for `GramSlack >= ExchangePenalty` is still missing.
2. Full PCL certificate: the trace-coupled determinant-update identity is separated from the missing PSD proof; need a global certificate for `det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S)>=0` or an equivalent Schur/Gram/SOS proof for `M`.
3. Equality geometry: coordinate signatures have exact restricted parametrized families, but no global equality-family classification.
4. Counterexample certification: no positive original-gap rank-two example has been found.
5. Literature: arXiv `2507.18278` is now source-verified; it confirms the sharp trace-corrected theorem is normal-only and the arbitrary-rank-two available theorem is too weak.

## Workstream summary

| Workstream | Goal | State | Latest evidence | Next action |
|---|---|---|---|---|
| `WS-scalar-slack` | G1 | active / escalation-relevant | LOOP-0013 exact restricted equality families with positive slack exactly equal to positive exchange penalty | Human steering: choose symbolic invariant/SOS route, SDP search, or alternate approach for the universal certificate |
| `WS-full-pcl-certificate` | G2 | active / escalation-relevant | LOOP-0013 determinant-update identity and diagnostics; D-only routes again refuted | Human steering: prioritize trace-coupled determinant/SOS, Schur-LDL certificate, or higher-compute search |
| `WS-equality-geometry` | G3 | active | LOOP-0013 restricted parametrized equality families for LOOP-0012 signatures | Decide whether to invest in global equality classification or keep as guardrails |
| `WS-counterexample-search` | G4 | dormant | prior searches and LOOP-0013 diagnostics found no certified positive gap | Re-run only with new parameterization or exact/rational certificate checker |
| `WS-literature-and-related-inequalities` | G5 | in_progress | LOOP-0013 retrieved arXiv `2507.18278` and verified exact hypotheses; no importable proof | Use source map as guardrail; optionally search broader literature only if steered |
| `WS-working-paper` | G6 | scaffolded | LOOP-0013 updated source-backed literature guardrails | Draft missing-lemma sections if user prioritizes exposition |

## Open escalations

Active escalation `ESC-0001` is open. Autonomous work is paused because the same scalar/full-PCL symbolic certificate bottleneck survived LOOP-0012 and LOOP-0013 without an accepted proof/counterexample/bridge defect.

## Promotion status

No success is recorded. LOOP-0013 skeptic verdict: `fail_closed_no_success_condition_survives`. LOOP-0013 auditor verdict: `completed_fail_closed; no_success_condition_met; reject_loop_success`.
