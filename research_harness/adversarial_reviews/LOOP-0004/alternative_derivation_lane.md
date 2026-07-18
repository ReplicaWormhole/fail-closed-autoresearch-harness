# LOOP-0004 alternative derivation lane

status: cleaner_equivalent_reduction_found; no_complete_proof
claim_focus: CLAIM-0001-rank-two-partial-trace

## Executive verdict

I did not find a complete proof of CLAIM-0001 and did not find a counterexample.
The useful outcome of this lane is a PAL-free equivalent reduction: replace the
phase-aware two-term SVD scalar lemma by a projected compression lemma over the
row and column supports of `C`.

This projected lemma has no nonnegative-coefficient cone and no SVD phase
bookkeeping. It says that a fixed Hermitian quadratic-form operator is
negative semidefinite on every `Hom(F,E)` block, where `E` and `F` are arbitrary
two-dimensional subspaces of `C^4 tensor C^4`. Proving this projected lemma is
exactly equivalent to CLAIM-0001 for rank at most two.

I regard this as a cleaner target than PAL for a future proof/search lane, but it
is still an open lemma here.

## 1. Quadratic-form operator formulation

Let `H = C^4 tensor C^4`, with the standard Hilbert-Schmidt inner product on
`M(H)`. Define the quadratic form

```text
q(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
       - (1/2)|tr C|^2 - 2||C||_F^2.
```

Thus `q(C)=gap(C)`. Let `Phi` be the self-adjoint linear operator on `M(H)`
representing this form:

```text
q(C) = <C, Phi(C)>_F,
Phi = tr_1^* tr_1 + tr_2^* tr_2 - (1/2) tr^* tr - 2 I.
```

With unnormalized traces, the adjoints are the standard inclusions

```text
tr_1^*(A) = I_4 tensor A,
tr_2^*(B) = B tensor I_4,
tr^*(z)   = z I_16,
```

up to the convention of which tensor factor is named first.

## 2. Projected compression lemma (PCL)

For two rank-two orthogonal projections `P,Q` on `H`, let

```text
M(P,Q) = { C in M(H) : C = P C Q } = Hom(QH, PH).
```

Equivalently, after choosing orthonormal bases `u_1,u_2` of `PH` and
`v_1,v_2` of `QH`, every element has the form

```text
C = sum_{i=1}^2 sum_{alpha=1}^2 z_{i alpha} |u_i><v_alpha|,
Z = (z_{i alpha}) in M_2(C).
```

The projected compression lemma is:

```text
(PCL)  For all rank-two projections P,Q on H,
       <C, Phi(C)>_F <= 0 for every C with C = P C Q.
```

Equivalently, in any orthonormal bases of `PH` and `QH`, the `4 x 4` Hermitian
matrix

```text
K_{(i,alpha),(j,beta)}
 = q_bilinear(|u_i><v_alpha|, |u_j><v_beta|)
```

is negative semidefinite. Here `q_bilinear` is the sesquilinear polarization of
`q`:

```text
q_bilinear(A,B)
 = <tr_1 A, tr_1 B>_F + <tr_2 A, tr_2 B>_F
   - (1/2) conjugate(tr A) tr B - 2 <A,B>_F.
```

This is often the cleanest computational form:

```text
lambda_max K(P,Q) <= 0      for all two-planes P,Q in H.
```

## 3. Equivalence with CLAIM-0001

PCL implies CLAIM-0001:

If `rank(C) <= 2`, let `P` be the orthogonal projection onto the range of `C`
and `Q` be the orthogonal projection onto the range of `C^*`. Then

```text
rank(P) <= 2, rank(Q) <= 2, and C = P C Q.
```

If one of the ranks is less than two, enlarge the corresponding support
projection arbitrarily to rank two. Applying PCL gives `gap(C)=q(C)<=0`.

CLAIM-0001 implies PCL:

Every `C` satisfying `C=PCQ` with `rank(P)=rank(Q)=2` has ordinary matrix rank at
most two. Hence CLAIM-0001 applied to all such `C` gives `q(C)<=0` on the whole
four-complex-dimensional space `M(P,Q)`.

Thus PCL is not a strengthened conjecture and not a weakened conjecture; it is an
exact Grassmannian/compression restatement of CLAIM-0001.

## 4. Why this bypasses PAL

The SVD/PAL route chooses a singular-vector representation

```text
C = s_1 |x_1><y_1| + s_2 |x_2><y_2|,   s_i >= 0,
```

and then has to track the nonnegative real coefficient cone and the phases that
can be absorbed into the right singular vectors. This is what leads to the PAL
quantity

```text
|a + conjugate(b)|^2 <= D_1 D_2.
```

The projected formulation instead fixes only the left and right two-dimensional
supports. It tests the full coefficient matrix `Z in M_2(C)`, not just a diagonal
SVD coefficient vector. Therefore all phase choices are already built into the
linear space `Hom(QH,PH)`. No hidden Hermitian, normal, positive, or convexity
assumption is introduced: the rank condition is handled only by the exact support
identity `C=PCQ`.

This makes the new target more invariant:

```text
PAL target:       scalar inequality for two SVD pairs plus phase maximization.
PCL target:       negative semidefiniteness of a canonical 4 x 4 compression.
```

## 5. Relation to the LOOP-0002 fixed-gauge failure

The LOOP-0002 counterexample showed that a fixed-gauge two-pair matrix inequality
was too strong. In the projected picture this pathology is less misleading,
because one tests the entire `Hom(QH,PH)` compression rather than an over-specific
surrogate extracted from a diagonal two-term ansatz.

For the LOOP-0002 sparse frames

```text
X_1=Y_1=E_00,
X_2=E_01,
Y_2=i E_01,
```

I computed the full projected compression on the four basis operators
`|x_i><y_alpha|`. Its eigenvalues are

```text
[-1, -1, -1, 0]
```

up to floating point roundoff. Thus the same data that refuted the overstrong
fixed-gauge surrogate is harmless, and in fact gives a sharp zero direction in
the correct support-compression problem.

## 6. Numerical smoke check for PCL

I ran a small direct compression test with random two-planes `P,Q`. For each
trial, I formed the `4 x 4` Hermitian matrix `K(P,Q)` by explicit partial traces
and recorded its largest eigenvalue.

Representative output:

```text
random PCL smoke seed=4004 trials=200
max_lambda = -1.1018633133307132
min        = -1.4871428101587065
mean       = -1.3231873323340586

LOOP-0002 full compression eigs = [-1. -1. -1.  0.]
```

This is only a smoke check, not evidence strong enough for promotion. It does
support that PCL is consistent with the previous direct gap searches and known
equality data.

## 7. Attempted proof directions and current gap

### 7.1 Operator-norm version

PCL can be written as an operator-norm bound for the linear map

```text
Gamma_{P,Q}: M(P,Q) -> M_4(C) oplus M_4(C) oplus C,
Gamma(C) = (tr_1 C, tr_2 C, tr C),
```

with the codomain quadratic form

```text
||(A,B,t)||_*^2 = ||A||_F^2 + ||B||_F^2 - (1/2)|t|^2.
```

The desired statement is

```text
||Gamma_{P,Q}(C)||_*^2 <= 2 ||C||_F^2
for every C in M(P,Q).
```

Equivalently, the largest eigenvalue of `Gamma_{P,Q}^* J Gamma_{P,Q}` is at most
`2`, where `J` is the signature operator implementing the `- (1/2)|t|^2` term.
The obstacle is that `J` is indefinite, so a direct contraction argument for the
two partial traces alone is too weak and does not capture the trace correction.

### 7.2 Exterior-algebra idea

Since `rank(C)<=2` is exactly the vanishing of all `3 x 3` minors, one might hope
to rewrite `-q(C)` as a sum of squares plus terms proportional to these minors.
The projected lemma suggests doing this after choosing support bases, where the
rank constraint is automatic and the problem is only the `4 x 4` compression.
I did not find the needed sum-of-squares decomposition. The likely formal target
would be an identity of the form

```text
-K(P,Q) = S(P,Q)^* S(P,Q) + R(P,Q),   R(P,Q) >= 0,
```

with `S,R` expressed in terms of Plucker coordinates of the two planes `P,Q`.
This remains speculative.

### 7.3 Equality mechanisms

The projected compression perspective accommodates both known equality
mechanisms:

1. product-type equality, where one tensor factor is rank one and the other is a
   scalar rank-two projection;
2. traceless two-product-atom equality with opposite coefficients.

In PCL language, these are simply zero eigenvectors of `K(P,Q)` for special pairs
of two-planes. A proof by strict negativity is therefore impossible; one must
allow nontrivial kernel in the compression.

## 8. Recommended next lemma

A cleaner LOOP-0004/LOOP-0005 proof target is:

```text
Projected Compression Lemma.
Let P,Q be arbitrary rank-two orthogonal projections on C^4 tensor C^4. Let Phi
be the self-adjoint operator

  Phi = tr_1^* tr_1 + tr_2^* tr_2 - (1/2) tr^* tr - 2 I.

Then the compression of Phi to Hom(QH,PH), i.e. to matrices C satisfying C=PCQ,
is negative semidefinite.
```

This target is exact, phase-free, and directly certifiable by a `4 x 4` Hermitian
matrix depending only on two points of the Grassmannian `Gr(2,16)`. It bypasses
PAL as a formulation, but I did not close the proof.

## 9. Final status

No proof of CLAIM-0001 was obtained. No counterexample was found. The deliverable
is the equivalent projected-compression reduction PCL, together with its exact
connection to CLAIM-0001 and a small numerical sanity check. The remaining gap is
proving `K(P,Q) <= 0` for all two-dimensional subspaces `P,Q` of
`C^4 tensor C^4`.
