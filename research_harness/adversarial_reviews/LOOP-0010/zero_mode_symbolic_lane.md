# LOOP-0010 equality zero-mode symbolic classification lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: local equality/symmetry tangent classification of Hessian zero modes
success_condition_met: none

## Executive verdict

I added and ran a reproducible local classification script comparing the numerical Hessian zero eigenspaces from the LOOP-0008 tangent lane with explicit analytic candidate tangent directions:

- global phase direction `i C0`,
- local product-unitary orbit directions under
  `C -> (U1⊗U2) C (V1⊗V2)^*`,
- small named core/equality-family diagnostic directions.

The result is mixed and fail-closed:

- `product_projection`: all 13 numerical zero modes are contained in the explicit candidate span to roundoff.
- `diag_difference`: only 5 of 9 numerical zero modes are contained in the explicit candidate span used here; 4 zero dimensions remain unclassified by this lane.

No positive Hessian directions were found in either control, matching LOOP-0008/0009.

## Real run output

Command:

```text
python3 -m py_compile research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py
python3 research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py \
  --out research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.json \
  > research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.stdout.log
```

Stdout summary:

```json
{
  "diag_difference": {
    "zero_count": 9,
    "positive_count": 0,
    "local_rank": 42,
    "all_candidate_rank": 43,
    "all_candidate_contains_zero_space": false,
    "classified_dim": 5,
    "unclassified_dim": 4,
    "max_residual": 0.7071067811865475,
    "min_principal_cosine": 0.0
  },
  "product_projection": {
    "zero_count": 13,
    "positive_count": 0,
    "local_rank": 32,
    "all_candidate_rank": 33,
    "all_candidate_contains_zero_space": true,
    "classified_dim": 13,
    "unclassified_dim": 0,
    "max_residual": 2.220446049250313e-16,
    "min_principal_cosine": 1.0
  }
}
```

## Method details

The script imports the LOOP-0008 tangent machinery, constructs the real Frobenius unit-sphere rank-two tangent basis, diagonalizes the Hessian quadratic form, and extracts the zero eigenspace using tolerance `1e-10`.

For each equality control it then constructs analytic candidate directions and compares subspaces using real Frobenius principal-angle diagnostics in the LOOP-0008 tangent coordinates.  The main containment metric is the maximum residual norm after projecting numerical zero eigenvectors onto the candidate span; principal cosines near 1 count as classified dimensions.

## Findings by control

### diag_difference

- Hessian zero modes: 9.
- Positive Hessian modes: 0.
- Candidate span rank after tangent projection: 43.
- Classified zero dimension: 5.
- Unclassified zero dimension: 4.
- Max zero-vector residual against candidates: `0.7071067811865475`.
- Principal cosines for all candidates include five values at numerical 1 and four near zero.

Interpretation: phase/local product-unitary/core candidates explain part, but not all, of the observed zero eigenspace.  The remaining 4 dimensions may require a more specific diagonal-difference equality-family parametrization, a larger analytic symmetry/equality family, or exact symbolic kernel analysis.  This lane does not certify them.

### product_projection

- Hessian zero modes: 13.
- Positive Hessian modes: 0.
- Candidate span rank after tangent projection: 33.
- Classified zero dimension: 13.
- Unclassified zero dimension: 0.
- Max zero-vector residual against candidates: `2.220446049250313e-16`.
- Minimum principal cosine: `1.0`.

Interpretation: the local zero eigenspace at the product-projection equality control is numerically contained in the explicit phase/product-unitary equality candidate span.

## Fail-closed caveats

- This is a local tangent-space classification check, not a global proof of CLAIM-0001.
- The comparison still depends on floating-point eigenspaces and a tolerance.
- For `diag_difference`, 4 numerical zero dimensions remain unclassified by the explicit candidates used here.
- Even where local containment succeeds (`product_projection`), it only identifies local zero modes with candidate equality/symmetry directions; it does not prove the full global equality set or the inequality.

## Artifacts

- `research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py`
- `research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.json`
- `research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.stdout.log`
- `research_harness/adversarial_reviews/LOOP-0010/zero_mode_symbolic_lane.md`
