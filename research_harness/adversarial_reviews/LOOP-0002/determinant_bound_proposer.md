# LOOP-0002 Determinant-Bound Proposer Report

## Verdict

Fail-closed. I did not find a complete direct proof of the determinant/off-diagonal form of Lemma M.

I reduced the desired inequality to a very concrete `2 x 2` positivity statement involving the two one-sided contraction Gram matrices, and I tested the most natural Cauchy-Schwarz/defect-vector route. That route explains the diagonal terms exactly but does not by itself prove the off-diagonal bound: the two natural defect kernels are individually indefinite even under the stated Hilbert-Schmidt orthonormality constraints. The trace-correction term can repair the sharp examples, but I did not find a Gram representation showing it always repairs them.

Therefore this report should not be treated as a proof of Lemma M or CLAIM-0001.

## Setup

Let `X_1,X_2,Y_1,Y_2 in M_4(C)` satisfy

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.
```

Define

```text
L_i = X_i Y_i^*,
R_i = X_i^* Y_i,
t_i = tr(X_i^*Y_i),
H_ij = <L_i,L_j>_F + <R_i,R_j>_F - (1/2) overline(t_i)t_j.
```

The determinant target is

```text
|H_12|^2 <= D_1 D_2,
D_i = 2 - H_ii
    = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2.
```

Equivalently, the matrix

```text
K = 2I - H
```

must be positive semidefinite.

## Useful exact reformulation

Introduce the two Gram matrices

```text
G^L_ij = <L_i,L_j>_F,
G^R_ij = <R_i,R_j>_F,
T_ij   = overline(t_i)t_j.
```

Since the `X`-frame and `Y`-frame are both orthonormal, the diagonal/off-diagonal determinant problem is exactly

```text
K = 2I - H
  = (I - G^L) + (I - G^R) + (1/2) T.        (1)
```

Thus the desired determinant inequality is

```text
det((I - G^L) + (I - G^R) + (1/2)T) >= 0,
```

or, in scalar form,

```text
| <L_1,L_2> + <R_1,R_2> - (1/2) overline(t_1)t_2 |^2
<= (1 - ||L_1||^2 + 1 - ||R_1||^2 + (1/2)|t_1|^2)
   (1 - ||L_2||^2 + 1 - ||R_2||^2 + (1/2)|t_2|^2).
```

This reformulation is tautological but useful because the two diagonal deficiencies have standard minor/wedge interpretations.

For a single unit pair `X,Y`,

```text
1 - ||XY^*||_F^2 >= 0,
1 - ||X^*Y||_F^2 >= 0,
```

by submultiplicativity. More explicitly, these are sums of squared `2 x 2` minors of the tensor `X tensor conjugate(Y)` after tracing over the appropriate tensor factor. Hence

```text
D_i = (1 - ||L_i||^2) + (1 - ||R_i||^2) + (1/2)|t_i|^2 >= 0.
```

This recovers the known diagonal part of Lemma M.

## Failed direct Cauchy-Schwarz route

The tempting proof would be:

1. Polarize the diagonal deficiencies `1 - ||L_i||^2` and `1 - ||R_i||^2` into two positive Gram kernels.
2. Add the manifestly positive rank-one kernel `(1/2) overline(t_i)t_j`.
3. Apply Cauchy-Schwarz in the resulting Gram space to get `|K_12|^2 <= K_11 K_22`, equivalently `|H_12|^2 <= D_1D_2`.

In the notation above, this would require at least that the kernels

```text
I - G^L,
I - G^R
```

be positive semidefinite, or that their sum plus the trace kernel have an evident Gram model.

The individual positivity statement is false, even with the exact orthonormality assumptions. A sharp elementary example is

```text
X_1 = Y_1 = E_11,
X_2 = Y_2 = E_12.
```

Then the two `X_i` are Hilbert-Schmidt orthonormal and the two `Y_i` are Hilbert-Schmidt orthonormal. But

```text
L_1 = X_1Y_1^* = E_11,
L_2 = X_2Y_2^* = E_11,
```

so

```text
G^L = [[1,1],[1,1]],
I - G^L = [[0,-1],[-1,0]],
```

which has eigenvalues `1` and `-1`. Thus the most direct defect-vector Cauchy-Schwarz proof cannot be correct in this separated form.

In the same example,

```text
R_1 = E_11,
R_2 = E_22,
t_1 = t_2 = 1,
```

and therefore

```text
H = [[3/2, 1/2],[1/2, 3/2]],
K = 2I-H = [[1/2,-1/2],[-1/2,1/2]],
```

which is positive semidefinite with determinant zero. This is the product-projection equality family already noted in LOOP-0001. The example shows that the trace correction is not cosmetic: it is exactly what compensates for a negative direction of `I-G^L` here.

A second sharp family, the traceless diagonal witness, shows complementary behavior:

```text
X_1 = Y_1 = E_11,
X_2 = -E_22,
Y_2 =  E_22.
```

Then

```text
L_1=R_1=E_11,
L_2=R_2=-E_22,
t_1=1,
t_2=-1,
H_12=1/2,
D_1=D_2=1/2.
```

Again the determinant bound is sharp.

## What would still be needed

The reformulation (1) suggests the right target for a successful direct proof:

```text
(I - G^L) + (I - G^R) + (1/2)tt^* >= 0              (2)
```

for every two-frame pair. A proof of (2) would immediately prove the determinant bound. However, because `I-G^L` and `I-G^R` are not separately positive, the proof must use a cancellation/correlation between the left contraction channel, the right contraction channel, and the scalar trace channel.

The direct Cauchy-Schwarz proof I attempted did not locate such a joint Gram representation. In particular, the standard wedge/minor identities prove only the diagonal inequalities and do not polarize to a positive kernel matching `K` without additional terms.

## Status

No counterexample to Lemma M was found in this lane, but no proof was found either. The determinant bound remains open from this report.

Recommended next steps:

1. Search specifically for a joint Gram/SOS representation of (2), not separate positivity of `I-G^L` and `I-G^R`.
2. If using wedge/minor variables, include the trace channel from the start; adding it after separately polarizing the two deficiencies loses the needed cancellation.
3. Continue numerical counterexample search for Lemma M as an independent lane, because a failure of (2) is exactly a failure of the proposed operator-matrix Lemma M.
