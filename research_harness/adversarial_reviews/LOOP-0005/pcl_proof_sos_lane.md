# LOOP-0005 PCL proof/SOS lane

status: no_complete_proof; exact_compression_formulas_and_sos_subproblem_isolated
claim_focus: CLAIM-0001 via projected compression lemma (PCL)

## Executive summary

I attacked the Projected Compression Lemma directly.  I did not find a complete
proof and did not find a counterexample.  The useful outcome is a clean algebraic
normal form for the 4 x 4 compression and a sharper description of what an
SOS/Plucker proof would have to certify.

Let `H=C^4 tensor C^4`.  For rank-two orthonormal frames

```text
U = [u_1,u_2] in H^2,       V = [v_1,v_2] in H^2,
P = UU^*,                  Q = VV^*,
```

write each vector as a `4 x 4` matrix, still denoted `U_i,V_alpha`, by
`u_{ab}=U[a,b]`.  On the basis operators

```text
E_{i alpha}=|u_i><v_alpha|,       i,alpha in {1,2},
```

the PCL compression matrix is

```text
K_{i alpha,j beta}
 = <tr_1 E_{i alpha}, tr_1 E_{j beta}>_F
   + <tr_2 E_{i alpha}, tr_2 E_{j beta}>_F
   - (1/2) conjugate(tr E_{i alpha}) tr E_{j beta}
   - 2 delta_ij delta_alpha,beta.
```

PCL is exactly

```text
K(U,V) <= 0       for every pair of two-planes U,V in Gr(2,16).
```

Equivalently, with

```text
A_{i alpha,j beta}=<tr_1 E_{i alpha},tr_1 E_{j beta}>_F,
B_{i alpha,j beta}=<tr_2 E_{i alpha},tr_2 E_{j beta}>_F,
T_{i alpha,j beta}=conjugate(tr E_{i alpha}) tr E_{j beta},
```

the exact remaining inequality is

```text
G(U,V) := A(U,V)+B(U,V)-(1/2)T(U,V) <= 2 I_4.        (PCL-G)
```

This is the most compact algebraic subproblem I found.  It avoids the false
`m>=3` PSD-kernel route and the false fixed-gauge `H<=2I` route: it is a genuine
four-dimensional support-compression statement depending on two independent
2-planes in `H`, not on a longer frame kernel or a frozen SVD gauge.

## 1. Explicit coordinate formulas

For a vector `u in H`, write `u=vec(U)` with `U in M_4(C)`.  For a rank-one
operator `|u><v|`, the two partial traces are

```text
tr_1 |vec(U)><vec(V)| = U^T conjugate(V),
tr_2 |vec(U)><vec(V)| = U V^*.
```

The scalar trace is

```text
tr |vec(U)><vec(V)| = <v,u> = tr(V^* U).
```

Thus, for `E_{i alpha}=|u_i><v_alpha|`,

```text
A_{i alpha,j beta}
 = <U_i^T conjugate(V_alpha), U_j^T conjugate(V_beta)>_F,

B_{i alpha,j beta}
 = <U_i V_alpha^*, U_j V_beta^*>_F,

T_{i alpha,j beta}
 = conjugate(tr(V_alpha^* U_i)) tr(V_beta^* U_j),

K = A + B - (1/2)T - 2I_4.
```

Equivalently, for a coefficient matrix `Z=(z_{i alpha}) in M_2(C)`,

```text
C = sum_{i,alpha} z_{i alpha} |u_i><v_alpha|,

q(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
       - (1/2)|tr C|^2 - 2||C||_F^2
     = vec(Z)^* K vec(Z).
```

So proving PCL is exactly proving

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2 <= 2||C||_F^2
```

for every `C` in the 4-complex-dimensional block `Hom(QH,PH)`.

## 2. Principal-minor/determinant target

Since `K` is `4 x 4` Hermitian, PCL is equivalent to nonnegativity of all
principal minors of

```text
M(U,V) := -K(U,V) = 2I_4 - A - B + (1/2)T.
```

The determinant/principal-minor target is therefore:

```text
all principal minors of M(U,V) are >= 0,
```

under only the two Grassmann constraints

```text
U^*U = I_2,       V^*V = I_2.
```

A Plucker version would choose coordinates

```text
p_{rs}=u_{1,r}u_{2,s}-u_{1,s}u_{2,r},
q_{rs}=v_{1,r}v_{2,s}-v_{1,s}v_{2,r},        1 <= r < s <= 16,
```

with the usual quadratic Plucker relations and normalization.  The concrete SOS
problem is then to express each principal minor, especially `det M`, as

```text
SOS in entries of U,V,conjugates
+ terms in the ideal <U^*U-I, V^*V-I, Plucker relations>.
```

I did not find such an identity.  The determinant is the natural two-plane
replacement for the LOOP-0004 PAL determinant: PAL checks the diagonal SVD slice
and phase-maximized `2 x 2` determinant, whereas PCL asks for the full `4 x 4`
support determinant and all its principal minors.

## 3. Diagonal SOS identities that do work

For a single unit pair `x=vec(X)`, `y=vec(Y)`, the one-dimensional compression
has

```text
-q(|x><y|)
 = 2 - ||X^T conjugate(Y)||_F^2 - ||XY^*||_F^2
   + (1/2)|tr(Y^*X)|^2.
```

The two contraction defects have elementary Lagrange/SOS decompositions.  If
`r_a(X)` denotes row `a` of `X` and `c_b(X)` denotes column `b`, then

```text
1 - ||XY^*||_F^2
 = sum_{a,c} ( ||r_a(X)||^2 ||r_c(Y)||^2 - |<r_c(Y),r_a(X)>|^2 )
 = sum_{a,c} || r_a(X) wedge r_c(Y) ||^2,

1 - ||X^T conjugate(Y)||_F^2
 = sum_{b,d} ( ||c_b(X)||^2 ||c_d(Y)||^2 - |<conjugate(c_d(Y)),c_b(X)>|^2 )
```

up to the same convention-dependent conjugation on the second line.  Hence the
diagonal entries satisfy

```text
-K_{i alpha,i alpha}
 = (row-wedge SOS) + (column-wedge SOS)
   + (1/2)|tr(V_alpha^*U_i)|^2 >= 0.
```

This recovers the known diagonal positivity.  The obstruction is polarizing these
SOS terms over the four basis elements `|u_i><v_alpha|`: the polarized row/column
wedge kernels alone do not dominate the off-diagonal terms.  The positive trace
term `+(1/2)T` in `M=-K` has to be included globally; adding it only after
separate contraction estimates loses the determinant-level cancellations.

## 4. Failed/blocked proof routes

### 4.1 Longer-frame PSD kernel

The tempting route

```text
K^PAL_ij = 2 delta_ij - <L_i,L_j> - conjugate(<R_i,R_j>)
           + (1/2)t_i conjugate(t_j)
```

cannot be promoted to an arbitrary `m`-frame positive kernel.  LOOP-0004 already
exhibited a `3 x 3` matrix-unit obstruction with eigenvalues `[-1/2,1,1]` for
the phase-aware kernel.  Therefore a PCL proof cannot be an all-frame PSD kernel
proof in disguise.  It must use the fact that both supports are exactly two
planes and that the tested block is exactly `Hom(QH,PH)`.

### 4.2 Fixed-gauge `H<=2I`

The LOOP-0002 fixed-SVD-gauge inequality is false.  In PCL language the same
sparse data is harmless because the correct object is the full support
compression, not one over-specific two-term slice.  The full compression for the
LOOP-0002 gauge pathology has eigenvalues `[-1,-1,-1,0]` (up to roundoff), so it
is a sharp equality case rather than a counterexample.

### 4.3 Separate contraction bounds

The inequalities

```text
||tr_1 C||_F^2 <= ? ||C||_F^2,
||tr_2 C||_F^2 <= ? ||C||_F^2
```

are too crude on `Hom(QH,PH)`.  PCL is not just two independent contraction
bounds; it is the signed bound for

```text
A+B-(1/2)T.
```

The negative trace correction is essential.  Any SOS proof should start from
`M=2I-A-B+(1/2)T`, not from separate SOS certificates for `2I-A-B`.

## 5. Numerical checks run in this lane

I wrote a small probe script at

```text
research_harness/experiments/LOOP-0005_pcl_probe.py
```

It constructs `K(P,Q)` from the explicit partial-trace formulas above and checks
selected equality families plus random two-plane pairs.  Representative actual
output from this lane:

```text
product K eig= [-1. -1. -1.  0.]
[[-0.5+0.j  0. +0.j  0. +0.j  0.5+0.j]
 [ 0. +0.j -1. +0.j  0. +0.j  0. +0.j]
 [ 0. +0.j  0. +0.j -1. +0.j  0. +0.j]
 [ 0.5+0.j  0. +0.j  0. +0.j -0.5+0.j]]
traceless K eig= [-2. -2. -1.  0.]
[[-0.5+0.j  0. +0.j  0. +0.j -0.5+0.j]
 [ 0. +0.j -2. +0.j  0. +0.j  0. +0.j]
 [ 0. +0.j  0. +0.j -2. +0.j  0. +0.j]
 [-0.5+0.j  0. +0.j  0. +0.j -0.5+0.j]]
random trials=2000 max_lambda -0.9643682736550798 seed_index 92 min -1.5189535128762641 mean -1.3247808793560303
block_identity_norm 0.0
sample eig A+B-.5T [0.31484941436  0.394676629552 0.479103179027 0.582960333844]
```

The random tests are not proof, but they are consistent with PCL.  The equality
families reproduce the expected zero eigenvalue.  The identity check confirms the
implemented block formula

```text
K = A+B-(1/2)T-2I.
```

## 6. Exact algebraic subproblem for the next lane

The next proof/SOS attempt should target the following precise certificate.

Input variables:

```text
U,V in C^{16 x 2},       U^*U=I_2,       V^*V=I_2.
```

Define the `4 x 4` Hermitian matrices `A,B,T` by the coordinate formulas in
Section 1 and set

```text
M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V).
```

Required certificate:

```text
M(U,V) >= 0 for all U,V.
```

Candidate SOS building blocks:

1. Row-wedge Lagrange terms coming from the defects of `XY^*`.
2. Column-wedge Lagrange terms coming from the defects of `X^T conjugate(Y)`.
3. Trace-coupled rank-one terms from `+(1/2)T`.
4. Plucker bilinears for the two support planes, especially products
   `p_{rs} conjugate(p_{r's'}) q_{tu} conjugate(q_{t'u'})`, because every
   principal minor of `M` is invariant under independent `U(2)` changes of basis
   in the two support planes.

The most promising concrete route is not to search for an SOS of `-q(C)` for all
rank-two `C` directly.  Instead, search for an invariant Hermitian Gram
factorization of `M(U,V)` or of its principal minors in the Plucker coordinate
ring of `Gr(2,16) x Gr(2,16)`.  The smallest decisive target is

```text
det M(U,V) >= 0
```

together with the lower principal minors; equality data above should be imposed
as interpolation constraints on the Gram ansatz.

## Verdict

No accepted PCL proof was found in this lane, and no PCL violation was found.
The lane leaves CLAIM-0001 fail-closed/open.  The exact remaining proof target is
`M(U,V)=2I-A-B+(1/2)T >= 0` on `Gr(2,16) x Gr(2,16)`, preferably via a
Plucker-coordinate principal-minor/SOS certificate that uses the trace-coupled
term globally and avoids both known false routes.
