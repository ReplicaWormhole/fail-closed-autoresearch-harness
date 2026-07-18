# LOOP-0007 PAL determinant lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: universal phase-aware PAL two-frame determinant inequality
success_condition_met: none

## Executive verdict

I attacked the universal phase-aware PAL determinant target

```text
|a+conjugate(b)|^2 <= D_1 D_2
```

for Hilbert-Schmidt orthonormal two-frames `X_1,X_2` and `Y_1,Y_2` in
`M_4(C)`.  I found a useful exact determinant-defect decomposition of the PAL
block into two partial-trace contraction-defect blocks plus the trace rank-one
update, and I stress-tested this decomposition numerically and on equality/
guardrail examples.

The decomposition is rigorous, but it does not prove PAL.  In fact, it explains
why several tempting Cauchy-Schwarz/SOS routes are too strong: the separated
left/right defect blocks are already indefinite on sharp two-frame examples, and
the phase-aware kernel cannot be promoted to all orthonormal `m>=3` frames.

Final status for this lane:

```text
PAL proved: no
PAL refuted: no
CLAIM-0001 proved/refuted: no
new certified counterexample: no
useful subidentity: yes
next subtarget: prove a two-frame-only SOS/mixed-discriminant certificate for
                det(KL+KR+TT), or switch to the crossed PCL 2x2 minor/full PCL
                rank-one-update certificate.
```

## 1. Conventions and PAL block

Use the Frobenius inner product

```text
<A,B>_F = tr(A^* B),
```

conjugate-linear in the first argument.  For orthonormal two-frames

```text
<X_i,X_j>_F = delta_ij,      <Y_i,Y_j>_F = delta_ij,
```

set

```text
L_i = X_i Y_i^*,
R_i = X_i^* Y_i,
t_i = tr(X_i^*Y_i),
a   = <L_1,L_2>_F,
b   = <R_1,R_2>_F - (1/2)conjugate(t_1)t_2,
D_i = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2.
```

The phase-aware off-diagonal is

```text
z = a + conjugate(b)
  = <L_1,L_2>_F + conjugate(<R_1,R_2>_F)
    - (1/2)t_1 conjugate(t_2).
```

PAL is equivalently positivity of the Hermitian `2 x 2` matrix

```text
K^PAL = [[D_1, -z],[-conjugate(z), D_2]],
```

or

```text
det K^PAL = D_1D_2 - |z|^2 >= 0.
```

## 2. Exact determinant-defect decomposition

For a finite paired frame list `(X_i,Y_i)`, define three Hermitian kernels

```text
(KL)_{ij} = delta_ij - <X_iY_i^*, X_jY_j^*>_F,
(KR)_{ij} = delta_ij - conjugate(<X_i^*Y_i, X_j^*Y_j>_F),
(TT)_{ij} = (1/2) tr(X_i^*Y_i) conjugate(tr(X_j^*Y_j)).
```

Then for `i,j in {1,2}`,

```text
K^PAL_{ij} = (KL)_{ij} + (KR)_{ij} + (TT)_{ij}.          (1)
```

This is an exact identity.  It is just the PCL/PAL rank-one-update structure
written on the SVD-diagonal slice:

```text
K^PAL = [left partial-trace defect]
        + [right partial-trace defect with PAL conjugation]
        + [trace rank-one update].
```

For the diagonal entries, (1) gives the known one-pair decomposition

```text
D_i = (1-||X_iY_i^*||_F^2)
    + (1-||X_i^*Y_i||_F^2)
    + (1/2)|t_i|^2 >= 0.
```

For the off-diagonal, (1) gives exactly

```text
K^PAL_{12}
 = -<L_1,L_2>_F - conjugate(<R_1,R_2>_F)
   + (1/2)t_1 conjugate(t_2)
 = -z.
```

Thus the determinant target can be restated as the two-frame-only determinant
inequality

```text
det(KL+KR+TT) >= 0.                                      (2)
```

This formulation is useful because it isolates the essential coupling: the trace
rank-one term must repair negative directions of the contraction-defect blocks.
It is not enough to prove separate Cauchy-Schwarz inequalities for `KL` and `KR`.

## 3. Why the separated Cauchy-Schwarz route fails

A natural attempted proof is:

1. treat `KL` and `KR` as positive Gram defects;
2. use Cauchy-Schwarz on each;
3. add the positive trace rank-one term.

This route is false.  The components `KL` and `KR` are not PSD even for sharp
orthonormal two-frame data.

### Product equality example

Take

```text
X_1=Y_1=E_00,       X_2=Y_2=E_01.
```

The script output gives

```text
K^PAL = [[ 1/2, -1/2],[-1/2, 1/2]],       eig(K^PAL)=[0,1].
KL    = [[ 0,   -1  ],[-1,   0  ]],       eig(KL)=[-1,1].
KR    = 0,
TT    = [[ 1/2, 1/2],[1/2, 1/2]].
```

So PAL is sharp and true on this skeleton, but the left defect block alone has a
negative eigenvalue.  The trace update is essential.

### Right-defect symmetric example

Take

```text
X_1=Y_1=E_00,       X_2=Y_2=E_10.
```

The output gives

```text
K^PAL = [[ 1/2, -1/2],[-1/2, 1/2]],       eig(K^PAL)=[0,1],
KR    = [[ 0,   -1  ],[-1,   0  ]],       eig(KR)=[-1,1].
```

So the analogous right contraction-defect Cauchy-Schwarz route is also blocked.

Conclusion: any SOS proof must be for the coupled determinant (2), not for the
separate channels.

## 4. Guardrail: no all-frame `m>=3` PSD promotion

The same phase-aware formula is indefinite for three orthonormal paired terms.
A concrete matrix-unit obstruction is

```text
X_i=Y_i=E_{0,i-1},        i=1,2,3.
```

Then

```text
K = [[ 1/2, -1/2, -1/2],
     [-1/2,  1/2, -1/2],
     [-1/2, -1/2,  1/2]],

eig(K) = [-1/2, 1, 1].
```

Every `2 x 2` principal submatrix in this example is the sharp PAL equality
matrix, but the `3 x 3` matrix is indefinite.  Therefore the desired theorem
cannot be obtained by proving that the PAL kernel is PSD for arbitrary longer
orthonormal frames.  A proof must use genuinely two-frame/determinant-level
constraints.

## 5. Guardrail: no fixed-gauge arbitrary-complex-coefficient strengthening

The LOOP-0002 fixed-gauge witness remains a decisive regression test.  Take

```text
X_1=Y_1=E_00,
X_2=E_01,
Y_2=i E_01.
```

For the correct phase-aware block, the script returns

```text
K^PAL = [[1/2,  i/2],[-i/2, 1/2]],
eig(K^PAL) = [0,1],
det(K^PAL) = 0.
```

For the old fixed-gauge overstrengthening, which uses `a+b` instead of
`a+conjugate(b)`, the corresponding block has

```text
eig(fixed_gauge_K) = [-1,2],
det(fixed_gauge_K) = -2.
```

Thus the phase-aware conjugation is not cosmetic; it is exactly what turns the
LOOP-0002 refutation into a PAL equality case.  This lane makes no use of the
false fixed-gauge `H <= 2I` or arbitrary-complex-coefficient target.

## 6. Numerical/stress-test artifacts

I wrote and ran

```text
research_harness/experiments/LOOP-0007_pal_determinant_identities.py
```

which produced

```text
research_harness/logs/LOOP-0007_pal_determinant_identities.json
```

Main checks from the run:

```text
identity_random_m2:
  seed: 7007
  trials: 200
  max_identity_residual: 4.440892098500626e-16
  min_eig_K: 1.2026683060621426
  min_eig_left_defect: 0.4839581608983716
  min_eig_right_defect: 0.5205630924154214
  min_det_slack_m2: 1.7189848517707407

identity_random_m3:
  seed: 7010
  trials: 200
  max_identity_residual: 2.220446049250313e-16
  min_eig_K: 1.1846726310879125
```

The random tests are not proof evidence beyond sanity checking.  Their main
purpose was to verify the exact decomposition implementation and ensure no
conjugation/sign error in (1).

I also ran the existing PAL random/BFGS search script as a regression:

```text
python3 research_harness/experiments/LOOP-0004_pal_search.py \
  --seed 7007 --random 3000 --maxiter 120 \
  --out research_harness/logs/LOOP-0007_pal_search_seed7007.json
```

The stdout log is

```text
research_harness/logs/LOOP-0007_pal_search_seed7007.stdout.log
```

The relevant PAL fields showed no robust PAL violation:

```text
matrix-unit best violation: 0.0
random best violation:     -1.6873856119785282
optimized best violation:  -1.1268763699945339e-13
```

Important caution: that legacy script also prints a field named
`max_original_gap_grid`; I did not use that field as evidence because the old
script predates the corrected LOOP-0006 partial-trace convention.  The PAL
violation fields in `pal_values` are the only fields used here.

## 7. Candidate two-frame-only SOS target

The exact coupled determinant target is now:

```text
Delta_PAL = det(KL+KR+TT) >= 0,                         (3)
```

where `KL,KR,TT` are the three `2 x 2` Hermitian matrices in Section 2.
Expanding (3) gives

```text
Delta_PAL
= (l_1+r_1+tau_1)(l_2+r_2+tau_2)
  - |ell+rho+theta|^2,
```

with

```text
l_i   = 1-||X_iY_i^*||_F^2,
r_i   = 1-||X_i^*Y_i||_F^2,
tau_i = (1/2)|t_i|^2,
ell  = -<X_1Y_1^*,X_2Y_2^*>_F,
rho  = -conjugate(<X_1^*Y_1,X_2^*Y_2>_F),
theta= (1/2)t_1 conjugate(t_2).
```

A viable SOS proof would need to show that the negative pieces in the mixed
quantity

```text
(l_1+r_1+tau_1)(l_2+r_2+tau_2) - |ell+rho+theta|^2
```

are exactly absorbed by the two-frame orthogonality constraints

```text
<X_1,X_2>_F = 0,      <Y_1,Y_2>_F = 0,
```

and by the coupled trace update.  The equality examples above imply that such an
SOS, if it exists, must vanish on both product-projection and traceless-diagonal
skeletons and must not decompose into independent left/right PSD certificates.

I did not find this SOS certificate.

## 8. Relation to PCL and fixed-basis limitations

By LOOP-0006, universal PAL is equivalent to CLAIM-0001/PCL at the level of
universal statements, but one fixed PAL block is only the SVD-diagonal `2 x 2`
principal slice of a fixed `4 x 4` PCL compression matrix.  This lane preserves
that distinction:

```text
single PAL determinant in one basis:  controls span{E_11,E_22} only;
universal PAL over all two-frames:    enough for CLAIM/PCL after re-SVD;
fixed-basis PCL certificate:          still requires all coefficient directions.
```

Therefore even a proof of (3) would prove CLAIM-0001 via the SVD route, but would
not automatically provide a closed-form full `4 x 4` PCL principal-minor/SOS
certificate in one fixed support basis.

## 9. What was proved and what remains open

Proved/verified in this lane:

1. Exact identity

```text
K^PAL = KL + KR + TT
```

with the PAL conjugations tracked.

2. Diagonal one-pair defect decomposition

```text
D_i = (1-||X_iY_i^*||^2)+(1-||X_i^*Y_i||^2)+(1/2)|t_i|^2.
```

3. Concrete guardrail examples showing:
   - separated `KL`/`KR` Cauchy-Schwarz routes are false;
   - all-frame `m>=3` PSD promotion is false;
   - fixed-gauge `a+b` overstrengthening is false, while phase-aware PAL is
     sharp on the same witness.

Not proved:

1. The determinant inequality `det(KL+KR+TT) >= 0`.
2. Any full two-frame SOS certificate.
3. Any full fixed-basis PCL `4 x 4` PSD/principal-minor certificate.
4. CLAIM-0001.

No counterexample was found.

## 10. Recommended next subtarget

The next precise subtarget is one of:

1. Directly certify the mixed determinant (3) as a two-frame-only SOS with
   multipliers for `<X_1,X_2>=0` and `<Y_1,Y_2>=0`.
2. Translate (3) into the crossed PCL principal minor language and attempt a
   coupled rank-one-update certificate for that minor.
3. If the `2 x 2` layer is solved, continue to the full PCL `4 x 4` matrix:
   all `3 x 3` principal minors and `det M`, or a direct Hermitian Gram/SOS.

Fail-closed verdict remains: this lane supplies useful identities and guardrails,
but no complete proof and no certified counterexample.
