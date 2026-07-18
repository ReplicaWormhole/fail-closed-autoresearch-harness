# LOOP-0010 skeptic review

status: FAIL-CLOSED / REJECT LOOP SUCCESS
claim_focus: CLAIM-0001-rank-two-partial-trace
role: skeptic / adversarial review
reviewed_artifacts:
- `research_harness/adversarial_reviews/LOOP-0010/scalar_trace_coupled_sos_lane.md`
- `research_harness/adversarial_reviews/LOOP-0010/full_pcl_certificate_lane.md`
- `research_harness/adversarial_reviews/LOOP-0010/zero_mode_symbolic_lane.md`
- `research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py`
- `research_harness/experiments/LOOP-0010_full_pcl_coordinate_orbit_atlas.py`
- `research_harness/experiments/LOOP-0010_zero_mode_symbolic_classification.py`
- `research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.stdout.log`
- `research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.json`
- `research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.stdout.log`
- `research_harness/logs/LOOP-0010_full_pcl_coordinate_orbit_atlas.json`
- `research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.stdout.log`
- `research_harness/logs/LOOP-0010_zero_mode_symbolic_classification.json`

## Executive verdict

LOOP-0010 does not prove CLAIM-0001 and must not be promoted.

The loop produced useful fail-closed reductions and guardrails:

1. an exact determinant-level split of the scalar crossed minor into mixed-Gram slack minus exchange penalty;
2. concrete coordinate obstructions to the tempting ansatz `D1 D2 >= N12 N21`;
3. a finite coordinate-support atlas for all principal minors of the full `4 x 4` PCL matrix, showing again that `D` and `det(D_S)` are false proof targets;
4. a local zero-mode classification diagnostic that completely classifies the product-projection numerical zero modes within the tested candidate span but leaves four diagonal-difference zero dimensions unclassified.

None of these is a complete proof, a certified counterexample, or a bridge defect.  The correct adversarial status remains:

```text
LOOP-0010: FAIL-CLOSED
CLAIM-0001: NOT PROVED
COUNTEREXAMPLE: NOT FOUND
PROMOTION: REJECTED
```

## Claim and skeptic standard

Target claim:

```text
rank(C) <= 2 in M_4(C) tensor M_4(C)
  implies

gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2||C||_F^2 - (1/2)|tr C|^2 <= 0.
```

Skeptic standard for LOOP-0010:

- no hidden Hermitian, normal, positive, diagonal, commuting, or real assumptions;
- no promotion of a scalar PAL/crossed-minor result to full PCL or CLAIM-0001 without the missing quantifier bridge;
- no treatment of finite coordinate-support atlases as proofs over `Gr(2,16) x Gr(2,16)`;
- no promotion of local tangent/Hessian evidence to a global inequality;
- no routes relying on `D >= 0`, `det(D_S) >= 0`, or contraction-defect-only positivity after the trace update has been shown essential.

## PASS/FAIL gates

### Gate A: certified rank-two positive-gap counterexample

Status: FAIL.

No LOOP-0010 artifact exports an explicit rank-at-most-two matrix `C` with rigorously certified positive corrected partial-trace gap.  The scalar lane found equality or near-equality scalar determinants only; the PCL coordinate atlas is a finite diagnostic; the zero-mode lane is local tangent classification.  No high-precision, interval, or exact positive-gap certificate appears in the reviewed artifacts.

### Gate B: scalar crossed PAL/PCL determinant proof

Status: FAIL, with surviving bookkeeping and rejected shortcut.

The scalar target is the crossed principal minor

```text
Delta = M_{00} M_{33} - |M_{03}|^2 >= 0.
```

What survives:

- LOOP-0010 records the exact mixed-Plucker determinant bookkeeping identity

```text
m = M_{03} = <W12, W21>,
N12 = ||W12||^2,
N21 = ||W21||^2,
D1 = M_{00},
D2 = M_{33},

Delta = D1 D2 - |m|^2
      = (N12 N21 - |m|^2) - (N12 N21 - D1 D2).
```

- The scalar lane log reports the random mixed offdiagonal / determinant identity residual at roundoff scale, with maximum residual `8.881784197001252e-16` in the lane writeup.

- The finite and numerical probes found no scalar violation: stdout reported `coordinate_min_delta = 0.0`, `random_min_delta = 1.8376015909653387`, and local `min_delta = 3.9613078512756795e-13`.

What does not survive:

- The identity is not a positivity proof.  It merely rewrites the target as

```text
mixed Gram slack >= exchange penalty.
```

- The tempting determinant-level shortcut

```text
D1 D2 >= N12 N21
```

is false on exact coordinate controls.  The scalar lane reports:

```text
coordinate_min_exchange_product_margin = -3.75
coordinate_positive_exchange_penalty_count = 6848
```

and gives exact controls including:

```text
product_LOOP9:   D1D2 = 0.25, N12N21 = 1.0, Delta = 0.0
traceless_LOOP9: D1D2 = 0.25, N12N21 = 4.0, Delta = 0.0
```

In both, nonnegativity is recovered only because the mixed Gram slack exactly cancels the exchange penalty.  Therefore any proof route that uses `D1D2 >= N12N21`, uncoupled mixed-vector norm domination, or an exchange-penalty-free Cauchy argument is rejected.

Skeptic verdict for Gate B: useful scalar reduction, no scalar proof.

### Gate C: scalar PAL/crossed-minor evidence promoted to CLAIM-0001

Status: FAIL.

Even if the scalar crossed determinant were eventually proven, LOOP-0010 does not provide a complete bridge from this scalar slice to the full `4 x 4` PCL PSD condition or directly to CLAIM-0001 with all quantifiers intact.  The current scalar lane is a necessary subtarget/regression, not a complete claim proof.

### Gate D: full PCL principal-minor proof

Status: FAIL, with a useful coordinate guardrail.

The full-PCL lane checks the matrix

```text
M = 2I - A - B + (1/2)T = D + (1/2)conjugate(t)t^T
```

on all coordinate rank-two support pairs and all principal subsets `S` of sizes `1,2,3,4`.  It uses the coupled rank-one-update identity

```text
det(M_S) = det(D_S) + (1/2)t_S^T adj(D_S)conjugate(t_S),
```

which remains polynomially valid even when `D_S` is singular.

What survives from the real run:

```text
max_update_identity_error = 8.881784197001252e-16
size 1: total 57600, negative_detM 0, negative_detD 0,  min_detM 0.5, min_detD 0.0
size 2: total 86400, negative_detM 0, negative_detD 48, min_detM 0.0, min_detD -1.0
size 3: total 57600, negative_detM 0, negative_detD 96, min_detM 0.0, min_detD -1.0
size 4: total 14400, negative_detM 0, negative_detD 48, min_detM 0.0, min_detD -1.0
```

This is useful because it again kills the false routes `D >= 0`, `det(D_S) >= 0`, and any contraction-defect-only argument.  The trace rank-one update is not optional; it repairs coordinate cases where `det(D_S) < 0`.

What does not survive:

- The coordinate-support atlas is finite and highly structured.  It is not a proof over arbitrary complex two-planes in `Gr(2,16) x Gr(2,16)`.
- The absence of negative coordinate principal minors of `M` does not establish full PCL PSD.
- Small coordinate orbit/triple counts suggest possible normal-form work only for coordinate/equality strata, not a universal finite atlas.
- The lane provides no Hermitian Gram/SOS certificate and no all-principal-minor symbolic proof for arbitrary frames.

Skeptic verdict for Gate D: useful finite regression and guardrail, no full PCL proof.

### Gate E: zero-mode/tangent classification as proof

Status: FAIL, with partial local classification.

The zero-mode lane compares numerical Hessian zero eigenspaces at equality controls with explicit candidate tangent directions.  The run reports:

```text
diag_difference:
  zero_count = 9
  positive_count = 0
  all_candidate_contains_zero_space = false
  classified_dim = 5
  unclassified_dim = 4
  max_residual = 0.7071067811865475
  min_principal_cosine = 0.0

product_projection:
  zero_count = 13
  positive_count = 0
  all_candidate_contains_zero_space = true
  classified_dim = 13
  unclassified_dim = 0
  max_residual = 2.220446049250313e-16
  min_principal_cosine = 1.0
```

What survives:

- Product-projection zero modes are numerically contained in the tested phase/product-unitary/equality candidate span to roundoff.
- No positive Hessian directions were found in either control, consistent with prior local evidence.

What does not survive:

- The diagonal-difference control still has four unclassified numerical zero dimensions in this lane.
- The classification depends on floating-point eigenspaces and tolerances.
- Local containment of zero modes does not prove exact local maximality, global equality classification, compactness/patching, or the universal inequality.
- Even a complete local equality classification at the visible controls would not exclude remote positive-gap examples.

Skeptic verdict for Gate E: useful local evidence, not a proof.

## Rejected overclaims and invalid routes

The following promotions are explicitly rejected:

1. `Delta = Gram slack - exchange penalty` proves `Delta >= 0`.
   False.  It identifies the exact remaining inequality but does not prove slack dominates penalty.

2. Mixed Cauchy plus `D1D2 >= N12N21` proves the scalar minor.
   False.  Coordinate controls give margins down to `-3.75`; equality survives only by cancellation.

3. Scalar PAL/crossed-minor success proves full PCL or CLAIM-0001.
   Not established in LOOP-0010.  A scalar slice is not a full fixed-basis `4 x 4` PSD certificate and is not by itself a complete proof of the original claim.

4. Coordinate atlas equals Grassmannian proof.
   False.  Coordinate two-planes are a finite subset, not a cover or quantifier elimination for arbitrary complex two-frames.

5. No negative coordinate principal minors implies full PCL PSD.
   False.  The lane is a regression test and normal-form hint, not a universal principal-minor certificate.

6. `D >= 0`, `D_S >= 0`, or `det(D_S) >= 0`.
   False/rejected.  LOOP-0010 again reports negative `det(D_S)` values for sizes `2`, `3`, and `4`, with minimum `-1.0`, repaired only by the trace update.

7. Trace rank-one update can be dropped, delayed, or treated independently.
   False.  The hard cases require coupled cancellation between the indefinite `D` part and the trace update.

8. Local Hessian or zero-mode classification proves global inequality.
   False.  The zero-mode lane is local and numerical; diagonal-difference remains partially unclassified.

9. Hidden structural assumptions on `C` or the frame matrices.
   Rejected.  CLAIM-0001 is over arbitrary complex rank-at-most-two operators, not Hermitian, normal, positive, diagonal, commuting, or real ones.

## Surviving reductions and useful facts

Accepted as useful but insufficient:

- The scalar crossed determinant can be studied through the exact coupled split

```text
Delta = (N12 N21 - |<W12,W21>|^2) - (N12 N21 - D1D2).
```

- Equality controls show the sharp cancellation pattern that any scalar SOS/Gram proof must encode: positive exchange penalty can be as large as the mixed Gram slack.

- Full PCL principal minors should be attacked with the coupled adjugate/rank-one-update polynomial

```text
det(D_S) + (1/2)t_S^T adj(D_S)conjugate(t_S),
```

not with `det(D_S)` alone.

- Coordinate supports provide exact regression cases and obstruction examples for proposed certificate subclaims.  They do not supply the universal proof.

- Product-projection local zero modes are plausibly explained by explicit symmetry/equality directions in the tested model; diagonal-difference zero modes are not fully classified.

## What remains unproved

- Universal scalar nonnegativity of the crossed determinant `Delta >= 0`.
- A non-circular decomposition proving mixed Gram slack dominates exchange penalty.
- Full `4 x 4` PCL PSD for all complex two-frame support pairs.
- Nonnegativity of all full-PCL principal minors for arbitrary frames.
- A Hermitian Gram/SOS or Schur/principal-minor certificate retaining the trace rank-one update.
- A complete equality-manifold classification plus global patching argument.
- A certified rank-at-most-two positive-gap counterexample.

## Next precise attacks

1. Coupled scalar SOS/Gram attack.
   Target

```text
D1D2 - |<W12,W21>|^2
```

directly on the complex orthonormal frame manifold.  Do not impose the false subclaim `D1D2 >= N12N21`.  Any ansatz must force vanishing on product and traceless equality controls where exchange penalty equals Gram slack.

2. Exchange-penalty sub-slack decomposition.
   Decompose

```text
N12 N21 - D1D2
```

against the actual mixed Gram slack rather than trying to prove it is nonpositive.  The goal is a manifest identity of the form `Gram slack - exchange penalty = SOS + constraints`, not a one-line Cauchy domination.

3. Full principal-minor certificates.
   For every principal subset `S`, prove or refute

```text
det(D_S) + (1/2)t_S^T adj(D_S)conjugate(t_S) >= 0
```

on `Gr(2,16) x Gr(2,16)`.  Start with `2 x 2` minors beyond the crossed scalar block, then move to `3 x 3` and `4 x 4` adjugate patterns.  Keep singular `D_S` cases in the polynomial identity.

4. Coordinate/equality stratum symbolic normal forms.
   The small coordinate determinant-triple counts may be useful for exact equality-stratum classification.  Treat this as a source of candidate null constraints, not as a finite proof of the Grassmannian case.

5. Exact zero-mode classification.
   Replace floating-point zero eigenspaces by exact symbolic tangent kernels.  First close the four unclassified diagonal-difference dimensions; then prove whether the classified directions integrate to equality families.

6. Bridge audit after any scalar success.
   If a scalar PAL/crossed-minor proof is found, separately prove the route to full PCL/CLAIM-0001 with all quantifiers intact.  Do not declare CLAIM-0001 from a scalar minor alone.

7. Counterexample certification route.
   If searches find `gap(C) > 0`, export `C`, verify `rank(C) <= 2`, recompute the corrected partial traces, and certify positivity using high precision, intervals, or exact algebra.  Roundoff-scale positives remain rejected.

## Final skeptic decision

```text
LOOP-0010: FAIL-CLOSED
CLAIM-0001: NOT PROVED
COUNTEREXAMPLE: NOT FOUND
BRIDGE DEFECT: NOT FOUND
PROMOTION: REJECTED
```

LOOP-0010 made real progress in sharpening what a valid proof must look like: the scalar target is a coupled cancellation problem, not a simple mixed Cauchy domination; the full PCL target must retain the trace rank-one update; coordinate atlases and local tangent classifications are diagnostics only.  The claim remains open.
