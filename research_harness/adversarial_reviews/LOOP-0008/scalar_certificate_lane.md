# LOOP-0008 scalar certificate lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: coupled phase-aware PAL determinant / crossed PCL minor
success_condition_met: none

## Executive verdict

I attacked the immediate scalar bottleneck

```text
D_1 D_2 - |a + conjugate(b)|^2 >= 0,
```

equivalently the crossed PCL principal minor

```text
det M[{(1,1),(2,2)}] >= 0,
```

with the trace rank-one update retained.  I did not find a complete Plucker/SOS/Gram certificate and did not find a counterexample.  The lane remains fail-closed.

What was obtained is a sharper obstruction to a tempting diagonal-wedge/SOS route: the one-pair diagonal defects have clean row/column wedge SOS identities, but their naive bilinear polarizations do not reproduce the off-diagonal crossed PAL/PCL entry.  Therefore the known diagonal SOS certificates do not extend mechanically to the scalar determinant.  Any certificate must include genuinely two-frame trace-coupled terms, not just a polarization of the one-pair Cauchy defects.

## 1. Assumptions and notation

No Hermitian, normal, positive, or commutative assumption is made.  Work with two Hilbert-Schmidt orthonormal frames

```text
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij,
X_i,Y_i in M_4(C).
```

Use the corrected partial-trace/PCL convention from LOOP-0007.  On the crossed PCL block `S={(1,1),(2,2)}` write

```text
D_S = [[x, c], [conjugate(c), y]],
u_S = [conjugate(t_1), conjugate(t_2)]^T,
M_S = D_S + (1/2) u_S u_S^*,
```

where

```text
t_i = tr(Y_i^* X_i)
```

in PCL notation.  Equivalently, in the PAL notation of prior loops,

```text
M_S = [[D_1, -z],[-conjugate(z), D_2]],
z = <X_1Y_1^*,X_2Y_2^*>_F
    + conjugate(<X_1^*Y_1,X_2^*Y_2>_F)
    - (1/2)t_1 conjugate(t_2).
```

The scalar target is exactly

```text
det M_S
= xy - |c|^2
  + (1/2)( y|t_1|^2 + x|t_2|^2
           - 2 Re(c t_1 conjugate(t_2)) ) >= 0.        (1)
```

This lane deliberately does not try to prove `D_S >= 0` or `det D_S >= 0`; both are false by the product equality family.

## 2. Exact identities retained

The trace rank-one update identity is exact:

```text
det(D_S + (1/2)u_Su_S^*)
= det D_S + (1/2)u_S^* adj(D_S) u_S.
```

Expanded, this is (1).  The mixed term

```text
- Re(c t_1 conjugate(t_2))
```

is not optional bookkeeping: in product equality examples it exactly cancels a negative contraction determinant.

The one-pair diagonal pieces also have exact Cauchy/wedge SOS identities.  For a single pair `X,Y` with `||X||_F=||Y||_F=1`, write `X_{i,*}` for rows and `X_{*,a}` for columns.  Then

```text
1 - ||XY^*||_F^2
= sum_{i,j} ( ||X_{i,*}||^2 ||Y_{j,*}||^2
              - |<X_{i,*},Y_{j,*}>|^2 ),              (2)
```

and

```text
1 - ||X^*Y||_F^2
= sum_{a,b} ( ||X_{*,a}||^2 ||Y_{*,b}||^2
              - |<X_{*,a},Y_{*,b}>|^2 ).              (3)
```

Thus each diagonal PAL/PCL defect is visibly nonnegative after adding the trace piece:

```text
D_i = (1-||X_iY_i^*||_F^2)
    + (1-||X_i^*Y_i||_F^2)
    + (1/2)|t_i|^2 >= 0.
```

The new issue is not the diagonal terms; it is the off-diagonal determinant coupling.

## 3. Obstruction found: diagonal wedge SOS does not polarize into the crossed block

A tempting route is to polarize (2) and (3), hope to obtain the off-diagonal entries of the left/right PAL defect blocks, and then use a two-vector Gram determinant argument with the trace vector appended.  This would give a clean Gram certificate.

This route fails.  The bilinear polarization of the row-wedge diagonal defect gives the kernel

```text
sum_{i,j} ( <X_1[i,*],X_2[i,*]> <Y_1[j,*],Y_2[j,*]>
          - <X_1[i,*],Y_2[j,*]> <Y_1[j,*],X_2[i,*]> ),
```

and the analogous column expression for (3).  These expressions are not the crossed PAL/PCL off-diagonal contractions

```text
-<X_1Y_1^*, X_2Y_2^*>_F,
-conjugate(<X_1^*Y_1, X_2^*Y_2>_F)
```

under only the two-frame constraints.  The probe script verified the diagonal identities to roundoff but found random mismatches up to approximately

```text
0.295153648209067
```

between the naive wedge polarizations and the actual crossed off-diagonal entries.  This is not a counterexample to the target inequality; it is an obstruction to a specific natural certificate route.

Interpretation: the scalar certificate, if it exists, cannot be obtained simply by taking the known one-pair Cauchy/SOS proofs for the diagonal entries and polarizing them.  Additional two-frame Plucker relations and the trace-coupled phase term must enter.

## 4. Equality/guardrail regressions

The product equality skeleton remains the main exact guardrail.  For

```text
X_1=Y_1=E_00,
X_2=Y_2=E_01,
```

the script records

```text
D_S = [[0,-1],[-1,0]],
det D_S = -1,
t_1=t_2=1,
trace update term = 1,
M_S = [[1/2,-1/2],[-1/2,1/2]],
det M_S = 0.
```

Thus every proof that first establishes `det D_S >= 0`, `D_S >= 0`, or separated left/right Cauchy-Schwarz is proving a false intermediate statement.

For the traceless diagonal equality skeleton

```text
X_1=Y_1=E_00,
X_2=Y_2=E_11,
```

the script records

```text
D_S = 0,
M_S = (1/2) [[1,1],[1,1]],
det M_S = 0.
```

The same zero determinant therefore has at least two different mechanisms: trace repair of a negative contraction determinant in the product case, and contraction degeneracy in the traceless case.

## 5. Script/log artifacts

I created and ran:

```text
research_harness/experiments/LOOP-0008_scalar_certificate_probe.py
```

Run command from repository root:

```text
python3 research_harness/experiments/LOOP-0008_scalar_certificate_probe.py \
  | tee research_harness/logs/LOOP-0008_scalar_certificate_probe_seed8008.stdout.log
```

JSON log:

```text
research_harness/logs/LOOP-0008_scalar_certificate_probe_seed8008.json
```

Stdout log:

```text
research_harness/logs/LOOP-0008_scalar_certificate_probe_seed8008.stdout.log
```

Actual run summary:

```text
random samples: 5000
random min_delta: 1.7774468279460423
random min_det_D: 1.552491745021106
max_trace_update_formula_error: 8.881784197001252e-16
max_one_pair_wedge_diag_error: 1.5543122344752192e-15
max_naive_wedge_bilinear_mismatch: 0.295153648209067

coordinate two-plane pairs: 14400
coordinate min_delta: 0.0
coordinate min_det_D: -1.0
coordinate negative_det_D_count: 48
coordinate zero_delta_count: 264
coordinate zero_delta_with_negative_det_D_count: 48

local optimization starts: 8
best optimized delta: 6.455059043026971e-13
```

The random/local optimization runs are only sanity checks.  They found no negative scalar defect but are not proof evidence.

## 6. What was proved vs. what remains open

Proved/verified in this lane:

1. The trace-coupled determinant expansion (1) was retained and regression-checked to roundoff.
2. The one-pair diagonal row/column wedge SOS identities (2), (3) were regression-checked to roundoff.
3. The naive diagonal-wedge polarization route does not reproduce the crossed off-diagonal PAL/PCL entries; therefore this natural Gram-certificate route is obstructed.
4. Sparse coordinate enumeration again confirms `det D_S` can be negative while `det M_S` is zero/nonnegative.

Not proved:

1. Universal scalar nonnegativity `det M_S >= 0`.
2. A trace-coupled Plucker/SOS/Gram certificate for (1).
3. Any full `4 x 4` PCL PSD certificate.
4. CLAIM-0001.

No counterexample was found.

## 7. Next subtarget

The next scalar certificate attempt should target the missing mixed two-frame identity directly.  Concretely, seek terms involving both frames simultaneously, not just polarized diagonal defects, of the form

```text
row/column Plucker cross-terms
+ trace-coupled bilinear squares involving c,t_1,t_2
+ orthogonality multipliers for <X_1,X_2>=0 and <Y_1,Y_2>=0,
```

whose sum equals (1).  The product equality skeleton should be used as a hard regression: the certificate must vanish when `D_S` has eigenvalues `[-1,1]` and the trace update exactly repairs the negative direction.

Fail-closed verdict: useful obstruction and reproducible diagnostics only; no proof, no refutation, and no bridge-defect success.
