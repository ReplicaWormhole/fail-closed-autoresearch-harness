# Escalations

## ESC-0001: Human steering requested for persistent scalar/full-PCL symbolic bottleneck

Status: open
Opened: 2026-06-03T21:10:12+02:00
Blocking status: autonomous work paused (`human_steering_required=true`)

LOOP-0012 and LOOP-0013 both made useful guardrail progress but did not materially close the central scalar/full-PCL symbolic certificate bottleneck. CLAIM-0001 remains open/fail-closed with no accepted proof, counterexample, or bridge defect.

Which direction should be prioritized before further autonomous loops?

1. symbolic invariant theory / Plucker-coordinate certificate for `GramSlack >= ExchangePenalty`;
2. full-PCL trace-coupled determinant/Schur/SOS certificate for `M`;
3. higher-compute SDP/SOS search to guess a certificate;
4. exact/rational counterexample certification search with a new parameterization;
5. global equality-geometry theorem;
6. living TeX derivation note/working paper to expose exact missing lemmas before more search;
7. broader source-backed literature search beyond arXiv `2507.18278`.

Evidence:

- Scalar LOOP-0013: exact restricted equality families show `GramSlack=ExchangePenalty>0`; no universal certificate.
- Full-PCL LOOP-0013: determinant-update identity and diagnostics sharpen the target; no PSD certificate.
- Literature LOOP-0013: arXiv `2507.18278` source verified; sharp theorem is normal-only and arbitrary rank-two theorem is too weak.

Escalation policy:

- Future cron ticks should stop at status check and report this escalation until the user gives steering or `human_steering_required` is cleared.
