# Failed explorations and refuted shortcuts

Failed routes are first-class project artifacts.  They must not be silently retried unless a new hypothesis changes the failure mode.

## F-0001: Fixed-gauge complex-coefficient lemma `H <= 2I`

Status: refuted.

Counterexample:

```text
X_1 = Y_1 = E_00,
X_2 = E_01,
Y_2 = i E_01,
eig(H) = {0, 3}.
```

Lesson: the original SVD problem has nonnegative real singular coefficients and phase freedom.  Do not upgrade it to arbitrary complex fixed-gauge coefficients.

## F-0002: D-only PCL certificate

Status: refuted as a proof route.

Evidence:
- Product/equality controls and coordinate atlases show negative eigenvalues/principal minors for `D`.
- LOOP-0011 found coordinate negative `det(D_S)` counts `48,96,48` for sizes `2,3,4` and `144` negative D-Schur splits.
- LOOP-0012 strengthened this to D-only pivot failure: coordinate support scan had `D_negative_eig_count=48` and `D_no_nonnegative_pivot_order=120`, while trace-coupled `M` had no negative eigenvalue and no no-pivot-order coordinate case.

Lesson: the trace rank-one update is essential.  Proofs must target `M`, not D alone, and Schur/LDL arguments must carry the trace update inside the pivot/complement formula.

## F-0003: Product domination shortcut `D1D2 >= N12N21`

Status: false.

Evidence:
- LOOP-0010 and LOOP-0011 coordinate cases show positive exchange penalty.
- LOOP-0012 coordinate ratio-1/equality signatures show the sharp obstruction: positive `ExchangePenalty` can exactly equal positive `GramSlack`; examples include same row/column identical supports, parallel disjoint translates, and diagonal identical supports.

Lesson: prove exact `GramSlack >= ExchangePenalty`; do not try to eliminate the exchange penalty or prove separated pointwise bounds `D1>=N12`, `D2>=N21`, or `D1D2>=N12N21`.

## F-0004: Coordinate atlas as proof

Status: invalid proof route.

Evidence:
- Coordinate support scans are finite normal-form hints, not proofs over `Gr(2,16) x Gr(2,16)`.

Lesson: coordinate results need an invariant or algebraic lift.

## F-0005: Local tangent evidence as global proof

Status: invalid proof route.

Evidence:
- LOOP-0010/0011 zero-mode classifications are local floating-point Hessian diagnostics.

Lesson: exact equality parametrization and global control are required before using equality geometry in a proof.

## F-0006: Importing arXiv 2507.18278 as a proof of CLAIM-0001

Status: rejected as a proof route after LOOP-0013 source verification.

Evidence:
- LOOP-0013 retrieved Costa Rico--Wolf, `Partial trace relations beyond normal matrices`, arXiv `2507.18278`, and verified source hypotheses in `PTI.tex`.
- The sharp trace-corrected inequality with coefficient `r` is stated for normal rank-`r` matrices; the beyond-normal rank-two case is explicitly open.
- The arbitrary rank-two theorem available from the source gives only the weaker fallback `||tr_1 C||_F^2+||tr_2 C||_F^2 <= 3||C||_F^2`.

Lesson: do not import the normal-matrix theorem, rank-one theorem, Werner-state equivalence, positivity/channel results, or operator-Schmidt-rank variants as proofs of arbitrary complex ordinary-rank-two CLAIM-0001.
