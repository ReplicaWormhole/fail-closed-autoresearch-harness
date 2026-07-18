# LOOP-0007 Certified Search Lane

status: fail_closed_no_counterexample
claim_focus: CLAIM-0001-rank-two-partial-trace
last_updated: 2026-06-03
script: research_harness/experiments/LOOP-0007_certified_search.py
log: research_harness/logs/LOOP-0007_certified_search_seed7007.json
stdout_log: research_harness/logs/LOOP-0007_certified_search_seed7007.stdout.log

## Scope

This lane searched for violations of the original rank-two inequality

```text
gap(C)=||tr_1 C||_F^2+||tr_2 C||_F^2-2||C||_F^2-(1/2)|tr C|^2 <= 0
```

for explicit rank-at-most-two matrices `C` in `M_4(C) tensor M_4(C)`. It used
the corrected LOOP-0006 partial-trace convention:

```text
tr_1(C)[a,b] = sum_i C[i,a,i,b]
tr_2(C)[i,j] = sum_a C[i,a,j,a]
```

All reported search scores are normalized by `||C||_F^2`. This is a numerical
search/regression lane, not a proof lane.

## Methods actually run

Command:

```text
python3 research_harness/experiments/LOOP-0007_certified_search.py \
  --seed 7007 --random-trials 20000 --perturb-trials 2000 \
  --out research_harness/logs/LOOP-0007_certified_search_seed7007.json
```

The script performed:

1. Equality regressions on three sparse rank-at-most-two controls.
2. `20000` random complex rank-two matrices `C=A B^*`, normalized in Frobenius norm.
3. Rank-two SVD-truncated perturbations around equality/control families, for
   epsilons `1e-4, 1e-3, 1e-2, 1e-1, 5e-1`, with `2000` perturbation trials per
   family/epsilon.
4. Exhaustive coordinate two-unit scan over normalized sums of one or two matrix
   units with phases `+1,-1,+i,-i`.

## Key numerical output

```text
seed: 7007
equality normalized gaps:
  diag_difference: 0.0
  product_projection: -2.2204460492503136e-16
  phase_sparse_control: -0.5
random_rank2 trials: 20000
random best normalized gap: -1.2143877928448128
random positive count tol 1e-10: 0
coordinate scan total: 130816
coordinate best normalized gap: 0.0
coordinate positive count tol 1e-10: 0
best perturbation normalized gap: -7.779413143726018e-10
robust_positive_gap_found: False
```

The two main equality controls reproduce zero up to roundoff:

- diagonal difference: exactly `0.0` in this run;
- product projection: `-2.2204460492503136e-16`, i.e. numerical zero.

The phase sparse control is nonpositive (`-0.5`) and is included as a guard
against promoting the older fixed-gauge false route.

## Verdict

No certified positive-gap rank-two counterexample was found.

This does not prove CLAIM-0001. It only says that this particular corrected
search lane found no robust positive original gap among random rank-two factors,
equality perturbations, and coordinate two-unit sparse scans.

## Fail-closed caveats

- Absence of positives in this search is only evidence, not a theorem.
- SVD truncation of equality perturbations is a search heuristic; it does not
  characterize all tangent directions of the rank-two variety.
- A future positive candidate must be recorded as an explicit `16 x 16` matrix
  with certified rank at most two and original-convention positive `gap(C)`, then
  independently checked by interval/rational or high-precision arithmetic.

## Next search subtargets

1. Add a tangent-space parameterization at the sharp equality manifolds instead
   of SVD-truncated ambient perturbations.
2. Couple the search to the PCL support-compression matrix and record both the
   largest compression eigenvector and the corresponding original `C=PCQ`.
3. If a near-zero optimizer appears, extract invariants and attempt exact
   reconstruction rather than treating numerical equality as success.
