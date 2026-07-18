# LOOP-0006 PCL symbolic Gram/SOS certificate lane

status: no_complete_certificate_found
claim_focus: CLAIM-0001 via projected compression lemma (PCL)
last_updated: 2026-06-03

## Executive summary

I tried to turn the LOOP-0005 PCL reduction into a certified Hermitian
Gram/SOS or principal-minor proof for the full `4 x 4` matrix

```text
M(U,V) = 2 I_4 - A(U,V) - B(U,V) + (1/2) T(U,V) >= 0
```

on `Gr(2,16) x Gr(2,16)`.  I did not find a complete certificate.  The useful
outcome is a sharper isolation of the first genuinely unresolved algebraic
object: the crossed `2 x 2` principal minor, i.e. the minor on two basis elements
`E_{i alpha}` and `E_{j beta}` with both `i != j` and `alpha != beta`.

The known diagonal/wedge SOS certificates remain valid, but they stop at the
`1 x 1` principal minors.  The separate contraction candidate

```text
D(U,V) := 2 I_4 - A(U,V) - B(U,V)
```

is false as a PSD matrix: in the product equality case it has eigenvalues
`[-1,1,1,1]`.  Thus any full certificate must use the trace rank-one correction
`+(1/2)T` globally.  The crossed `2 x 2` minor is exactly the first place where
this correction is forced; it vanishes in the product and traceless equality
families and is not implied by the diagonal Lagrange identities.

No counterexample to PCL was found in this lane.  Equality regressions reproduced
`M` spectra `[0,1,1,1]` and `[0,1,2,2]`, equivalent to the LOOP-0005 `K` spectra
`[-1,-1,-1,0]` and `[-2,-2,-1,0]`.

## 1. Algebraic target used

For orthonormal two-frames

```text
U = [u_1,u_2],       V = [v_1,v_2]        in C^16,
```

write `u_i=vec(U_i)`, `v_alpha=vec(V_alpha)` with `U_i,V_alpha in M_4(C)`, and
let

```text
E_{i alpha} = |u_i><v_alpha|,       i,alpha in {1,2}.
```

The partial traces are

```text
tr_1 E_{i alpha} = U_i^T conjugate(V_alpha),
tr_2 E_{i alpha} = U_i V_alpha^*,
tr   E_{i alpha} = tr(V_alpha^* U_i).
```

With multi-index `p=(i,alpha)`, the compression pieces are

```text
A_{i alpha,j beta}
 = <U_i^T conjugate(V_alpha), U_j^T conjugate(V_beta)>_F,

B_{i alpha,j beta}
 = <U_i V_alpha^*, U_j V_beta^*>_F,

T_{i alpha,j beta}
 = conjugate(tr(V_alpha^* U_i)) tr(V_beta^* U_j),

M_{i alpha,j beta}
 = 2 delta_ij delta_alpha,beta - A_{i alpha,j beta} - B_{i alpha,j beta}
   + (1/2) T_{i alpha,j beta}.
```

Equivalently, for every coefficient matrix `Z=(z_{i alpha})`, with
`C=sum z_{i alpha} E_{i alpha}`,

```text
vec(Z)^* M vec(Z)
 = 2||C||_F^2 - ||tr_1 C||_F^2 - ||tr_2 C||_F^2 + (1/2)|tr C|^2.
```

PCL is exactly `M >= 0` for all such pairs of support frames.

## 2. What still has a certificate: the diagonal minors

For a single unit pair `x=vec(X)`, `y=vec(Y)`,

```text
M_{xy,xy}
 = 2 - ||X^T conjugate(Y)||_F^2 - ||X Y^*||_F^2
   + (1/2)|tr(Y^*X)|^2.
```

The two contraction defects have Lagrange identities:

```text
1 - ||X Y^*||_F^2
 = sum_{a,c} ( ||row_a(X)||^2 ||row_c(Y)||^2
              - |<row_c(Y),row_a(X)>|^2 )
 = sum_{a,c} || row_a(X) wedge row_c(Y) ||^2,
```

and analogously for the column contraction in
`1 - ||X^T conjugate(Y)||_F^2`.  Therefore each diagonal entry has the certified
form

```text
M_{i alpha,i alpha}
 = row-wedge SOS + column-wedge SOS
   + (1/2)|tr(V_alpha^* U_i)|^2 >= 0.
```

This certifies all `1 x 1` principal minors, but it does not polarize to a full
Hermitian Gram certificate for `M`.  The off-diagonal terms mix four independent
support vectors, and the trace term must be kept as one global rank-one update.

## 3. Failed direct Gram route: `2I-A-B` is not PSD

A tempting route is to seek a Gram/SOS certificate for the contraction defect

```text
D := 2I - A - B
```

and then add the positive semidefinite rank-one term `(1/2)T`.  This is false.
In the product projection equality case

```text
P=Q=span{|0>|0>, |0>|1>},
```

the actual eigenvalues are

```text
eig(D) = [-1, 1, 1, 1],       eig((1/2)T) = [0,0,0,1],
eig(M) = [0,1,1,1].
```

Thus no certificate proving `D >= 0` can exist.  The rank-one trace correction is
not cosmetic; it exactly repairs the bad direction in this equality family.

In the traceless two-product-atom equality case

```text
P=Q=span{|0>|0>, |1>|1>},
```

the corresponding values are

```text
eig(D) = [0,0,2,2],       eig((1/2)T) = [0,0,0,1],
eig(M) = [0,1,2,2].
```

This case does not refute `D >= 0`, but it also has zero crossed minors, so it is
still a sharp regression for any proposed certificate.

## 4. Principal-minor analysis and the smallest unresolved object

For a `4 x 4` Hermitian matrix, PCL is equivalent to nonnegativity of all
principal minors of `M`.  The diagonal minors are certified as above.  The first
uncertified minors are the `2 x 2` determinants

```text
Delta_{i alpha,j beta}
 = M_{i alpha,i alpha} M_{j beta,j beta}
   - |M_{i alpha,j beta}|^2.
```

There are two types.

1. Shared-index minors: `i=j, alpha != beta` or `i != j, alpha=beta`.
   These should be easier because one support side is fixed; they resemble a
   two-vector polarization of one row/column Lagrange identity.

2. Crossed minors: `i != j` and `alpha != beta`.  These are the first genuinely
   coupled Grassmann objects.  In the natural order
   `(1,1),(1,2),(2,1),(2,2)`, the representative crossed minor is

```text
Delta_cross = det M[{(1,1),(2,2)}]
            = M_{11,11} M_{22,22} - |M_{11,22}|^2.
```

Both known equality families have

```text
Delta_cross = 0
```

for the `(1,1),(2,2)` minor, while the diagonal entries are strictly positive
there.  Therefore diagonal positivity cannot imply even this `2 x 2` minor.
This crossed minor is the smallest unresolved algebraic object I can honestly
isolate from the current symbolic lane.

A plausible next certificate would be an identity of the schematic form

```text
Delta_cross
 = SOS(row/column wedge polarizations)
   + SOS(trace-coupled bilinears)
   + Plucker-relation terms for Gr(2,16) x Gr(2,16),
```

where the Plucker terms use both support planes.  I did not find the coefficients
or a closed invariant formula.

## 5. Schur/rank-one-update reformulation

Since

```text
M = D + (1/2) t t^*,       t_{i alpha}=tr(V_alpha^* U_i),
```

another possible route is a rank-one-update certificate:

```text
D + (1/2)t t^* >= 0.
```

The product equality case shows that `D` may have a single negative direction
and that the negative direction can be exactly cancelled by `t`.  A Schur-style
proof would need at least:

```text
inertia(D) has at most one negative eigenvalue,
and the negative part is dominated by (1/2)t t^*.
```

I did not prove either statement.  This route is nevertheless more faithful than
trying to prove `D >= 0`, and it is equivalent to proving all principal minors of
`M` with the rank-one update retained.

## 6. Numerical/equality verification run in this lane

I added a small probe script:

```text
research_harness/experiments/LOOP-0006_pcl_principal_minors.py
```

It computes `A,B,T,M`, all principal minors, and random principal-minor samples.
Actual run command:

```text
python3 research_harness/experiments/LOOP-0006_pcl_principal_minors.py
```

Actual relevant output:

```text
== product ==
eig(M)= [0. 1. 1. 1.]
minor (0, 3) 0
minor (0, 1, 3) 0
minor (0, 2, 3) 0
minor (0, 1, 2, 3) 0

== traceless ==
eig(M)= [0. 1. 2. 2.]
minor (0, 3) 0
minor (0, 1, 3) 0
minor (0, 2, 3) 0
minor (0, 1, 2, 3) 0

== random_1000_summary ==
min eigenvalue (1.1194780997234, 13)
min principal minor size 1 (1.2517674839200585, 421, (1,))
min principal minor size 2 (1.758457750257567, 398, (0, 2))
min principal minor size 3 (2.5159253924879192, 421, (0, 1, 2))
min principal minor size 4 (4.0342570886025975, 363, (0, 1, 2, 3))
```

The random values are only regression evidence.  The important certified lesson
from the exact equality matrices is that zero crossed minors occur while the
matrix remains PSD, so any successful proof must be determinant/principal-minor
aware and must retain the trace coupling.

## 7. Guardrails respected

This lane did not use any of the known false or overstrong routes:

```text
- no m >= 3 all-frame PSD promotion;
- no fixed-gauge H <= 2I replacement;
- no independent local Schmidt normalization of both support planes;
- no inference from diagonal positivity to full PSD.
```

The attempted routes were confined to the exact PCL compression entries and to
principal minors of the exact `4 x 4` Hermitian matrix `M`.

## Verdict / handoff

No full Hermitian Gram/SOS or principal-minor certificate was found.  PCL remains
open/unproved and not refuted.

The smallest unresolved algebraic target for the next symbolic lane is the
crossed `2 x 2` principal minor

```text
Delta_cross
 = M_{11,11} M_{22,22} - |M_{11,22}|^2 >= 0
```

under `U^*U=I_2`, `V^*V=I_2`, together with its relabelings.  A certificate for
this minor must include trace-coupled terms and likely Plucker relations for both
two-planes.  Once crossed `2 x 2` minors are certified, the next targets are the
`3 x 3` principal minors containing a crossed equality pair, then `det M`.
