# LOOP-0010 full PCL coordinate-orbit / principal-minor lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: full `4 x 4` PCL principal-minor coordinate atlas
success_condition_met: none

## Executive verdict

The delegated full-PCL lane failed before writing an artifact, so I repaired the lane in the controller by creating and running a finite coordinate-support atlas for all principal minors of the full PCL matrix

```text
M = 2I - A - B + (1/2)T = D + (1/2)conjugate(t)t^T.
```

This is not a proof for arbitrary frames.  It is a finite exact-coordinate diagnostic designed to identify which principal-minor patterns actually need the trace rank-one update and to prevent false `D >= 0` / `det(D) >= 0` routes from resurfacing.

## Real run output

Command from repository root:

```text
python3 research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py   > research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.stdout.log
python3 -m py_compile research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py
```

Stdout summary:

```json
{
  "max_update_identity_error": 8.881784197001252e-16,
  "by_size": {
    "1": {"total": 57600, "negative_detM": 0, "negative_detD": 0, "min_detM": 0.5, "min_detD": 0.0, "unique_det_triple_count": 3, "coarse_signature_count": 2},
    "2": {"total": 86400, "negative_detM": 0, "negative_detD": 48, "min_detM": 0.0, "min_detD": -1.0, "unique_det_triple_count": 7, "coarse_signature_count": 33},
    "3": {"total": 57600, "negative_detM": 0, "negative_detD": 96, "min_detM": 0.0, "min_detD": -1.0, "unique_det_triple_count": 9, "coarse_signature_count": 21},
    "4": {"total": 14400, "negative_detM": 0, "negative_detD": 48, "min_detM": 0.0, "min_detD": -1.0, "unique_det_triple_count": 11, "coarse_signature_count": 21}
  }
}
```

## Interpretation

The coordinate atlas checks every coordinate rank-two support pair `P,Q` and every principal subset `S` of sizes `1,2,3,4`.  It records the determinant split

```text
det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conjugate(t_S)
```

using the adjugate polynomial identity, so singular `D_S` cases are included.

Findings:

- No coordinate principal minor of `M` was negative at tolerance in any size.
- `D` alone is again confirmed false as a certificate target:
  - size `2`: `48` negative `det(D_S)` cases, minimum `-1.0`;
  - size `3`: `96` negative `det(D_S)` cases, minimum `-1.0`;
  - size `4`: `48` negative `det(D_S)` cases, minimum `-1.0`.
- The trace update repairs all these finite coordinate negative-`D` cases to `det(M_S) >= 0`.
- The number of determinant triples is small on coordinate supports: `3`, `7`, `9`, and `11` by minor size.  This suggests a possible symbolic finite-orbit normal-form exercise for coordinate/equality strata, but does not cover arbitrary Grassmannian frames.

## What this lane rules out

The lane gives another explicit guardrail against any full-PCL proof attempt that first tries to prove `D >= 0`, `det(D_S) >= 0`, or contraction-defect-only positivity.  These fail already on coordinate supports for sizes `2`, `3`, and `4`.

## What remains open

- No universal principal-minor proof for arbitrary complex two-frames.
- No direct Hermitian Gram/SOS certificate for the full `4 x 4` matrix `M`.
- No scalar-to-full-PCL bridge beyond the known quantifier relationships.
- No certified positive-gap rank-two counterexample.

Artifacts:

- `research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py`
- `research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.json`
- `research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.stdout.log`
