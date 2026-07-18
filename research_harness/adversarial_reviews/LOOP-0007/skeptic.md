# LOOP-0007 Skeptic Review

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_verdict: no_success_condition_met
last_updated: 2026-06-03

reviewed:
  - research_harness/status.json
  - research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
  - research_harness/adversarial_reviews/LOOP-0007/pcl_crossed_minor_lane.md
  - research_harness/adversarial_reviews/LOOP-0007/pal_determinant_lane.md
  - research_harness/adversarial_reviews/LOOP-0007/certified_search_lane.md
  - research_harness/experiments/LOOP-0007_pcl_crossed_minor_probe.py
  - research_harness/experiments/LOOP-0007_pal_determinant_identities.py
  - research_harness/experiments/LOOP-0007_certified_search.py
  - research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.stdout.log
  - research_harness/logs/LOOP-0007_pal_search_seed7007.stdout.log
  - research_harness/logs/LOOP-0007_certified_search_seed7007.stdout.log
  - research_harness/adversarial_reviews/LOOP-0006/skeptic.md

## Executive verdict

Fail closed. LOOP-0007 does not prove or refute CLAIM-0001.

No success condition survives adversarial review:

```text
complete proof of CLAIM-0001: no
complete proof of universal PAL: no
complete proof of PCL / full 4x4 compression PSD: no
certified rank-two positive-gap counterexample: no
accepted bridge defect: no
```

The LOOP-0007 lanes are useful because they sharpen the trace-coupled algebra,
reconfirm the corrected partial-trace convention, and block several overstrong
routes. They are not sufficient for promotion. The current status in
`status.json` remains accurate: the claim is still running/open, and the stop
condition has not been met.

## 1. Baseline claim and convention audit

The claim card states the correct target:

```text
gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2||C||_F^2 - (1/2)|tr C|^2 <= 0
```

for arbitrary complex `16 x 16` matrices `C` with ordinary matrix rank at most
2. The explicit non-assumptions remain essential:

```text
C need not be Hermitian, normal, positive semidefinite, or a vector state.
```

LOOP-0007 mostly respects this. The proof lanes work with SVD/support frames and
PCL compression data, not with positivity or Hermiticity of `C`. The search lane
uses arbitrary complex rank-two factorizations `C=A B^*`, which is appropriate.

The partial-trace convention used in the LOOP-0007 scripts is the corrected
LOOP-0006 convention:

```text
tr_1(C)[a,b] = sum_i C[i,a,i,b]
tr_2(C)[i,j] = sum_a C[i,a,j,a]
```

For a rank-one atom `E=|vec(U)><vec(V)|`, this gives

```text
tr_1 E = U^T conjugate(V)
tr_2 E = U V^*
tr E   = tr(V^* U)
```

The scripts and reports are internally consistent with this convention. I do
not see a surviving partial-trace index error in the LOOP-0007 artifacts I
reviewed. The remaining issue is not convention but overinterpretation risk:
identities and numerical regressions are sometimes close to the desired theorem,
but they do not close it.

## 2. PCL crossed-minor lane audit

The crossed-minor lane correctly attacks the sharp LOOP-0006 subtarget:

```text
M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0
```

on the crossed principal block

```text
S = {(1,1),(2,2)}.
```

The lane's strongest contribution is an exact identification:

```text
Delta_cross = det M_S
            = M_{11,11}M_{22,22} - |M_{11,22}|^2
```

is the phase-aware PAL determinant for the diagonal SVD atoms. It also records
the exact rank-one-update formula

```text
det M_S = det D_S + (1/2) u_S^* adj(D_S) u_S,
D_S = (2I-A-B)_S.
```

This is credible algebra and is backed by the probe script, whose stdout reports
roundoff-scale residuals:

```text
max_rank_one_update_identity_error: 8.881784197001252e-16
max_pal_block_identity_error:       8.881784197001252e-16
```

However, this lane does not prove the crossed minor. The exact identity reduces
one unresolved object to another unresolved equivalent object: the PAL
determinant. It is therefore a reduction/translation, not a certificate.

### 2.1 Trace rank-one update cannot be dropped

The lane correctly blocks the false contraction-defect route. In the product
coordinate equality regression it reports

```text
D_S = [[0,-1],[-1,0]], det D_S=-1
M_S = [[1/2,-1/2],[-1/2,1/2]], det M_S=0
```

Thus any attempted proof of `D_S >= 0`, `det D_S >= 0`, or full `D >= 0` before
adding the trace update is false. This is a serious guardrail: the trace rank-one
update is not an optional positive term that can be appended after a separate
Cauchy-Schwarz proof. It is essential and sign-coupled through the mixed term.

### 2.2 Principal-minor insufficiency

Even if the crossed `2 x 2` minor were proved, that alone would not prove PCL.
A full fixed-basis `4 x 4` Hermitian PSD certificate still needs all principal
minors, or an equivalent direct Gram/SOS/inertia certificate. The lane states
this caveat, and it must remain attached to any future citation of the result.

### 2.3 Numerical evidence remains non-proof

The crossed-minor script reports no negative crossed determinant in 2000 random
samples or in coordinate two-plane enumeration, but this is only regression
evidence on finite/random classes. It is not a theorem on
`Gr(2,16) x Gr(2,16)`. The reported random `negative_Dfull_count=0` must not be
read as evidence for `D>=0`, because coordinate/equality examples already refute
that route.

Verdict on this lane: useful exact reduction and guardrails; no proof, no
counterexample, no success condition.

## 3. PAL determinant lane audit

The PAL determinant lane works with the phase-aware two-frame target

```text
|a+conjugate(b)|^2 <= D_1 D_2
```

or equivalently positivity of

```text
K^PAL = [[D_1, -z],[-conjugate(z), D_2]].
```

The lane proves/records the exact decomposition

```text
K^PAL = KL + KR + TT
```

where `KL` and `KR` are left/right partial-trace contraction-defect kernels and
`TT` is the trace rank-one update. The identity residuals in the script are at
roundoff scale, and the formulas track the phase-aware conjugation rather than
the old false fixed-gauge term.

This is not a proof of PAL. It is only a decomposition of the matrix whose PSD
is still unknown.

### 3.1 No hidden Hermitian/positive assumption on C found

The PAL lane is formulated on SVD reshaped singular vectors `X_i,Y_i`, not on a
Hermitian/normal/positive `C`. That is acceptable. The dangerous hidden
assumption would be to treat the paired frame kernel as PSD for all lengths or to
handle arbitrary fixed-gauge complex coefficients; the lane explicitly rejects
both.

### 3.2 Separated Cauchy-Schwarz/SOS routes are false

The product and right-defect equality examples show that `KL` and `KR` can be
indefinite even when the coupled PAL block is sharp PSD. This blocks proofs that
try to certify left and right contraction defects independently. Any future proof
must certify the coupled determinant with the trace update included.

### 3.3 All-frame m>=3 promotion is false

The lane gives the matrix-unit obstruction

```text
X_i=Y_i=E_{0,i-1}, i=1,2,3
K = [[ 1/2,-1/2,-1/2],[-1/2,1/2,-1/2],[-1/2,-1/2,1/2]]
eig(K) = [-1/2,1,1]
```

This is an important adversarial point. Every `2 x 2` principal block in this
example can look sharp, while the `3 x 3` extension is indefinite. Therefore the
PAL theorem cannot be proved by a naive universal PSD-kernel promotion to
arbitrary `m>=3` paired frames. Any such future proof must be rejected unless it
uses genuinely two-frame/determinant-specific structure.

### 3.4 Fixed-gauge overstrengthening remains false

The LOOP-0002 witness remains fatal to fixed-gauge `a+b` variants. The PAL lane
correctly uses `a+conjugate(b)` and reports that the same witness is a sharp PAL
equality case while the fixed-gauge matrix is indefinite. This avoids the old
false promotion from arbitrary complex coefficients in a fixed SVD gauge.

### 3.5 Numerical PAL search is not certification

The legacy PAL search reports no robust violation:

```text
matrix-unit best violation: 0.0
random best violation:     -1.6873856119785282
optimized best violation:  -1.1268763699945339e-13
```

The optimized value is near zero and negative at floating-point scale. It should
be interpreted as convergence to equality/roundoff, not as proof. The lane also
correctly refuses to use the legacy `max_original_gap_grid` field because that
script predates the corrected partial-trace convention.

Verdict on this lane: correct guardrails and useful decomposition; PAL remains
unproved and unrefuted; no success condition.

## 4. Certified-search lane audit

Despite the lane name, this is a numerical search/regression lane, not a
certificate lane. It explicitly says so, and that caveat is correct.

The script searches the original rank-two inequality using corrected partial
traces. It includes equality regressions, random rank-two factorizations,
SVD-truncated perturbations around controls, and coordinate two-unit scans. The
reported stdout is:

```text
equality normalized gaps:
  diag_difference:      0.0
  product_projection:  -2.2204460492503136e-16
  phase_sparse_control:-0.5
random_rank2 trials: 20000
random best normalized gap: -1.2143877928448128
random positive count tol 1e-10: 0
coordinate scan total: 130816
coordinate best normalized gap: 0.0
coordinate positive count tol 1e-10: 0
best perturbation normalized gap: -7.779413143726018e-10
robust_positive_gap_found: False
```

This gives no counterexample. It also gives no proof.

### 4.1 No certified positive candidate exists

A valid counterexample success would require an explicit `16 x 16` matrix `C`
with ordinary rank at most two and original-convention `gap(C)>0`, checked by
rational, interval, or high-precision arithmetic. LOOP-0007 supplies no such
matrix. The best reported values are zero equality controls or negative
near-equality values.

### 4.2 Search coverage limitations

The search is not exhaustive over the rank-two variety:

- random `A B^*` sampling is finite;
- SVD truncation of ambient perturbations is heuristic and does not parametrize
  the full tangent cone near equality manifolds;
- coordinate two-unit scans cover only sparse skeletons with phases
  `+1,-1,+i,-i`;
- no interval/rational certificate is produced because no positive candidate was
  found.

Thus the only acceptable conclusion is fail-closed absence of found positives.

Verdict on this lane: no positive-gap rank-two counterexample and no proof.

## 5. Bridge/equivalence risks to keep closed

LOOP-0006 established the useful universal-level relation:

```text
PCL => PAL
PAL => CLAIM-0001
CLAIM-0001 => PCL
```

LOOP-0007 uses this relation but does not improve it into a proof. The following
caveats remain mandatory:

1. A single fixed PAL block is only the SVD-diagonal `2 x 2` principal slice of a
   fixed PCL compression matrix. It is not a full fixed-basis `4 x 4` PSD
   certificate.

2. Universal PAL over all two-frames would imply CLAIM-0001 by moving to the SVD
   basis of each tested `C`. This moving-basis route is logically valid only if
   PAL is proved universally, which LOOP-0007 has not done.

3. PCL as a fixed support-compression statement still asks for all coefficient
   directions `C=PCQ`, not only the diagonal SVD coefficient direction.

4. The trace rank-one update must be retained in any bridge or certificate. The
   product equality case refutes any proof that drops the trace update and tries
   to add it back as an independent nonnegative afterthought.

## 6. Hidden-assumption checklist

Adversarial checklist result:

```text
hidden Hermitian/normal/positive assumption: not found in LOOP-0007 conclusions,
  but must remain a hard guardrail for future proofs.

fixed-gauge overstrengthening: explicitly avoided; old a+b route remains false.

all-frame m>=3 false promotion: explicitly refuted by the PAL lane; any proof
  relying on it must be rejected.

dropped trace rank-one update: explicitly blocked; D or det(D_S) routes are
  false on product equality examples.

numerical evidence promoted to proof: lanes mostly avoid this, but all searches
  remain non-certifying and must not be promoted.

partial-trace convention mistakes: no surviving LOOP-0007 index error seen;
  corrected convention is used in the reviewed scripts.

principal-slice promoted to full PCL: not done as a final claim, but this remains
  the main risk when citing the crossed/PAL identities.
```

## 7. Sharpest next bottleneck

The sharpest immediate bottleneck is the coupled two-frame determinant/crossed
minor with the trace rank-one update retained:

```text
Delta_PAL = D_1D_2 - |z|^2 >= 0
```

equivalently

```text
Delta_cross = det M[{(1,1),(2,2)}] >= 0.
```

A viable next proof attempt should produce an actual two-frame-only SOS/Gram or
rank-one-update certificate for this scalar, with multipliers for the two-frame
orthogonality constraints and with the product and traceless equality families as
mandatory zero regressions.

However, this is only the sharpest scalar bottleneck. If the route is PCL rather
than universal PAL, a complete claim proof still needs the full `4 x 4`
compression matrix PSD certificate: all relevant `2 x 2`, `3 x 3`, and `4 x 4`
principal minors or a direct Hermitian Gram/SOS/inertia proof.

For counterexample work, the sharpest next search bottleneck is not more generic
random sampling but a tangent-space/equality-manifold parameterization coupled to
PCL eigenvectors, followed by exact reconstruction and interval/rational checking
if any positive candidate appears.

## Final decision

```text
LOOP-0007 status: fail_closed
CLAIM-0001 status: open / fail_closed
PAL proved: no
PCL proved: no
crossed minor proved: no
rank-two positive-gap counterexample: no
bridge defect accepted: no
success condition survives: none
```

LOOP-0007 narrows the problem and records useful guardrails, but it does not meet
any stop condition. The next accepted success must be either a rigorous universal
PAL/PCL proof, a full bridge-defect accepted by audit, or an explicit certified
rank-at-most-two positive-gap counterexample.
