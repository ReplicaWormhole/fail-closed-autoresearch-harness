# Co-mathematician adversarial autoloop

This file defines the durable co-mathematician-style research policy for attacking `CLAIM-0001`, the rank-two partial-trace inequality.

Reference inspiration: arXiv:2605.06651, "AI co-mathematician: Accelerating mathematicians with agentic AI".

## Active claim

Claim card:

```text
research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
```

Current status: open / fail-closed / proof gap found.

## Workspace files

The autoloop must treat these as the high-level state of the project:

```text
research_harness/CO_MATHEMATICIAN_MODE.md
research_harness/PROJECT_STATE.md
research_harness/GOALS.md
research_harness/dashboard.md
research_harness/uncertainty_ledger.md
research_harness/failed_explorations.md
research_harness/ESCALATIONS.md
research_harness/status.json
```

Persistent workstreams live under:

```text
research_harness/workstreams/
```

Loop-specific adversarial artifacts still live under:

```text
research_harness/adversarial_reviews/LOOP-XXXX/
research_harness/experiments/
research_harness/logs/
```

## Machine status

`research_harness/status.json` is the machine-readable control file.  Important fields:

- `success`: if `true`, the autoloop must stop doing research work.
- `next_loop_number`: next `LOOP-XXXX` directory to create.
- `loops_completed_by_autoloop`: number of loops run by the automatic loop.
- `max_autoloop_loops`: hard cap to avoid unbounded spending.
- `approved_goals`: goal IDs from `GOALS.md`.
- `active_workstreams`: persistent workstreams eligible for advancement.
- `blocked_workstreams`: workstreams that need escalation or a dependency.
- `human_steering_required`: if `true`, do not run autonomous research; report the open escalation.
- `success_record`: path to the accepted proof/counterexample/bridge-defect summary, normally `research_harness/success_record.md`.

## Success condition

Record success only if one of these is accepted by skeptic and auditor.

### Proof success

- CLAIM-0001 has a complete proof of the original rank-two inequality.
- The proof avoids hidden Hermitian, normal, positive, convexity, density, operator-Schmidt-rank, and fixed-gauge complex-coefficient assumptions.
- The proof handles the known equality families.
- The auditor marks the result at least `ready_for_derivation_note`.

### Counterexample success

- A reconstructable rank-two `C` is found with positive original gap

```text
gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2 ||C||_F^2 - (1/2)|tr C|^2 > 0.
```

- An independent checker verifies rank <= 2 and positive gap under the corrected partial-trace convention.
- The skeptic and auditor accept it.

### Bridge-defect success

- A precise mathematical defect is found in the PAL/PCL/CLAIM bridge equivalence artifact.
- The auditor accepts that the active claim/target must be replaced.

## Current bottleneck after LOOP-0011

The obsolete LOOP-0003 phase-aware lane list is superseded.  The current bottleneck is:

1. Scalar: prove exactly

```text
Delta = D1D2 - |m|^2 = GramSlack - ExchangePenalty >= 0.
```

Coordinate equality can reach `ExchangePenalty/GramSlack = 1`, so a proof must explain exact cancellation and cannot use false product-domination shortcuts.

2. Full PCL: find a trace-coupled Schur/Gram/SOS/rank-one-update certificate for `M` itself.  D-only determinant/Schur routes are false.

3. Equality: convert local zero-mode classifications at the two main equality controls into exact equality-family parametrizations, without treating local Hessian evidence as a global proof.

4. Literature: build a source-backed map of related singular-value/partial-trace/operator inequalities.

## Per-run policy

Each cron tick should run at most one complete co-mathematician loop:

1. Read `status.json`.
2. If `success=true`, stop and cite `success_record`.
3. If `human_steering_required=true`, stop and report the open escalation from `ESCALATIONS.md`.
4. If `loops_completed_by_autoloop >= max_autoloop_loops`, stop and report capped/no-success.
5. Read `PROJECT_STATE.md`, `GOALS.md`, `dashboard.md`, `uncertainty_ledger.md`, `failed_explorations.md`, and active workstream states.
6. Create `research_harness/adversarial_reviews/LOOP-XXXX/` using `next_loop_number`.
7. Choose workstream actions that reduce named uncertainties.  Do not run obsolete fixed lanes unless they match the current goals.
8. Run specialized subagents/workstream coordinators in parallel where useful.
9. Require every workstream lane to write durable reports and, where computational, scripts/logs.
10. Run skeptic and auditor review.
11. Write loop `coordinator.md` with dashboard-level summary, artifacts, unresolved uncertainties, and next workstream actions.
12. Update affected workstream `incremental_report.md`, `state.json`, and review files.
13. Update `dashboard.md`, `uncertainty_ledger.md`, `failed_explorations.md` if needed, `status.json`, and the claim card.
14. Write or update `success_record.md` only if the auditor accepts a success gate.
15. If no material progress occurs on repeated bottlenecks, write `ESCALATIONS.md`, set `human_steering_required=true`, and stop future autonomous loops until user steering is provided.

## Review policy

Each loop must include at least:

- a skeptic that attacks hidden assumptions, overclaims, bridge errors, numerical-only claims, and refuted shortcuts;
- an auditor that checks artifacts/scripts/logs and decides promotion gates.

Workstream final reports are not complete until review rounds mark them `accepted`, `accepted_with_caveats`, `blocked_escalate`, or `rejected`.  If reviewer iterations spiral without progress, mark `death_spiral_stop` and escalate.

## Fail-closed reporting

Report success only if the auditor accepts a complete proof, certified counterexample, or bridge defect.  Otherwise say the loop completed fail-closed, even if it sharpened the bottleneck.

Final responses should include:

- loop directory;
- workstreams advanced;
- artifacts written;
- reviewer/auditor verdict;
- whether success was recorded;
- updated dashboard bottleneck;
- next action or cap/escalation status.
