# Uncertainty ledger

This ledger tracks unresolved mathematical uncertainty. It is not a task list; it is the map of what the workspace does not yet know.

## U-0001: Scalar slack domination

Claim: `GramSlack >= ExchangePenalty` for the scalar crossed PAL/PCL minor.

Status: unresolved; sharpened through LOOP-0013.

Evidence for:
- Coordinate equality controls in LOOP-0011 had `Delta >= 0` with sharp ratio `ExchangePenalty/GramSlack = 1`.
- LOOP-0012 re-ran scalar diagnostics with seed `12012`; no scalar violation was found, local search approached equality (`local_min_delta≈6.63e-12`, ratio `≈0.9999999898468404`).
- LOOP-0012 organized coordinate ratio-1/equality cases into three exact finite support signatures.
- LOOP-0013 promoted these signatures into exact restricted parametrized row/column/diagonal equality families with `Delta=0` and `GramSlack=ExchangePenalty>0` (constants `3/4`, `3`, `15/4` in representative charts).

Evidence against / danger:
- Natural shortcuts `D1D2>=N12N21`, `N12<=D1`, and `N21<=D2` are false.
- Explicit LOOP-0013 equality families have positive `GramSlack` exactly matched by positive `ExchangePenalty`; a proof must explain cancellation, not separated positivity.
- Restricted equality charts are not a universal certificate on the full two-frame Grassmannian.

Needed to resolve:
- Symbolic mixed Plucker/Gram/SOS certificate proving `GramSlack >= ExchangePenalty` with the exchange term retained, or explicit scalar violation converted back to original gap context.

Blocking workstreams: `WS-scalar-slack`, `WS-full-pcl-certificate`.

## U-0002: Full PCL certificate

Claim: The full `4 x 4` trace-coupled PCL matrix `M` is PSD for all rank-two support projections.

Status: unresolved; trace-coupled determinant/Schur target sharpened in LOOP-0013.

Evidence for:
- Coordinate and random diagnostics found no negative `M` eigenvalue/principal minor.
- LOOP-0012 coordinate scan over `14400` support-pair cases had `M_negative_eig_count=0` and `M_no_nonnegative_pivot_order=0`; 300 random full-frame trials had no negative `M` eigenvalue.
- LOOP-0013 coordinate scan again had `coordinate_M_negative_eig_count=0` and `coordinate_M_no_nonnegative_pivot_order_count=0`; 500 random trials had no negative `M` eigenvalue.
- LOOP-0013 separated the valid determinant identity `det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S)` from the missing nonnegativity proof.

Evidence against / danger:
- D-only principal-minor, pivot, and Schur routes are false; LOOP-0012 and LOOP-0013 again found coordinate D failures (`D_negative_eig_count=48`, `D_no_nonnegative_pivot_order_count=120`).
- Scalar crossed-minor positivity is insufficient for full PSD.
- The determinant-update identity is algebraic bookkeeping, not a PSD certificate.

Needed to resolve:
- Direct trace-coupled Gram/SOS/Schur/rank-one-update certificate for `M`, especially proving `det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S)>=0` for every principal subset `S`, or a certified negative eigenvector converted to a rank-two positive original gap.

Blocking workstreams: `WS-full-pcl-certificate`.

## U-0003: Equality families

Claim: The visible product-projection and traceless two-product-atom controls may generate the relevant equality manifolds.

Status: reduced but unresolved.

Evidence for:
- LOOP-0010 classified product-projection zero modes locally.
- LOOP-0011 classified diagonal-difference zero modes locally using expanded active support-plane directions.
- LOOP-0012 organized coordinate ratio-1/equality cases into three finite signatures.
- LOOP-0013 promoted those signatures into exact restricted parametrized families, no longer just isolated coordinate points.

Evidence against / danger:
- Local Hessian zero modes, coordinate support enumeration, and restricted chart families do not prove a global equality classification.
- Equality classification alone does not prove the inequality.

Needed to resolve:
- Exact global parametrized equality families and a proof that no other zero/unstable mechanisms matter in the chosen proof route.

Blocking workstreams: `WS-equality-geometry`.

## U-0004: Literature transfer

Claim: Existing singular-value, partial-trace, or quantum-information inequalities may contain a usable certificate or normal form.

Status: network/source uncertainty substantially reduced in LOOP-0013; no proof transfer found.

Evidence:
- LOOP-0013 retrieved arXiv `2507.18278` and stored source/e-print copies.
- The source verifies the sharp trace-corrected rank-`r` inequality only for normal matrices and explicitly treats the beyond-normal rank-two case as open.
- The source-backed arbitrary-rank-two result gives only the weaker `||tr_1 C||_F^2+||tr_2 C||_F^2 <= 3||C||_F^2` bound.

Needed to resolve:
- If literature work continues, search beyond arXiv `2507.18278` for exact arbitrary non-Hermitian ordinary-rank-two hypotheses; otherwise use the verified source only as guardrail/context.
- Continue avoiding normality, positivity, density-matrix, complete-positivity, and operator-Schmidt-rank assumptions unless an explicit reduction is proved.

Blocking workstreams: `WS-literature-and-related-inequalities`.
