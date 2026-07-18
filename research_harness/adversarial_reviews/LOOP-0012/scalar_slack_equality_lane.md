# LOOP-0012 scalar slack / equality geometry lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
workstreams: WS-scalar-slack, WS-equality-geometry
success_condition_met: none

## Executive verdict

This lane advanced U-0001 and U-0003 but did not prove CLAIM-0001, did not prove scalar slack domination, and did not give a global equality theorem.

The durable contribution is an exact coordinate-support equality/orbit classification for cases where the scalar crossed-minor exchange penalty equals the Gram/Cauchy slack.  The result reinforces that the scalar target must prove exact cancellation:

```text
Delta = D1D2 - |m|^2
      = GramSlack - ExchangePenalty >= 0.
```

The finite coordinate ratio-1 cases have positive exchange penalty exactly matched by positive Gram slack, so product-domination shortcuts remain invalid.

## Fresh executable run

Commands run from repository root by the lane coordinator:

```text
/usr/bin/python3 research_harness/experiments/LOOP-0011_scalar_slack_domination_lane.py \
  --seed 12012 \
  --samples 3000 \
  --opt-starts 3 \
  --maxiter 80 \
  --out research_harness/logs/LOOP-0012_scalar_slack_domination_seed12012.json \
  > research_harness/logs/LOOP-0012_scalar_slack_domination_seed12012.stdout.log

/usr/bin/python3 -m py_compile research_harness/experiments/LOOP-0011_scalar_slack_domination_lane.py
```

Artifacts:

- `research_harness/logs/LOOP-0012_scalar_slack_domination_seed12012.json`
- `research_harness/logs/LOOP-0012_scalar_slack_domination_seed12012.stdout.log`
- prior script reused: `research_harness/experiments/LOOP-0011_scalar_slack_domination_lane.py`

Summary of real output:

```json
{
  "coordinate_eq": 264,
  "coordinate_sigs": 3,
  "coordinate_max_ratio": 1.0,
  "random_min_delta": [1.7981937112983, 648],
  "random_max_ratio": [0.3263744923143517, 475],
  "random_min_gap": [0.6716069430278583, 2601],
  "local_min_delta": 6.631749030725257e-12,
  "local_max_ratio_objective": -0.9999999898468404,
  "local_min_gap": 1.994077129807703e-08
}
```

Interpretation: coordinate equality remains sharp with ratio `1`; random samples stayed away from violation; local optimization approached equality/roundoff but did not cross it.

## Exact scalar bookkeeping

Let `X_1,X_2` and `Y_1,Y_2` be Hilbert-Schmidt orthonormal two-frames in `M_4(C)`.  For the crossed scalar PAL/PCL minor indexed by `(1,1)` and `(2,2)`, write

```text
Delta = D1D2 - |m|^2.
```

Using the mixed Plucker vector identity from LOOP-0009, the crossed entry can be written

```text
m = <W_12, W_21>,
N12 = ||W_12||^2,
N21 = ||W_21||^2.
```

Thus Cauchy gives the Gram/Cauchy slack

```text
GramSlack = N12 N21 - |m|^2 >= 0.
```

The exact target decomposes as

```text
Delta = (N12 N21 - |m|^2) - (N12 N21 - D1D2)
      = GramSlack - ExchangePenalty.
```

Therefore the unresolved scalar inequality is exactly

```text
GramSlack >= ExchangePenalty.
```

The false routes `D1D2 >= N12N21`, `D1 >= N12`, and `D2 >= N21` would make the exchange penalty nonpositive or separately bounded.  They are contradicted by the equality controls below.

## Coordinate ratio-1/equality signatures

Coordinate two-frames were enumerated by unordered two-element supports in the standard basis of `C^4 tensor C^4`.  Write a coordinate index as `(row,column)`.

The coordinate cases with `ExchangePenalty/GramSlack = 1` were exactly the coordinate equality cases in this scan: `Delta=0`.  There are `264` cases in `3` exact signatures.

### Signature A: same row or same column, identical supports

Count: `48`.

Representative row case:

```text
U=V={(0,0),(0,1)}.
```

Representative column case:

```text
U=V={(0,0),(1,0)}.
```

Exact scalar data:

```text
D1 = D2 = 1/2,
N12 N21 = 1,
|m|^2 = 1/4,
GramSlack = 3/4,
ExchangePenalty = 3/4,
Delta = 0.
```

### Signature B: same-row/same-column parallel disjoint translates

Count: `144`.

Representative row case:

```text
U={(0,0),(0,1)}, V={(1,0),(1,1)}.
```

Representative column case:

```text
U={(0,0),(1,0)}, V={(0,1),(1,1)}.
```

Exact scalar data:

```text
D1 = D2 = 1,
N12 N21 = 4,
|m|^2 = 1,
GramSlack = 3,
ExchangePenalty = 3,
Delta = 0.
```

### Signature C: diagonal supports, identical supports

Count: `72`.

Representative case:

```text
U=V={(0,0),(1,1)}.
```

Exact scalar data:

```text
D1 = D2 = 1/2,
N12 N21 = 4,
|m|^2 = 1/4,
GramSlack = 15/4,
ExchangePenalty = 15/4,
Delta = 0.
```

## Consequences for a mixed Plucker/SOS certificate

The natural three-step route remains only partially viable:

1. `m=<W_12,W_21>` is exact.
2. `N12 N21 - |m|^2` is an honest Gram/Cauchy slack.
3. Proving this slack dominates `N12 N21 - D1D2` is still open.

The coordinate equality cases show that equality is not simply Cauchy equality of `W_12` and `W_21`; in the controls the Gram slack is positive and exactly consumed by a positive exchange penalty.  A valid certificate therefore needs exchange-coupled terms and cannot be a pure pointwise norm domination of same-pair defects over mixed Plucker norms.

## Consequences for equality geometry

The coordinate equality families are now organized as:

1. same row/column identical support;
2. same row/column parallel disjoint translates preserving internal coordinate pattern;
3. diagonal identical support.

This is consistent with the LOOP-0011 local zero-mode classifications for product-projection and diagonal-difference controls.  It is not a global equality classification on `Gr(2,16) x Gr(2,16)`: coordinate enumeration and local Hessian zero-mode data cannot exclude non-coordinate equality components or prove global stability.

## Fail-closed caveats

- No complete proof of CLAIM-0001 was produced.
- No scalar violation was found.
- No global equality theorem was proved.
- No hidden Hermitian, normal, positive, density, convexity, operator-Schmidt-rank, or fixed-gauge complex-coefficient assumption is used.
- The scalar crossed-minor target, even if proved later, is not by itself a full PCL certificate.
