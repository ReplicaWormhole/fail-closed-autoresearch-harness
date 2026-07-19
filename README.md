# Fail-closed autonomous research harness

A case study in structured autonomous mathematical research.  The repository records an adversarial agent workflow applied to an open rank-two partial-trace inequality arising from a Kronecker-sum singular-value problem.

## What this demonstrates

- a precise claim card, explicit success conditions, and a machine-readable project state;
- proposer, skeptic, auditor, and coordinator roles with durable per-loop artifacts;
- reproducible numerical and symbolic diagnostics with fixed seeds;
- uncertainty tracking, failed-route memory, escalation, and a working-paper layer;
- fail-closed reporting: numerical non-violation does not count as proof, and a rejected lemma is recorded as refuted rather than silently reused.

## Mathematical status

The central rank-two partial-trace inequality is **open** in this repository.  The documented work reduced and stress-tested several equivalent formulations, produced counterexamples to an intermediate lemma, and isolated remaining scalar and matrix-certificate bottlenecks.  Nothing here should be cited as a proof of the central claim.

## Layout

`research_harness/` contains the full case-study workspace:

- `claim_cards/`: statement, status, and adversarial history for each claim;
- `adversarial_reviews/`: numbered proposer/skeptic/auditor/coordinator loops;
- `experiments/`: deterministic Python diagnostics;
- `logs/`: machine-readable outputs from the recorded runs;
- `workstreams/`, `uncertainty_ledger.md`, and `failed_explorations.md`: persistent research state;
- `AUTOLOOP.md` and `CO_MATHEMATICIAN_MODE.md`: operating protocol.

## Reproducing a small diagnostic

Python 3.11+ with NumPy, PyTorch, and SymPy is required.

```bash
python -m pip install -r requirements.txt
python research_harness/experiments/LOOP-0003_direct_gap_search.py \
  --rank 2 --restarts 1 --steps 5 --lbfgs-steps 0 \
  --out-json /tmp/loop-0003-smoke.json
```

The experiment is a search diagnostic only; its output does not establish or refute the conjecture.

## Scope

This public extraction excludes third-party source payloads, compiled documents, raw terminal logs, temporary files, and machine-specific paths.  No license has yet been selected; obtain permission before redistributing or reusing this code.

## Portfolio extraction

This public repository is a representative extraction moved from a local research workspace for portfolio purposes.  It preserves selected protocols, experiment scripts, fixed-seed outputs, and review records, rather than the complete working tree or a full development history.
