# LOOP-0005 Auditor Review

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_verdict: no_success_condition_met
pcl_status: exact_reformulation_open_unproved_not_refuted
last_updated: 2026-06-03
reviewed:
  - research_harness/status.json
  - research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
  - research_harness/adversarial_reviews/LOOP-0005/pcl_normal_form_lane.md
  - research_harness/adversarial_reviews/LOOP-0005/pcl_numerical_eigen_lane.md
  - research_harness/adversarial_reviews/LOOP-0005/pcl_proof_sos_lane.md
  - research_harness/adversarial_reviews/LOOP-0005/skeptic.md

## Executive verdict

Fail closed. LOOP-0005 does not meet any stop/success condition for CLAIM-0001.

Exact success verdict:

```text
success: false
success_type: null
success_condition_met: none
```

Conservative decision:

1. Complete proof: not met.
   - PCL was given as a precise 4 x 4 support-compression matrix inequality, but no universal proof of compression negativity was produced.
   - The proof/SOS lane isolated the target `M(U,V)=2I-A-B+(1/2)T >= 0` on `Gr(2,16) x Gr(2,16)`, but supplied no Gram factorization, no SOS certificate, and no proof of all principal minors.

2. Verified rank-two positive-gap counterexample: not met.
   - The numerical/eigenvalue lane found no robust positive compression eigenvalue.
   - The main run reported `random_positive_count_tol_1e_10 = 0`, `positive_robust_tol_1e_8 = false`, and best optimized `lambda_max = -8.4668383415476e-14`, consistent with near-equality/roundoff.
   - No explicit rank-at-most-two `C` with certified positive original gap was produced.

3. Accepted bridge-defect: not met.
   - LOOP-0005 clarified normal-form/covariance restrictions and blocked several overstrong proof routes, but these are proof-strategy defects, not a defect in the CLAIM-0001 bridge sufficient to close the target.
   - PCL remains accepted only as an exact equivalent formulation, not as a proved theorem and not as a refuted bridge.

Therefore CLAIM-0001 remains open/fail-closed: no accepted proof and no accepted counterexample.

## What LOOP-0005 established

### PCL normal-form lane

The normal-form lane gave an explicit coordinate target for PCL. For orthonormal bases `p_1,p_2` of `ran P` and `q_1,q_2` of `ran Q`, with

```text
E_{alpha beta} = |p_alpha><q_beta|,
```

the PCL compression matrix is

```text
K_{alpha beta, gamma delta}
 = <tr_1 E_{alpha beta}, tr_1 E_{gamma delta}>
 + <tr_2 E_{alpha beta}, tr_2 E_{gamma delta}>
 - (1/2) conjugate(tr E_{alpha beta}) tr E_{gamma delta}
 - 2 delta_{alpha gamma} delta_{beta delta}.
```

Equivalently, using the `2 x 2` matrices

```text
A_{ab}[alpha,beta] = sum_i p_alpha[i,a] conjugate(q_beta[i,b]),
B_{ij}[alpha,beta] = sum_a p_alpha[i,a] conjugate(q_beta[j,a]),
T[alpha,beta]      = <q_beta,p_alpha>,
```

the compression has the Gram form

```text
K = Gram({A_ab}) + Gram({B_ij}) - (1/2) vec(T) vec(T)^* - 2 I_4.
```

PCL is exactly the assertion `K <= 0` for all pairs of rank-two support planes.

The lane also correctly warned that PCL has only simultaneous local-conjugation covariance of the ambient bipartite space, not arbitrary independent local normalization of `P` and `Q`. Thus a future proof cannot simply Schmidt-normalize both support planes independently unless it explicitly preserves the partial-trace quadratic form.

This is a useful exact reduction and guardrail, but not a proof.

### PCL numerical/eigenvalue lane

The numerical lane implemented the compression matrix, self-checked the adjoint/quadratic identities, tested equality regressions, and searched for positive top eigenvalues.

Main reported evidence:

```text
self_check_adjoint.sesquilinear_abs_error = 2.0097183471152322e-14
self_check_adjoint.quadratic_abs_error    = 2.2737367544323206e-13
random_samples                            = 5000
random_positive_count_tol_1e_10           = 0
random_best_lambda_max                    = -1.047205640060712
optimization_restarts                     = 8
optimization_maxiter                      = 200
optimization_best_lambda_max              = -8.4668383415476e-14
optimization_best_reconstructed_gap       = -8.504308368628699e-14
best_overall_lambda_max                   = 0.0
best_overall_reconstructed_gap            = 0.0
positive_robust_tol_1e_8                  = false
```

Equality regressions were reproduced:

```text
traceless diagonal equality:      eigvals [-2, -2, -1, 0]
product projection equality:      eigvals [-1, -1, -1, 0]
LOOP-0002 phase-absorbed equality eigvals [-1, -1, -1, 0]
```

Auditor interpretation: this supports “no counterexample found” and validates the implementation against known equality cases, but it is numerical evidence only. It does not prove PCL, and the near-zero optimizer output is not a certified positive-gap counterexample.

### PCL proof/SOS lane

The proof/SOS lane identified a compact algebraic subproblem. With `u_i=vec(U_i)`, `v_alpha=vec(V_alpha)`, and `E_{i alpha}=|u_i><v_alpha|`, it used

```text
tr_1 |vec(U)><vec(V)| = U^T conjugate(V),
tr_2 |vec(U)><vec(V)| = U V^*,
tr |vec(U)><vec(V)|   = tr(V^* U),
```

and defined

```text
K = A + B - (1/2)T - 2I_4,
M = -K = 2I_4 - A - B + (1/2)T.
```

The remaining exact PCL target is

```text
M(U,V) >= 0
```

for all orthonormal two-frames `U,V in C^{16 x 2}`, i.e. on `Gr(2,16) x Gr(2,16)`.

The lane gave valid diagonal Lagrange/wedge SOS identities showing diagonal entries of `M` are nonnegative, but diagonal nonnegativity is much weaker than `M >= 0`. It did not prove all lower principal minors, did not prove `det M >= 0`, and did not supply a direct Hermitian Gram/SOS factorization. It also correctly rejected false/overstrong routes: the all-frame `m >= 3` PSD-kernel route and the fixed-gauge `H <= 2I` route.

Auditor interpretation: the lane isolates the right-looking algebraic certificate problem but does not solve it.

## Current bottleneck

The updated current bottleneck should be recorded as:

```text
Prove the equivalent PCL compression inequality M(U,V)=2I-A-B+(1/2)T >= 0 on Gr(2,16) x Gr(2,16), or prove the PAL two-frame determinant inequality, or produce a certified rank-two positive-gap counterexample.
```

More explicitly, the primary PCL target is:

```text
For all rank-two projections P,Q on C^4 tensor C^4,
Phi|_{Hom(QH,PH)} <= 0,
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I.
```

Equivalently, for all orthonormal two-frames `U,V in C^{16 x 2}`:

```text
M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0.
```

## Next loop recommendation

Recommended LOOP-0006 focus:

```text
Pursue a certified PCL proof/counterexample, with emphasis on invariant Plucker-coordinate or Hermitian Gram/SOS certificates for the full 4 x 4 matrix M, not only diagonal entries or determinant alone.
```

Suggested LOOP-0006 tasks:

1. Build a symbolic/invariant certificate search for `M(U,V) >= 0` on `Gr(2,16) x Gr(2,16)`.
   - Respect `U^*U=I_2`, `V^*V=I_2`, support-plane `U(2)` gauge freedom, and Plucker relations.
   - Target a direct Hermitian Gram factorization of `M`, or all principal minors of `M`; do not treat determinant nonnegativity alone as sufficient.

2. Use the known equality families as interpolation/regression constraints:
   - product-projection equality;
   - traceless two-product-atom equality;
   - LOOP-0002 phase-absorbed equality support.

3. Preserve the known route-blockers:
   - no independent local Schmidt normalization of both `P` and `Q` unless covariance is proved;
   - no all-frame `m >= 3` kernel promotion;
   - no fixed-gauge complex-coefficient `H <= 2I` replacement;
   - no inference from diagonal positivity to full PSD.

4. In parallel, continue counterexample search only if it reconstructs an original rank-at-most-two matrix `C` and certifies

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2 - (1/2)|tr C|^2 - 2||C||_F^2 > 0
```

with robust rational/interval or otherwise independently checkable certification.

## Suggested claim-card update language

Append language like the following to `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`:

```text
## LOOP-0005 update

LOOP-0005 did not prove or refute CLAIM-0001. It attacked the Projected Compression Lemma (PCL), the exact support-compression reformulation introduced in LOOP-0004.

For orthonormal two-frames `p_alpha,q_beta` in `H=C^4 tensor C^4`, with `E_{alpha beta}=|p_alpha><q_beta|`, the PCL compression matrix is

K_{alpha beta,gamma delta}
 = <tr_1 E_{alpha beta}, tr_1 E_{gamma delta}>
 + <tr_2 E_{alpha beta}, tr_2 E_{gamma delta}>
 - (1/2)conjugate(tr E_{alpha beta}) tr E_{gamma delta}
 - 2 delta_{alpha gamma} delta_{beta delta}.

Equivalently, `K = Gram({A_ab}) + Gram({B_ij}) - (1/2)vec(T)vec(T)^* - 2I_4`, and PCL asks for `K <= 0` for every pair of rank-two support planes.

Numerical PCL compression searches found no robust positive eigenvalue. Equality regressions reproduced the known sharp spectra `[-2,-2,-1,0]` and `[-1,-1,-1,0]`; the main random/BFGS run had `random_positive_count_tol_1e_10=0`, best optimized `lambda_max=-8.47e-14`, and `positive_robust_tol_1e_8=false`.

The proof/SOS lane isolated the exact algebraic target `M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V) >= 0` on `Gr(2,16) x Gr(2,16)`, but supplied no complete PSD/SOS certificate. Diagonal wedge-SOS identities were found, but they do not imply full `4 x 4` PSD. PCL remains open/unproved and not refuted.

Fail-closed verdict remains: no accepted proof, no accepted rank-two positive-gap counterexample, and no accepted bridge-defect. Current bottleneck: prove PCL via a full Hermitian Gram/SOS or principal-minor certificate, prove the PAL two-frame determinant inequality, or produce a certified rank-two positive-gap counterexample.
```

## Suggested status.json update language

Do not change `status.json` automatically in this auditor review. If the coordinator updates it, suggested values are:

```json
{
  "status": "running",
  "success": false,
  "success_type": null,
  "success_record": null,
  "last_completed_loop": "LOOP-0005",
  "next_loop_number": 6,
  "loops_completed_by_autoloop": 3,
  "current_bottleneck": "prove the equivalent PCL compression inequality M(U,V)=2I-A-B+(1/2)T >= 0 on Gr(2,16) x Gr(2,16), prove the PAL two-frame determinant inequality, or produce a certified rank-two positive-gap counterexample"
}
```

The `stop_condition` can remain unchanged:

```text
auditor-accepted proof, auditor-accepted rank-two positive-gap counterexample, or auditor-accepted bridge-defect
```

## Final auditor decision

```text
LOOP-0005 status: fail_closed
CLAIM-0001 status: open / fail_closed
complete proof found: no
rank-two positive-gap counterexample found: no
accepted bridge-defect found: no
PCL: open; exact equivalent support-compression reformulation; unproved; not refuted
PAL: open; exact two-frame determinant bottleneck from prior loop remains available
success verdict: no_success_condition_met
```
