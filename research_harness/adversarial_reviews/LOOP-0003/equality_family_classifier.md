# LOOP-0003 Equality-Family Classifier

status: completed_partial_classification
claim_focus: CLAIM-0001 rank-two partial-trace inequality

## Scope and verdict

This note classifies equality families visible from the known witnesses and the LOOP-0002 SVD-phase story. It does not claim a complete classification of all rank-two equality cases.

Main conclusions:

1. The two headline witnesses are not in the same local-unitary orbit.
2. There are at least two genuinely different visible equality mechanisms:
   - product-type rank-two equality: one tensor factor is trace-maximal rank 2 and the other factor is rank 1;
   - traceless two-site diagonal equality: two orthogonal product atoms with opposite coefficients.
3. The LOOP-0002 matrix-unit/phase-absorption example lands in the product-type family, not in a new violation family.
4. Any phase-aware replacement for the refuted Lemma M must be sharp on both mechanisms. In particular, it cannot strengthen the coefficient of `|tr C|^2` below `1/2`, cannot demand a strictly negative defect away from one orbit, and cannot use a fixed-gauge `H <= 2I` statement for arbitrary complex coefficients.

## Notation

For `C in M_4 tensor M_4`, define

```text
gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2 ||C||_F^2 - (1/2)|tr C|^2.
```

The target inequality is `gap(C) <= 0` for `rank(C) <= 2`.

Local-unitary orbit means conjugation by a product unitary on the underlying bipartite space:

```text
C -> (U_A tensor U_B) C (U_A tensor U_B)^*.
```

Such transformations preserve rank, spectrum, trace, Frobenius norm, and the two partial-trace Frobenius norms up to swapping only if a separate tensor-factor swap is also allowed.

## Family 1: product equality with one rank-two trace-maximal factor

Let

```text
C = A tensor B.
```

Then

```text
tr_1(C) = tr(A) B,
tr_2(C) = tr(B) A,
||C||_F^2 = ||A||_F^2 ||B||_F^2,
tr(C) = tr(A) tr(B).
```

Writing

```text
alpha = |tr A|^2 / ||A||_F^2,
beta  = |tr B|^2 / ||B||_F^2,
```

for nonzero `A,B`, the product gap is exactly

```text
gap(A tensor B)
 = ||A||_F^2 ||B||_F^2 ( alpha + beta - 2 - alpha beta/2 ).
```

A visible rank-two equality subfamily is:

```text
rank(A) = 1,
rank(B) = 2,
|tr B|^2 = 2 ||B||_F^2,
```

or the same with the two tensor factors interchanged. Under the standard trace/Frobenius equality condition, the rank-two factor is a scalar multiple of a rank-two orthogonal projection. The rank-one factor may be arbitrary nonzero: if `rank(A)=1`, then `alpha <= 1`, and with `beta=2` the factor in parentheses is identically zero.

Thus

```text
C = A tensor (lambda P_2),       rank(A)=1,
P_2=P_2^*=P_2^2,
rank(P_2)=2,
```

is equality whenever `C` has rank 2. The known witness

```text
(P_2 tensor |0><0|)/sqrt(2)
```

is the special Hermitian-positive normalized case with `A=P_2`, `B=|0><0|`.

Important consequence: the product-projection witness is only the most symmetric point of a larger product equality family. Positivity or Hermiticity of the rank-one factor is not needed for equality in the product formula.

## Family 2: traceless diagonal/two-product-atom equality

Let `P,R` be orthogonal rank-one projections on the first factor and `Q,S` be orthogonal rank-one projections on the second factor. Consider

```text
C = a P tensor Q + b R tensor S.
```

The two summands have disjoint support in both tensor factors. Hence

```text
rank(C) <= 2,
||C||_F^2 = |a|^2 + |b|^2,
||tr_1 C||_F^2 = |a|^2 + |b|^2,
||tr_2 C||_F^2 = |a|^2 + |b|^2,
tr(C) = a + b.
```

Therefore

```text
gap(C) = - (1/2) |a+b|^2.
```

Equality holds exactly when

```text
a+b=0.
```

This gives the known traceless diagonal witness

```text
C = (1/sqrt(2)) ( |00><00| - |11><11| ).
```

The local-unitary closure gives the same construction for any pair of orthogonal product atoms with distinct first and second local supports.

This equality is not product-type in general: for `a=-b != 0`, the operator has trace zero and two nonzero eigenvalues with opposite sign/phase. It cannot be locally unitarily conjugate to the positive product projection witness, whose trace is nonzero and whose two nonzero eigenvalues are equal.

## Adjacent diagonal case: shared one local index

If the two product atoms share one local factor, e.g.

```text
C = P tensor (a Q + b S)
```

with `P,Q,S` rank-one projections and `Q S=0`, then

```text
||C||_F^2 = |a|^2+|b|^2,
||tr_1 C||_F^2 = |a|^2+|b|^2,
||tr_2 C||_F^2 = |a+b|^2,
tr(C)=a+b,
```

so

```text
gap(C) = (1/2)|a+b|^2 - (|a|^2+|b|^2).
```

By the two-term Cauchy equality condition, equality occurs exactly when `a` and `b` have the same phase and equal modulus. Then `aQ+bS` is a scalar multiple of a rank-two projection, so this is precisely the product rank-two projection family above, not a third mechanism.

The two diagonal patterns are therefore:

```text
same local index shared: equality -> product projection type;
no local index shared: equality -> traceless/opposite-coefficient type.
```

## Relation to LOOP-0002 phase absorption

LOOP-0002 used

```text
X_1=Y_1=E_00,
X_2=E_01,
Y_2=i E_01,
```

and showed that the fixed-gauge matrix `H` has eigenvalues `[0,3]`, refuting the overstrong Lemma M target `H <= 2I`.

The top fixed-gauge coefficient vector is complex. When its phases are absorbed so that the rank-two operator is written in genuine SVD form with nonnegative singular coefficients, the resulting `C` is, up to an overall scalar phase, of the form

```text
|0><0| tensor ( |0><0| + |1><1| ) / sqrt(2),
```

or the corresponding tensor-factor convention. That is exactly Family 1. Hence the LOOP-0002 example explains sharpness of the phase-aware problem but does not reveal a positive-gap counterexample or a new equality mechanism.

## Local-unitary orbit separation

The two headline witnesses are genuinely different local-unitary orbits.

Traceless diagonal witness:

```text
C_A = ( |00><00| - |11><11| )/sqrt(2)
tr(C_A)=0,
spectrum nonzero part = {+1/sqrt(2), -1/sqrt(2)},
||tr_1 C_A||_F^2 = ||tr_2 C_A||_F^2 = 1.
```

Product-projection witness:

```text
C_B = (P_2 tensor |0><0|)/sqrt(2)
tr(C_B)=sqrt(2),
spectrum nonzero part = {1/sqrt(2), 1/sqrt(2)},
partial-trace norm squares = {2,1}.
```

Trace and spectrum are invariant under local-unitary conjugation, so these cannot be the same orbit. Even allowing tensor-factor swap, the partial-trace norm multiset for `C_B` is `{2,1}`, while for `C_A` it is `{1,1}`.

## Explicit calculation checks

I verified the formulas numerically by direct construction of `4 x 4` tensor factors and unnormalized partial traces. Representative output:

```text
product rank 2 gap -1.7763568394002505e-15 norm 20.000000000000004 trace ratio B 1.9999999999999996
traceless diagonal gap 0.0 trace 0j
disjoint formula gap numeric/formula -8.5 -8.5
shared product projection-like gap 1.7763568394002505e-15 expected 0.0
A gap 0.0 rank 2 ptr norms [0.9999999999999998, 0.9999999999999998] tr 0j
B gap -2.220446049250313e-16 rank 2 ptr norms [1.9999999999999996, 0.9999999999999998] tr2 1.9999999999999996
```

The small nonzero values are floating-point roundoff.

## Implications for a phase-aware lemma

Any replacement for the refuted LOOP-0001 Lemma M must satisfy the following constraints.

1. Sharpness is unavoidable.

Both Family 1 and Family 2 attain `gap=0` at rank 2. A proof cannot rely on a uniform negative margin for all rank-two nonzero `C`.

2. The coefficient `1/2` on `|tr C|^2` is forced by known stronger-variant failures.

Family 2 supplies exact equality at trace zero, while existing LOOP evidence records exact stronger-variant refutations for `alpha < 1/2`. Any phase-aware lemma must preserve the `1/2` constant and should be tested against these equality/near-equality slices.

3. Product equality forbids strengthening one partial trace independently.

For `C=A tensor lambda P_2` with `rank(A)=1`, one partial trace can carry the entire rank-two trace-maximal contribution. Any proof that tries to bound both partial traces separately by a symmetric strict estimate will fail on this family.

4. Fixed-gauge `H <= 2I` is too strong.

LOOP-0002 already refuted it. The equality-family interpretation is that the offending complex fixed-gauge direction corresponds, after phase absorption into a valid SVD representation, to a legitimate sharp product equality case. Therefore the correct target must be scalar and phase-aware: nonnegative singular coefficients, with phases absorbed before evaluating the two-pair expression, or an explicitly gauge-invariant/minimized formulation.

5. Equality is multi-mechanism.

A lemma tailored only to traceless cancellation misses product projection equality. A lemma tailored only to product support misses traceless cancellation. A complete proof likely needs a defect decomposition that can vanish in at least these two different ways.

## Not a complete classification

This report classifies only visible families generated by:

- tensor-product rank factorization;
- two diagonal product atoms with shared or disjoint local support;
- the LOOP-0002 matrix-unit phase example.

It does not rule out nonnormal, non-diagonal, or genuinely entangled singular-vector equality cases. In particular, the broader product family already includes non-Hermitian rank-one factors, so equality is not confined to positive or normal matrices.

## Next research recommendations

1. Formulate the exact phase-aware SVD scalar inequality.

Write

```text
C = s_1 |x_1><y_1| + s_2 |x_2><y_2|,
s_i >= 0,
```

reshape `x_i,y_i` into `X_i,Y_i`, and express `gap(C)` directly as a real scalar quadratic in `s_1,s_2`. Do not replace this by fixed-gauge positivity for arbitrary complex coefficient vectors.

2. Build equality tests into every proposed lemma.

Every candidate lemma should be checked on:

```text
A tensor lambda P_2, rank(A)=1;
(P tensor Q - R tensor S), with P,R,Q,S orthogonal rank-one projections;
the LOOP-0002 phase-absorbed matrix-unit example.
```

3. Search for additional equality cases numerically, but classify by invariants.

Record for optimized equality candidates:

```text
trace,
spectrum,
partial-trace norm pair,
normality defect,
operator-Schmidt rank,
whether singular vectors are product or entangled.
```

This will separate genuinely new mechanisms from local-unitary or phase-gauge copies of Families 1 and 2.

4. Attempt a diagonal-support mini-classification.

For `C` diagonal in a product basis with exactly two nonzero diagonal entries, the above shared/disjoint dichotomy appears complete. Formalizing this small lemma would provide a useful regression test for any general proof.

5. Avoid hidden positivity/normality assumptions.

Family 1 permits arbitrary rank-one `A`, so even equality can be non-Hermitian. A proof that first reduces to positive or normal `C` is suspect unless it proves the reduction exactly.
