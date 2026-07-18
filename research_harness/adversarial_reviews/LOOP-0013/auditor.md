# LOOP-0013 auditor review

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
success_condition_met: none
promotion_verdict: reject_loop_success
verdict: fail_closed

## Executive verdict

I audited the LOOP-0013 lane reports, referenced scripts/logs, and promotion gates A/B/C.  The artifacts exist and the executable Python scripts compile.  The JSON logs parse and support the lane summaries.  However, the reported work does **not** meet any success condition: no complete proof, no certified counterexample, and no accepted bridge defect.

Final auditor verdict: **FAIL-CLOSED / no success condition met.**

## File-existence audit

All required lane reports for LOOP-0013 are present:

| Artifact | Status |
|---|---:|
| `./research_harness/adversarial_reviews/LOOP-0013/scalar_slack_equality_lane.md` | exists |
| `./research_harness/adversarial_reviews/LOOP-0013/full_pcl_certificate_lane.md` | exists |
| `./research_harness/adversarial_reviews/LOOP-0013/literature_related_inequalities_lane.md` | exists |
| `./research_harness/experiments/LOOP-0013_scalar_slack_equality_symbolic.py` | exists |
| `./research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.json` | exists |
| `./research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.stdout.log` | exists |
| `./research_harness/experiments/LOOP-0013_full_pcl_rank_update_diagnostics.py` | exists |
| `./research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.json` | exists |
| `./research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.stdout.log` | exists |
| `./research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/00README.json` | exists |
| `./research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/2507.18278.eprint` | exists |
| `./research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex` | exists |

## Compilation and JSON audit

Commands run from repository root `.`:

```text
python3 --version
python3 -m py_compile \
  research_harness/experiments/LOOP-0013_scalar_slack_equality_symbolic.py \
  research_harness/experiments/LOOP-0013_full_pcl_rank_update_diagnostics.py
python3.12 --version
python3.12 -m py_compile \
  research_harness/experiments/LOOP-0013_scalar_slack_equality_symbolic.py \
  research_harness/experiments/LOOP-0013_full_pcl_rank_update_diagnostics.py
python3 - <<'PY'
import json
for p in [
 'research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.json',
 'research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.json',
 'research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/00README.json',
]:
    data=json.load(open(p))
    print(p, 'OK', type(data).__name__, sorted(data)[:8])
PY
sha256sum \
  research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/2507.18278.eprint \
  research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex
```

Observed output:

```text
Python 3.11.15
research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.json OK dict ['adversarial_caveat', 'claim', 'elapsed_sec', 'exact_real_rotation_families', 'loop', 'numeric_complex_unitary_family_tests', 'status', 'workstreams']
research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.json OK dict ['D_only_route_status', 'coordinate_scan', 'lane', 'loop', 'proved_algebraic_identity', 'random_scan', 'success_condition_met', 'unproved_certificate_target']
research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/00README.json OK dict ['process', 'sources']
3dcb51d22a3b7596c9c78f881041e3cf1f77e1dfac858ab3a7b40f6fcd1ab2c8  research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/2507.18278.eprint
38f576f8f5f82552a8f68d572855bdbe0c6fe465be841af1c8b6ed6208dce077  research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex
/usr/bin/python3.12
Python 3.12.3
```

Both scripts compile under `python3` and `python3.12`; the JSON logs parse; the arXiv source hashes match the literature lane.

## Lane audit

### 1. Scalar slack / equality geometry lane

Report status: `completed_fail_closed`; `success_condition_met: none`.

Accepted as durable progress:

- Exact real-rotation equality families were produced in restricted row/column/diagonal charts.
- JSON records `Delta = 0` and `GramSlack = ExchangePenalty > 0` on the exact families.
- Complex-unitary numerical stress tests have roundoff-scale `max_abs_delta` values for 100 samples per family.

Not accepted as success:

- No universal scalar SOS/Plucker/Gram certificate was produced.
- No global equality classification was produced.
- Complex-unitary generalization is numerical evidence, not a symbolic theorem.
- Scalar equality guardrails do not prove full PCL or CLAIM-0001.

### 2. Full-PCL trace-coupled certificate lane

Report status: `completed_fail_closed`; `success_condition_met: none`.

Accepted as durable progress:

- The determinant-update identity
  `det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S)`
  is a valid matrix-determinant-lemma/adjugate polynomial identity for
  `M_S = D_S + (1/2)conj(t_S)t_S^T`.
- Diagnostics confirm the identity on coordinate and random samples to roundoff.
- The lane correctly rejects D-only routes; the log records `D_negative_eig_count = 48`, `D_no_nonnegative_pivot_order_count = 120`, and coordinate examples with `detD = -1` repaired by the trace update.

Not accepted as success:

- No symbolic proof that all principal minors of `M` are nonnegative was produced.
- No Gram/SOS representation of `q_S` or `det(M_S)` was produced.
- Coordinate scans and 500 random trials are not a proof over arbitrary two-frames.
- A determinant identity is not itself a PSD/PCL certificate.

### 3. Literature and related inequalities lane

Report status: fail-closed/no theorem imported as proof.

Accepted as durable progress:

- arXiv `2507.18278` was retrieved and source copied durably.
- The hashes recorded in the lane match audit output.
- The lane correctly identifies the sharp trace-corrected theorem as normal-only and the arbitrary-rank-two available bound as weaker: `||M_A||_2^2 + ||M_B||_2^2 <= 3||M||_2^2`.

Not accepted as success:

- The normal-matrix theorem exceeds CLAIM-0001 hypotheses.
- The arbitrary-rank-two theorem is too weak for the required trace-corrected coefficient.
- Rank-one and quantum-information results do not cover arbitrary non-Hermitian ordinary-rank-two `C`.
- No bridge defect is identified; the lane confirms missing external proof rather than replacing the claim.

## Promotion gates A/B/C

### A. Proof success

Rejected.  A complete proof of the original rank-two partial-trace inequality was not produced.  The missing pieces are explicitly acknowledged: universal scalar certificate, full trace-coupled PCL PSD/Schur/Gram/SOS certificate, and global equality/classification or bridge completion.  The literature theorem with the desired sharp shape is normal-only and cannot be promoted to arbitrary non-normal rank two.

### B. Counterexample success

Rejected.  No reconstructable rank-two matrix `C` with

```text
gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2||C||_F^2 - (1/2)|tr C|^2 > 0
```

is reported.  The scalar lane reports equality-family controls (`Delta = 0`), and the PCL lane reports no negative `M` eigenvalue/minor in tested samples, not a positive original-gap counterexample.

### C. Bridge-defect success

Rejected.  No precise mathematical defect in the PAL/PCL/CLAIM bridge is found or accepted.  LOOP-0013 clarifies guardrails and missing certificates but does not invalidate the active target or establish that it must be replaced.

## Auditor conclusion

LOOP-0013 artifacts are present and technically auditable; scripts compile; logs parse; source hashes check out.  Mathematically, the loop remains fail-closed.  It produced useful guardrails and diagnostics, but no proof/counterexample/bridge-defect success.

Final verdict: `completed_fail_closed; no_success_condition_met; reject_loop_success`.
