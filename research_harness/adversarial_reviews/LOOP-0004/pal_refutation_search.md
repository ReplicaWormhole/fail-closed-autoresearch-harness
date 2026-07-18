# LOOP-0004 PAL Refutation/Search Report

status: completed_no_violation_found
claim_focus: CLAIM-0001-rank-two-partial-trace
pal_status: no_refutation_found
last_updated: 2026-06-03

## Target

LOOP-0004 attacked the phase-aware scalar candidate PAL isolated in LOOP-0003.
For Hilbert-Schmidt orthonormal two-frames `X_1,X_2` and `Y_1,Y_2` in `M_4(C)`, define

```text
L_i = X_i Y_i^*,
R_i = X_i^* Y_i,
t_i = tr(X_i^*Y_i),
a = <L_1,L_2>_F,
b = <R_1,R_2>_F - (1/2) conjugate(t_1)t_2,
D_i = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2.
```

PAL is

```text
|a + conjugate(b)|^2 <= D_1 D_2.
```

A positive value of

```text
violation = |a + conjugate(b)|^2 - D_1D_2
```

would refute PAL. A PAL refutation would still need conversion back to an original
rank-two `C` and a direct check of `gap(C)` before it could refute CLAIM-0001.

## Executable artifact

Script:

```text
research_harness/experiments/LOOP-0004_pal_search.py
```

Main command actually run:

```text
python3 research_harness/experiments/LOOP-0004_pal_search.py   --seed 4004   --random 8000   --maxiter 250   --out research_harness/logs/LOOP-0004_pal_search_seed4004.json   > research_harness/logs/LOOP-0004_pal_search_seed4004.stdout.log
```

Log files:

```text
research_harness/logs/LOOP-0004_pal_search_seed4004.json
research_harness/logs/LOOP-0004_pal_search_seed4004.stdout.log
```

## Searches performed

1. Exhaustive matrix-unit two-frame sweep.
   - `X_1,X_2,Y_1,Y_2` chosen from distinct matrix units, so each pair is
     Hilbert-Schmidt orthonormal.
   - Total cases: 57,600.

2. Random complex two-frame search.
   - 8,000 random QR-generated two-frames for `X` and `Y`.

3. Continuous nonconvex optimization.
   - SciPy BFGS over unconstrained real parameters, projected to orthonormal
     two-frames by Gram-Schmidt.
   - 8 restarts, 250 BFGS iterations each.

## Results

### Matrix-unit sweep

```text
cases checked: 57600
equality cases: 528
best violation: 0.0
best |z|^2: 0.25
best D_1,D_2: 0.5, 0.5
example X: E_00, E_01
example Y: E_00, E_01
```

No sparse matrix-unit PAL violation was found. The best cases are exact equality
within floating-point arithmetic.

### Random frame search

```text
trials: 8000
best violation: -1.549087158428483
negative D_i count: 0
```

The random search did not approach a positive violation. This is only numerical
evidence; it is not a proof.

### Continuous optimization

```text
SciPy available: true
best optimized violation: -6.211697822777751e-14
best |z|^2: 0.25671573363309635
best D_1,D_2: 0.5066712245799205, 0.5066712321111203
```

The optimizer reached PAL equality to roundoff but did not find a robust positive
violation. The best value is negative at approximately `6e-14`, consistent with
an equality boundary.

A coarse conversion scan over phases and singular-value ratios for the best
optimized PAL near-equality frame gave no original-gap counterexample:

```text
max original gap on grid: -1.206496300001389
```

This conversion scan is not certification; it is recorded only to rule out an
obvious original-gap violation from the best near-equality PAL point.

## Interpretation

No PAL refutation was found in LOOP-0004. The result is useful because it adds
structured evidence beyond LOOP-0003:

- exhaustive sparse matrix-unit two-frame search found no violation;
- BFGS optimization drove the PAL defect to equality but not positive values;
- known equality mechanisms remain regression tests for sharpness.

However, this lane does not prove PAL. Nonconvex optimization and finite sparse
searches cannot certify a universal inequality over all complex two-frames.

## Caveats

- The continuous search is local and floating-point.
- The matrix-unit sweep only tests very sparse support patterns.
- The conversion from PAL near-equality to original `gap(C)` was a coarse grid,
  not an exact optimization or proof.
- The absence of violations should be used as evidence to focus the next proof
  attempt, not as a theorem.

## Next recommendation

The next proof attempt should exploit the equality cases seen in both sparse and
optimized searches. In particular, try to express

```text
D_1D_2 - |a+conjugate(b)|^2
```

as a two-frame determinant defect with constraint multipliers. Avoid proving any
m-frame or full complex-coefficient kernel PSD statement, since LOOP-0002 and the
LOOP-0004 proof lane identify those as false overextensions.
