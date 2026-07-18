# LOOP-0002 Lemma M Counterexample Hunter

status: completed_with_counterexample_to_Lemma_M_as_stated

## Goal

Search for violations of the LOOP-0001 sufficient Lemma M:

```text
X_1,X_2,Y_1,Y_2 in M_4(C),
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij,
L_i = X_iY_i^*,
R_i = X_i^*Y_i,
t_i = tr(X_i^*Y_i),
H_ij = <L_i,L_j>_F + <R_i,R_j>_F - (1/2) overline(t_i)t_j.
```

The proposed sufficient lemma was

```text
H <= 2 I_2.
```

Equivalently, with `D_i=2-H_ii`, one expects

```text
|H_12|^2 <= D_1D_2.
```

## Commands/logs

A numerical/exact-search script was produced by the counterexample lane before timeout:

```text
research_harness/logs/loop_0002_lemma_m_search.py
```

Log files found:

```text
research_harness/logs/loop_0002_lemma_m_search_seed2002.json
research_harness/logs/loop_0002_lemma_m_search_seed2002.stdout.log
research_harness/logs/loop_0002_smoke.json
research_harness/logs/loop_0002_smoke.stdout.log
```

I independently re-ran the exact calculation in the parent session to verify the key numbers.

## Exact counterexample to Lemma M as stated

Take matrix units in `M_4(C)` and set

```text
X_1 = Y_1 = E_00,
X_2 = E_01,
Y_2 = i E_01.
```

Then both pairs are Hilbert-Schmidt orthonormal:

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.
```

The verified values are

```text
t = [1, i]
H = [[3/2, -3i/2],
     [3i/2,  3/2]]
eig(H) = [0, 3]
```

Thus

```text
lambda_max(H) = 3 > 2,
K = 2I-H has lambda_min = -1,
D = [1/2, 1/2],
|H_12|^2 = 9/4,
|H_12|^2 - D_1D_2 = 2.
```

So Lemma M, in the operator-matrix form `H <= 2I_2`, is false.

Parent-session verification output:

```text
X orth err 0.0
Y orth err 0.0
t [1.+0.j 0.+1.j]
H=
[[1.5+0.j  0. -1.5j]
 [0. +1.5j 1.5+0.j ]]
eig(H) [0. 3.]
D [0.5 0.5] |H12|^2 2.25 det violation 2.0
top w [-0.70710678+0.j          0.        -0.70710678j]
claim gap after phase absorption -2.220446049250313e-16
rank 2 sv [0.70710678 0.70710678 0.         0.        ]
```

## Does this refute CLAIM-0001?

No. The same exact example does not produce a positive-gap rank-two `C` for the original partial-trace inequality.

Using the top eigenvector of `H` gives a complex coefficient vector. But in an SVD representation of a rank-two operator, the singular coefficients must be nonnegative real after phases are absorbed into the right singular vectors. Performing that phase absorption changes the `Y_i` phases and hence changes the off-diagonal entries of the matrix `H` used above.

The reconstructed rank-two `C` has

```text
rank = 2,
singular values = [1/sqrt(2), 1/sqrt(2)],
claim gap alpha=1/2 = -2.22e-16.
```

This is equality to roundoff, not a violation.

## Interpretation

LOOP-0002 found that the LOOP-0001 Lemma M was overstrong because it demanded positivity for arbitrary complex coefficient vectors in the fixed `Y_i` gauge.

The original SVD problem has a phase gauge:

```text
s_i |x_i><y_i| = s_i |x_i><e^{i theta_i} y_i| e^{?}
```

More concretely, singular values are nonnegative real, and relative phases can be moved into the singular vectors. Since `H` depends on the chosen phases of `Y_i`, the condition `H <= 2I` is not gauge-invariant and is stronger than needed.

The correct replacement target should not be `H <= 2I` for all complex coefficient vectors in a fixed gauge. It should be one of:

1. A real-coefficient/gauge-optimized inequality for nonnegative singular coefficients `s_i >= 0`.
2. A phase-minimized or phase-normalized version of the off-diagonal term.
3. A direct inequality for the original expression

```text
Q(s_1,s_2; X_i,Y_i) <= 0
```

with `s_i >= 0` and allowed independent phase choices of the singular vectors.

## Fail-closed verdict

- Lemma M as stated is refuted.
- CLAIM-0001 is not refuted by this example.
- The proof bottleneck must be reformulated to respect SVD phase gauge and nonnegative singular coefficients.
