# LOOP-0001 Proposer Report: rank-factorization reduction for CLAIM-0001

## Verdict

I do not claim a complete proof of CLAIM-0001.  The rank-factorization/SVD lane gives a clean and apparently sharp reduction to a concrete two-pair contraction lemma.  The missing lemma is stated below as Lemma M.  It is a finite-dimensional inequality for four arbitrary `4 x 4` complex matrices satisfying only two Hilbert-Schmidt orthonormality constraints.  No Hermitian, normal, positivity, or convexity assumption is used.

A short random numerical check of Lemma M over 20,000 random two-frame pairs found no violation, but this is evidence only.

## 1. Target statement

Let `H = C^4 \otimes C^4`, and identify vectors `x in H` with `4 x 4` matrices `X` by

```text
x = sum_{a,b=1}^4 X_{ab} e_a \otimes f_b.
```

For `C in End(H) ~= M_4(C) tensor M_4(C)` with usual matrix rank at most two, prove

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2
  <= 2 ||C||_F^2 + (1/2) |tr C|^2.        (PT)
```

Here `tr_1` traces over the first tensor factor and `tr_2` traces over the second tensor factor, with the convention

```text
tr_1(A tensor B) = tr(A) B,
tr_2(A tensor B) = tr(B) A.
```

The Hilbert-Schmidt inner product is

```text
<A,B> = tr(A^* B),
||A||_F^2 = <A,A>.
```

## 2. Correct rank factorization

Because `rank(C) <= 2`, take an SVD of `C` as an ordinary `16 x 16` matrix:

```text
C = sum_{i=1}^r s_i |x_i><y_i|,     r <= 2,
```

where `s_i >= 0`, and `{x_i}` and `{y_i}` are orthonormal families in `C^4 tensor C^4`.  Let `X_i,Y_i in M_4(C)` denote the matrix reshapes of `x_i,y_i`.  Then

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.
```

Important: this is not an operator-Schmidt decomposition of `C` as an element of `M_4 tensor M_4`.  The ordinary rank-two hypothesis does not imply operator-Schmidt rank two.  Any proof route using

```text
C = s_1 A_1 tensor B_1 + s_2 A_2 tensor B_2
```

from ordinary matrix rank alone is invalid.

## 3. Partial traces in matrix-reshape notation

For a rank-one operator `|x><y|`, with reshapes `X,Y`, its entries are

```text
(|x><y|)_{ab,a'b'} = X_{ab} overline{Y_{a'b'}}.
```

Tracing over the first factor gives

```text
(tr_1 |x><y|)_{b,b'}
  = sum_a X_{ab} overline{Y_{ab'}}
  = (X^* Y)_{b,b'}.
```

Tracing over the second factor gives

```text
(tr_2 |x><y|)_{a,a'}
  = sum_b X_{ab} overline{Y_{a'b}}
  = (X Y^*)_{a,a'}.
```

Therefore define

```text
L_i := X_i Y_i^*,          in M_4(C),
R_i := X_i^* Y_i,          in M_4(C),
t_i := tr(X_i^* Y_i) = <x_i,y_i>.
```

Then

```text
tr_2 C = sum_i s_i L_i,
tr_1 C = sum_i s_i R_i,
tr C   = sum_i s_i t_i,
||C||_F^2 = sum_i s_i^2.
```

Thus (PT) is exactly

```text
||sum_i s_i L_i||_F^2 + ||sum_i s_i R_i||_F^2
  <= 2 sum_i s_i^2 + (1/2) |sum_i s_i t_i|^2.       (1)
```

This derivation is valid for arbitrary non-Hermitian/non-normal/non-positive `C`.

## 4. Equivalent 2 x 2 matrix inequality

Put the pair `P_i := (L_i,R_i)` in the Hilbert direct sum `M_4(C) direct-sum M_4(C)`, with

```text
<P_i,P_j> := <L_i,L_j>_F + <R_i,R_j>_F.
```

For `r <= 2`, define the Hermitian `r x r` matrix

```text
H_{ij} := <P_i,P_j> - (1/2) overline{t_i} t_j.       (2)
```

Then (1) is equivalent to

```text
s^* H s <= 2 s^* s                         (3)
```

for the singular-value vector `s = (s_1,...,s_r)`.

Since phases of the singular vectors can absorb arbitrary coefficient phases, a robust sufficient and essentially equivalent target is the operator inequality

```text
H <= 2 I_r.                                  (4)
```

For `r = 1`, this is immediate:

```text
||X Y^*||_F <= ||X||_F ||Y||_op <= ||X||_F ||Y||_F = 1,
||X^* Y||_F <= ||X||_F ||Y||_F = 1,
```

hence

```text
H_11 = ||XY^*||_F^2 + ||X^*Y||_F^2 - (1/2)|tr(X^*Y)|^2 <= 2.
```

The nontrivial issue is the rank-two off-diagonal interaction.

## 5. Precise missing lemma

The following lemma is exactly the gap left by the factorization route.

### Lemma M: two-pair contraction lemma

Let `X_1,X_2,Y_1,Y_2 in M_4(C)` satisfy

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.                       (5)
```

Define

```text
L_i = X_i Y_i^*,
R_i = X_i^* Y_i,
t_i = tr(X_i^* Y_i),
H_{ij} = <L_i,L_j>_F + <R_i,R_j>_F - (1/2) overline{t_i} t_j.
```

Then

```text
H <= 2 I_2.                                  (M)
```

Equivalently, since the diagonal inequalities follow from submultiplicativity, Lemma M is equivalent to the scalar determinant inequality

```text
| <L_1,L_2>_F + <R_1,R_2>_F - (1/2) overline{t_1} t_2 |^2
 <= D_1 D_2,                                  (M')
```

where

```text
D_i := 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2 >= 0.
```

In fully expanded form, the off-diagonal term is

```text
<L_1,L_2>_F + <R_1,R_2>_F - (1/2) overline{t_1} t_2

= tr((X_1Y_1^*)^* (X_2Y_2^*))
  + tr((X_1^*Y_1)^* (X_2^*Y_2))
  - (1/2) overline{tr(X_1^*Y_1)} tr(X_2^*Y_2)

= tr(Y_1 X_1^* X_2 Y_2^*)
  + tr(Y_1^* X_1 X_2^* Y_2)
  - (1/2) overline{tr(X_1^*Y_1)} tr(X_2^*Y_2).
```

No positivity of `X_i`, `Y_i`, or `C` is present in this lemma.

## 6. Proof of CLAIM-0001 assuming Lemma M

Assume Lemma M.  For a rank-at-most-two `C`, use the ordinary SVD above.  Let `H` be (2).  Then

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2
 = s^* H s
 <= 2 s^*s
 = 2 ||C||_F^2.
```

Rearranging gives (PT).  The argument is homogeneous and includes the cases `r=0` and `r=1` by deleting zero singular values.

Thus CLAIM-0001 is reduced to Lemma M.

## 7. Equality witness check

Take

```text
C = (1/sqrt(2)) ( |00><00| - |11><11| ).
```

Use the SVD-format representation

```text
s_1 = s_2 = 1/sqrt(2),
X_1 = Y_1 = E_00,
X_2 = -E_11,
Y_2 =  E_11.
```

Then

```text
L_1 = R_1 = E_00,       t_1 = 1,
L_2 = R_2 = -E_11,      t_2 = -1.
```

So

```text
H_11 = H_22 = 1 + 1 - 1/2 = 3/2,
H_12 = 0 + 0 - (1/2)(1)(-1) = 1/2,
H = [[3/2, 1/2], [1/2, 3/2]].
```

The singular-value vector is `s = (1/sqrt(2),1/sqrt(2))`, and

```text
s^* H s = 2,
2 s^*s = 2.
```

Hence the reduction is sharp on the known equality witness.  In determinant form,

```text
D_1 = D_2 = 1/2,
|H_12|^2 = 1/4 = D_1 D_2,
```

so Lemma M is also sharp.

## 8. Obstruction and why the naive factorization proof fails

The tempting argument in `trace_inequality/rank_two_partial_trace_proof.tex` starts from an operator-Schmidt decomposition

```text
C = s_1 A_1 tensor B_1 + s_2 A_2 tensor B_2.
```

That decomposition has at most two tensor summands only when the operator-Schmidt rank of `C` is at most two.  CLAIM-0001 assumes ordinary matrix rank at most two as an operator on `C^4 tensor C^4`; these are different notions.  A rank-one ordinary operator `|x><y|` can already have large operator-Schmidt rank, depending on the Schmidt ranks of `x` and `y`.  Therefore the scalar reduction to four traces `tr(A_i), tr(B_i)` is not valid for CLAIM-0001.

The correct ordinary-rank factorization keeps the contractions `X_iY_i^*` and `X_i^*Y_i`; their cross terms are exactly what Lemma M controls.

## 9. Numerical sanity check performed

I ran a random check of Lemma M for 20,000 independently sampled pairs of orthonormal two-frames in `C^16`.  For each sample I reshaped the vectors into `4 x 4` matrices, formed `H`, and checked `lambda_max(H) <= 2` and the equivalent determinant inequality.  The run reported:

```text
bad 0 mindelta 1.7080902474338568 maxratio 0.03054945916148508
```

This does not prove Lemma M; it only failed to find a violation.

## 10. Final fail-closed status

The factorization lane reduces CLAIM-0001 to the exact finite-dimensional Lemma M above.  A complete proof still requires proving Lemma M, preferably by finding a Gram/wedge representation of the positive kernel

```text
K_{ij} := 2 delta_ij - H_{ij}
```

under the orthonormality constraints (5), or by proving the determinant bound (M') directly.

Until Lemma M is proved, CLAIM-0001 remains open in this report.
