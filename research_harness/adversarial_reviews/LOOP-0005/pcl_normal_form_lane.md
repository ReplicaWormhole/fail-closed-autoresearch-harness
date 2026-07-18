# LOOP-0005 PCL Normal-Form Lane

status: completed_reduction_only
claim_focus: CLAIM-0001-rank-two-partial-trace
pcl_status: exact_reformulation_open
last_updated: 2026-06-03

## Target

Let `H = C^4_A tensor C^4_B`.  LOOP-0004 introduced the Projected Compression
Lemma (PCL): for every pair of rank-two support projections `P,Q` on `H`, the
quadratic form

```text
q(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2 - 2||C||_F^2
```

is nonpositive on

```text
Hom(QH,PH) = { C : C = P C Q }.
```

Equivalently, if `p_1,p_2` and `q_1,q_2` are orthonormal bases of `ran P` and
`ran Q`, then the `4 x 4` compression matrix of `Phi` in the basis

```text
E_{alpha beta} = |p_alpha><q_beta|,      alpha,beta in {1,2},
```

must be negative semidefinite.

## Local-unitary covariance

For local unitaries `U=U_A tensor U_B` on the range side and
`V=V_A tensor V_B` on the co-range side, define

```text
C' = U C V^*.
```

The Frobenius norm and trace term are invariant in the expected two-sided way,
and the partial-trace norms obey covariance:

```text
tr_1(U C V^*) = U_B tr_1(C) V_B^*      if U_A = V_A,
tr_2(U C V^*) = U_A tr_2(C) V_A^*      if U_B = V_B.
```

For independent left/right local unitaries, the individual partial traces do not
simply conjugate unless the traced-side left/right unitaries match. Therefore PCL
is covariant under simultaneous local conjugation of the ambient bipartite space,

```text
P -> W P W^*,       Q -> W Q W^*,       W=W_A tensor W_B,
```

but not under arbitrary independent local changes of `P` and `Q` on the two
sides. This limits how much of both planes can be canonically fixed at once.

## Compression matrix entries

Write tensor components as

```text
p_alpha[i,a],       q_beta[j,b],       i,j,a,b in {0,1,2,3}.
```

For

```text
E_{alpha beta} = |p_alpha><q_beta|,
```

the partial traces are

```text
tr_1(E_{alpha beta})[a,b] = sum_i p_alpha[i,a] conjugate(q_beta[i,b]),
tr_2(E_{alpha beta})[i,j] = sum_a p_alpha[i,a] conjugate(q_beta[j,a]),
tr(E_{alpha beta}) = <q_beta,p_alpha>.
```

Thus, using multi-indices `(alpha,beta)` and `(gamma,delta)`, the PCL compression
matrix is

```text
K_{alpha beta, gamma delta}
 = <tr_1 E_{alpha beta}, tr_1 E_{gamma delta}>
 + <tr_2 E_{alpha beta}, tr_2 E_{gamma delta}>
 - (1/2) conjugate(tr E_{alpha beta}) tr E_{gamma delta}
 - 2 delta_{alpha gamma} delta_{beta delta}.
```

Equivalently, define the two families of `2 x 2` matrices indexed by subsystem
coordinates

```text
A_{ab}[alpha,beta] = sum_i p_alpha[i,a] conjugate(q_beta[i,b]),
B_{ij}[alpha,beta] = sum_a p_alpha[i,a] conjugate(q_beta[j,a]),
T[alpha,beta]      = <q_beta,p_alpha>.
```

Then the compression matrix is the Gram combination

```text
K = Gram({A_{ab}}) + Gram({B_{ij}}) - (1/2) vec(T) vec(T)^* - 2 I_4.
```

PCL is `K <= 0` for all orthonormal two-frames `p` and `q`.

## Normal-form observations

A single rank-two plane `P` in `C^4 tensor C^4` is a two-dimensional subspace of
matrices `M_4(C)` under vectorization. Local unitaries act by left/right unitary
multiplication on this two-dimensional matrix subspace. One can put one vector in
Schmidt form,

```text
p_1 = sum_r s_r |r>|r>,      s_r >= 0,
```

and then use stabilizers of `p_1` plus `U(2)` rotation inside the plane to simplify
`p_2`. However, a generic two-plane has continuous Plucker invariants; there is
no simple simultaneous Schmidt form for both `p_1,p_2` analogous to a single
bipartite vector.

For a pair `(P,Q)`, simultaneous local conjugation can simplify one plane, but it
cannot independently Schmidt-normalize both `P` and `Q`. Therefore a full proof
probably needs either:

1. Plucker-coordinate identities for both two-planes;
2. a principal-angle description of `P,Q` together with subsystem reductions; or
3. a direct Gram/SOS certificate for the compression matrix above.

## Equality regression cases in PCL language

Known equality cases correspond to `K` having top eigenvalue zero:

- product-projection equality: spectrum `[-1,-1,-1,0]`;
- traceless diagonal two-atom equality: spectrum `[-2,-2,-1,0]`;
- LOOP-0002 phase-absorbed equality support: spectrum `[-1,-1,-1,0]`.

These kernels mean any attempted proof must allow zero modes and cannot prove a
uniformly negative bound.

## Status

This lane did not prove PCL. It produced an explicit coordinate target and
clarified the normal-form obstruction: the local-unitary action is not large
enough to reduce an arbitrary pair of two-planes to only a few Schmidt parameters.

## Next sublemma

A concrete next sublemma is:

```text
For all orthonormal two-frames p_alpha,q_beta in C^4 tensor C^4, the 4x4 matrix
K = Gram({A_ab}) + Gram({B_ij}) - (1/2)vec(T)vec(T)^* - 2I_4 is negative
semidefinite.
```

The most promising route is a Plucker/SOS certificate for the four principal
minors of `-K`, with equality factors corresponding to the known product and
traceless diagonal equality families.
