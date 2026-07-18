# LOOP-0010 scalar crossed-minor certificate lane

## Scope and fail-closed status

Lane target: the determinant-level scalar crossed PAL/PCL principal minor

```text
Delta = M_{00} M_{33} - |M_{03}|^2 >= 0
```

for Hilbert-Schmidt orthonormal two-frames `X1,X2` and `Y1,Y2` in `M_4(C)`, with the trace rank-one update retained.  This is only the scalar crossed minor, not a full PCL certificate.  No Hermitian, positive, normal, or simultaneous-basis assumptions are made.

Verdict: no proof and no counterexample.  The useful output of this lane is an exact determinant-level bookkeeping identity plus a concrete obstruction to the natural determinant-level mixed-Cauchy ansatz `D1 D2 >= N12 N21`.

## Reproducible artifact

Script:

```text
research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py
```

Run command used from repository root:

```text
python research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py --samples 3000 --opt-starts 6 --maxiter 120 2>&1 | tee research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.stdout.log
```

Logs:

```text
research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.json
research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.stdout.log
```

The stdout summary reported:

```text
coordinate_min_delta = 0.0
coordinate_min_exchange_product_margin = -3.75
coordinate_positive_exchange_penalty_count = 6848
random_min_delta = 1.8376015909653387 at sample 1989
random_min_exchange_product_margin = -0.9634774182502084 at sample 2226
random_max_penalty_minus_slack = -1.837601590965339 at sample 1989
local min_delta = 3.9613078512756795e-13
local min_exchange_product_margin = -3.7499999999888525
local max_penalty_minus_slack objective value = 8.313350008393172e-13
```

The maximum mixed offdiagonal / determinant identity residual in the random scan was `8.881784197001252e-16`.

## Exact determinant bookkeeping identity

LOOP-0009 established the crossed mixed Plucker identity

```text
m := M_{03}
   = <W12, W21>
```

where `W12` is the direct-sum vector made from row wedges of `(X1,Y2)`, column wedges of `(X1,Y2)`, and the half-trace scalar component, and similarly `W21` is built from `(X2,Y1)`.  Let

```text
N12 = ||W12||^2
N21 = ||W21||^2
D1  = M_{00} = D(X1,Y1)
D2  = M_{33} = D(X2,Y2)
```

Then the crossed determinant has the exact split

```text
Delta = D1 D2 - |m|^2
      = (N12 N21 - |m|^2) - (N12 N21 - D1 D2).
```

Interpretation:

* `N12 N21 - |m|^2` is the ordinary Gram/Cauchy slack of the two mixed Plucker vectors.
* `N12 N21 - D1 D2` is the exchange penalty caused by the mismatch between the mixed pairs in the offdiagonal and the same-pair PAL diagonals.
* A scalar crossed-minor proof via this route must prove that the Gram slack dominates the exchange penalty.  The simpler determinant-level sub-ansatz `D1 D2 >= N12 N21` is false.

This identity is algebraic bookkeeping after LOOP-0009's exact `m=<W12,W21>` identity; it is not itself a positivity proof.

## Concrete obstruction to the natural refined ansatz

The determinant-level strengthening

```text
D1 D2 >= N12 N21
```

would let mixed Cauchy prove the crossed minor immediately.  It fails sharply.

Coordinate controls from the JSON log:

1. Product control (`product_LOOP9`):

```text
D1 = D2 = 0.5
D1 D2 = 0.25
N12 = N21 = 1.0
N12 N21 = 1.0
m = -0.5
Delta = 0.0
exchange product margin D1D2-N12N21 = -0.75
Gram slack = 0.75
exchange penalty = 0.75
```

Here the crossed determinant is repaired by exact cancellation: the positive exchange penalty is exactly matched by the mixed Gram slack.  Thus `D1D2 >= N12N21` fails even at equality.

2. Traceless control (`traceless_LOOP9`):

```text
D1 = D2 = 0.5
D1 D2 = 0.25
N12 = N21 = 2.0
N12 N21 = 4.0
m = 0.5
Delta = 0.0
exchange product margin D1D2-N12N21 = -3.75
Gram slack = 3.75
exchange penalty = 3.75
```

This is a larger equality obstruction: the determinant is nonnegative only because the mixed Cauchy slack cancels a large exchange penalty.

The full coordinate scan found:

```text
total coordinate two-plane pairs = 14400
positive_exchange_penalty_count = 6848
min exchange product margin = -3.75
min Delta = 0.0
max determinant identity residual = 0.0
max penalty/slack ratio = 1.0
```

So the false ansatz is not an isolated floating-point artifact; it fails throughout many exact sparse cases.

## Random and local optimization probes

Random scan with 3000 samples:

```text
min Delta = 1.8376015909653387
min D1D2-N12N21 = -0.9634774182502084
positive exchange penalty count = 1517 / 3000
max penalty/slack ratio = 0.32529075132502455
max identity/offdiagonal residual = 8.881784197001252e-16
```

Local BFGS probes with 6 starts and 120 max iterations found equality-adjacent points but no scalar violation:

```text
best min_delta objective = 3.9613078512756795e-13
best min_exchange_product_margin = -3.7499999999888525
best penalty_minus_slack = -8.313350008393172e-13
```

For the best near-equality `max_penalty_minus_slack` record:

```text
D1 ~= 0.7311845074
D2 ~= 0.7311847288
D1D2 ~= 0.5346309457
N12N21 ~= 3.9068011823
exchange penalty ~= 3.3721702366
Gram slack ~= 3.3721702366
Delta ~= 8.3149e-13
penalty/slack ratio ~= 0.9999999999997534
```

This again shows determinant-level cancellation between exchange penalty and Gram slack.  The optimizer did not produce `penalty > slack` beyond roundoff, hence did not refute the scalar minor.

## Takeaways for the next loop

1. The mixed Plucker route has an exact determinant-level split:

```text
Delta = mixed Gram slack - exchange penalty.
```

2. The simple determinant-level correction ansatz `D1D2 >= N12N21` is false; equality controls give exact obstructions with exchange margins `-0.75` and `-3.75`.

3. Numerics suggest the remaining sharp scalar target is the coupled inequality

```text
N12 N21 - |<W12,W21>|^2 >= N12 N21 - D1 D2,
```

but this is just the crossed-minor inequality in mixed-Gram coordinates unless the exchange penalty is further decomposed into a manifest sub-slack.  No such SOS/Gram sub-slack decomposition was found in this lane.

4. Fail-closed: this lane does not prove CLAIM-0001, does not prove full PCL, and found no certified scalar crossed-minor or rank-two positive-gap counterexample.
