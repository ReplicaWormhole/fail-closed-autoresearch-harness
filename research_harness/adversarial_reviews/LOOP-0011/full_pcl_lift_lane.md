# LOOP-0011 full-PCL lift / Schur-certificate lane

status: completed_fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
lane: lift LOOP-0010 coordinate rank-one-update patterns toward arbitrary-frame full-PCL Schur/Gram certificate
success_condition_met: none

## Executive verdict

No proof or refutation of CLAIM-0001/PCL was obtained.  I failed closed.

The attempted lift did produce a reproducible diagnostic script which probes the full `4 x 4` PCL matrix

```text
M = 2I - A - B + (1/2)T = D + (1/2)conjugate(t)t^T
```

by principal-minor update identities, Schur complements over all nontrivial principal pivots, and all unpivoted LDL/Schur pivot permutations.  The output reinforces the LOOP-0010 warning: the trace rank-one update is structurally necessary, while `D >= 0`, `det(D_S) >= 0`, or any D-only Schur route is invalid.

This lane does not promote the coordinate atlas to a proof over arbitrary Grassmannian two-frames.

## Artifact and run

Created diagnostic script:

```text
research_harness/experiments/LOOP-0011_full_pcl_schur_diagnostics.py
```

Real commands run from repository root:

```text
python3 -m py_compile research_harness/experiments/LOOP-0011_full_pcl_schur_diagnostics.py
python3 research_harness/experiments/LOOP-0011_full_pcl_schur_diagnostics.py --trials 250 --seed 11011 > research_harness/logs/LOOP-0011_full_pcl_schur_diagnostics_seed11011.stdout.log
```

Logs written:

```text
research_harness/logs/LOOP-0011_full_pcl_schur_diagnostics_seed11011.stdout.log
research_harness/logs/LOOP-0011_full_pcl_schur_diagnostics_seed11011.json
```

Stdout summary:

```json
{
  "loop": "LOOP-0011",
  "seed": 11011,
  "trials": 250,
  "negative_min_eig_M": 0,
  "negative_principal_detM_cases": 0,
  "negative_principal_detD_cases": 0,
  "repaired_negative_D_principal_cases": 0,
  "random_min_eig_M_min": 1.1697749192794171,
  "random_min_detM_min_by_size": {
    "1": 1.2643178307437337,
    "2": 1.8030174134343648,
    "3": 2.6684871233818708,
    "4": 3.940048989547342
  },
  "random_min_detD_min_by_size": {
    "1": 1.1360138630142997,
    "2": 1.6088330612392496,
    "3": 2.3544488859003407,
    "4": 3.4721494353828986
  },
  "random_schur_M_negative_splits": 0,
  "random_schur_D_negative_splits": 0,
  "random_pivot_M_negative_sequences": 0,
  "random_pivot_D_negative_sequences": 0,
  "coordinate_negative_min_eig_M": 0,
  "coordinate_negative_min_eig_D": 48,
  "coordinate_negative_detD_by_size": {
    "1": 0,
    "2": 48,
    "3": 96,
    "4": 48
  },
  "coordinate_repaired_negative_D_by_size": {
    "1": 0,
    "2": 48,
    "3": 96,
    "4": 48
  },
  "coordinate_M_schur_negative_splits": 0,
  "coordinate_D_schur_negative_splits": 144,
  "max_update_identity_error": 3.552715515154371e-15,
  "log": "./research_harness/logs/LOOP-0011_full_pcl_schur_diagnostics_seed11011.json"
}
```

## What was tested

The script reconstructs `M` from `D` and the trace vector `t`, rather than accepting a D-only surrogate.  For each case it records:

1. all principal determinant identities

```text
det(M_S) = det(D_S) + (1/2)t_S^T adj(D_S)conjugate(t_S),
```

including singular `D_S` via the adjugate polynomial identity;

2. all Schur complements for principal splits `S | S^c`, for both `M` and `D`, when the pivot block is numerically invertible;

3. all 24 unpivoted one-by-one Schur/LDL pivot orders for `M` and `D`;

4. a finite coordinate Schur scan over all `120 x 120 = 14400` coordinate support pairs, used only as an orbit-pattern diagnostic;

5. 250 Haar/random two-frame pairs with seed `11011`, plus the standard product/diagonal equality controls.

## Findings

### 1. Coordinate Schur/update atlas again rejects D-only certificates

For all coordinate support pairs, no negative eigenvalue of `M` was found and no coordinate principal minor of `M` was negative.  But `D` alone failed in exactly the same principal-minor pattern as LOOP-0010:

```text
negative det(D_S), by |S|: 0, 48, 96, 48
repaired by trace update: 0, 48, 96, 48
coordinate negative min eig(D) pairs: 48
coordinate negative min eig(M) pairs: 0
```

The Schur version gives the same obstruction:

```text
coordinate M Schur negative splits: 0
coordinate D Schur negative splits: 144
```

So any Schur certificate that first proves positivity of `D`, principal minors of `D`, or D-only Schur complements is already false on finite coordinate supports.

### 2. Random arbitrary-frame probes did not find a violation

In 250 random full-frame trials:

```text
negative min eig(M): 0
negative principal det(M_S): 0
random minimum eig(M): 1.1697749192794171
random Schur negative splits for M: 0
random negative unpivoted M pivot sequences: 0
```

These random cases are far from the boundary; in this sample even `D` stayed positive.  Therefore the random run is a sanity check for conventions, not serious evidence of a proof.

### 3. Boundary/equality controls expose why Schur must be trace-coupled

The product equality controls have `min_eig(M)=0` while `min_eig(D)=-1`.  Their principal minors include negative `det(D_S)` at sizes 2, 3, and 4, all repaired to `det(M_S)>=0` by the update.  Their D-Schur complements also go negative while M-Schur complements do not.

This is the strongest local warning from the lane: near equality strata, the certificate cannot be a perturbative or Schur argument for `D`; it must carry the rank-one trace term through every pivot or use an equivalent Gram/SOS object for the full `M`.

### 4. No lifted symbolic Schur/Gram certificate was found

The numerical pivot data suggests the trace-updated `M` behaves well under tested Schur pivots, including coordinate boundary cases, but I did not find a closed-form nonnegative decomposition of the resulting Schur complement entries or determinants for arbitrary complex two-frames.

The coordinate orbit patterns remain useful as regression tests and examples, but they do not constitute a finite normal form for arbitrary support planes.  No scalar-to-full-PCL bridge was established.

## Fail-closed conclusion

This lane does not prove PCL and does not refute CLAIM-0001.  It creates a reproducible LOOP-0011 diagnostic and sharpens the obstruction to false certificate routes:

- reject `D >= 0`;
- reject `det(D_S) >= 0`;
- reject D-only Schur complements;
- do not treat coordinate-support checks as proof over arbitrary frames;
- retain `M = D + (1/2)conjugate(t)t^T` throughout any future Schur/Gram/SOS argument.

Recommended next target: derive symbolic formulas for the trace-coupled Schur complement of `M` under a pivot chosen from a positive diagonal/minor, then attempt a Gram decomposition of that Schur complement directly, without separating off a D-only positive claim.
