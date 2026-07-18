# LOOP-0006 PAL-PCL bridge lane

status: bridge_relation_identified; no_new_claim_proof
claim_focus: CLAIM-0001-rank-two-partial-trace

## Executive verdict

PAL is exactly the `2 x 2` principal compression of the PCL matrix on the
SVD-diagonal coefficient slice, provided the PCL partial-trace convention is
matched correctly.  More precisely, for SVD support bases

```text
p_i = x_i = vec(X_i),       q_i = y_i = vec(Y_i),       i=1,2,
E_{i alpha}=|p_i><q_alpha|,
```

the principal subspace

```text
D_SVD = span{ E_11, E_22 } subset Hom(QH,PH)
```

has compression matrix `M=-K` equal to the PAL determinant matrix

```text
M|_{D_SVD} = K^PAL
          = [[D_1, -z],[-conjugate(z), D_2]],

z = <X_1Y_1^*,X_2Y_2^*>_F
    + conjugate(<X_1^*Y_1,X_2^*Y_2>_F)
    - (1/2)t_1 conjugate(t_2),
t_i = tr(X_i^*Y_i).
```

Thus PCL implies PAL immediately by taking this principal submatrix.
Conversely, a universal PAL theorem would imply PCL, but not because one fixed
PAL block controls a fixed `4 x 4` PCL matrix.  It implies PCL indirectly: every
coefficient matrix `Z in M_2(C)` in a fixed support block has its own `2 x 2`
SVD, which rotates the support bases and turns that particular vector into a
PAL diagonal slice.  Therefore PAL is a principal/minimized block of PCL for a
chosen SVD basis, while the universal quantification of PAL over all two-frames
is strong enough to cover all PCL directions after re-diagonalizing each
coefficient matrix.

The practical proof-status implication is:

```text
PCL  => PAL       by principal submatrix.
PAL  => CLAIM     by the rank-two SVD route.
CLAIM => PCL      by support compression equivalence.
```

Therefore the universal statements PAL, CLAIM-0001, and PCL are equivalent once
PAL is formulated for all Hilbert-Schmidt orthonormal two-frames.  However, PAL
alone for one fixed support basis is only a `2 x 2` principal subproblem and does
not supply a `4 x 4` PSD/principal-minor certificate for that fixed PCL block.

## 1. Conventions imported from LOOP-0003/0005

Let

```text
H = C^4 tensor C^4,
C in M(H),
q(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2 - 2||C||_F^2.
```

PCL fixes rank-two support planes `P,Q` with orthonormal bases
`p_1,p_2` and `q_1,q_2`.  In the basis

```text
E_{i alpha}=|p_i><q_alpha|,       i,alpha in {1,2},
```

the compression matrix for `q` is

```text
K_{i alpha,j beta}
 = <tr_1 E_{i alpha}, tr_1 E_{j beta}>_F
 + <tr_2 E_{i alpha}, tr_2 E_{j beta}>_F
 - (1/2)conjugate(tr E_{i alpha}) tr E_{j beta}
 - 2 delta_ij delta_alpha,beta.
```

PCL asks for

```text
K <= 0,
M := -K = 2I_4 - A - B + (1/2)T >= 0.
```

PAL starts from an ordinary rank-two SVD

```text
C = s_1 |x_1><y_1| + s_2 |x_2><y_2|,       s_i >= 0,
```

where `x_i=vec(X_i)`, `y_i=vec(Y_i)`, and the matrix reshapes satisfy

```text
<X_i,X_j>_F = delta_ij,       <Y_i,Y_j>_F = delta_ij.
```

Define

```text
L_i = X_iY_i^*,
R_i = X_i^*Y_i,
t_i = tr(X_i^*Y_i),
D_i = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2.
```

The phase-aware PAL off-diagonal is

```text
z = <L_1,L_2>_F + conjugate(<R_1,R_2>_F) - (1/2)t_1 conjugate(t_2),
```

and PAL is

```text
D_1D_2 - |z|^2 >= 0,
```

equivalently `K^PAL=[[D_1,-z],[-conjugate(z),D_2]] >= 0`.

## 2. SVD pairs as PCL support planes

Given SVD data `x_i=vec(X_i)`, `y_i=vec(Y_i)`, set

```text
P = projection onto span{x_1,x_2},
Q = projection onto span{y_1,y_2}.
```

Then the four PCL basis vectors are

```text
E_11=|x_1><y_1|,       E_12=|x_1><y_2|,
E_21=|x_2><y_1|,       E_22=|x_2><y_2|.
```

The original SVD coefficient vector lives only in the diagonal subspace

```text
C = s_1 E_11 + s_2 E_22,       s_i >= 0.
```

The full PCL block instead allows

```text
C_Z = sum_{i,alpha} z_{i alpha}E_{i alpha},       Z=(z_{i alpha}) in M_2(C).
```

This is the key geometric difference:

```text
PAL in a fixed SVD basis: one diagonal two-dimensional slice.
PCL in a fixed support basis: the full four-complex-dimensional Hom(QH,PH).
```

## 3. Exact restriction of the PCL matrix to the SVD diagonal slice

For `E_{i i}=|vec(X_i)><vec(Y_i)|`, the partial traces are, up to the naming of
tensor factors used in the prior reports,

```text
tr_2 E_{i i} = X_iY_i^* = L_i,
tr_1 E_{i i} = X_i^T conjugate(Y_i) = conjugate(R_i),
tr E_{i i}   = <y_i,x_i> = conjugate(t_i).
```

Consequently, for the off-diagonal entry between `E_11` and `E_22`,

```text
K_{11,22}
 = <L_1,L_2>_F
   + <conjugate(R_1),conjugate(R_2)>_F
   - (1/2)conjugate(conjugate(t_1)) conjugate(t_2)
 = <L_1,L_2>_F
   + conjugate(<R_1,R_2>_F)
   - (1/2)t_1 conjugate(t_2)
 = z.
```

For the diagonal entries,

```text
K_{ii,ii}
 = ||L_i||_F^2 + ||R_i||_F^2 - (1/2)|t_i|^2 - 2
 = -D_i.
```

Hence the `E_11,E_22` principal submatrix of `M=-K` is exactly

```text
M[{11,22},{11,22}]
 = [[D_1, -z],[-conjugate(z),D_2]]
 = K^PAL.
```

This also resolves the LOOP-0002 warning about the false fixed-gauge Hermitian
cone.  If one incorrectly uses `<R_1,R_2>` instead of
`conjugate(<R_1,R_2>)`, the off-diagonal becomes the refuted fixed-gauge
quantity `H_12=a+b`.  The actual PCL principal submatrix uses the phase-aware
quantity `z=a+conjugate(b)` because `tr_1 |vec(X)><vec(Y)|` is `conjugate(X^*Y)`,
not `X^*Y`, under the vectorization convention.

I checked the LOOP-0002 sparse equality data by a short Python calculation:

```text
X_1=Y_1=E_00,
X_2=E_01,
Y_2=iE_01.
```

The calculation returned

```text
a=-i, b=-i/2, H=a+b=-3i/2, z=a+conjugate(b)=-i/2,
D_1=D_2=1/2,
PAL det = 0,
fixed-gauge det = -2,
PCL diagonal M principal = [[0.5, 0.5i],[-0.5i, 0.5]], eig=[0,1].
```

So the PCL principal submatrix agrees with PAL and is positive semidefinite; it
is not the false `|H_12|` matrix.

## 4. Does PAL prove only a principal subproblem or all of PCL?

Both statements are true at different quantifier levels.

For fixed support bases `p_i=x_i`, `q_alpha=y_alpha`, PAL checks only the
principal slice

```text
Z = diag(s_1,s_2),       s_i >= 0,
```

and, after phase maximization, the real two-dimensional cone generated by
`E_11,E_22`.  It does not by itself check vectors involving `E_12` or `E_21`, nor
linear combinations such as

```text
z_11 E_11 + z_12 E_12 + z_21 E_21 + z_22 E_22.
```

Thus PAL is not a direct `4 x 4` PSD certificate for a fixed PCL matrix.
The missing fixed-basis PCL requirements include the `E_12,E_21` diagonal
entries, mixed `2 x 2` minors, `3 x 3` minors, and the full determinant of
`M(U,V)`.

However, every `Z in M_2(C)` has a two-by-two SVD

```text
Z = A diag(s_1,s_2) B^*,       A,B in U(2),       s_i >= 0.
```

Therefore

```text
C_Z = U Z V^*
    = sum_r s_r |u'_r><v'_r|,
```

where `u'_r` and `v'_r` are orthonormal bases obtained by rotating the original
support bases inside `P` and `Q`.  Since PAL is stated for arbitrary
orthonormal two-frames, it applies to these rotated SVD bases.  Hence a universal
PAL theorem would give `q(C_Z)<=0` for every `Z`, and therefore would prove the
full PCL compression for the fixed support planes.

This is an important distinction:

```text
single PAL block in one basis         = principal subproblem only;
universal PAL over all two-frames     = enough to cover all PCL directions by
                                        re-SVD of each coefficient matrix.
```

## 5. Implication diagram and proof-status consequences

The clean implication diagram is

```text
PCL
  => PAL
     because K^PAL is a principal submatrix of M=-K on span{E_11,E_22}.

PAL
  => CLAIM-0001
     because every rank <=2 C has an ordinary SVD with nonnegative singular
     values, and PAL is exactly the needed phase-aware determinant inequality.

CLAIM-0001
  => PCL
     because every C in Hom(QH,PH) has ordinary matrix rank <=2.
```

Thus, modulo the already recorded PCL-CLAIM equivalence, the universal PAL and
PCL targets are logically equivalent.  The difference is not logical strength but
certificate shape:

```text
PAL certificate shape:  prove a universal 2 x 2 determinant after SVD/phase
                        optimization.

PCL certificate shape:  prove a basis-free 4 x 4 Hermitian compression PSD on
                        Gr(2,16) x Gr(2,16).
```

A PAL proof would be enough for the original claim and would imply PCL indirectly.
But it would not automatically hand over a closed-form `4 x 4` principal-minor or
SOS certificate for `M(U,V)` in a fixed support basis.  Conversely, a PCL proof
would immediately prove PAL and would likely be the more robust certificate,
because it controls all coefficient directions in one support block at once.

## 6. Answer to the LOOP-0006 bridge questions

1. Does PAL imply PCL?

Yes, as a universal theorem.  Given fixed `P,Q` and arbitrary `C in Hom(QH,PH)`,
SVD the `2 x 2` coefficient matrix of `C`; PAL applies to the rotated SVD bases
inside `P,Q` and gives `q(C)<=0`.  Therefore `K(P,Q)<=0`.

2. Does PCL imply PAL?

Yes, directly.  For SVD support bases, `K^PAL` is the `{E_11,E_22}` principal
submatrix of `M=-K`.  PSD of `M` gives PSD of that principal submatrix, i.e. PAL.

3. Is PAL a principal minor, Schur complement, or weaker condition?

PAL is exactly the `2 x 2` principal submatrix condition for the SVD-diagonal
basis directions.  No Schur complement is needed.  In one fixed support basis it
is weaker than full PCL because full PCL asks for the entire `4 x 4` matrix to be
PSD.  Universally over all frame rotations, PAL is equivalent to PCL via the SVD
of the coefficient matrix.

4. Is proving PAL enough because SVD diagonalizes every `C`?

Yes for CLAIM-0001 and hence for PCL as a universal statement.  But this should
not be misread as saying that the off-diagonal PCL directions are unnecessary in
a fixed compression matrix.  They are necessary for a fixed-basis PSD certificate;
they are handled by PAL only after changing to the SVD basis of the particular
coefficient matrix being tested.

5. Can PCL be block-diagonalized into PAL-like determinants under one gauge?

No such single-gauge block diagonalization is identified here, and the relation
above suggests why it should not be expected generically.  A generic `4 x 4`
Hermitian compression contains all coefficient directions simultaneously, while
PAL diagonalizes one chosen coefficient matrix at a time by a basis change that
depends on that matrix.  Thus PAL gives a moving family of `2 x 2` diagonal
slices, not a fixed decomposition of `M(U,V)` into PAL blocks.

## Final status

This lane closes the conceptual bridge but not the inequality.  PAL and PCL are
not competing conjectures of different logical strength; they are equivalent
universal formulations with different proof burdens.  PAL is the exact
SVD-diagonal principal `2 x 2` subproblem of PCL.  Full PCL includes additional
off-diagonal support directions in a fixed basis, but those directions are
covered by universal PAL only after re-SVD/rotating the support bases for each
coefficient matrix.  No PCL-to-PAL block reduction beyond this principal-slice
identification was found, and no new proof or counterexample to CLAIM-0001 was
obtained.
