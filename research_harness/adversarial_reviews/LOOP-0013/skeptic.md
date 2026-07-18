# LOOP-0013 skeptic review

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_condition_met: none
verdict: fail_closed_no_success_condition_survives

## Executive verdict

No LOOP-0013 lane supplies a complete proof, a reconstructable positive-gap rank-two counterexample, or an accepted bridge defect.  The three lane reports are useful incremental evidence/guardrails, but every attempted promotion is blocked by an unclosed global or hypothesis gap.

Final skeptic verdict: **FAIL-CLOSED / CLAIM-0001 remains open.**

## Materials reviewed

- `research_harness/adversarial_reviews/LOOP-0013/scalar_slack_equality_lane.md`
- `research_harness/adversarial_reviews/LOOP-0013/full_pcl_certificate_lane.md`
- `research_harness/adversarial_reviews/LOOP-0013/literature_related_inequalities_lane.md`
- Associated scripts/logs referenced by those reports:
  - `research_harness/experiments/LOOP-0013_scalar_slack_equality_symbolic.py`
  - `research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.json`
  - `research_harness/experiments/LOOP-0013_full_pcl_rank_update_diagnostics.py`
  - `research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.json`
  - `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex`

## Hidden-assumption attacks

### 1. Hermitian / normal / positive / density assumptions

The literature lane explicitly identifies the closest sharp external theorem as a **normal-matrix** result.  CLAIM-0001 allows arbitrary complex ordinary-rank-two matrices, with no Hermitian, normal, positive, density, channel, or CP-map hypothesis.  Importing the normal theorem would therefore be a fatal hidden-assumption error.  The cited source also states the beyond-normal rank-two case is open, so it cannot be used as an authority for CLAIM-0001.

The PCL lane studies a Hermitian trace-coupled matrix `M` derived from the reduction.  That is admissible only if all bridge steps are retained exactly.  It does not license replacing the original arbitrary non-normal rank-two matrix `C` by a positive/Hermitian object.  No lane proved such a replacement.

### 2. Diagonal / coordinate / fixed-gauge assumptions

The scalar lane promotes selected coordinate equality signatures to explicit real one-parameter equality families and numerically stress-tests analogous complex-unitary families.  This is not a global classification on `Gr(2,16) x Gr(2,16)`.  The report itself leaves open non-row, non-column, non-diagonal equality branches and does not prove the complex-unitary families exhaust a local branch.

Therefore no conclusion may be promoted from these row/column/diagonal charts to all rank-two planes.  The promoted families are guardrails for certificates, not a proof domain covering the claim.

### 3. Arbitrary-complex-coefficient and fixed-coordinate reuse

Previous fixed-gauge complex-coefficient shortcuts were refuted.  LOOP-0013 does not revive them: the scalar exact work is real-symbolic on selected charts, while the complex-unitary extension is numerical.  Any attempt to claim a universal complex certificate from those data would reuse a refuted fixed-coordinate/fixed-gauge shortcut.

## Scalar-to-full overclaim check

The scalar lane does not prove the universal scalar crossed-minor inequality `Delta >= 0`; it proves equality and cancellation on selected families.  Even a future scalar proof would still need a complete bridge to full PCL/CLAIM-0001.  LOOP-0013 supplies neither:

- no universal scalar SOS/Plucker/Gram certificate for `GramSlack >= ExchangePenalty`;
- no proof that scalar equality families imply full-PCL equality families;
- no proof that all full-PCL principal minors reduce to the scalar target;
- no complete derivation from scalar crossed-minor nonnegativity to CLAIM-0001.

Thus scalar progress cannot be promoted to success condition A.

## Local-to-global overclaim check

The scalar families have `Delta = 0` with positive `GramSlack = ExchangePenalty`, but only on selected parametrized charts.  The PCL diagnostics scan all coordinate plane pairs and 500 random trials, but numerical and coordinate scans cannot prove global PSD for arbitrary two-frames.  The literature result gives a global theorem only for a weaker bound or stronger normal/rank-one hypotheses.

No lane proves a global theorem over all ordinary rank-two `C`.

## Reuse of refuted shortcuts

The following routes remain rejected and cannot be recycled as LOOP-0013 success:

- D-only PCL determinant, pivot, or Schur routes.  The full-PCL lane records coordinate cases with `detD = -1` and `D_negative_eig_count = 48`; the trace update is essential.
- Dropping the exchange penalty or attempting pure Cauchy slack domination.  The scalar equality families have positive Cauchy slack exactly cancelled by positive exchange penalty.
- Importing normal, positive, density, channel, or rank-one external theorems as arbitrary-rank-two theorems.
- Treating random samples, coordinate atlases, or selected equality branches as global proof.

## Success-condition review

A. **Proof success:** rejected.  No complete proof of CLAIM-0001 appears.  Hidden-assumption and local-to-global gaps remain, and the full trace-coupled PCL certificate is still unproved.

B. **Counterexample success:** rejected.  No reconstructable rank-two `C` with positive original gap is reported; logs show diagnostics/equality controls, not a positive-gap counterexample.

C. **Bridge-defect success:** rejected.  The literature lane and local lanes do not identify a precise defect in the PAL/PCL/CLAIM bridge that would replace the target.  They preserve the bridge as a guardrail while leaving missing certificates open.

## Skeptic conclusion

LOOP-0013 should be recorded as completed but unsuccessful.  Durable progress consists of equality-family guardrails, a trace-coupled determinant-update identity, and source-backed external-hypothesis clarification.  None closes CLAIM-0001.

Final verdict: `fail_closed_no_success_condition_survives`.
