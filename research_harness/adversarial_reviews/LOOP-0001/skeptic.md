# LOOP-0001 Skeptic Report for CLAIM-0001

verdict: proof_gap_found

first_problematic_step:
  The current proposer material does not prove CLAIM-0001.  The first missing step in the new factorization route is `proposer_factorization.md`, Section 5, Lemma M: the asserted two-pair contraction lemma `H <= 2 I_2` for arbitrary Hilbert-Schmidt orthonormal two-frames `X_1,X_2` and `Y_1,Y_2` is not proved.  The reduction to Lemma M appears to use the correct ordinary-rank SVD setup, but Lemma M is exactly the hard inequality and remains an unverified finite-dimensional conjectural subclaim.

missing_or_false_lemma:
  Missing lemma: for arbitrary `X_1,X_2,Y_1,Y_2 in M_4(C)` satisfying only
  `<X_i,X_j>_F = delta_ij` and `<Y_i,Y_j>_F = delta_ij`, with
  `L_i=X_iY_i^*`, `R_i=X_i^*Y_i`, `t_i=tr(X_i^*Y_i)`, one must prove
  `H_{ij}=<L_i,L_j>_F+<R_i,R_j>_F-(1/2) overline{t_i}t_j <= 2 I_2`.
  Equivalently, after the diagonal estimates, one must prove the determinant/off-diagonal inequality
  `|H_12|^2 <= D_1 D_2`, where
  `D_i=2-||L_i||_F^2-||R_i||_F^2+(1/2)|t_i|^2`.
  No proof of this inequality is supplied, and the numerical sampling reported by the proposer is evidence only.

repair_suggestion:
  Do not promote CLAIM-0001.  A repair must provide an actual proof of Lemma M or replace it with a weaker lemma sufficient for all ordinary rank-two SVD coefficient vectors.  The proof must explicitly use only the two orthonormality constraints on the reshaped singular-vector matrices and must not import positivity, Hermiticity, normality, convexity of the rank constraint, or operator-Schmidt-rank assumptions.  A credible next artifact would be either:
  1. a Gram/wedge/sum-of-squares representation of `K=2I-H` under the stated constraints; or
  2. a direct proof of `|H_12|^2 <= D_1D_2`; or
  3. a counterexample to Lemma M, which would either refute this proof route or possibly refute CLAIM-0001 if it corresponds to valid SVD data and coefficients.

constants/equality_check:
  The constants and tensor-index conventions pass the basic equality checks.  I verified with the repository convention `tr_1(A tensor B)=tr(A)B`, `tr_2(A tensor B)=tr(B)A` that
  `C=(|00><00|-|11><11|)/sqrt(2)` has rank 2, `||C||_F^2=1`, `|tr C|^2=0`, both partial-trace squared norms equal `1`, and gap `0`.
  I also verified the proposer-counterexample family `C_r=P_r tensor |0><0| / sqrt(r)`: for `r=2` it is another equality case at coefficient `1/2`, while for `r=3` it violates the rank-three extension with gap `1/2`.  Thus the coefficient `1/2` and the rank-two restriction are both sharp against natural stronger variants.

next_required_artifact:
  A proof or disproof of Lemma M, with exact algebra and no hidden structural assumptions.  Numerical checks may remain as regression tests but cannot close the proof gap.

## Scope and inputs checked

I reviewed the required claim card, skeptic prompt, proposer factorization report, proposer stronger-variant/counterexample report, and repo audit:

- `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`
- `research_harness/prompts/skeptic_prompt.md`
- `research_harness/adversarial_reviews/LOOP-0001/proposer_factorization.md`
- `research_harness/adversarial_reviews/LOOP-0001/proposer_counterexample.md`
- `research_harness/adversarial_reviews/LOOP-0001/repo_audit.md`

I also spot-checked the repo files singled out by the audit where the claimed proof failures occur:

- `trace_inequality/rank_two_partial_trace_proof.tex`
- `problem_statement_aristotle/partial_trace_rank2_inequality.tex`
- `partial_trace_inequality_needed_for_sv_bound.tex`

## Skeptical assessment of the proposer factorization route

### What appears correct

The ordinary-rank SVD starting point is the right one:

`C = sum_i s_i |x_i><y_i|`, `r <= 2`, with orthonormal vector families `x_i,y_i in C^4 tensor C^4`.

Under the reshape convention `x_i <-> X_i in M_4(C)`, the partial-trace formulas are consistent:

- `tr_2(|x><y|)=X Y^*`
- `tr_1(|x><y|)=X^* Y`
- `tr(|x><y|)=tr(X^*Y)`

Thus for `L_i=X_iY_i^*`, `R_i=X_i^*Y_i`, `t_i=tr(X_i^*Y_i)`, the target inequality becomes the quadratic inequality

`||sum_i s_i L_i||_F^2 + ||sum_i s_i R_i||_F^2 <= 2 sum_i s_i^2 + (1/2)|sum_i s_i t_i|^2`.

The diagonal `r=1` bound also appears valid by submultiplicativity/Frobenius estimates.

### First gap

The route stops at Lemma M.  Lemma M is not a minor technicality: it is precisely the off-diagonal rank-two interaction.  In determinant form it requires

`| <L_1,L_2>_F + <R_1,R_2>_F - (1/2) overline{t_1}t_2 |^2 <= D_1D_2`.

This is not established by the individual bounds `||L_i||_F <= 1`, `||R_i||_F <= 1`; those bounds only control the diagonal entries.  The missing part is the correlation between the two contraction channels `X_iY_i^*` and `X_i^*Y_i`, minus the trace correction, under the cross-orthogonality constraints on the `X` frame and the `Y` frame.

### Caution about “equivalent” strengthening

The report states that `H <= 2I_r` is a robust sufficient and essentially equivalent target because phases can be varied.  This is plausible as a proof target, but it should be justified carefully if used as an equivalence.  The actual SVD has nonnegative singular values; coefficient phases are absorbed into singular-vector choices and consequently change the associated `Y_i`, `L_i`, `R_i`, and `t_i`.  This does not invalidate the reduction, but a final proof should state explicitly whether it proves the full operator inequality `H <= 2I_2` or only the quadratic inequality needed for all valid rank-two summands and coefficient phases.

## Skeptical assessment of proposer counterexample report

The stronger-variant counterexamples are consistent and useful guardrails.

For `C_r=P_r tensor E_00 / sqrt(r)`, with `P_r=diag(1,...,1,0,...)`, the report's formulas check out:

- rank `r`
- `||C_r||_F^2=1`
- `||tr_1 C_r||_F^2=r`
- `||tr_2 C_r||_F^2=1`
- `|tr C_r|^2=r`
- `gap_alpha(C_r)=r(1-alpha)-1`

Consequences are correct:

- `r=2`, `alpha=1/2`: equality.
- `r=2`, any `alpha<1/2`: positive gap, so smaller trace coefficient is false.
- `r=3`, `alpha=1/2`: positive gap `1/2`, so the rank-three extension is false.

These witnesses do not refute CLAIM-0001.  Instead, they show that any proof must hit the exact rank-two/rhs constants and cannot silently prove common stronger variants.

## Skeptical assessment of repo audit

The repo audit's bottom-line classification is fail-closed and is supported by the inspected files.

### Invalid old proof: ordinary rank does not imply operator-Schmidt rank two

In `trace_inequality/rank_two_partial_trace_proof.tex`, Step 1 asserts that ordinary matrix rank `<=2` gives a two-term operator-Schmidt decomposition

`C=s_1 A_1 tensor B_1 + s_2 A_2 tensor B_2`.

This implication is false.  Ordinary operator rank on `C^4 tensor C^4` and operator-Schmidt rank as an element of `M_4 tensor M_4` are different notions.  A concrete rank-one ordinary operator can already have high operator-Schmidt rank: if

`x=(1/2) sum_{i=0}^3 e_i tensor f_i`,

then

`|x><x|=(1/4) sum_{i,j=0}^3 |i><j| tensor |i><j|`,

which has 16 orthogonal elementary tensor terms in its operator-Schmidt expansion while its ordinary matrix rank is 1.  Hence the first step of that proof is invalid for CLAIM-0001.

There is an additional independent problem later in the same proof: the scalar step `a+b <= 2+ab` for all `a,b in [0,4]` is false, e.g. `a=4,b=0` gives `4 <= 2`.  Moreover, the use of an upper bound on the positive trace term cannot by itself prove the desired inequality with the smaller actual trace term.  But the proof already fails at Step 1.

### Circular Aristotle proof

In `problem_statement_aristotle/partial_trace_rank2_inequality.tex`, the proof invokes the Kronecker-sum singular-value bound

`s_1(W)^2+s_2(W)^2 <= (1/2)||W||_F^2`

for all traceless Kronecker sums `W`.  The bridge file `partial_trace_inequality_needed_for_sv_bound.tex` identifies this singular-value bound as equivalent to the rank-two partial-trace inequality/projection estimate.  Therefore this is not an independent proof of CLAIM-0001; it is circular if used to establish the missing bridge.

## Verification run

I ran a direct Python check of the two key equality/variant witnesses under the stated tensor convention.  The run returned:

```text
traceless equality: rank 2, norm2 ~ 1, pt1 ~ 1, pt2 ~ 1, trace_abs2 0, gap 0
P_2 tensor E00/sqrt(2): rank 2, norm2 ~ 1, pt1 ~ 2, pt2 ~ 1, trace_abs2 ~ 2, gap_{1/2} ~ 0
P_3 tensor E00/sqrt(3): rank 3, norm2 ~ 1, pt1 ~ 3, pt2 ~ 1, trace_abs2 ~ 3, gap_{1/2} ~ 0.5
```

This confirms convention consistency and the sharpness/refutation claims for the tested witnesses.  It does not prove CLAIM-0001.

## Final fail-closed conclusion

CLAIM-0001 must remain conjectural.  The new proposer report is valuable because it replaces the false operator-Schmidt route with the correct ordinary-rank SVD/vector-factorization route, but it merely reduces the theorem to Lemma M.  Since Lemma M is unproved and is exactly the nontrivial rank-two interaction, there is no complete proof to promote.
