# Experiments: Partial-Trace Search

This directory is for reproducible numerical and symbolic searches related to `CLAIM-0001`.

## Existing baseline

The existing script lives at:

```text
problem_statement_aristotle/co_mathematician/scripts/check_partial_trace_ineq.py
```

Baseline command:

```bash
python3 problem_statement_aristotle/co_mathematician/scripts/check_partial_trace_ineq.py --samples 20000 --restarts 8 --maxiter 400
```

## Logging convention

Put machine-readable logs in:

```text
research_harness/logs/
```

Prefer JSON/JSONL for:

- command;
- timestamp;
- seed;
- samples/restarts/maxiter;
- best gap;
- candidate rank;
- singular values;
- Frobenius norm;
- trace term;
- partial-trace norms;
- candidate matrix path, if saved.
