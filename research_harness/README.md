# Adversarial Research Harness

This directory organizes agent-scale attacks on the Kronecker-sum singular-value open problem and its current bottleneck: the rank-two partial-trace inequality.

The harness is fail-closed. A claim is not considered proved because an agent states that it is proved. It must pass adversarial review, executable checks where applicable, and eventually a checked derivation note or formalization target.

## Current central bottleneck

For `C in M_4(C) tensor M_4(C)` with `rank(C) <= 2`, prove or refute

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2
  <= 2 ||C||_F^2 + (1/2) |tr C|^2.
```

This is tracked as `claim_cards/CLAIM-0001-rank-two-partial-trace.md`.

## Directory roles

```text
problem_briefs/        Compact mathematical statements and known state.
claim_cards/           Unit-of-progress files for each precise claim.
adversarial_reviews/   Loop outputs: proposer, skeptic, auditor, coordinator.
experiments/           Reproducible numerical/symbolic scripts.
logs/                  Machine-readable run logs and command outputs.
notes/                 Human-readable derivation notes and interpretations.
prompts/               Role prompts for subagents.
```

## Promotion gates

A mathematical statement moves through these gates:

```text
raw idea
  -> claim card
  -> proposer proof/reduction/counterexample attempt
  -> skeptic review
  -> numerical/symbolic stress checks when applicable
  -> auditor verdict
  -> checked derivation note
  -> formalization target
  -> formalized theorem or certified counterexample
```

Allowed statuses:

- `conjectural`
- `numerically_supported`
- `proof_sketch`
- `proof_gap_found`
- `refuted`
- `ready_for_derivation_note`
- `ready_for_formalization`
- `formalized`

## Loop protocol

Each loop should have a numbered directory, e.g. `adversarial_reviews/LOOP-0001/`.

Minimum files for a full loop:

```text
proposer_factorization.md
proposer_counterexample.md
repo_audit.md
skeptic.md
auditor.md
coordinator.md
```

The coordinator updates claim cards only after the auditor has assigned a fail-closed status.

## Evidence accounting

- Numerical failure to find a violation is evidence only, not proof.
- Numerical near-equality is a candidate requiring exact reconstruction.
- A proof sketch with an unproved lemma remains `proof_gap_found` or `proof_sketch`, not proved.
- Do not assume positivity, Hermiticity, normality, convexity, or density unless explicitly justified.
- Equality witnesses must be checked against all proposed constants.
