# LOOP-0006 Auditor Review

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_verdict: no_success_condition_met
pcl_status: open_unproved_not_refuted
pal_status: open_unproved_not_refuted
bridge_status: conceptual_relation_identified_no_bridge_defect
last_updated: 2026-06-03
reviewed:
  - research_harness/status.json
  - research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
  - research_harness/adversarial_reviews/LOOP-0006/pcl_symbolic_certificate_lane.md
  - research_harness/adversarial_reviews/LOOP-0006/pcl_structured_counterexample_lane.md
  - research_harness/adversarial_reviews/LOOP-0006/pal_pcl_bridge_lane.md
  - research_harness/adversarial_reviews/LOOP-0006/skeptic.md

## Executive verdict

Fail closed. LOOP-0006 does not prove or refute CLAIM-0001, and it does not meet any stop/success condition.

Exact success verdict:

```text
success: false
success_type: null
success_condition_met: none
complete proof found: no
verified rank-two positive-gap counterexample found: no
accepted bridge-defect found: no
```

Conservative decision:

1. Complete proof: not met.
   - The symbolic lane did not produce a full Hermitian Gram/SOS, all-principal-minor, Schur/rank-one-update, or other rigorous certificate for
     `M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0` on `Gr(2,16) x Gr(2,16)`.
   - Diagonal wedge/SOS identities certify only the `1 x 1` principal minors, not full PSD.
   - The crossed `2 x 2` principal minor was isolated as a sharp unresolved target, but was not proved.

2. Verified rank-two positive-gap counterexample: not met.
   - The structured PCL counterexample lane found no robust positive eigenvalue of the compression matrix `K` and no positive original gap.
   - The corrected run reports `best overall lambda_max: 0.0`, `robust_positive: false`, and local optimization `best lambda_max: -5.20317946714477e-13`, consistent with equality/roundoff rather than a counterexample.
   - No rational, interval, or independently checkable certificate for a positive-gap rank-at-most-two matrix was produced.

3. Accepted bridge-defect: not met.
   - The PAL-PCL bridge lane identifies the correct universal relation between PAL, PCL, and CLAIM-0001.
   - It finds no defect in the claimed equivalence strong enough to close or invalidate the target.
   - The relation is conceptual and quantifier-sensitive: one fixed PAL block is only a principal slice of one fixed PCL matrix, while universal PAL covers all PCL directions only after re-SVD/rotating support bases for each coefficient matrix.

Therefore CLAIM-0001 remains open/fail-closed.

## What LOOP-0006 actually established

### 1. Symbolic PCL certificate lane

The symbolic lane used the exact PCL matrix

```text
M = -K = 2I_4 - A - B + (1/2)T,
```

where for orthonormal two-frames `u_i=vec(U_i)`, `v_alpha=vec(V_alpha)` and `E_{i alpha}=|u_i><v_alpha|`,

```text
tr_1 E_{i alpha} = U_i^T conjugate(V_alpha),
tr_2 E_{i alpha} = U_i V_alpha^*,
tr   E_{i alpha} = tr(V_alpha^* U_i).
```

It established useful guardrails and subresults:

- Each diagonal entry `M_{i alpha,i alpha}` has a Lagrange/wedge SOS certificate and is nonnegative.
- The tempting route `D=2I-A-B >= 0` is false. In the product equality case,

```text
eig(D) = [-1, 1, 1, 1],
eig((1/2)T) = [0, 0, 0, 1],
eig(M) = [0, 1, 1, 1].
```

  Hence any proof must retain the trace rank-one correction globally.
- The sharpest small unresolved symbolic target identified in this lane is the crossed `2 x 2` principal minor, for example

```text
Delta_cross = M_{11,11} M_{22,22} - |M_{11,22}|^2 >= 0,
```

  together with relabelings. This minor vanishes in known equality regressions, so it is a serious certificate stress test.

Auditor interpretation: these are useful reductions and negative-route exclusions, but they are not a PCL proof. In particular, diagonal positivity plus equality regressions do not imply full `4 x 4` PSD, and the crossed minor itself remains unproved.

### 2. Structured counterexample lane

The counterexample lane corrected a partial-trace implementation error from an initial draft. The corrected convention is

```python
tr_1(C)[a,b] = sum_i C[i,a,i,b]   via np.einsum('iaib->ab', T)
tr_2(C)[i,j] = sum_a C[i,a,j,a]   via np.einsum('iaja->ij', T)
```

After correction, equality controls matched the expected spectra:

```text
product projection K eigenvalues:  [-1, -1, -1, 0]
traceless diagonal K eigenvalues:  [-2, -2, -1, 0]
```

The corrected structured search reported:

```text
structured support cases: 2592
structured support best lambda_max: -0.24830718408995792
perturb eps=0.01 best lambda_max: -0.004606073165632001
perturb eps=0.1 best lambda_max: -0.3137722327674509
local optimization best lambda_max: -5.20317946714477e-13
best overall lambda_max: 0.0
robust_positive: false
```

Auditor interpretation: this is useful regression evidence and removes spurious positives caused by a wrong trace convention. It is not exhaustive and not a proof. It also does not provide a counterexample, because no robust positive top eigenvalue or positive reconstructed original gap survived.

### 3. PAL-PCL bridge lane

The bridge lane clarified the relation between PAL and PCL:

```text
PCL => PAL
PAL => CLAIM-0001
CLAIM-0001 => PCL
```

at the level of universal statements.

The principal-slice identification is:

```text
M[{E_11,E_22},{E_11,E_22}]
 = [[D_1, -z],[-conjugate(z), D_2]],
```

where

```text
z = <X_1Y_1^*,X_2Y_2^*>_F
    + conjugate(<X_1^*Y_1,X_2^*Y_2>_F)
    - (1/2)t_1 conjugate(t_2),
t_i = tr(X_i^*Y_i).
```

This is the phase-aware PAL determinant matrix, not the refuted fixed-gauge `a+b` quantity from LOOP-0002.

The bridge lane also correctly warns that one fixed PAL/SVD diagonal block in one support basis is not a full fixed-basis PCL certificate. Full PCL includes directions involving `E_12`, `E_21`, mixed minors, `3 x 3` minors, and `det M`. Universal PAL would cover those directions only by taking the SVD of each coefficient matrix and rotating the support bases accordingly.

Auditor interpretation: the bridge relation is accepted as a conceptual clarification, but it is not a proof of the inequality and not a bridge-defect success.

## Updated current bottleneck

The updated current bottleneck should be recorded as:

```text
Prove the equivalent PCL compression inequality M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0 on Gr(2,16) x Gr(2,16), prove the universal phase-aware PAL two-frame determinant inequality, or produce a certified rank-two positive-gap counterexample.
```

More detailed technical bottleneck:

```text
Find a rigorous full-matrix PSD certificate for M, or a complete all-principal-minor certificate. The immediate principal-minor subtarget is all 2 x 2 minors, especially the sharp crossed minor Delta_cross, followed by the relevant 3 x 3 minors and det M. The trace rank-one update must remain coupled globally; the false route D=2I-A-B >= 0 is blocked.
```

## Next loop recommendation

Recommended LOOP-0007 focus:

```text
Pursue a rigorous PCL/PAL certificate with primary emphasis on the crossed 2 x 2 principal minors and the trace-coupled rank-one-update structure, while maintaining the corrected partial-trace convention and equality-family regressions.
```

Suggested tasks:

1. Attempt an exact certificate for all `2 x 2` principal minors of `M`, starting with the crossed minor

```text
Delta_cross = M_{11,11}M_{22,22} - |M_{11,22}|^2.
```

Use row/column wedge polarizations, trace-coupled bilinears, and Plucker relations for both `Gr(2,16)` factors. Do not treat one crossed minor alone as a full proof.

2. If the `2 x 2` layer is certified, continue to `3 x 3` principal minors and `det M`, or replace the principal-minor route with a direct Hermitian Gram/SOS certificate for the full matrix.

3. Explore the rank-one-update route

```text
M = D + (1/2)t t^*,        D=2I-A-B,
```

but only with a rigorous inertia/domination statement; do not try to prove `D >= 0`, which is already refuted.

4. Keep the structured counterexample script as a regression harness. Any claimed counterexample must reconstruct an explicit rank-at-most-two `C` and certify positive gap by rational, interval, or otherwise independently checkable arithmetic.

5. Preserve all known guardrails:
   - no fixed-gauge `a+b` or `H <= 2I` replacement;
   - no all-frame `m >= 3` PSD-kernel promotion;
   - no independent local Schmidt normalization of both support planes unless covariance is proved;
   - no inference from diagonal positivity or numerical nonpositivity to full PSD.

## Suggested claim-card update language

Append language like the following to `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`:

```text
## LOOP-0006 update

LOOP-0006 did not prove or refute CLAIM-0001. It attacked the equivalent PCL formulation by symbolic certificate search, structured counterexample search, and a PAL/PCL bridge audit.

The symbolic PCL lane confirmed diagonal wedge/SOS certificates for the `1 x 1` principal minors of `M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V)`, but found no full Hermitian Gram/SOS or all-principal-minor certificate. It also showed that the overstrong contraction-defect route `D=2I-A-B >= 0` is false: in the product equality case `eig(D)=[-1,1,1,1]`, while the trace rank-one update repairs the bad direction and `eig(M)=[0,1,1,1]`. The sharp next symbolic target is the crossed `2 x 2` principal minor `M_{11,11}M_{22,22}-|M_{11,22}|^2 >= 0`, but this minor remains unproved and is not by itself sufficient for full PCL.

The structured PCL counterexample lane corrected a partial-trace convention error that had produced spurious positives. With the corrected convention, equality controls reproduced the known `K` spectra `[-1,-1,-1,0]` and `[-2,-2,-1,0]`; structured search, equality perturbations, and BFGS optimization found no robust positive eigenvalue. The main corrected run had `best overall lambda_max=0.0`, `robust_positive=false`, and local optimization `best lambda_max=-5.20317946714477e-13`, consistent with equality/roundoff. No certified positive-gap rank-two counterexample was produced.

The PAL/PCL bridge lane identified the exact quantifier-level relation: PCL implies PAL by taking the SVD-diagonal `2 x 2` principal submatrix, PAL implies CLAIM-0001 by the rank-two SVD route, and CLAIM-0001 implies PCL by support compression. Thus universal PAL, CLAIM-0001, and PCL are equivalent formulations. However, one fixed PAL block is only a principal slice of a fixed PCL matrix; it is not a full fixed-basis `4 x 4` PSD certificate.

Fail-closed verdict remains: no accepted proof, no accepted rank-two positive-gap counterexample, and no accepted bridge-defect. Current bottleneck: prove PCL via a full Hermitian Gram/SOS, rank-one-update, or all-principal-minor certificate; prove universal phase-aware PAL; or produce a certified rank-two positive-gap counterexample.
```

## Suggested status.json update language

Do not change `status.json` automatically in this auditor review. If the coordinator updates it, suggested values are:

```json
{
  "status": "running",
  "success": false,
  "success_type": null,
  "success_record": null,
  "last_completed_loop": "LOOP-0006",
  "next_loop_number": 7,
  "current_bottleneck": "prove the equivalent PCL compression inequality M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0 on Gr(2,16) x Gr(2,16), prove the universal phase-aware PAL two-frame determinant inequality, or produce a certified rank-two positive-gap counterexample"
}
```

The `stop_condition` can remain unchanged:

```text
auditor-accepted proof, auditor-accepted rank-two positive-gap counterexample, or auditor-accepted bridge-defect
```

## Final auditor decision

```text
LOOP-0006 status: fail_closed
CLAIM-0001 status: open / fail_closed
complete proof found: no
rank-two positive-gap counterexample found: no
accepted bridge-defect found: no
PCL proved: no
PAL proved: no
PCL refuted: no
PAL/PCL bridge relation: clarified, no defect accepted
success verdict: no_success_condition_met
```
