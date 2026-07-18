# LOOP-0003 Phase-aware lemma proposer

status: reduced_to_phase-aware_scalar_lemma; no_complete_proof
claim_focus: CLAIM-0001-rank-two-partial-trace

## Executive verdict

The fixed-gauge Hermitian matrix lemma `H <= 2I` from LOOP-0001 is too strong and was correctly refuted in LOOP-0002. The exact SVD reduction only needs a real-cone quadratic inequality for nonnegative singular values. When the SVD phase freedom is tracked correctly, the off-diagonal quantity is not `|H_12|`; the relevant gauge-uniform scalar is

```text
| a + conjugate(b) |,
```

where

```text
a = <X_1Y_1^*, X_2Y_2^*>_F,
b = <X_1^*Y_1, X_2^*Y_2>_F - (1/2) conjugate(t_1)t_2,
t_i = tr(X_i^*Y_i).
```

The proposed replacement for false Lemma M is the scalar inequality

```text
|a + conjugate(b)|^2 <= D_1 D_2,              (PAL)
```

with

```text
D_i = 2 - ||X_iY_i^*||_F^2 - ||X_i^*Y_i||_F^2 + (1/2)|t_i|^2.
```

This is exactly the phase-aware two-term SVD inequality needed by the rank-two proof route, in a gauge-uniform form. I did not find a proof of (PAL). The proof gap is now the precise scalar inequality (PAL), not the false PSD matrix inequality.

## 1. Exact two-term SVD inequality needed

Let

```text
C = s_1 |x_1><y_1| + s_2 |x_2><y_2|,
s_1,s_2 >= 0,
```

be an ordinary matrix SVD of a rank-at-most-two operator on `C^4 tensor C^4`. Let `X_i,Y_i in M_4(C)` be the reshapes of `x_i,y_i`. Then

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.
```

Define

```text
L_i = X_iY_i^*,
R_i = X_i^*Y_i,
t_i = tr(X_i^*Y_i),
H_ij = <L_i,L_j>_F + <R_i,R_j>_F - (1/2) conjugate(t_i)t_j.
```

The partial traces are

```text
tr_2 C = s_1 L_1 + s_2 L_2,
tr_1 C = s_1 R_1 + s_2 R_2,
tr C   = s_1 t_1 + s_2 t_2,
||C||_F^2 = s_1^2+s_2^2.
```

Therefore CLAIM-0001 for this SVD is exactly

```text
s^* H s <= 2(s_1^2+s_2^2),        s=(s_1,s_2), s_i>=0 real.      (SVD-2)
```

Writing

```text
h_i = H_ii
D_i = 2-h_i
c = Re(H_12),
```

this is

```text
D_1 s_1^2 + D_2 s_2^2 - 2 c s_1s_2 >= 0
for all s_1,s_2 >= 0.                                           (RC)
```

Since the one-term diagonal estimates give `D_i >= 0`, condition (RC) is equivalent to the real-cone scalar condition

```text
Re(H_12) <= sqrt(D_1D_2).                         (fixed-gauge RC)
```

This is the weakest condition for one fixed SVD gauge. It is strictly weaker than the false Hermitian condition

```text
|H_12| <= sqrt(D_1D_2),
```

which is equivalent to `H <= 2I`.

## 2. Phase/gauge transformations

There are two distinct phase operations and they should not be conflated.

### 2.1 Compatible phase change of a fixed SVD term

For a fixed SVD representation of the same operator, one may replace

```text
x_i -> e^{i phi_i} x_i,
y_i -> e^{i phi_i} y_i.
```

Then

```text
|x_i><y_i| is unchanged,
L_i, R_i, t_i, H_ij are unchanged.
```

So this compatible SVD phase does not repair the false fixed-gauge PSD statement; it simply leaves `H` invariant.

### 2.2 Absorbing coefficient phases into the right singular vectors

If one starts from a complex coefficient combination

```text
sum_i c_i |x_i><y_i|,       c_i = s_i e^{i theta_i}, s_i>=0,
```

then it can be rewritten as an SVD-form expression

```text
sum_i s_i |x_i><y_i'|,
y_i' = e^{-i theta_i} y_i.
```

This operation changes the right singular vectors but preserves their orthonormality. It also changes `H`, because `L_i,R_i,t_i` change.

Let

```text
Y_i' = eta_i Y_i,       |eta_i|=1,
delta = arg(eta_1) - arg(eta_2).
```

Then

```text
L_i' = conjugate(eta_i) L_i,
R_i' = eta_i R_i,
t_i' = eta_i t_i.
```

For the off-diagonal, decompose

```text
a = <L_1,L_2>_F,
b = <R_1,R_2>_F - (1/2) conjugate(t_1)t_2.
```

Then

```text
H_12' = e^{i delta} a + e^{-i delta} b.                  (phase law)
```

The diagonal quantities `H_ii` and `D_i` are unchanged by these right-vector phases.

For nonnegative real singular values only `Re(H_12')` enters. Optimizing over the relative right-vector phase gives

```text
max_delta Re(H_12')
 = max_delta Re(e^{i delta}a + e^{-i delta}b)
 = max_delta Re(e^{i delta}(a + conjugate(b)))
 = |a + conjugate(b)|.                                  (phase max)
```

This is the basic correction to LOOP-0001: the phase-uniform worst real off-diagonal is `|a+conjugate(b)|`, not `|a+b|=|H_12|` in an arbitrary fixed gauge.

## 3. Weakest scalar/gauge-aware replacement for Lemma M

The exact fixed-gauge statement needed for a particular SVD is

```text
Re(H_12) <= sqrt(D_1D_2).                                (FG)
```

To obtain a lemma stated for arbitrary Hilbert-Schmidt orthonormal two-frames, independent of how right-vector phases are chosen, the natural gauge-uniform replacement is:

### Lemma PAL: phase-aware two-pair scalar lemma

Let `X_1,X_2,Y_1,Y_2 in M_4(C)` satisfy

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.
```

Define

```text
L_i = X_iY_i^*,
R_i = X_i^*Y_i,
t_i = tr(X_i^*Y_i),
a = <L_1,L_2>_F,
b = <R_1,R_2>_F - (1/2) conjugate(t_1)t_2,
D_i = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2.
```

Then

```text
|a + conjugate(b)|^2 <= D_1D_2.                         (PAL)
```

Equivalently, for every relative phase `delta` and every `s_1,s_2>=0`,

```text
D_1 s_1^2 + D_2 s_2^2
 - 2 s_1s_2 Re(e^{i delta}a + e^{-i delta}b) >= 0.
```

This lemma implies CLAIM-0001 by applying it to the SVD data of `C`. It is also necessary for this SVD-proof strategy in the sense that arbitrary right-vector phases are legitimate SVD data for some rank-two operator with nonnegative singular values.

## 4. Check against the LOOP-0002 counterexample

LOOP-0002 used

```text
X_1=Y_1=E_00,
X_2=E_01,
Y_2=iE_01.
```

The false fixed-gauge target has

```text
H_12 = -3i/2,
D_1=D_2=1/2,
|H_12|^2 = 9/4 > 1/4 = D_1D_2.
```

For the phase-aware split,

```text
a = <L_1,L_2> = -i,
b = <R_1,R_2> - (1/2)conjugate(t_1)t_2 = -i/2,
a + conjugate(b) = -i/2,
|a + conjugate(b)|^2 = 1/4 = D_1D_2.
```

Thus the exact counterexample to `H<=2I` becomes a sharp equality case of (PAL). This matches the reconstructed rank-two operator having `gap=0`, not a positive violation.

## 5. Proof attempt and current failure point

The diagonal terms are controlled by the standard contraction estimates:

```text
||XY^*||_F <= ||X||_F ||Y||_F = 1,
||X^*Y||_F <= ||X||_F ||Y||_F = 1,
```

so

```text
D_i = (1-||X_iY_i^*||_F^2)
    + (1-||X_i^*Y_i||_F^2)
    + (1/2)|t_i|^2 >= 0.
```

The desired Cauchy-Schwarz proof would require a real or complex Gram model whose diagonal norm squared is `D_i` and whose cross inner product is

```text
a + conjugate(b)
 = <X_1Y_1^*,X_2Y_2^*>_F
   + conjugate(<X_1^*Y_1,X_2^*Y_2>_F)
   - (1/2)t_1 conjugate(t_2).                         (cross-PAL)
```

I did not find such a Gram representation. The older attempted kernel

```text
2 delta_ij - <L_i,L_j> - <R_i,R_j> + (1/2)conjugate(t_i)t_j
```

cannot be PSD because LOOP-0002 refutes it. A correct identity must either:

1. use a real-bilinear Gram/SOS structure rather than a Hermitian one;
2. incorporate the right-vector phase law explicitly; or
3. prove (PAL) directly as a scalar determinant inequality.

The precise remaining gap is therefore:

```text
Prove | <L_1,L_2> + conjugate(<R_1,R_2> - (1/2)conjugate(t_1)t_2) |^2
      <= D_1D_2
under <X_i,X_j>=<Y_i,Y_j>=delta_ij in M_4(C).
```

No Hermitian, normal, positive, convexity, density, or arbitrary-complex coefficient PSD assumption is used in this reduction.

## 6. Numerical sanity tests run in this lane

I ran random tests of (PAL) using independently sampled orthonormal two-frames in `C^16`, reshaped as `4 x 4` matrices. No violation was found. A corrected 50,000-sample run tracked the minimum slack.

Terminal output:

```text
PAL random n=4 samples=50000 bad 0 minslack 1.635292979678297 minrec (7824, 1.2293478034709808, 1.3385669021777444, 0.10134742874325252)
```

This is evidence only, not a proof; random Haar-like frames do not stress the sparse equality cases well.

## 7. Next tests / next proof targets

1. Run exact matrix-unit searches for (PAL), especially among sparse two-frame pairs that make one or both contraction defects vanish.

2. Search for a real Gram identity for the kernel with cross term `(cross-PAL)`, not for the refuted Hermitian kernel `2I-H`.

3. Try gauge normalization such as choosing the relative phase so `a+conjugate(b)` is nonnegative real, then attempt a direct determinant/SOS expansion of

```text
D_1D_2 - |a+conjugate(b)|^2.
```

4. Check whether dimension `4` is essential. Earlier LOOP-0002 notes saw dimension-sensitive behavior for naive kernels; (PAL) should be tested in dimensions `2,3,4` separately before seeking a dimension-free proof.

## Final status

CLAIM-0001 remains open/proof-gap-found. The phase-aware SVD route has a precise replacement bottleneck: Lemma PAL above. Proving Lemma PAL would complete the rank-two SVD proof of CLAIM-0001; refuting Lemma PAL would likely produce a genuine rank-two counterexample after choosing the maximizing right-vector phase and nonnegative singular values.
