# LOOP-0002 Skeptic Report

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace

## Verdict

The LOOP-0002 counterexample is a valid refutation of Lemma M as stated:

```text
H <= 2 I_2
```

is false for arbitrary complex Hermitian quadratic testing in the fixed `Y_i` gauge.

However, this counterexample does not refute CLAIM-0001.  It exposes that the LOOP-0001 reduction strengthened the actual SVD requirement incorrectly: the original rank-two inequality only needs the quadratic form on nonnegative real singular-value coefficients after choosing singular-vector phases.  Lemma M tested the full complex sesquilinear extension, including phase directions that are gauge artifacts.

Therefore CLAIM-0001 remains open/proof-gap-found, not disproved and not proved.

## 1. Exact verification of the Lemma M counterexample

Take matrix units in `M_4(C)`:

```text
X_1 = Y_1 = E_00,
X_2 = E_01,
Y_2 = i E_01.
```

The Hilbert-Schmidt frame constraints hold exactly:

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.
```

Direct calculation gives

```text
L_1 = E_00,        R_1 = E_00,        t_1 = 1,
L_2 = -i E_00,     R_2 =  i E_11,     t_2 = i.
```

With

```text
H_ij = <L_i,L_j>_F + <R_i,R_j>_F - (1/2) overline(t_i)t_j,
```

one obtains

```text
H = [[3/2, -3i/2],
     [3i/2,  3/2]],

eig(H) = {0, 3}.
```

Thus `lambda_max(H)=3>2`, so `K=2I-H` has eigenvalues `{2,-1}` and is not PSD.  The determinant formulation also fails:

```text
D_1 = D_2 = 1/2,
|H_12|^2 = 9/4,
|H_12|^2 - D_1 D_2 = 2.
```

This is not a numerical-roundoff issue; it is an exact matrix-unit example.  I independently reproduced the calculation in Python and got the same `H`, eigenvalues, `D`, and determinant violation.

## 2. Why this does not refute CLAIM-0001

The violating eigenvector is complex, e.g.

```text
c = (-1, -i)/sqrt(2)
```

for the fixed gauge above.  Testing `c^* H c` is exactly the overstrong part of Lemma M.  In the actual SVD reduction for a rank-two operator, the coefficients are singular values `s_i >= 0`; relative phases are absorbed into the right singular vectors.  The required inequality is therefore a real-coefficient/gauge-normalized one, not `H <= 2I` in every fixed phase gauge.

The distinction is visible in the counterexample itself:

- In the original gauge `Y_2=iE_01`, the imaginary off-diagonal `H_12=-3i/2` creates a bad complex Rayleigh quotient, but it is invisible to real singular-value vectors: for real `s`, the off-diagonal contribution has zero real part and `s^*Hs=(3/2)(s_1^2+s_2^2) <= 2||s||^2`.
- Absorbing the phase of the complex coefficient into `Y_2` gives an equivalent SVD gauge with real nonnegative coefficients and, for example, `Y_2'=-E_01`.  Then

```text
H' = [[3/2, -1/2],
      [-1/2, 3/2]],

eig(H') = {1,2},
```

so the same rank-two operator is an equality case, not a positive-gap counterexample.

The reconstructed operator has numerical metrics

```text
rank = 2,
singular values = [1/sqrt(2), 1/sqrt(2)],
||tr_1 C||_F^2 + ||tr_2 C||_F^2 = 3,
||C||_F^2 = 1,
|tr C|^2 = 2,
gap = 3 - 2*1 - (1/2)*2 = 0.
```

Thus the counterexample kills Lemma M as a sufficient operator-matrix lemma, but it does not kill the original partial-trace inequality.

## 3. Critique of the LOOP-0001 reduction step

The problematic phrase is the promotion from the real singular-value quadratic form to the full operator inequality:

```text
Since phases of the singular vectors can absorb arbitrary coefficient phases,
... target H <= 2I.
```

This is not valid as an equivalence.  Absorbing phases changes the `Y_i` and hence changes `L_i`, `R_i`, `t_i`, and `H`.  The matrix `H` is gauge-dependent.  A complex phase direction in one fixed `H` is not a legitimate independent SVD coefficient direction for that same fixed gauge.

At most, the reduction supports one of these weaker/gauge-aware targets:

```text
(1) for every gauge, s^* H s <= 2 s^*s for all real s_i >= 0;
(2) after optimizing/normalizing phases, the required real quadratic form is bounded;
(3) a direct inequality for C=sum_i s_i |x_i><y_i| with s_i>=0.
```

The full Hermitian matrix inequality `H<=2I` is stronger and false.

## 4. Critique of SOS/Gram proposer output

The SOS/Gram report correctly refuses to claim a proof, so there is no promotion-worthy proof to accept.  Skeptical issues:

1. Its projection/Gram reformulation treats `K=2I-H` as the target for arbitrary complex coefficient vectors.  The counterexample shows this target is false.  Any identity implying PSD of that `K` cannot exist under only the stated constraints.
2. The report's indefinite-operator observation is useful but not a proof route.  Positivity of `2I-4P_S` on all two-dyad complex spans is exactly the false overstrong statement unless the coefficient/gauge restriction is encoded.
3. The proposed missing Gram identity cannot be the right artifact in its stated sesquilinear form, because it would imply the refuted `H<=2I`.
4. A viable SOS target must encode real singular coefficients or phase minimization explicitly; a complex Gram kernel for the fixed-gauge `K` is now ruled out.

Fail-closed conclusion for this lane: useful localization only; no proof; stated Gram target refuted.

## 5. Critique of determinant-bound proposer output

The determinant-bound report also correctly refuses to claim a proof.  Skeptical issues:

1. The determinant inequality

```text
|H_12|^2 <= D_1D_2
```

is equivalent to the false full complex `H<=2I` target, not to the real singular-value requirement.  The matrix-unit example violates it exactly by `2`.

2. The direct Cauchy-Schwarz/separate-defect strategy is not merely incomplete; any strategy proving the determinant target as stated would prove a false theorem.

3. The examples in that report showing `I-G^L` and `I-G^R` are separately indefinite are valid obstructions to a naive proof, but the stronger obstruction is now decisive: even the combined fixed-gauge determinant target fails.

4. Future determinant work should replace `|H_12|` by the relevant phase/gauge-aware real off-diagonal control.  For real coefficients the necessary two-dimensional condition is not the Hermitian determinant condition; it is the bound for the real quadratic form, depending on the real part of the off-diagonal in the chosen SVD gauge.

Fail-closed conclusion for this lane: no determinant proof; determinant target as stated refuted.

## 6. Current status of CLAIM-0001

- Lemma M as stated: false.
- LOOP-0001 proof route via Lemma M: broken at the phase/gauge strengthening step.
- LOOP-0002 SOS/Gram and determinant proposer outputs: no accepted proof; their fixed-gauge complex PSD targets are refuted.
- CLAIM-0001 itself: not refuted by this counterexample; still open/proof-gap-found.

Recommended next target: formulate the exact gauge-invariant real-coefficient two-pair lemma needed by the SVD reduction and test/prove that statement instead of `H<=2I`.
