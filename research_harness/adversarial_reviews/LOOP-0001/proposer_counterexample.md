# LOOP-0001 Proposer Counterexample / Stronger-Variant Report

## Scope

Target claim (CLAIM-0001): for `C in M_4(C) tensor M_4(C)` with `rank(C) <= 2`,

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 <= 2 ||C||_F^2 + (1/2) |tr C|^2.
```

Gap convention throughout:

```text
gap_alpha(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
               - 2 ||C||_F^2 - alpha |tr C|^2.
```

Positive gap means violation of the variant with coefficient `alpha`. The original claim uses `alpha = 1/2`.

## Executive verdict

I did not find a counterexample to the exact rank-2/alpha-1/2 claim. However, two natural stronger variants are refuted by explicit elementary witnesses:

1. Smaller trace coefficient `alpha < 1/2` is false already at rank 2.
2. Extending the original inequality from rank 2 to rank 3 is false.

The numerical optimization also independently rediscovered these witnesses/families.

## Exact witness family

Let

```text
P_r = diag(1,...,1,0,...,0) in M_4(C),  rank(P_r)=r,
E = |0><0| in M_4(C),
C_r = (1/sqrt(r)) P_r tensor E,     1 <= r <= 4.
```

Then `rank(C_r)=r`, `||C_r||_F^2=1`, and with the repository's partial-trace convention,

```text
||tr_1 C_r||_F^2 = r,
||tr_2 C_r||_F^2 = 1,
|tr C_r|^2 = r.
```

Therefore

```text
gap_alpha(C_r) = (r + 1) - 2 - alpha r = r(1-alpha) - 1.
```

Consequences:

- For `r=2`, `gap_alpha(C_2) = 1 - 2 alpha`.
  - At `alpha=1/2`, this is equality.
  - For every `alpha < 1/2`, this is positive, so the smaller-coefficient stronger variant is false.
- For `r=3`, original `alpha=1/2` gives `gap_{1/2}(C_3)=1/2 > 0`, so the rank-3 extension is false.
- For one-partial-trace variants, `||tr_1 C_r||_F^2 = r ||C_r||_F^2`; in particular rank 2 already gives an individual partial trace with squared norm `2`, so any proposed one-trace bound with coefficient below `2` is false at rank 2.

This exact family also explains a likely equality structure: product operators with one tensor factor a rank-r projection and the other a rank-one projection make one partial trace large and force the trace term to pay exactly the missing amount when `r=2`, `alpha=1/2`.

## Exact arithmetic/logged verification

Command run:

```bash
python3 - <<'PY' | tee research_harness/logs/loop_0001_exact_witnesses.log
import numpy as np, math
N=4; D=16

def partial_traces(C):
    T=C.reshape(N,N,N,N)
    return np.einsum('abac->bc',T), np.einsum('abcb->ac',T)

def metrics(C, alpha):
    t1,t2=partial_traces(C)
    pt1=float(np.vdot(t1,t1).real); pt2=float(np.vdot(t2,t2).real)
    norm2=float(np.vdot(C,C).real); tr2=float(abs(np.trace(C))**2)
    return dict(rank=int((np.linalg.svd(C,compute_uv=False)>1e-10).sum()), norm2=norm2, pt1=pt1, pt2=pt2, lhs=pt1+pt2, trace_abs2=tr2, alpha=alpha, gap=pt1+pt2-2*norm2-alpha*tr2)

def kron_witness(r):
    A=np.diag([1]*r+[0]*(N-r)).astype(complex)
    B=np.zeros((N,N),complex); B[0,0]=1
    return np.kron(A,B)/math.sqrt(r)
for r in [1,2,3,4]:
    C=kron_witness(r)
    for alpha in ([0.5] if r!=2 else [0.5,0.49,0.25,0.0]):
        print(f"P_{r} tensor E00 / sqrt({r}), alpha={alpha}:", metrics(C, alpha))
C=np.zeros((D,D),complex)
for i,v in enumerate([1,1,-2]): C[i*N+i,i*N+i]=v
C=C/math.sqrt(np.vdot(C,C).real)
print('diag(|00><00|+|11><11|-2|22><22|)/sqrt6:', metrics(C,0.5))
PY
```

Key output from `research_harness/logs/loop_0001_exact_witnesses.log`:

```text
P_2 tensor E00 / sqrt(2), alpha=0.5: gap = -2.220446049250313e-16
P_2 tensor E00 / sqrt(2), alpha=0.49: gap = 0.019999999999999796
P_2 tensor E00 / sqrt(2), alpha=0.25: gap = 0.49999999999999967
P_2 tensor E00 / sqrt(2), alpha=0.0: gap = 0.9999999999999996
P_3 tensor E00 / sqrt(3), alpha=0.5: gap = 0.5000000000000007
diag(|00><00|+|11><11|-2|22><22|)/sqrt6: gap = 0.0
```

The last traceless diagonal rank-3 example shows that some rank-3 matrices still saturate the original-form inequality; the rank-3 extension fails because of `C_3`, not because all rank-3 equality-like constructions violate.

## Numerical searches run

### Existing repository script

Command:

```bash
python3 problem_statement_aristotle/co_mathematician/scripts/check_partial_trace_ineq.py \
  --seed 1001 --samples 5000 --restarts 4 --maxiter 150 \
  | tee research_harness/logs/loop_0001_existing_script_seed1001.log
```

Output summary:

```text
best random rank-1: gap lhs-rhs = -1.2100867361647392e+00
best random rank-2: gap lhs-rhs = -1.1633264621458861e+00
best optimized: rank parameter 2, numerical rank 2,
  lhs = 2.0000000000000018
  rhs = 2.0000000000000098
  gap lhs-rhs = -7.9936057773011271e-15
  |tr C|^2 = 0.0000000000000199
```

This did not find a violation of the exact claim and converged to near equality.

### Custom stronger-variant search

Script created:

```text
research_harness/logs/loop_0001_counterexample_search.py
```

Command:

```bash
python3 research_harness/logs/loop_0001_counterexample_search.py \
  --seed 1001 --samples 4000 --restarts 6 --maxiter 220 \
  --out research_harness/logs/loop_0001_counterexample_search_seed1001.json \
  | tee research_harness/logs/loop_0001_counterexample_search_seed1001.stdout.log
```

Important numerical results:

```text
optimized_rank2_gap_alpha_alpha0.25:
  rank parameter 2, numerical rank 2
  lhs ≈ 3.000000000000
  ||C||_F^2 ≈ 1
  |tr C|^2 ≈ 2
  gap_{1/2} ≈ -9.88e-15
  objective gap_{0.25} ≈ 0.5

optimized_rank2_alpha_needed_alpha0.5:
  alpha_needed ≈ 0.4999999999999844

optimized_rank3_sum_minus_2norm_alpha0.5:
  rank parameter 3, numerical rank 3
  lhs ≈ 4.000000000000
  ||C||_F^2 ≈ 1
  |tr C|^2 ≈ 3
  gap_{1/2} ≈ 0.4999999999999851

optimized_rank3_pt1_minus_norm_alpha0.5:
  pt1 ≈ 3.000000000000
  gap_{1/2} ≈ 0.9470153079674046
```

Caveat: the `optimized_rank3_alpha_needed` objective produced a large `alpha_needed` by driving the trace nearly to zero while keeping a small positive rank-3 original gap. That objective is ill-conditioned near zero trace and should not be interpreted as a sharp coefficient estimate. The exact `C_3` construction above is the clean rank-3 refutation.

## Attacked stronger statements and outcomes

### 1. Coefficient smaller than `1/2`

Statement attacked:

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 <= 2 ||C||_F^2 + alpha |tr C|^2,
rank(C) <= 2,
alpha < 1/2.
```

Outcome: refuted exactly by `C_2 = (1/sqrt(2)) P_2 tensor E`.

For this rank-2 witness,

```text
||C_2||_F^2 = 1,
||tr_1 C_2||_F^2 = 2,
||tr_2 C_2||_F^2 = 1,
|tr C_2|^2 = 2,
gap_alpha(C_2) = 1 - 2 alpha.
```

Thus any `alpha < 1/2` gives a positive gap. The known traceless equality witness in the claim card does not refute smaller `alpha` because its trace is zero; this product-projection equality witness does.

### 2. Rank 3 extension

Statement attacked: same inequality with `rank(C) <= 3`.

Outcome: refuted exactly by `C_3 = (1/sqrt(3)) P_3 tensor E`.

For this rank-3 witness,

```text
||C_3||_F^2 = 1,
||tr_1 C_3||_F^2 = 3,
||tr_2 C_3||_F^2 = 1,
|tr C_3|^2 = 3,
gap_{1/2}(C_3) = 4 - 2 - 3/2 = 1/2 > 0.
```

### 3. One partial trace alone

A possible sharper one-trace statement such as `||tr_i C||_F^2 <= ||C||_F^2` is false. The same family gives

```text
||tr_1 C_r||_F^2 = r ||C_r||_F^2.
```

In particular, `C_2` has rank 2 and `||tr_1 C_2||_F^2 = 2 ||C_2||_F^2`. Therefore any rank-2 one-partial-trace coefficient below `2` is impossible. The numerical one-trace optimization also converged to `pt1 ≈ 2` for rank 2 and `pt1 ≈ 3` for rank 3.

### 4. Dimension/rank-dependent variants

The exact family in dimension 4 suggests the natural rank-dependent obstruction

```text
gap_{1/2}(C_r) = r/2 - 1.
```

So the original coefficient `1/2` is compatible with this product-projection family only for `r <= 2`. For `r > 2`, it fails. In larger local dimensions, the same construction works for any available `r`, so any dimension-independent theorem allowing ranks greater than 2 would need a different right-hand side.

## Structural conjecture suggested by failures/successes

The rank-2 claim appears to be sharp in at least two different ways:

1. Traceless diagonal equality, as recorded in CLAIM-0001:
   `(|00><00| - |11><11|)/sqrt(2)` with zero trace.
2. Product-projection equality:
   `(P_2 tensor |0><0|)/sqrt(2)` with nonzero trace and one large partial trace.

The second family shows why the `1/2 |tr C|^2` term cannot be reduced and why rank 2 is a genuine boundary. Any proof of CLAIM-0001 must account not only for cancellation/traceless equality cases, but also for high-trace product-projection equality cases where one partial trace has squared Frobenius norm `2 ||C||_F^2`.

## Files created/modified

- Created `research_harness/logs/loop_0001_counterexample_search.py`.
- Created `research_harness/logs/loop_0001_counterexample_search_seed1001.json`.
- Created `research_harness/logs/loop_0001_counterexample_search_seed1001.stdout.log`.
- Created `research_harness/logs/loop_0001_existing_script_seed1001.log`.
- Created `research_harness/logs/loop_0001_exact_witnesses.log`.
- Created this report: `research_harness/adversarial_reviews/LOOP-0001/proposer_counterexample.md`.

## Caveats

- Numerical evidence is not proof of the exact rank-2 claim.
- The explicit stronger-variant counterexamples above are exact up to the displayed elementary arithmetic; the Python logs only verify implementation/convention consistency.
- No positive gap was found for the exact rank-2, alpha-1/2 claim in the runs above.
