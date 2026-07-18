# LOOP-0012 full-PCL trace-coupled Schur/pivot lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: WS-full-pcl-certificate / trace-coupled Schur, Gram, SOS, rank-one-update candidate
success_condition_met: none

## Executive verdict

No proof or counterexample was obtained.  The lane does, however, sharpen the next admissible certificate shape and gives fresh regression data rejecting D-only pivots.

The only admissible matrix target remains

```text
M = 2I_4 - A - B + (1/2)T = D + (1/2) conjugate(t) t^T,
D = 2I_4 - A - B.
```

A Schur proof may not pivot on `D` or prove positivity of a D-only Schur complement.  In the coordinate/control cases, `D` has negative or singular pivot behavior exactly where the trace term repairs `M`.

## Artifact and run

Created diagnostic script:

```text
research_harness/experiments/LOOP-0012_trace_coupled_pivot_candidate.py
```

Commands run from repository root:

```text
python3.12 -m py_compile research_harness/experiments/LOOP-0012_trace_coupled_pivot_candidate.py
python3.12 research_harness/experiments/LOOP-0012_trace_coupled_pivot_candidate.py --trials 300 --seed 12012 > research_harness/logs/LOOP-0012_trace_coupled_pivot_candidate_seed12012.stdout.log
```

Note: the Hermes `python3` environment lacks numpy; this repository's previous numerical scripts require the system `python3.12`, where numpy is installed.  The compile/run above used `python3.12` successfully.

Logs written:

```text
research_harness/logs/LOOP-0012_trace_coupled_pivot_candidate_seed12012.stdout.log
research_harness/logs/LOOP-0012_trace_coupled_pivot_candidate_seed12012.json
```

Stdout summary:

```json
{
  "loop": "LOOP-0012",
  "seed": 12012,
  "trials": 300,
  "D_only_route_status": "explicitly rejected; D pivot/minor positivity is false on controls/coordinate cases",
  "coordinate_total_pairs": 14400,
  "coordinate_M_negative_eig_count": 0,
  "coordinate_D_negative_eig_count": 48,
  "coordinate_M_no_nonnegative_pivot_order": 0,
  "coordinate_D_no_nonnegative_pivot_order": 120,
  "random_M_negative_eig_count": 0,
  "random_D_negative_eig_count": 0,
  "random_M_no_nonnegative_pivot_order": 0,
  "random_D_no_nonnegative_pivot_order": 0,
  "worst_random_M_min_eig": 1.054577270164715,
  "log": "./research_harness/logs/LOOP-0012_trace_coupled_pivot_candidate_seed12012.json"
}
```

## Trace-coupled Schur candidate

For any principal pivot `i` with complement `R`, write

```text
m = M_ii = D_ii + (1/2)|t_i|^2,
c = M_Ri = D_Ri + (1/2) conjugate(t_R) t_i.
```

The only acceptable one-step Schur object is

```text
S_R(M) = M_RR - c c^*/m
       = D_RR + (1/2)conjugate(t_R)t_R^T
         - (D_Ri + (1/2)conjugate(t_R)t_i)
           (D_iR + (1/2)conjugate(t_i)t_R^T) / (D_ii + (1/2)|t_i|^2).
```

Equivalently, at the principal-minor level the admissible target is

```text
det(M_S) = det(D_S) + (1/2) t_S^T adj(D_S) conjugate(t_S) >= 0
```

for every principal subset `S`, including singular `D_S` by the adjugate polynomial identity.  This is a trace-coupled rank-one-update candidate, not a D-only certificate.  A future proof should find a Hermitian Gram/SOS decomposition of either `S_R(M)` after an invariantly chosen positive `M` pivot, or all of the update determinants above.

## Findings

1. **D-only pivots are rejected again, more strongly.**  In all `14400` coordinate support-pair cases, `M` had no negative eigenvalue and had at least one nonnegative one-by-one pivot order.  By contrast, `D` had `48` negative-eigenvalue cases and `120` cases with no nonnegative pivot order.  Thus an LDL/Schur certificate that first certifies `D` or uses D-only pivots is not merely incomplete; it is false on the finite coordinate atlas.

2. **The trace update repairs the bad D directions in the controls.**  In the product projection control, `eig(D)=[-1,1,1,1]` while `eig(M)=[0,1,1,1]`.  The `D` minimum direction has Rayleigh value `-1`, and the trace update contributes `+1`, giving `M` Rayleigh value `0` on that same direction.  This shows the update must be carried inside the Schur complement, not appended after a D-only argument.

3. **The tested M-pivot route remains numerically plausible but unproved.**  In the coordinate atlas, `coordinate_M_no_nonnegative_pivot_order=0`; in `300` random full-frame trials, `random_M_negative_eig_count=0` and `random_M_no_nonnegative_pivot_order=0`, with worst sampled `min eig(M)=1.054577270164715`.  These are diagnostics only; random cases are far from equality and do not establish a Grassmannian proof.

4. **No scalar-to-full bridge was found.**  The scalar crossed minor remains insufficient for full PSD.  The candidate must cover all principal minors or a full Hermitian Schur/Gram object.

## Fail-closed conclusion

This lane advances U-0002 by isolating an admissible trace-coupled Schur/rank-one-update target and by adding durable regression data that explicitly rejects D-only pivot certificates.  It does not prove `M >= 0`, does not refute CLAIM-0001, and does not supply a complete Gram/SOS decomposition.

Recommended next action: derive symbolic formulas for the entries/principal minors of `S_R(M)` above in two-frame Plucker coordinates, then attempt an SOS/Gram decomposition of that trace-coupled Schur complement.  Regression tests should include the LOOP-0012 coordinate examples where `D` has no nonnegative pivot order but `M` is repaired by the trace update.
