# LOOP-0006 PCL Structured Counterexample Lane

status: completed_no_counterexample_found
claim_focus: CLAIM-0001-rank-two-partial-trace
pcl_status: no_refutation_found
last_updated: 2026-06-03

## Target

This lane searched for a violation of the PCL compression inequality. For
rank-two support planes `P,Q` in `H=C^4 tensor C^4`, the compression matrix `K`
of

```text
Phi = tr_1^*tr_1 + tr_2^*tr_2 - (1/2)tr^*tr - 2I
```

on `Hom(QH,PH)` should satisfy `K <= 0`. A robust positive `lambda_max(K)` would
produce a rank-at-most-two `C` with positive original gap.

## Executable artifact

Script:

```text
research_harness/experiments/LOOP-0006_pcl_structured_search.py
```

Command actually run after fixing the partial-trace convention:

```text
python3 research_harness/experiments/LOOP-0006_pcl_structured_search.py   --seed 6006   --trials 3000   --opt-restarts 6   --maxiter 150   --out research_harness/logs/LOOP-0006_pcl_structured_seed6006.json   > research_harness/logs/LOOP-0006_pcl_structured_seed6006.stdout.log
```

Logs:

```text
research_harness/logs/LOOP-0006_pcl_structured_seed6006.json
research_harness/logs/LOOP-0006_pcl_structured_seed6006.stdout.log
```

## Important convention check

An initial draft of the script used the wrong Einstein sums for partial traces,
`summing all traced/untraced indices` rather than enforcing equality of the traced
index. That produced spurious positive values even on the product-projection
control. The script was corrected to use

```python
tr_1(C)[a,b] = sum_i C[i,a,i,b]   via np.einsum('iaib->ab', T)
tr_2(C)[i,j] = sum_a C[i,a,j,a]   via np.einsum('iaja->ij', T)
```

All results below are from the corrected run. The corrected controls match prior
LOOP-0005 spectra.

## Searches performed

1. Equality controls.
2. Structured low-dimensional support-plane search over small rectangular
   subsystem supports.
3. Perturbations around product-projection and traceless equality planes with
   `eps=0.01` and `eps=0.1`.
4. SciPy/BFGS optimization over unconstrained parameters projected to two-planes.

## Corrected results

Equality controls:

```text
product projection lambda_max: 0.0
product projection top gap: 0.0
product projection eigenvalues: [-1.0, -1.0, -1.0, 0.0]

traceless diagonal lambda_max: 0.0
traceless diagonal top gap: 0.0
traceless diagonal eigenvalues: [-2.0, -2.0, -1.0, 0.0]
```

Structured support search:

```text
cases: 2592
best lambda_max: -0.24830718408995792
best reconstructed gap: -0.2483071840899591
```

Equality perturbations:

```text
eps=0.01 cases: 3000
best lambda_max: -0.004606073165632001
best reconstructed gap: -0.004606073165631219

eps=0.1 cases: 3000
best lambda_max: -0.3137722327674509
best reconstructed gap: -0.3137722327674515
```

Local optimization:

```text
SciPy available: true
restarts: 6
best lambda_max: -5.20317946714477e-13
best reconstructed gap: -5.198064201294983e-13
eigenvalues: [-2.0, -2.0, -1.3173847052651628, -5.2e-13]
```

Overall:

```text
best overall lambda_max: 0.0
robust_positive: false
```

## Interpretation

No PCL counterexample was found. The structured search adds evidence in three
ways:

- it checks support patterns beyond pure matrix-unit equality cases;
- it probes neighborhoods of known equality families;
- it drives local optimization back to equality-scale negative roundoff rather
  than a positive eigenvalue.

This is still numerical evidence only. It is not a proof of PCL or CLAIM-0001.

## Caveats

- The support-pattern search is finite and not exhaustive over all two-planes.
- BFGS is local and floating-point.
- No rational/interval certificate was attempted because no positive candidate
  was found.

## Next recommendation

Use the corrected structured script as a regression harness for any symbolic PCL
certificate. The most useful next symbolic target remains the crossed `2 x 2`
principal minor identified by the LOOP-0006 symbolic lane, because diagonal
controls and equality perturbations do not expose a counterexample but also do
not prove full PSD.
