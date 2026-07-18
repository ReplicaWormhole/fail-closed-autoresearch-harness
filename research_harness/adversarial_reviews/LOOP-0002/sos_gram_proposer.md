# LOOP-0002 SOS/Gram proposer report: Lemma M

## Verdict

I do **not** claim a proof of Lemma M.  I tried to turn

```text
K_ij = 2 delta_ij - H_ij
     = 2 delta_ij
       - <X_iY_i^*, X_jY_j^*>
       - <X_i^*Y_i, X_j^*Y_j>
       + (1/2) overline(t_i) t_j
```

into a Gram/wedge/sum-of-squares kernel under the constraints

```text
<X_i,X_j> = delta_ij,     <Y_i,Y_j> = delta_ij.
```

The clean algebraic rewrites below localize what a Gram proof would have to show, but I did not find the missing PSD identity.  In particular, the most tempting universal Gram kernel is false unless additional rank/two-frame constraints are used.

## 1. Exact projection/Gram reformulation

Let `x_i=vec(X_i)`, `y_i=vec(Y_i)` and

```text
Z_i = |x_i><y_i| in End(C^4 tensor C^4).
```

For one rank-one summand, with the repository partial-trace convention,

```text
tr_2 Z_i = X_i Y_i^*,
tr_1 Z_i = X_i^* Y_i,
tr Z_i   = t_i.
```

Let `S = { A tensor I + I tensor B : tr A = tr B = 0 }`.  The bridge note gives

```text
4 ||P_S(C)||_F^2
 = ||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2.
```

Therefore for `C=sum_i c_i Z_i` with the two-frame orthogonality,

```text
sum_ij overline(c_i) K_ij c_j
 = 2 ||C||_F^2 - 4 ||P_S(C)||_F^2
 = <C, (2 I - 4 P_S) C>.
```

So Lemma M is exactly positivity of the indefinite quadratic form

```text
Q(C) = <C, (2 I - 4 P_S) C>
```

on the special rank-at-most-two SVD subspaces spanned by two mutually left/right orthonormal dyads `Z_i=|x_i><y_i|`.

This is a useful Gram target but not yet a Gram proof: the operator `2 I - 4 P_S` is not positive on all of `End(C^4 tensor C^4)`, since it is negative on `S`.  Any SOS proof must therefore use the rank/two-frame constraints, not just the linear projection identity.

## 2. Tempting kernel split and why it is insufficient

Using the constraints, for `i,j in {1,2}` we can write

```text
K_ij = A_ij + B_ij + (1/2) overline(t_i) t_j,
```

where

```text
A_ij = <X_i,X_j><Y_i,Y_j> - <X_iY_i^*, X_jY_j^*>,
B_ij = <X_i,X_j><Y_i,Y_j> - <X_i^*Y_i, X_j^*Y_j>.
```

If both `A=[A_ij]` and `B=[B_ij]` were PSD on arbitrary paired two-frames, Lemma M would follow immediately because the trace term is rank-one PSD.  This would be the cleanest Gram decomposition: `A` and `B` would be the two partial-trace contraction defects, and the trace correction would be explicit.

However, this split is not valid as a proof.  I ran a quick random check of the split in dimensions 2, 3, and 4.  The individual defect matrices can have negative eigenvalues; in dimension 2 the full `K` can also be negative.  The run returned:

```text
kernel check for unrestricted 3-point kernel:
2 -1.1391632872323116
3 0.007461676028107489
4 0.8633051747513422

split check for paired orthonormal two-frames, min eigenvalues of (A,B,K):
2 [-0.69933325 -0.59010623 -0.24035103]
3 [-0.01369508  0.11656314  0.70542931]
4 [0.40545833 0.42748329 1.07686942]
```

The dimension-2 failures do not refute Lemma M, which is specifically dimension 4, but they rule out a dimension-free proof based solely on this naive contraction-defect split.

## 3. Wedge/SOS interpretation attempted

The diagonal part has a natural “defect of contraction” interpretation:

```text
K_ii
 = [1 - ||X_iY_i^*||_F^2]
   + [1 - ||X_i^*Y_i||_F^2]
   + (1/2)|<X_i,Y_i>|^2.
```

The two bracketed terms are nonnegative because, writing

```text
A_X = X_i^* X_i,    A_Y = Y_i^* Y_i,
B_X = X_i X_i^*,    B_Y = Y_i Y_i^*,
```

one has

```text
||X_iY_i^*||_F^2 = tr(B_X B_Y) <= 1,
||X_i^*Y_i||_F^2 = tr(A_X A_Y) <= 1,
```

with all four matrices positive semidefinite of trace one.  This recovers the known diagonal bound.

For the off-diagonal, the analogous bilinear defects are exactly `A_12` and `B_12` above.  A wedge proof would need a polarization identity of the form

```text
A_ij + B_ij + (1/2) overline(t_i)t_j
 = <W_i, W_j>
```

for some explicitly constructed wedge/minor vectors `W_i` depending bilinearly on `(X_i,Y_i)`, after imposing

```text
<X_1,X_2> = 0,     <Y_1,Y_2> = 0.
```

I could not find such `W_i`.  The obstruction is that the two contraction defects by themselves do not give PSD kernels; any correct wedge formula must include additional mixed terms using the cross-orthogonality constraints.  Equivalently, it must encode a dimension-4 identity not visible in the diagonal estimates.

## 4. Relation to determinant form

The desired Gram identity is equivalent to the determinant inequality

```text
|H_12|^2 <= D_1 D_2,
D_i = 2 - ||X_iY_i^*||_F^2 - ||X_i^*Y_i||_F^2 + (1/2)|t_i|^2.
```

The projection formulation says the same thing as

```text
4 ||P_S(c_1 Z_1 + c_2 Z_2)||_F^2
 <= 2 (|c_1|^2 + |c_2|^2)
```

for all coefficient vectors `c`.  Thus a determinant proof and a Gram proof are interchangeable here.  I did not find a determinant/SOS factorization of

```text
D_1 D_2 - |H_12|^2
```

into manifest squares.

## 5. Exact missing identity/inequality

The missing artifact is one of the following equivalent statements.

### Missing Gram identity

Find an explicit Hilbert-space valued expression `W(X,Y)` and possibly constraint-multiplier terms vanishing when

```text
<X_1,X_2>=0,     <Y_1,Y_2>=0,
```

such that

```text
< W(X_i,Y_i), W(X_j,Y_j) >
 = 2 delta_ij
   - <X_iY_i^*, X_jY_j^*>
   - <X_i^*Y_i, X_j^*Y_j>
   + (1/2) overline(t_i)t_j.
```

### Missing wedge/SOS identity

Equivalently, produce a manifest sum of Hermitian squares for

```text
D_1 D_2
 - | <X_1Y_1^*,X_2Y_2^*>
     + <X_1^*Y_1,X_2^*Y_2>
     - (1/2) overline(t_1)t_2 |^2
```

modulo the four frame constraints

```text
<X_i,X_j> = delta_ij,
<Y_i,Y_j> = delta_ij.
```

### Missing constrained projection inequality

Equivalently, prove directly that the indefinite operator `2I-4P_S` is nonnegative on every subspace spanned by two dyads `|x_i><y_i|` with both `{x_i}` and `{y_i}` orthonormal:

```text
<C, (2I-4P_S) C> >= 0
```

for every `C` in such a two-dimensional SVD subspace.

## 6. Status

No complete Gram/wedge/SOS proof was found in this lane.  The target remains Lemma M, and CLAIM-0001 should remain fail-closed/proof-gap-found until the missing constrained PSD identity or determinant SOS is supplied and survives skeptical review.
