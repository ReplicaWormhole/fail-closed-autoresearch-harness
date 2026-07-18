You are running the co-mathematician adversarial research autoloop for the repository `.`.

Do not schedule additional cron jobs. Run exactly one co-mathematician loop per cron tick, then stop.

Repository root:

```text
.
```

Read these files first, in this order:

```text
research_harness/AUTOLOOP.md
research_harness/CO_MATHEMATICIAN_MODE.md
research_harness/status.json
research_harness/PROJECT_STATE.md
research_harness/GOALS.md
research_harness/dashboard.md
research_harness/uncertainty_ledger.md
research_harness/failed_explorations.md
research_harness/ESCALATIONS.md
research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
```

Then read active workstream states from:

```text
research_harness/workstreams/*/state.json
research_harness/workstreams/*/goal.md
research_harness/workstreams/*/incremental_report.md
research_harness/workstreams/*/uncertainty.md
```

Control logic:

1. Read `research_harness/status.json`.
2. If `success` is true, do not run research work. Reply briefly that success is already recorded and cite `success_record`.
3. If `human_steering_required` is true, do not run research work. Reply with the open escalation from `research_harness/ESCALATIONS.md` and the reason autonomous work is paused.
4. If `loops_completed_by_autoloop >= max_autoloop_loops`, do not run research work. Reply that the autoloop cap has been reached without accepted success.
5. Otherwise create one new loop directory using `next_loop_number`, formatted as `LOOP-0012`, `LOOP-0013`, etc.
6. Choose workstream actions that reduce named uncertainties from `uncertainty_ledger.md`; do not use obsolete LOOP-0003 lane instructions unless they are still relevant to the active goals.
7. Run exactly one complete co-mathematician loop using subagents/workstream coordinators.
8. Run skeptic and auditor review.
9. Update the loop coordinator, affected workstreams, `dashboard.md`, uncertainty/failed-exploration ledgers, `status.json`, and the claim card narrative.
10. Only write/overwrite `research_harness/success_record.md` and set `success=true` if the auditor accepts one of the success conditions below.

Success conditions:

A. Proof success:
- A complete proof of CLAIM-0001 is produced.
- The proof is for the original rank-two partial-trace inequality, not an overstrong or irrelevant fixed-gauge lemma.
- It avoids hidden Hermitian, normal, positive, convexity, density, operator-Schmidt-rank, and arbitrary-complex-coefficient assumptions.
- It handles known equality families.
- Skeptic finds no fatal gap.
- Auditor marks at least `ready_for_derivation_note`.

B. Counterexample success:
- A reconstructable rank-two `C` is found with positive original gap:

```text
gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2 ||C||_F^2 - (1/2)|tr C|^2 > 0.
```

- An independent checker verifies rank <= 2 and positive gap under the corrected partial-trace convention.
- Skeptic and auditor accept it.

C. Bridge-defect success:
- A precise mathematical defect is found in the PAL/PCL/CLAIM bridge equivalence artifact.
- Auditor accepts that the active claim/target must be replaced.

Current mathematical context after LOOP-0011:

- CLAIM-0001 is still open/fail-closed/proof_gap_found.
- The fixed-gauge complex-coefficient lemma `H <= 2I` is refuted.
- D-only PCL determinant/Schur routes are false.
- The scalar crossed PAL/PCL minor is organized as:

```text
Delta = D1D2 - |m|^2 = GramSlack - ExchangePenalty.
```

- The current scalar target is exact `GramSlack >= ExchangePenalty`; equality cases can have penalty/slack ratio `1`.
- Full PCL requires a trace-coupled certificate for `M` itself, not D.
- Product-projection and diagonal-difference equality controls have local numerical zero-mode classifications, but not global equality theorems.

Preferred LOOP-0012 workstream mix unless the current status/workstreams indicate otherwise:

1. `WS-scalar-slack`: symbolic equality-signature/orbit analysis for coordinate ratio-1 cases; attempt mixed Plucker/SOS certificate for `GramSlack >= ExchangePenalty`.
2. `WS-full-pcl-certificate`: trace-coupled Schur/Gram/SOS candidate for full `M`; explicitly reject D-only pivots.
3. `WS-literature-and-related-inequalities`: source-backed search for partial-trace, singular-value, matrix-subspace compression, and quantum-information inequalities with exact hypotheses.
4. Optional `WS-working-paper`: if the other lanes stall, draft a provenance-rich working-paper section exposing the exact missing lemmas.

Review requirements:

- Every lane must write a durable report in the loop directory and update its workstream incremental report.
- Numerical lanes must save executable scripts/logs.
- The skeptic must reject hidden Hermitian/normal/positive/diagonal/coordinate assumptions, scalar-to-full overclaims, local-to-global overclaims, and any reuse of refuted shortcuts.
- The auditor must verify file existence, script compilation/log JSON where applicable, and promotion gates.

After auditor:

- Write/update `coordinator.md` in the loop directory.
- Increment `loops_completed_by_autoloop` by 1.
- Set `last_completed_loop` to the loop just completed.
- Increment `next_loop_number` by 1 unless success is recorded.
- If no success, keep `success=false` and update `current_bottleneck` from the auditor/coordinator.
- Update `dashboard.md` and affected workstreams.
- If a repeated bottleneck is not materially reduced, add an escalation to `ESCALATIONS.md` and consider setting `human_steering_required=true`.
- If success, set `success=true`, `status=success`, `success_type`, `success_record`, and write `research_harness/success_record.md`.

Final response should be concise and include:

- loop directory;
- workstreams advanced;
- artifacts written;
- whether success was recorded;
- updated bottleneck;
- next action or cap/escalation status.
