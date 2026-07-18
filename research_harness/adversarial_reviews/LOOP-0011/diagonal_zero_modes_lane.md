# LOOP-0011 diagonal-difference zero-mode lane

## Scope
Targeted the four `diag_difference` Hessian zero modes left unclassified by LOOP-0010 phase/product-unitary candidates.  This is fail-closed local evidence only, not a global proof.

Control:
`C0 = (|00><00| - |11><11|)/sqrt(2)` with row/column tensor index `(i,a)`.

## Method
Reused LOOP-0008 tangent/Hessian construction and LOOP-0010 real principal-angle containment diagnostics.  Added active support-plane candidates in the 2x2 atom plane:

- `P = |0><0| + |1><1|`
- `A,B in {E01, E10}`
- candidate real directions from `i C0`, `A ⊗ P`, `i A ⊗ P`, `P ⊗ B`, `i P ⊗ B`

These directions match the exact support pattern of the numerical zero kernel and include individual sampled rank-2 zero-gap rays.

## Results

- Hessian zero count at tol `1e-10`: `9`
- Negative count: `110`
- Positive count: `0`
- Eigenvalue range: `-2.0` to `0.0`

Containment diagnostics:

| candidate set | rank | zero dim | classified | unclassified | contains zero space | max residual | min principal cosine |
|---|---:|---:|---:|---:|---|---:|---:|
| LOOP-0010 prior candidates | 43 | 9 | 5 | 4 | False | 7.071e-01 | 0.000e+00 |
| expanded support-plane only | 9 | 9 | 9 | 0 | True | 1.570e-16 | 1.000e+00 |
| prior + expanded support-plane | 47 | 9 | 9 | 0 | True | 3.189e-16 | 1.000e+00 |
| four-dimensional prior residual vs expanded | 9 | 4 | 4 | 0 | True | 7.850e-17 | 1.000e+00 |

Expanded orthonormal candidate Rayleigh abs max: `0.000e+00`.

## Interpretation
The added active support-plane family locally classifies all nine `diag_difference` Hessian zero modes.  More specifically, the four-dimensional residual left after LOOP-0010 prior candidates is contained in the expanded support-plane span with max residual `7.850e-17`.

Individual sampled one-parameter rays `C0 + tD` for the expanded directions stayed rank <= 2 and had zero gap to floating-point precision in the JSON log.  This supports, but does not prove globally, that the missing directions come from active two-product-atom support-plane equality families.

## Artifacts

- JSON log: `./research_harness/logs/LOOP-0011_diagonal_zero_modes_lane.json`
- Script: `research_harness/experiments/LOOP-0011_diagonal_zero_modes_lane.py`

## Caveat
This is a local tangent-space classification of the numerical zero kernel. The sampled one-parameter zero-gap rays support the equality-family interpretation, but this is not a global proof of the inequality or a complete global equality classification.
