# LOOP-0004 PAL proof lane

status: no_complete_proof; reduced_to_exact_2x2_phase_aware_kernel_PSD
claim_focus: CLAIM-0001 via the phase-aware scalar PAL lemma

## Executive summary

I attacked the phase-aware scalar PAL inequality by rewriting it as a precise 2 x 2 determinant-defect problem. The strongest clean result of this lane is an exact reformulation:

```text
PAL is equivalent to positivity of the 2 x 2 Hermitian matrix

K^PAL = [[D_1, -z], [-conjugate(z), D_2]],
z = a + conjugate(b)
  = <L_1,L_2>_F + conjugate(<R_1,R_2>_F) - (1/2)t_1 conjugate(t_2).
```

Equivalently,

```text
K^PAL_ij
 = 2 delta_ij
   - <L_i,L_j>_F
   - conjugate(<R_i,R_j>_F)
   + (1/2)t_i conjugate(t_j),          i,j in {1,2}.
```

Here `K^PAL_ii=D_i`, and `K^PAL_12=-z`. Thus

```text
D_1D_2 - |a+conjugate(b)|^2 = det K^PAL.
```

I did not find a manifest real Gram/SOS identity for this determinant. The smallest exact remaining sublemma is therefore:

```text
For Hilbert-Schmidt orthonormal two-frames X_1,X_2 and Y_1,Y_2 in M_4(C),
K^PAL >= 0.
```

A key obstruction is that this cannot be proved by upgrading `K^PAL` to a positive kernel for arbitrary longer frames: the analogous 3 x 3 phase-aware kernel is already indefinite on matrix units. Thus any successful Gram/SOS proof must be genuinely two-frame/two-dimensional, or must use determinant-level cancellations that disappear for three or more terms.

## Conventions

Throughout this report the Frobenius inner product is conjugate-linear in the first argument:

```text
<A,B>_F = tr(A^* B).
```

For Hilbert-Schmidt orthonormal two-frames

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij,
```

define

```text
L_i = X_i Y_i^*,
R_i = X_i^* Y_i,
t_i = tr(X_i^*Y_i),

a = <L_1,L_2>_F,
b = <R_1,R_2>_F - (1/2)conjugate(t_1)t_2,

D_i = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2.
```

The PAL target is

```text
|a+conjugate(b)|^2 <= D_1D_2.                         (PAL)
```

## 1. Phase law derived with conjugations tracked

Right singular-vector phase absorption sends

```text
Y_i -> eta_i Y_i,          |eta_i|=1.
```

Then

```text
L_i -> conjugate(eta_i)L_i,
R_i -> eta_i R_i,
t_i -> eta_i t_i.
```

For the usual off-diagonal entry

```text
H_12 = <L_1,L_2>_F + <R_1,R_2>_F - (1/2)conjugate(t_1)t_2
     = a + b,
```

the transformed entry is, with `delta=arg(eta_1)-arg(eta_2)`,

```text
H'_12 = e^{i delta} a + e^{-i delta} b.
```

Only `Re(H'_12)` enters the SVD proof with nonnegative real singular values. Hence

```text
max_delta Re(H'_12)
 = max_delta Re(e^{i delta}a + e^{-i delta}b)
 = max_delta Re(e^{i delta}(a+conjugate(b)))
 = |a+conjugate(b)|.
```

This is the source of PAL. It is not the false fixed-gauge target `|a+b|^2 <= D_1D_2` refuted in LOOP-0002.

## 2. Exact determinant-defect formulation

Set

```text
z = a+conjugate(b)
  = <L_1,L_2>_F
    + conjugate(<R_1,R_2>_F)
    - (1/2)t_1 conjugate(t_2).
```

Define the phase-aware defect matrix

```text
K^PAL_ij
 = 2 delta_ij
   - <L_i,L_j>_F
   - conjugate(<R_i,R_j>_F)
   + (1/2)t_i conjugate(t_j),       i,j in {1,2}.
```

Then, because `<L_i,L_i>=||L_i||^2`, `conjugate(<R_i,R_i>)=||R_i||^2`, and `t_i conjugate(t_i)=|t_i|^2`,

```text
K^PAL_ii = D_i.
```

For the off-diagonal,

```text
K^PAL_12
 = -<L_1,L_2>_F - conjugate(<R_1,R_2>_F) + (1/2)t_1 conjugate(t_2)
 = -z.
```

Also `K^PAL_21=conjugate(K^PAL_12)`, so `K^PAL` is Hermitian. Therefore

```text
K^PAL >= 0
iff D_1 >= 0, D_2 >= 0, det K^PAL >= 0
iff D_1D_2 - |z|^2 >= 0,
```

and the last line is exactly PAL.

This is the clean determinant-defect form that a proof should target.

## 3. Diagonal terms and the one-pair defect

For a unit Frobenius pair `X,Y`,

```text
||XY^*||_F^2 = tr((X^*X)(Y^*Y)) <= tr(X^*X) tr(Y^*Y) = 1,
||X^*Y||_F^2 = tr((XX^*)(YY^*)) <= tr(XX^*) tr(YY^*) = 1.
```

Thus

```text
D(X,Y)
 = (1-||XY^*||_F^2)
   + (1-||X^*Y||_F^2)
   + (1/2)|tr(X^*Y)|^2 >= 0.
```

This proves the diagonal positivity needed by the determinant formulation. The real difficulty is the off-diagonal determinant.

## 4. Real Gram/SOS attempt

The PAL cross term has a useful Gram-like rewrite:

```text
conjugate(<R_i,R_j>_F) = <conjugate(R_i), conjugate(R_j)>_F,

t_i conjugate(t_j) = <conjugate(t_i), conjugate(t_j)>_C.
```

So formally

```text
K^PAL_ij
 = 2 delta_ij
   - <L_i,L_j>_F
   - <conjugate(R_i),conjugate(R_j)>_F
   + (1/2)<conjugate(t_i),conjugate(t_j)>_C.
```

This identifies PAL as a Cauchy-Schwarz/determinant statement for an indefinite Hermitian form of signature schematically

```text
2 ||u||^2 - ||L||^2 - ||conjugate(R)||^2 + (1/2)||conjugate(t)||^2
```

restricted to two rank-one SVD dyads with both left and right vectors orthonormal.

A direct positive Gram proof would need explicit vectors `W_i`, depending on `(X_i,Y_i)` and using the two-frame constraints, such that

```text
<W_i,W_j> = K^PAL_ij,       i,j in {1,2}.
```

I did not find such `W_i`. The standard separate contraction defects do not suffice: they would require positivity of kernels like `I-G^L` and `I-G^R`, but those kernels are indefinite even for matrix units. The trace channel is essential and must be built into any SOS identity from the beginning.

## 5. Important obstruction: no longer-frame positive kernel

One tempting route is to prove that the formula for `K^PAL_ij` defines a positive kernel for arbitrary orthonormal `m`-frames, then take `m=2`. This route is false.

Exact 3-frame matrix-unit obstruction:

```text
X_1=Y_1=E_{0,3},
X_2=Y_2=E_{1,3},
X_3=Y_3=E_{3,3}.
```

These are Hilbert-Schmidt orthonormal frames. For the 3 x 3 phase-aware kernel above, direct exact arithmetic gives

```text
K^PAL = [[ 1/2, -1/2, -1/2],
         [-1/2,  1/2, -1/2],
         [-1/2, -1/2,  1/2]],
```

with eigenvalues

```text
-1/2, 1, 1.
```

Every 2 x 2 principal submatrix of this example is positive semidefinite and sharp, but the 3 x 3 kernel is indefinite. Therefore the missing proof cannot be a naive all-frame PSD kernel proof. It must exploit the fact that only two SVD terms are present.

## 6. Matrix-unit two-frame check

I exhaustively checked all matrix-unit two-frame data

```text
X_i = E_{a_i b_i},
Y_i = E_{c_i d_i},
(a_1,b_1) != (a_2,b_2),
(c_1,d_1) != (c_2,d_2)
```

in dimension 4, with phases set to 1. Phases only rotate the two basic cross contributions and do not change the support/equality pattern in this sparse test. The run found no PAL violations. Slack counts were:

```text
slack D_1D_2-|z|^2:
0.0 :   528 cases
0.5 :  2688 cases
1.0 : 11904 cases
2.0 : 24192 cases
4.0 : 18288 cases
```

The maximum ratio `|z|^2/(D_1D_2)` was exactly `1.0`, attained by the equality cases.

Representative equality cases:

```text
Product-projection adjacent case:
X_1=Y_1=E_{0,0},   X_2=Y_2=E_{0,1}
D_1=D_2=1/2,       z=1/2.

One-sided shifted case:
X_1=E_{0,0}, Y_1=E_{1,0},
X_2=E_{0,1}, Y_2=E_{1,1}
D_1=D_2=1,         z=1.

Traceless diagonal-type case:
X_1=Y_1=E_{0,0},   X_2=Y_2=E_{1,1}
D_1=D_2=1/2,       z=-1/2.
```

This supports PAL on the sparse equality skeleton but is not a proof.

## 7. Checks against LOOP-0003 equality mechanisms

### 7.1 Product rank-two projection family

A standard SVD skeleton for the product equality family is

```text
X_1=Y_1=E_{0,0},
X_2=Y_2=E_{0,1}.
```

Then

```text
L_1=L_2=E_{0,0},
R_1=E_{0,0},
R_2=E_{1,1},
t_1=t_2=1,

a=1,
<R_1,R_2>=0,
b=-1/2,
z=a+conjugate(b)=1/2,
D_1=D_2=1/2.
```

Thus

```text
|z|^2 = 1/4 = D_1D_2.
```

PAL is sharp on this family.

### 7.2 Traceless two-product-atom family

Use the skeleton

```text
X_1=Y_1=E_{0,0},
X_2=-E_{1,1},
Y_2= E_{1,1}.
```

The sign puts the opposite coefficient into the second left singular vector. Then

```text
L_1=R_1=E_{0,0},
L_2=R_2=-E_{1,1},
t_1=1,
t_2=-1,

a=0,
<R_1,R_2>=0,
b=1/2,
z=1/2,
D_1=D_2=1/2.
```

Again

```text
|z|^2 = 1/4 = D_1D_2.
```

PAL is sharp on the traceless diagonal equality mechanism as well.

### 7.3 LOOP-0002 false-H<=2I witness

The fixed-gauge counterexample to the stronger matrix inequality was

```text
X_1=Y_1=E_{0,0},
X_2=E_{0,1},
Y_2=iE_{0,1}.
```

Then

```text
a=-i,
b=-i/2,
z=a+conjugate(b)=-i/2,
D_1=D_2=1/2.
```

Hence

```text
|z|^2 = 1/4 = D_1D_2.
```

So the old counterexample is exactly a PAL equality case, not a PAL violation.

## 8. Numerical/tool output used in this lane

I used Python/Numpy for exact sparse enumeration and kernel obstruction checks. Relevant terminal outputs:

```text
slack counts Counter({2.0: 24192, 4.0: 18288, 1.0: 11904, 0.5: 2688, 0.0: 528})
maxratio 1.0 eq count 528
```

For the longer-frame obstruction:

```text
found xs [(0, 3), (1, 3), (3, 3)] ys [(0, 3), (1, 3), (3, 3)]
eigs [-0.5  1.   1. ]
K [[ 0.5 -0.5 -0.5]
   [-0.5  0.5 -0.5]
   [-0.5 -0.5  0.5]]
```

The repository shell lacks some standard commands in this environment (`git`, and tool-internal `head` surfaced as unavailable), so I used Python-based file and enumeration operations where needed.

## 9. Current failure point / smallest exact sublemma

The smallest isolated missing statement is the following determinant sublemma.

### PAL determinant sublemma

Let `X_1,X_2,Y_1,Y_2 in M_4(C)` satisfy

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.
```

Set

```text
K^PAL_ij
 = 2 delta_ij
   - <X_iY_i^*,X_jY_j^*>_F
   - conjugate(<X_i^*Y_i,X_j^*Y_j>_F)
   + (1/2)tr(X_i^*Y_i) conjugate(tr(X_j^*Y_j)).
```

Then prove

```text
K^PAL >= 0      for i,j in {1,2}.
```

Equivalently, prove the scalar determinant identity/inequality

```text
[2-||X_1Y_1^*||^2-||X_1^*Y_1||^2+(1/2)|t_1|^2]
[2-||X_2Y_2^*||^2-||X_2^*Y_2||^2+(1/2)|t_2|^2]
-
| <X_1Y_1^*,X_2Y_2^*>_F
  + conjugate(<X_1^*Y_1,X_2^*Y_2>_F)
  - (1/2)t_1 conjugate(t_2) |^2
>= 0.
```

This is exactly PAL. I did not find a smaller non-tautological sublemma that is both true and sufficient.

## 10. Recommended next steps

1. Search for a determinant-level SOS that is explicitly two-frame, not an all-frame kernel PSD identity.
2. Use the 3-frame matrix-unit obstruction above as a regression test: any proposed Gram kernel extending to `m>=3` is probably too strong unless it contains two-frame-only constraint multipliers.
3. Try a normal form using simultaneous local-unitary covariance: transform `X_i,Y_i` by `X_i -> U X_i V^*`, `Y_i -> U Y_i V^*` to simplify one pair, then attack the determinant as a polynomial in the remaining pair plus orthogonality constraints.
4. Run an exact symbolic SOS/SDP search on the real and imaginary variables after fixing a sparse normal form. The equality skeletons in Sections 6 and 7 should be enforced as sharpness tests.
5. Keep the LOOP-0002 fixed-gauge refutation separate: do not attempt to prove `H<=2I`; the correct cross term is `a+conjugate(b)`, not `a+b`.
