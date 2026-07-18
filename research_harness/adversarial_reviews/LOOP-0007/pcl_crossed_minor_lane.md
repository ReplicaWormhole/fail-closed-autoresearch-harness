# LOOP-0007 PCL crossed-minor / trace-rank-one-update lane

status: partial_reduction_no_complete_certificate
claim_focus: CLAIM-0001 via PCL
last_updated: 2026-06-03

## Executive summary

I attacked the immediate LOOP-0006 bottleneck: the crossed `2 x 2` principal
minor of the PCL matrix

```text
M(U,V) = 2I_4 - A(U,V) - B(U,V) + (1/2)T(U,V) >= 0
```

on `Gr(2,16) x Gr(2,16)`.  I did not find a complete nonnegativity proof for
this minor, hence did not prove CLAIM-0001.  The lane did produce a clean exact
reduction of the crossed minor to the phase-aware PAL determinant and an exact
rank-one-update determinant identity that isolates where the trace term must be
used.

Main fail-closed result:

```text
Delta_cross = M_{11,11}M_{22,22} - |M_{11,22}|^2
```

is exactly the PAL determinant for the two diagonal SVD atoms
`(U_1,V_1)` and `(U_2,V_2)`.  Equivalently, writing `D=2I-A-B` and
`M=D+(1/2)T`, the crossed block satisfies

```text
det M_S = det D_S + (1/2) u_S^* adj(D_S) u_S,
S={(1,1),(2,2)},     u_{i alpha}=conjugate(tr(V_alpha^* U_i)).
```

This is a useful reduction, not a proof: the first term `det D_S` can be
negative.  In the product equality regression,

```text
D_S = [[0,-1],[-1,0]],     det D_S=-1,
(1/2)u_S^*adj(D_S)u_S=1,  det M_S=0.
```

Thus the trace rank-one update is essential even at the crossed `2 x 2` level;
it cannot be treated as an optional positive after proving a contraction-defect
minor.

## 1. Conventions and notation

No Hermitian, normal, or positive assumption is made on the original rank-two
operator.  This lane works only with the exact PCL support-compression
formulation.

Let

```text
U=[u_1,u_2],       V=[v_1,v_2]       in C^16
```

be orthonormal two-frames.  Reshape `u_i=vec(U_i)` and `v_alpha=vec(V_alpha)`
with `U_i,V_alpha in M_4(C)`.  The rank-one compression basis is

```text
E_{i alpha}=|u_i><v_alpha|,     i,alpha in {1,2}.
```

The partial-trace convention used throughout is the corrected convention:

```text
tr_1(C)[a,b] = sum_i C[i,a,i,b],
tr_2(C)[i,j] = sum_a C[i,a,j,a].
```

Therefore, for `E_{i alpha}=|vec(U_i)><vec(V_alpha)|`, the three scalar/block
objects are

```text
tr_1 E_{i alpha} = U_i^T conjugate(V_alpha),
tr_2 E_{i alpha} = U_i V_alpha^*,
tr   E_{i alpha} = tr(V_alpha^* U_i).
```

With multi-indices `p=(i,alpha)`, `q=(j,beta)`, define

```text
A_{p,q} = <U_i^T conjugate(V_alpha), U_j^T conjugate(V_beta)>_F,
B_{p,q} = <U_i V_alpha^*, U_j V_beta^*>_F,
t_p     = tr(V_alpha^* U_i),
T_{p,q} = conjugate(t_p) t_q,
D       = 2I - A - B,
M       = D + (1/2)T.
```

The crossed principal block studied here is

```text
S = {(1,1),(2,2)}.
```

In zero-based script notation this is `S=(0,3)` for the ordered basis
`(1,1),(1,2),(2,1),(2,2)`.

## 2. Exact crossed-minor identity: PAL determinant slice

Let

```text
X_1=U_1,  Y_1=V_1,
X_2=U_2,  Y_2=V_2,
t_i=tr(Y_i^* X_i).
```

Since `U` and `V` are orthonormal two-frames in `C^16`, the pairs satisfy

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij.
```

The two diagonal crossed-block entries are

```text
M_{11,11}
 = 2 - ||X_1^T conjugate(Y_1)||_F^2 - ||X_1Y_1^*||_F^2
   + (1/2)|t_1|^2,

M_{22,22}
 = 2 - ||X_2^T conjugate(Y_2)||_F^2 - ||X_2Y_2^*||_F^2
   + (1/2)|t_2|^2.
```

The off-diagonal crossed entry is

```text
M_{11,22}
 = - <X_1^T conjugate(Y_1), X_2^T conjugate(Y_2)>_F
   - <X_1Y_1^*, X_2Y_2^*>_F
   + (1/2) conjugate(t_1)t_2.
```

Set

```text
z = <X_1Y_1^*, X_2Y_2^*>_F
    + <X_1^T conjugate(Y_1), X_2^T conjugate(Y_2)>_F
    - (1/2)conjugate(t_1)t_2.
```

Then `M_{11,22}=-z`, and therefore

```text
Delta_cross
 = M_{11,11}M_{22,22} - |M_{11,22}|^2
 = D_1D_2 - |z|^2,
```

where `D_i` denotes the corresponding diagonal PCL defect.  This is precisely
the phase-aware PAL determinant block from the prior loops, after matching the
`tr_1` convention.  Consequently the crossed minor is not merely analogous to
PAL; it is the PAL determinant slice of PCL.

This identity is rigorous algebra, but it does not prove `Delta_cross>=0`, since
the PAL determinant inequality itself is one of the open equivalent formulations.

## 3. Exact rank-one-update determinant formula

The same block gives a faithful formulation of the trace-coupled update.  Write

```text
D_S = [[x,c],[conjugate(c),y]],
u_S = [conjugate(t_1), conjugate(t_2)]^T.
```

Then

```text
M_S = D_S + (1/2) u_S u_S^*.
```

For a `2 x 2` matrix this gives the exact determinant identity

```text
det M_S
 = det D_S + (1/2) u_S^* adj(D_S) u_S
```

or, expanded,

```text
Delta_cross
 = xy - |c|^2
   + (1/2)( y|t_1|^2 + x|t_2|^2
            - 2 Re( c t_1 conjugate(t_2) ) ).
```

This identity is useful because it shows exactly what a trace-coupled proof would
have to control:

```text
xy - |c|^2 may be negative,
```

so the proof cannot be decomposed as `det D_S>=0` plus a positive correction.
The correction is sign-dependent through the mixed term
`-2 Re(c t_1 conjugate(t_2))`, not merely a sum of squares visible separately
from `D_S`.

## 4. Obstruction: the contraction-defect crossed minor is false

The product equality family already obstructs the overstrong crossed-minor route.
Take

```text
U=V=span{|0,0>, |0,1>}.
```

For `S={(1,1),(2,2)}` the exact crossed blocks are

```text
D_S = [[0,-1],[-1,0]],
T_S = [[1,1],[1,1]],
M_S = [[1/2,-1/2],[-1/2,1/2]].
```

Thus

```text
eig(D_S)=[-1,1],        det D_S=-1,
eig(M_S)=[0,1],         det M_S=0.
```

The trace update exactly repairs the bad direction.  This gives a concrete
obstruction to any proof attempting to show either `D>=0`, `D_S>=0`, or
`det D_S>=0` before adding `(1/2)T`.

The traceless equality regression

```text
U=V=span{|0,0>, |1,1>}
```

has instead

```text
D_S=0,
M_S=(1/2)[[1,1],[1,1]],
det M_S=0.
```

So both visible equality mechanisms force the crossed minor to vanish, but for
different reasons: in the product case trace coupling cancels a negative
contraction determinant; in the traceless case the crossed contraction block is
already degenerate.

## 5. Numerical/symbolic regression script

I added and ran the probe script

```text
research_harness/experiments/LOOP-0007_pcl_crossed_minor_probe.py
```

It writes a JSON log to

```text
research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.json
```

and stdout to

```text
research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.stdout.log
```

Actual run command:

```text
python3 research_harness/experiments/LOOP-0007_pcl_crossed_minor_probe.py \
  | tee research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.stdout.log
```

Actual stdout summary:

```text
random samples: 2000
min_delta_cross: 1.7189848517707407 at sample 137
min_det_D2: 1.5892325445991295 at sample 137
max_rank_one_update_identity_error: 8.881784197001252e-16
max_pal_block_identity_error: 8.881784197001252e-16
negative_D2_count: 0
negative_Dfull_count: 0

coordinate two-plane pairs: 14400
min_delta_cross: 0.0
min_det_D2: -1.0
negative_D2_count: 48
```

Interpretation:

1. The exact rank-one-update determinant identity and the exact PAL-slice identity
   were verified to roundoff on 2000 random frame pairs.
2. Random Gaussian frames did not sample a negative `D_S`; this is not evidence
   for `D_S>=0`, because the coordinate enumeration and product equality case
   explicitly give negative `D_S`.
3. Coordinate two-plane enumeration found no negative `Delta_cross`, but it is
   only a finite sparse regression class and not a proof on the Grassmannians.

## 6. What was proved vs. what remains open

Proved in this lane:

```text
1. The crossed PCL minor for S={(1,1),(2,2)} is exactly the phase-aware PAL
   determinant slice for (U_1,V_1),(U_2,V_2).

2. The crossed determinant has the exact trace-rank-one-update expansion

   det M_S = det D_S + (1/2)u_S^*adj(D_S)u_S.

3. The contraction-defect-only crossed determinant route is false:
   det D_S can be negative, with det D_S=-1 in the product equality case.
```

Not proved:

```text
1. Delta_cross >= 0 for all U,V.
2. Any complete set of 2 x 2 PCL principal minors.
3. Any 3 x 3 principal minors, det M, or full PSD certificate for M.
4. CLAIM-0001.
```

No counterexample was found.  The numerical tests remain regression evidence
only.

## 7. Next subtarget

The next symbolic subtarget should not be `D_S>=0` or `det D_S>=0`; those are
false.  A viable next target is a direct certificate for

```text
xy - |c|^2
+ (1/2)( y|t_1|^2 + x|t_2|^2 - 2 Re(c t_1 conjugate(t_2)) ) >= 0
```

under the two-frame constraints

```text
<U_i,U_j>_F=delta_ij,
<V_alpha,V_beta>_F=delta_alpha,beta.
```

Concretely, the next lane should try to express this scalar as a sum of:

```text
- row/column wedge polarization squares,
- trace-coupled bilinear squares involving c,t_1,t_2,
- Plucker-relation multiples for both two-planes.
```

If that succeeds, the result still proves only one family of `2 x 2` minors;
full PCL would still require the shared-index `2 x 2` minors, the `3 x 3` minors,
and `det M`, or a separate full Hermitian Gram/SOS certificate.

## Verdict

Fail closed.  This lane sharpened the crossed-minor algebra and blocked a false
contraction-defect determinant route, but it did not produce a complete proof or
a rank-two positive-gap counterexample.  CLAIM-0001 remains open.
