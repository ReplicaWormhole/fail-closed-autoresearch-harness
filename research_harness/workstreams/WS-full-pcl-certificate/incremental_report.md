# WS-full-pcl-certificate incremental report

Initialized in co-mathematician migration at 2026-06-03T20:01:29+02:00.

Current summary:

LOOP-0011 Schur diagnostics reject D-only routes and found no M violation.

LOOP-0012 added a trace-coupled pivot candidate diagnostic and durable lane report:

```text
research_harness/experiments/LOOP-0012_trace_coupled_pivot_candidate.py
research_harness/logs/LOOP-0012_trace_coupled_pivot_candidate_seed12012.stdout.log
research_harness/logs/LOOP-0012_trace_coupled_pivot_candidate_seed12012.json
research_harness/adversarial_reviews/LOOP-0012/full_pcl_certificate_lane.md
```

Real run used `python3.12` because the Hermes `python3` environment lacks numpy:

```text
python3.12 -m py_compile research_harness/experiments/LOOP-0012_trace_coupled_pivot_candidate.py
python3.12 research_harness/experiments/LOOP-0012_trace_coupled_pivot_candidate.py --trials 300 --seed 12012 > research_harness/logs/LOOP-0012_trace_coupled_pivot_candidate_seed12012.stdout.log
```

Key output: coordinate scan over `14400` support-pair cases had `M_negative_eig_count=0`, `M_no_nonnegative_pivot_order=0`, but `D_negative_eig_count=48` and `D_no_nonnegative_pivot_order=120`; random scan over `300` cases had no `M` negative eigenvalue and worst sampled `min eig(M)=1.054577270164715`.

Candidate to attack next: for pivot `i`, complement `R`, `m=M_ii=D_ii+(1/2)|t_i|^2` and `c=M_Ri=D_Ri+(1/2)conj(t_R)t_i`, prove PSD/nonnegative principal minors of the trace-coupled Schur object `S_R(M)=M_RR-c c^*/m` directly.  Equivalently prove all update determinants `det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S)` by Gram/SOS.  Do not replace this with a D-only pivot/minor claim.

## LOOP-0013 update (2026-06-03T21:10:12+02:00)

Artifacts:

- `research_harness/adversarial_reviews/LOOP-0013/full_pcl_certificate_lane.md`
- `research_harness/experiments/LOOP-0013_full_pcl_rank_update_diagnostics.py`
- `research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.json`
- `research_harness/logs/LOOP-0013_full_pcl_rank_update_seed13013.stdout.log`

Concrete actions:

- Recorded the trace-coupled determinant-update identity `det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S)` as the proved algebraic part.
- Re-ran coordinate/random diagnostics with seed `13013`: coordinate `M` had no negative eigenvalue and no no-pivot-order case; `D` again had `48` negative eigenvalue cases and `120` no-nonnegative-pivot-order cases.
- Isolated the remaining certificate target: prove `det(D_S)+(1/2)q_S>=0` for all principal subsets or produce a full trace-coupled Schur/Gram/SOS certificate.

Current summary:

U-0002 remains unresolved. The determinant identity and diagnostics sharpen the target, but do not prove PSD of `M` for arbitrary two-frames. D-only routes remain refuted.

Reviewer status: accepted_with_caveats / fail-closed.
