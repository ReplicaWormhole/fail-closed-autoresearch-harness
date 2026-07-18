# LOOP-0001 Auditor Report

Role: fail-closed auditor.

Inputs checked:

- `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`
- `research_harness/claim_cards/CLAIM-0002-kronecker-weaker-than-bridge.md`
- `research_harness/prompts/auditor_prompt.md`
- `research_harness/adversarial_reviews/LOOP-0001/proposer_factorization.md`
- `research_harness/adversarial_reviews/LOOP-0001/proposer_counterexample.md`
- `research_harness/adversarial_reviews/LOOP-0001/repo_audit.md`
- `research_harness/adversarial_reviews/LOOP-0001/skeptic.md`
- Spot-check source for the bridge/equivalence claim: `partial_trace_inequality_needed_for_sv_bound.tex`

Auditor policy: do not mark an open claim as solved unless a proof survived adversarial review and artifact verification. Numerical evidence, exact sharpness witnesses, and reductions to new unproved lemmas are not proofs of the original claim.

---

```text
claim_id: CLAIM-0001
old_status: conjectural
new_status_recommendation: proof_gap_found
reason: |
  LOOP-0001 produced a useful corrected reduction of the rank-two partial-trace
  inequality to the ordinary-rank SVD/vector-factorization setting, but it did
  not prove the required rank-two interaction inequality. The proposer report
  explicitly leaves Lemma M unproved, and the skeptic identifies Lemma M as the
  first fatal missing step. Therefore CLAIM-0001 is not proved and must not be
  promoted to ready_for_derivation_note, ready_for_formalization, or formalized.

  The recommendation is `proof_gap_found` rather than merely `conjectural`
  because the loop found and localized the precise current proof gap:
  prove the two-pair contraction lemma `H <= 2 I_2`, equivalently the determinant
  bound `|H_12|^2 <= D_1 D_2`, under only the two Hilbert-Schmidt orthonormality
  constraints on the reshaped singular-vector matrices.

  The exact rank-two claim is not refuted. No positive-gap rank-two witness for
  the alpha=1/2 statement was found. Stronger variants are refuted: alpha < 1/2
  at rank 2 and the rank-3 extension at alpha=1/2.
what_was_checked: |
  - Claim card statement, assumptions, non-assumptions, known equality witness,
    and promotion gates.
  - Proposer factorization report: ordinary SVD `C=sum_i s_i |x_i><y_i|`, reshape
    formulas `tr_2(|x><y|)=XY^*`, `tr_1(|x><y|)=X^*Y`, and reduction to Lemma M.
  - Proposer counterexample report: exact family
    `C_r=P_r tensor |0><0| / sqrt(r)`, giving equality at rank 2 for alpha=1/2,
    violations for alpha<1/2, and a rank-3 violation for alpha=1/2.
  - Skeptic report: agrees the SVD setup appears correct but Lemma M is unproved
    and is not a minor detail.
  - Repo audit: old operator-Schmidt proof route is invalid; Aristotle proof is
    circular for the intended theorem; Lean main theorem still has `sorry`.
what_was_not_checked: |
  - No independent proof of Lemma M was supplied or verified.
  - No exhaustive symbolic search or certified global optimization over the
    two-frame parameter space was supplied.
  - No Lean/formal proof artifact for CLAIM-0001 or Lemma M was supplied.
  - The numerical random checks of Lemma M and rank-two `C` were not treated as
    proof.
blocking_gaps: |
  1. Prove or disprove Lemma M:

       Let `X_1,X_2,Y_1,Y_2 in M_4(C)` satisfy
       `<X_i,X_j>_F=delta_ij` and `<Y_i,Y_j>_F=delta_ij`. Define
       `L_i=X_iY_i^*`, `R_i=X_i^*Y_i`, `t_i=tr(X_i^*Y_i)`, and
       `H_ij=<L_i,L_j>_F+<R_i,R_j>_F-(1/2) overline(t_i)t_j`.
       Show `H <= 2 I_2`, or otherwise prove the exact quadratic inequality
       needed for all valid rank-two SVD coefficient vectors.

  2. Any proof must avoid hidden Hermitian, normal, positive-semidefinite,
     convexity, or operator-Schmidt-rank assumptions.

  3. Any promoted proof must account for both known sharp rank-two equality
     families: the traceless diagonal witness and the product-projection witness.
next_loop: |
  - Primary target: Lemma M.
  - Try to produce either:
      (a) a Gram/wedge/sum-of-squares representation of `K=2I-H` under the two
          orthonormality constraints;
      (b) a direct proof of `|H_12|^2 <= D_1D_2`;
      (c) an exact counterexample to Lemma M. If found, test whether it gives a
          valid positive-gap rank-two `C` for CLAIM-0001 or only refutes the
          stronger operator-matrix formulation.
  - Add deterministic regression tests for:
      (a) `(|00><00|-|11><11|)/sqrt(2)`;
      (b) `(P_2 tensor |0><0|)/sqrt(2)`;
      (c) `(P_3 tensor |0><0|)/sqrt(3)` as a forbidden rank-3 extension.
  - Do not reuse the obsolete proof route based on ordinary rank implying
    operator-Schmidt rank two.
claim_card_patch_suggestion: |
  Suggested patch to `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`:

  - Change `status: conjectural` to `status: proof_gap_found`.
  - Under `Existing evidence`, add:

      - LOOP-0001 corrected the ordinary-rank SVD/vector-factorization reduction.
        The claim reduces to an unproved two-pair contraction lemma for reshaped
        singular-vector matrices (`Lemma M` in
        `research_harness/adversarial_reviews/LOOP-0001/proposer_factorization.md`).
      - LOOP-0001 numerical checks of Lemma M found no violation, but this is
        evidence only.
      - LOOP-0001 found exact refutations of stronger variants: coefficient
        `alpha < 1/2` is false at rank 2, and the same alpha=1/2 inequality is
        false at rank 3.

  - Under `Known sharpness/equality witness`, add a second equality family:

      `C=(P_2 tensor |0><0|)/sqrt(2)`, where `P_2=diag(1,1,0,0)`. Then
      `rank(C)=2`, `||C||_F^2=1`, `||tr_1 C||_F^2=2`, `||tr_2 C||_F^2=1`,
      `|tr C|^2=2`, and `gap(C)=0`.

  - Under `Current proof status`, add:

      LOOP-0001 status: proof gap localized to Lemma M. No accepted proof of
      Lemma M, and hence no accepted proof of CLAIM-0001.

  - Under `Open attack surfaces`, add:

      Prove or disprove Lemma M / determinant bound from LOOP-0001.
```

---

```text
claim_id: CLAIM-0002
old_status: conjectural
new_status_recommendation: refuted
reason: |
  As currently written, CLAIM-0002 says the Kronecker-sum singular-value problem
  may require only a restricted/projected version of CLAIM-0001 rather than the
  full rank-two partial-trace inequality for arbitrary rank-two `C`.

  The repository bridge note inspected in this loop,
  `partial_trace_inequality_needed_for_sv_bound.tex`, states and derives the
  opposite under the current formulation: the Kronecker-sum singular-value bound
  is equivalent to the projection estimate for every ordinary rank-two `C`, and
  that projection estimate is algebraically equivalent to the full partial-trace
  inequality CLAIM-0001. In particular, Step 4 runs the implication backward from
  the singular-value bound to the projection estimate for an arbitrary rank-two
  `C` by taking `X=P_S(C)/||P_S(C)||_F`.

  Therefore LOOP-0001 does not support a weaker-image escape hatch. The current
  strategic branch should be retired or rewritten unless a future audit finds an
  error in the bridge equivalence or changes the target theorem/reduction.
what_was_checked: |
  - CLAIM-0002 statement, tasks, and promotion criterion.
  - Repo audit's status map entry for `partial_trace_inequality_needed_for_sv_bound.tex`.
  - The bridge note itself, especially:
      * projection formula for `P_S(C)`;
      * identity equating CLAIM-0001 to the projection estimate;
      * rank-two variational formula for the top two singular values;
      * forward implication PT => Kronecker-sum SV bound;
      * backward implication Kronecker-sum SV bound => projection estimate for
        arbitrary rank-two `C`.
what_was_not_checked: |
  - No independent formalization of the bridge equivalence was checked.
  - No alternative formulation of the Kronecker-sum problem was considered beyond
    the one in the inspected bridge note.
  - No new restricted-image map was proposed in LOOP-0001.
blocking_gaps: |
  - If CLAIM-0002 is to remain alive, it must identify a specific flaw in the
    bridge equivalence or specify a different Kronecker-sum target/reduction.
  - Merely saying the problem "may be weaker" is no longer a supported claim in
    the presence of the current equivalence note.
next_loop: |
  - Do not spend the next loop searching for an unspecified restricted image.
  - Instead, either:
      (a) formalize/audit the bridge equivalence as a stable derivation artifact;
      (b) if someone believes CLAIM-0002 is still viable, require them to point
          to the exact line in the bridge note where the backward implication
          fails; or
      (c) replace CLAIM-0002 with a new precise claim only if a genuinely
          different target theorem or constrained variational class is introduced.
claim_card_patch_suggestion: |
  Suggested patch to `research_harness/claim_cards/CLAIM-0002-kronecker-weaker-than-bridge.md`:

  - Change `status: conjectural` to `status: refuted`.
  - Replace `Current status` with:

      LOOP-0001 audit recommends retiring this claim as currently worded. The
      bridge note `partial_trace_inequality_needed_for_sv_bound.tex` gives an
      equivalence between the Kronecker-sum singular-value bound and the full
      rank-two projection/partial-trace estimate for arbitrary ordinary rank-two
      `C`. No restricted-image formulation was identified.

  - Add `Refutation basis`:

      The backward direction in the bridge note takes an arbitrary rank-two `C`,
      projects it to the traceless Kronecker-sum subspace, and applies the
      Kronecker-sum singular-value bound to recover the projection estimate for
      that same arbitrary `C`. Via the centered partial-trace identity, this is
      exactly CLAIM-0001.

  - Add `Possible replacement`:

      Create a new claim only if a future loop identifies a different target
      inequality, a different variational class, or a verified defect in the
      bridge equivalence.
```

---

## Bottom-line LOOP-0001 auditor verdict

- CLAIM-0001: not proved, not refuted; promote only to `proof_gap_found` because the proof gap is now precisely localized to Lemma M.
- CLAIM-0002: recommend `refuted`/retired as currently worded because the inspected bridge artifact makes the Kronecker-sum target equivalent to the full rank-two projection/partial-trace estimate, not weaker.
- No claim is ready for derivation-note promotion, formalization, or solved status.
