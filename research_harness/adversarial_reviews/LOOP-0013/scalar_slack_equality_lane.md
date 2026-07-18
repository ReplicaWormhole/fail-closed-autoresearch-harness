# LOOP-0013 scalar slack / equality geometry lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
workstreams: WS-scalar-slack, WS-equality-geometry
success_condition_met: none

## Executive verdict

This lane advances U-0001 and U-0003, but does **not** prove CLAIM-0001, does **not** prove the universal scalar target

```text
Delta = D1 D2 - |m|^2 = GramSlack - ExchangePenalty >= 0,
```

and does **not** classify the global equality set on `Gr(2,16) x Gr(2,16)`.

Durable progress:

1. The LOOP-0012 coordinate equality signatures were promoted to explicit exact parametrized equality families in restricted charts.
2. On these families the mixed Plucker identity is exact and
   `GramSlack = ExchangePenalty > 0`, so any valid mixed Plucker/Gram/SOS certificate must contain an exchange-coupled cancellation mechanism.  A pure Cauchy-slack or product-domination shortcut is still impossible.
3. Complex-unitary random stress tests of the promoted families match the exact symbolic constants to roundoff.

Fail-closed verdict: **U-0003 is reduced by explicit equality families; U-0001 is sharpened by certificate guardrails, not closed.**

## Artifacts produced

- Script: `research_harness/experiments/LOOP-0013_scalar_slack_equality_symbolic.py`
- JSON log: `research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.json`
- Stdout log: `research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.stdout.log`
- Lane report: `research_harness/adversarial_reviews/LOOP-0013/scalar_slack_equality_lane.md`

Executable commands run from repository root:

```text
uv run --with numpy --with scipy --with sympy python \
  research_harness/experiments/LOOP-0013_scalar_slack_equality_symbolic.py \
  --seed 13013 \
  --samples 100 \
  --out research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.json \
  > research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.stdout.log

uv run --with numpy --with scipy --with sympy python -m py_compile \
  research_harness/experiments/LOOP-0013_scalar_slack_equality_symbolic.py
```

Stdout summary:

```json
{
  "elapsed_sec": 1.706650733947754,
  "numeric_max_abs_delta_by_family": {
    "diagonal_identical": 2.886579864025413e-15,
    "same_column_identical": 2.2204460492503135e-15,
    "same_column_translate": 4.440892098500635e-15,
    "same_row_identical": 2.2204460492503135e-15,
    "same_row_translate": 4.884981308350685e-15
  },
  "status": "parametric equality families certified in restricted charts; no universal scalar SOS/Plucker certificate; fail_closed"
}
```

## Symbolic mixed Plucker / Gram / SOS certificate attempt

Starting point retained from LOOP-0010/0012:

```text
m = <W_12, W_21>,
N12 = ||W_12||^2,
N21 = ||W_21||^2,
GramSlack = N12 N21 - |m|^2 >= 0,
ExchangePenalty = N12 N21 - D1 D2,
Delta = GramSlack - ExchangePenalty.
```

The LOOP-0013 script symbolically evaluates the scalar data on real one-parameter promoted equality charts.  In every chart below the exact SymPy result, reduced modulo `c^2+s^2=1`, has

```text
mixed_plucker_M03_residual = 0,
Delta = 0,
slack_minus_penalty = 0,
GramSlack = ExchangePenalty > 0.
```

Therefore a universal proof cannot be a certificate that merely exhibits the Cauchy slack as positive and then drops or pointwise bounds the exchange penalty.  The equality charts force exact positive-slack/positive-penalty cancellation.

This is an adversarial obstruction/guardrail, not a completed SOS certificate.  No global Gram matrix with positive semidefinite coefficients was found, and no Plucker-ideal Positivstellensatz/SOS identity for `Delta` was derived.

## Exact parametrized equality families from LOOP-0012 signatures

The symbolic parametrization uses real `c,s` with `c^2+s^2=1`,

```text
q1 = (c,s,0,0),
q2 = (-s,c,0,0),
```

and embeds `q1,q2` as row or column matrix vectors.  These are exact non-coordinate curves through the LOOP-0012 coordinate signatures.

### Family A1: same row, identical support

```text
X1 = Y1 = e_0 q1^T,
X2 = Y2 = e_0 q2^T.
```

Exact reduced scalar data:

```text
D1 = D2 = 1/2,
N12 = N21 = 1,
|m|^2 = 1/4,
GramSlack = 3/4,
ExchangePenalty = 3/4,
Delta = 0.
```

This globalizes the LOOP-0012 same-row identical-support coordinate signature.  The same computation applies to same-column identical support by transposition.

### Family A2: same column, identical support

```text
X1 = Y1 = q1 e_0^T,
X2 = Y2 = q2 e_0^T.
```

Exact reduced scalar data is again:

```text
D1 = D2 = 1/2,
N12 = N21 = 1,
|m|^2 = 1/4,
GramSlack = 3/4,
ExchangePenalty = 3/4,
Delta = 0.
```

### Family B1: same-row parallel disjoint translate

```text
X1 = e_0 q1^T,
X2 = e_0 q2^T,
Y1 = e_1 q1^T,
Y2 = e_1 q2^T.
```

Exact reduced scalar data:

```text
D1 = D2 = 1,
N12 = N21 = 2,
|m|^2 = 1,
GramSlack = 3,
ExchangePenalty = 3,
Delta = 0.
```

This globalizes the LOOP-0012 parallel disjoint row-translate signature.  The same computation applies to column translates by transposition.

### Family B2: same-column parallel disjoint translate

```text
X1 = q1 e_0^T,
X2 = q2 e_0^T,
Y1 = q1 e_1^T,
Y2 = q2 e_1^T.
```

Exact reduced scalar data is again:

```text
D1 = D2 = 1,
N12 = N21 = 2,
|m|^2 = 1,
GramSlack = 3,
ExchangePenalty = 3,
Delta = 0.
```

### Family C: diagonal identical support

```text
X1 = Y1 = e_0 q1^T,
X2 = Y2 = e_1 q2^T.
```

Exact reduced scalar data:

```text
D1 = D2 = 1/2,
N12 = N21 = 2,
|m|^2 = 1/4,
GramSlack = 15/4,
ExchangePenalty = 15/4,
Delta = 0.
```

This globalizes the LOOP-0012 diagonal identical-support coordinate signature.

## Complex-unitary stress test of the parametrized families

The script also replaced the real rotation `(q1,q2)` by random complex `4 x 2` orthonormal frames `Q` and evaluated the same row/column/diagonal constructions using the LOOP-0011 scalar bookkeeping.  With `100` samples per family:

```text
same_row_identical:      max |Delta| = 2.2204460492503135e-15
same_row_translate:      max |Delta| = 4.884981308350685e-15
same_column_identical:   max |Delta| = 2.2204460492503135e-15
same_column_translate:   max |Delta| = 4.440892098500635e-15
diagonal_identical:      max |Delta| = 2.886579864025413e-15
```

The first-record constants in the JSON log match the exact values above to floating-point precision, with penalty/slack ratio `1` up to roundoff.

This strongly suggests the real symbolic families extend to corresponding complex-unitary families.  However, the script only proves the real rotation charts exactly; the complex-unitary extension remains recorded as numerical evidence unless separately symbolized.

## Consequences for U-0001: scalar slack domination

The scalar inequality remains open.  LOOP-0013 did not find a counterexample and did not produce a proof.  It does sharpen the required certificate shape:

- `GramSlack >= 0` by Cauchy is too weak on its own.
- `ExchangePenalty <= 0`, `D1D2 >= N12N21`, `D1 >= N12`, and `D2 >= N21` remain false routes.
- Equality can occur with `GramSlack` equal to `3/4`, `3`, or `15/4`, exactly consumed by an equal positive `ExchangePenalty`.
- Any SOS/Gram certificate for `Delta` must vanish on the promoted equality families even though the underlying mixed Cauchy slack is positive.

Thus U-0001 is reduced only by stronger guardrails for the next symbolic attempt.

## Consequences for U-0003: equality geometry

The LOOP-0012 coordinate signatures are no longer isolated coordinate artifacts.  They sit inside explicit parametrized equality families:

1. same row/column identical support;
2. same-row/same-column parallel disjoint translates with shared internal two-frame;
3. diagonal identical support.

This reduces U-0003 by supplying exact equality families suitable for future tangent/normal-cone and certificate-vanishing tests.

It does not close U-0003.  The following remain unproved:

- no global classification of all equality components;
- no exclusion of non-row/column/diagonal equality families;
- no proof that the complex-unitary promoted families exhaust a local branch;
- no proof that these scalar equality families imply full-PCL equality families.

## Fail-closed caveats

- No proof of CLAIM-0001 was produced.
- No proof of the universal scalar crossed-minor inequality was produced.
- No full PCL certificate was produced.
- No scalar counterexample was found.
- The exact symbolic work is restricted to selected parametrized charts.
- The complex-unitary globalization is numerical stress evidence, not a symbolic theorem.
- Coordinate/local evidence is not promoted to a global proof.
