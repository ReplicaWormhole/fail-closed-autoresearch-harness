# WS-full-pcl-certificate goal

Goal: G2
State: active

## Purpose

Find a trace-coupled certificate that the full PCL matrix `M` is PSD.

## Current evidence

LOOP-0011 Schur diagnostics reject D-only routes and found no M violation.

## Hard constraints

- Preserve fail-closed status unless reviewer/auditor gates are met.
- Write incremental progress to `incremental_report.md`.
- Record dead ends in `failed_attempts.md` or the global failed-explorations ledger.
- Record unresolved assumptions in `uncertainty.md` or the global uncertainty ledger.
- Attach scripts/logs under this workstream or `research_harness/experiments` and `research_harness/logs` with loop prefixes.
