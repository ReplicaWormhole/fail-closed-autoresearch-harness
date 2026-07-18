# LOOP-0009 zero-mode classification lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: tangent/equality zero-mode diagnostics
success_condition_met: none

## Executive verdict

I repaired and ran the zero-mode lane after the earlier failed attempt.  It confirms the LOOP-0008 numerical observation: at both sharp equality controls, the original rank-two gap is stationary on the real Frobenius unit sphere and the Hessian has no positive eigenvalues.  The observed zero modes are numerical diagnostics, not a classification theorem.

## Real run output

Command:

```text
python3 research_harness/experiments/LOOP-0009_zero_mode_classification.py \
  --out research_harness/logs/LOOP-0009_zero_mode_classification.json \
  > research_harness/logs/LOOP-0009_zero_mode_classification.stdout.log
python3 -m py_compile research_harness/experiments/LOOP-0009_zero_mode_classification.py
```

Summary:

```text
diag_difference: zero_count=9, positive_count=0, eigmax=0.0
product_projection: zero_count=13, positive_count=0, eigmax=0.0
```

## Interpretation

For the diagonal-difference control, the zero-mode aggregate core block mean is
`0.11111111111111109`.  For the product-projection control it is
`0.0769230769230769`.  The finite epsilon sweeps in the JSON log stay at equality/negative values to numerical precision along sampled Hessian-zero basis vectors.

This supports the working hypothesis that the Hessian-zero directions are symmetry/equality-family directions rather than missed unstable directions.  It does not prove that all zero modes are exactly tangent to equality manifolds, because the basis was obtained numerically and no symbolic orbit parametrization was certified.

## Fail-closed caveats

- No global proof of CLAIM-0001.
- No exact equality-manifold classification.
- No use of local tangent evidence as a substitute for the full PCL certificate.

Artifacts:

- `research_harness/experiments/LOOP-0009_zero_mode_classification.py`
- `research_harness/logs/LOOP-0009_zero_mode_classification.json`
- `research_harness/logs/LOOP-0009_zero_mode_classification.stdout.log`
