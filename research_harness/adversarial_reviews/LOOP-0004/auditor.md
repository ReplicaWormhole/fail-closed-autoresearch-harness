# LOOP-0004 Auditor Review

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_verdict: no_success_condition_met
pal_status: open_unproved_not_refuted
pcl_status: exact_reformulation_open_unproved
last_updated: 2026-06-03
reviewed:
  - research_harness/status.json
  - research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
  - research_harness/adversarial_reviews/LOOP-0004/pal_proof_lane.md
  - research_harness/adversarial_reviews/LOOP-0004/pal_refutation_search.md
  - research_harness/adversarial_reviews/LOOP-0004/alternative_derivation_lane.md
  - research_harness/adversarial_reviews/LOOP-0004/skeptic.md

## Executive verdict

Fail closed. LOOP-0004 does not meet any stop/success condition for CLAIM-0001.

Exact success verdict:

```text
success: false
success_type: null
success_condition_met: none
```

Conservative decision:

1. Complete proof: not met.
   - PAL was reduced to an exact 2 by 2 determinant/PSD statement, but that determinant inequality remains unproved.
   - PCL was introduced as an exact support-compression restatement of CLAIM-0001, but the universal compression negativity remains unproved.

2. Verified rank-two positive-gap counterexample: not met.
   - The PAL refutation/search lane found no robust PAL violation.
   - It found matrix-unit equality cases and floating-point near-equality only.
   - No reconstructed rank-two matrix `C` with positive original `gap(C)` was certified.

3. Accepted bridge-defect: not met.
   - LOOP-0004 found useful formulation defects in overstrong proof strategies, especially the impossibility of a naive all-frame `m >= 3` PSD kernel extension.
   - This is a warning against an overstrong route, not a defect in CLAIM-0001 or in the bridge sufficient to close/refute the target.

Therefore CLAIM-0001 remains open/fail-closed: no accepted proof and no accepted counterexample.

## What LOOP-0004 established

### PAL proof lane

The proof lane correctly sharpened the LOOP-0003 phase-aware scalar target. With Hilbert-Schmidt inner product `<A,B> = tr(A^*B)`, orthonormal two-frames `X_1,X_2` and `Y_1,Y_2`, and

```text
L_i = X_i Y_i^*,
R_i = X_i^* Y_i,
t_i = tr(X_i^*Y_i),
a = <L_1,L_2>,
b = <R_1,R_2> - (1/2)conjugate(t_1)t_2,
D_i = 2 - ||L_i||_F^2 - ||R_i||_F^2 + (1/2)|t_i|^2,
```

right singular-vector phase absorption gives the phase-optimized PAL cross term

```text
z = a + conjugate(b)
  = <L_1,L_2> + conjugate(<R_1,R_2>) - (1/2)t_1 conjugate(t_2).
```

The lane reformulated PAL as positivity of the Hermitian matrix

```text
K^PAL = [[D_1, -z],[-conjugate(z), D_2]],
```

equivalently

```text
D_1D_2 - |z|^2 >= 0.
```

This is accepted as a useful exact reformulation of PAL, not a proof. The remaining missing sublemma is still the universal nonnegativity of this determinant for all Hilbert-Schmidt orthonormal two-frames.

The lane also established an important route-blocker: the analogous all-frame phase-aware kernel is not PSD for `m=3`; a matrix-unit 3-frame gives eigenvalues `[-1/2, 1, 1]`. Thus any future proof cannot simply promote PAL to a naive longer-frame positive-kernel theorem. This is a proof-strategy obstruction, not a disproof of the two-frame PAL.

PAL status after LOOP-0004:

```text
PAL: exact phase-aware SVD bottleneck; open; unproved; not refuted.
```

### PAL refutation/search lane

The search lane attacked

```text
violation = |a + conjugate(b)|^2 - D_1D_2.
```

Reported evidence:

```text
matrix-unit two-frame cases checked: 57600
matrix-unit equality cases: 528
best matrix-unit violation: 0.0
random trials: 8000
best random violation: -1.549087158428483
best optimized violation: -6.211697822777751e-14
best optimized |z|^2: 0.25671573363309635
best optimized D_1,D_2: 0.5066712245799205, 0.5066712321111203
coarse original-gap grid from best PAL near-equality: -1.206496300001389
```

Auditor interpretation: this is negative numerical evidence only. It found equality and roundoff-scale near-equality, but no robust positive PAL violation and no original rank-two positive-gap counterexample. It cannot certify PAL.

### Alternative derivation / PCL lane

The alternative lane introduced the quadratic-form operator

```text
q(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
       - (1/2)|tr C|^2 - 2||C||_F^2,
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I,
q(C) = <C,Phi(C)>_F.
```

It proposed the Projected Compression Lemma (PCL): for every pair of rank-two orthogonal projections `P,Q` on `H = C^4 tensor C^4`, the compression of `Phi` to

```text
Hom(QH,PH) = { C : C = P C Q }
```

is negative semidefinite, i.e. `q(C) <= 0` for all `C=PCQ`.

The equivalence check is accepted:

- PCL implies CLAIM-0001 by taking `P` and `Q` to be the range and co-range support projections of any rank-at-most-two `C`, enlarged to rank two if necessary.
- CLAIM-0001 implies PCL because every `C=PCQ` with rank-two `P,Q` has ordinary matrix rank at most two.

Thus PCL is not a theorem proved in LOOP-0004; it is an exact reformulation of CLAIM-0001 as a `4 x 4` support-compression negativity problem over pairs of two-planes in `Gr(2,16)`.

PCL status after LOOP-0004:

```text
PCL: exact Grassmannian/support-compression restatement of CLAIM-0001; open; unproved.
```

## Current bottleneck

The updated bottleneck is no longer merely "prove or refute PAL". LOOP-0004 produced two viable equivalent/open targets. The current bottleneck should be recorded as:

```text
Prove either the phase-aware two-frame PAL determinant inequality or the equivalent Projected Compression Lemma (PCL), or produce a certified rank-two C with robust positive original gap.
```

More explicitly, the two proof targets are:

1. PAL determinant target:

```text
D_1D_2 - |a+conjugate(b)|^2 >= 0
```

for all Hilbert-Schmidt orthonormal two-frames in `M_4(C)`.

2. PCL support-compression target:

```text
For all rank-two projections P,Q on C^4 tensor C^4,
Phi|_{Hom(QH,PH)} <= 0,
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I.
```

## Next loop recommendation

Recommended LOOP-0005 focus:

```text
Attack PCL as the primary lane, while keeping PAL determinant equality cases as regression tests.
```

Rationale:

- PCL is exactly equivalent to CLAIM-0001 and avoids SVD phase bookkeeping and the nonnegative diagonal singular-coefficient cone.
- It gives a concrete `4 x 4` Hermitian compression matrix for each pair of two-planes, which may be amenable to Grassmannian normal forms, Plucker-coordinate identities, or certified SDP/SOS searches.
- Any proposed proof must allow nontrivial kernels because known equality cases are sharp.
- Any proposed PAL proof must be genuinely two-frame/determinant-level; naive fixed-gauge complex PSD statements and all-frame `m >= 3` PSD kernels are already known false/obsolete.

Suggested LOOP-0005 tasks:

1. Derive a local-unitary/Grassmannian normal form for pairs of two-planes `P,Q` in `C^4 tensor C^4` and express the PCL compression matrix in that normal form.
2. Search for an exact SOS/PSD decomposition of `-Phi|_{Hom(QH,PH)}` using support-plane constraints or Plucker coordinates.
3. Preserve regression tests:
   - product-projection equality family;
   - traceless two-product-atom equality family;
   - LOOP-0002 phase-absorbed equality case;
   - LOOP-0004 3-frame obstruction, to reject overstrong all-frame kernel proofs.
4. In parallel, continue direct certified counterexample search only if it reconstructs an original rank-two `C` and verifies `gap(C) > 0` with rational/interval or otherwise robust certification.

## Suggested claim-card update language

Append language like the following to `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`:

```text
## LOOP-0004 update

LOOP-0004 did not prove or refute CLAIM-0001. The phase-aware scalar PAL target from LOOP-0003 was sharpened to an exact determinant formulation. For orthonormal two-frames `X_i,Y_i`, PAL is equivalent to positivity of the 2 by 2 Hermitian matrix

K^PAL = [[D_1, -z],[-conjugate(z), D_2]],
z = <X_1Y_1^*,X_2Y_2^*> + conjugate(<X_1^*Y_1,X_2^*Y_2>)
    - (1/2)tr(X_1^*Y_1)conjugate(tr(X_2^*Y_2)).

The determinant inequality `D_1D_2-|z|^2 >= 0` remains unproved. Sparse matrix-unit enumeration and floating-point random/BFGS searches found no PAL violation, only equality or near-equality.

LOOP-0004 also introduced the Projected Compression Lemma (PCL): for every pair of rank-two support projections `P,Q` on `C^4 tensor C^4`, the quadratic-form operator

Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I

should be negative semidefinite on `Hom(QH,PH)={C:C=PCQ}`. PCL is exactly equivalent to CLAIM-0001, not a proof or a strengthening. Its universal compression negativity remains open.

Fail-closed verdict remains: no accepted proof and no accepted rank-two positive-gap counterexample. Current bottleneck: prove PAL or PCL, or produce a certified rank-two positive-gap counterexample.
```

## Suggested status.json update language

Do not change `status.json` automatically in this auditor review. If the coordinator updates it, suggested values are:

```json
{
  "status": "running",
  "success": false,
  "success_type": null,
  "success_record": null,
  "last_completed_loop": "LOOP-0004",
  "next_loop_number": 5,
  "current_bottleneck": "prove the PAL two-frame determinant inequality or the equivalent Projected Compression Lemma, or produce a certified rank-two positive-gap counterexample"
}
```

The `stop_condition` can remain unchanged:

```text
auditor-accepted proof, auditor-accepted rank-two positive-gap counterexample, or auditor-accepted bridge-defect
```

## Final auditor decision

```text
LOOP-0004 status: fail_closed
CLAIM-0001 status: open / fail_closed
complete proof found: no
rank-two positive-gap counterexample found: no
accepted bridge-defect found: no
PAL: open; exact determinant bottleneck; unproved; not refuted
PCL: open; exact equivalent support-compression reformulation; unproved
success verdict: no_success_condition_met
```
