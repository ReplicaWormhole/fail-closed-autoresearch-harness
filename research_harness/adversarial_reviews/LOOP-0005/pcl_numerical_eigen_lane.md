# LOOP-0005 PCL numerical/eigenvalue lane

## Scope

Implemented and ran a deterministic Projected Compression Lemma (PCL) checker/search for the CLAIM-0001 quadratic form

```text
q(C)=||tr_1 C||_F^2+||tr_2 C||_F^2-(1/2)|tr C|^2-2||C||_F^2.
```

For orthonormal two-frame bases `p1,p2` and `q1,q2` in `H = C^4 tensor C^4`, the script builds the four basis operators

```text
E_ij = |p_i><q_j|,  i,j in {1,2},
```

then forms the Hermitian compression matrix

```text
K_ab = <E_a, Phi(E_b)>,
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I.
```

A robust positive `lambda_max(K)` would reconstruct a rank-at-most-two positive-gap counterexample by taking the top eigenvector coefficients in the `E_ij` basis.

## Files

```text
research_harness/experiments/LOOP-0005_pcl_compression_search.py
research_harness/logs/LOOP-0005_pcl_search_seed5005.json
research_harness/logs/LOOP-0005_pcl_search_seed5005.stdout.log
research_harness/logs/LOOP-0005_pcl_search_smoke.json
research_harness/logs/LOOP-0005_pcl_search_smoke.stdout.log
research_harness/adversarial_reviews/LOOP-0005/pcl_numerical_eigen_lane.md
```

The smoke log was an initial low-budget executable check. The seed5005 log is the main run after fixing the LOOP-0002 equality regression gauge.

## Implementation notes

The script explicitly implements:

```text
tr_1(C)_{ab} = sum_i C_{ia,ib}
tr_2(C)_{ij} = sum_a C_{ia,ja}
tr(C)       = sum_{i,a} C_{ia,ia}
```

and adjoints:

```text
(tr_1^* M)_{ia,jb} = delta_{ij} M_{ab}
(tr_2^* N)_{ia,jb} = delta_{ab} N_{ij}
tr^*(z) = z I_16.
```

It also reconstructs the top-eigenvector operator and verifies directly that

```text
< C, Phi(C) > = gap(C)
```

up to floating-point roundoff.

## Commands run

Executable bit and smoke test:

```text
chmod +x research_harness/experiments/LOOP-0005_pcl_compression_search.py && python3 research_harness/experiments/LOOP-0005_pcl_compression_search.py --seed 5005 --random 100 --opt-restarts 2 --maxiter 20 --out research_harness/logs/LOOP-0005_pcl_search_smoke.json 2>&1 | tee research_harness/logs/LOOP-0005_pcl_search_smoke.stdout.log
```

Main run:

```text
python3 research_harness/experiments/LOOP-0005_pcl_compression_search.py --seed 5005 --random 5000 --opt-restarts 8 --maxiter 200 --out research_harness/logs/LOOP-0005_pcl_search_seed5005.json 2>&1 | tee research_harness/logs/LOOP-0005_pcl_search_seed5005.stdout.log
```

JSON summary extraction:

```text
python3 - <<'PY'
import json
p='research_harness/logs/LOOP-0005_pcl_search_seed5005.json'
out=json.load(open(p))
print(json.dumps({
 'self_check_adjoint': out['self_check_adjoint'],
 'equality': [{k:c[k] for k in ['name','witness_gap','lambda_max','eigvals','reconstructed_gap']} for c in out['equality_regressions']],
 'random_samples': out['random_search']['samples'],
 'random_positive_count': out['random_search']['positive_count_tol_1e_10'],
 'random_best_lambda_max': out['random_search']['best']['lambda_max'],
 'random_best_iter': out['random_search']['best']['iter'],
 'optimization_scipy': out['optimization']['scipy'],
 'optimization_restarts': out['optimization']['restarts'],
 'optimization_maxiter': out['optimization']['maxiter'],
 'optimization_best_lambda_max': out['optimization']['best']['lambda_max'],
 'optimization_best_reconstructed_gap': out['optimization']['best']['reconstructed_gap'],
 'best_overall_lambda_max': out['best_overall']['lambda_max'],
 'best_overall_reconstructed_gap': out['best_overall']['reconstructed_gap'],
 'positive_robust_tol_1e_8': out['positive_robust_tol_1e_8'],
 'elapsed_sec': out['elapsed_sec']
}, indent=2))
PY
```

## Exact main stdout summary

From `research_harness/logs/LOOP-0005_pcl_search_seed5005.stdout.log`:

```text
LOOP-0005 PCL compression search
{
  "scipy_available": true,
  "self_check_adjoint": {
    "sesquilinear_abs_error": 2.0097183471152322e-14,
    "quadratic_abs_error": 2.2737367544323206e-13
  }
}
equality regressions:
{"eigvals": [-2.0, -2.0, -1.0, 0.0], "lambda_max": 0.0, "name": "traceless_diagonal_E00_minus_E11", "reconstructed_gap": 0.0, "witness_gap": 0.0}
{"eigvals": [-1.0, -1.0, -1.0, 0.0], "lambda_max": 0.0, "name": "product_projection_P2_tensor_00", "reconstructed_gap": 4.440892098500626e-16, "witness_gap": -2.220446049250313e-16}
{"eigvals": [-1.0, -1.0, -1.0, 0.0], "lambda_max": 0.0, "name": "LOOP-0002_phase_absorbed_equality", "reconstructed_gap": 4.440892098500626e-16, "witness_gap": -2.220446049250313e-16}
random best:
{
  "name": null,
  "eigvals": [
    -1.771492703728363,
    -1.5983975168326383,
    -1.5125477296006746,
    -1.047205640060712
  ],
  "lambda_max": -1.047205640060712,
  "reconstructed_gap": -1.0472056400607115,
  "reconstructed_rank_tol_1e_10": 2,
  "gap_minus_lambda_max": 4.440892098500626e-16,
  "iter": 594
}
optimization best:
{
  "name": null,
  "eigvals": [
    -1.9999999999999658,
    -1.9999999999999571,
    -1.1506878160660161,
    -8.4668383415476e-14
  ],
  "lambda_max": -8.4668383415476e-14,
  "reconstructed_gap": -8.504308368628699e-14,
  "reconstructed_rank_tol_1e_10": 2,
  "gap_minus_lambda_max": -3.7470027081099033e-16,
  "restart": 5,
  "optimizer_success": false,
  "optimizer_message": "Desired error not necessarily achieved due to precision loss.",
  "nit": 130
}
summary:
{
  "best_lambda_max": 0.0,
  "best_reconstructed_gap": 0.0,
  "positive_robust_tol_1e_8": false,
  "out": "research_harness/logs/LOOP-0005_pcl_search_seed5005.json",
  "elapsed_sec": 88.37829041481018
}
```

The full stdout log contains the complete top eigenvector coefficients and singular-value lists.

## Exact extracted JSON summary

```text
{
  "self_check_adjoint": {
    "quadratic_abs_error": 2.2737367544323206e-13,
    "sesquilinear_abs_error": 2.0097183471152322e-14
  },
  "equality": [
    {
      "name": "traceless_diagonal_E00_minus_E11",
      "witness_gap": 0.0,
      "lambda_max": 0.0,
      "eigvals": [
        -2.0,
        -2.0,
        -1.0,
        0.0
      ],
      "reconstructed_gap": 0.0
    },
    {
      "name": "product_projection_P2_tensor_00",
      "witness_gap": -2.220446049250313e-16,
      "lambda_max": 0.0,
      "eigvals": [
        -1.0,
        -1.0,
        -1.0,
        0.0
      ],
      "reconstructed_gap": 4.440892098500626e-16
    },
    {
      "name": "LOOP-0002_phase_absorbed_equality",
      "witness_gap": -2.220446049250313e-16,
      "lambda_max": 0.0,
      "eigvals": [
        -1.0,
        -1.0,
        -1.0,
        0.0
      ],
      "reconstructed_gap": 4.440892098500626e-16
    }
  ],
  "random_samples": 5000,
  "random_positive_count": 0,
  "random_best_lambda_max": -1.047205640060712,
  "random_best_iter": 594,
  "optimization_scipy": true,
  "optimization_restarts": 8,
  "optimization_maxiter": 200,
  "optimization_best_lambda_max": -8.4668383415476e-14,
  "optimization_best_reconstructed_gap": -8.504308368628699e-14,
  "best_overall_lambda_max": 0.0,
  "best_overall_reconstructed_gap": 0.0,
  "positive_robust_tol_1e_8": false,
  "elapsed_sec": 88.37829041481018
}
```

## Findings

1. The adjoint/quadratic implementation self-check passed to roundoff:
   `sesquilinear_abs_error = 2.0097183471152322e-14`,
   `quadratic_abs_error = 2.2737367544323206e-13`.

2. Equality regressions passed:
   - traceless diagonal equality had eigenvalues `[-2, -2, -1, 0]` and witness gap `0`;
   - product-projection equality had eigenvalues `[-1, -1, -1, 0]` and witness gap `-2.22e-16`;
   - LOOP-0002 phase-absorbed equality support had eigenvalues `[-1, -1, -1, 0]` and witness gap `-2.22e-16`.

3. Random Grassmannian search over 5000 samples found no positive compression eigenvalue. Best random `lambda_max` was `-1.047205640060712`.

4. SciPy BFGS local optimization over 8 restarts / 200 max iterations drove the best compression eigenvalue to equality within roundoff, not positive: `lambda_max = -8.4668383415476e-14`, reconstructed direct gap `-8.504308368628699e-14`.

5. Best overall was one of the equality regressions: `lambda_max = 0.0`, reconstructed gap `0.0`.

## Verdict

No robust positive PCL compression eigenvalue was found. This is numerical evidence only, not a proof of PCL. The run supports the fail-closed status: no accepted proof and no accepted rank-two positive-gap counterexample from this lane.
