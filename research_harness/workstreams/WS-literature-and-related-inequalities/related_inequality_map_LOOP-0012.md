# LOOP-0012 related-inequality map for CLAIM-0001

Date: 2026-06-03T20:11:48+02:00

Scope: source-backed guardrail map for the rank-two partial-trace inequality

\[
\|\operatorname{tr}_1 C\|_F^2+\|\operatorname{tr}_2 C\|_F^2
\le 2\|C\|_F^2+\tfrac12|\operatorname{tr} C|^2,
\qquad C\in M_4(\mathbb C)\otimes M_4(\mathbb C),\ \operatorname{rank} C\le2.
\]

Here rank is ordinary matrix rank on \(\mathbb C^{4}\otimes\mathbb C^4\); \(C\) is not assumed Hermitian, normal, positive, trace-one, or a channel/CP map. Partial traces are ordinary unnormalized partial traces. Local source for these hypotheses: `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md:34-48`.

## Source availability note

Network access was unavailable in this run (`urllib` to arXiv failed with `No route to host`). The map below therefore distinguishes (a) locally checked repository sources and (b) bibliographic anchors whose exact theorem statements should be verified before import into a final manuscript. No external theorem below is used as a proof of CLAIM-0001.

## A. Partial-trace inequalities

| Result/source pointer | Hypotheses | Relation to CLAIM-0001 | Applicability verdict |
|---|---|---|---|
| Costa Rico--Wolf, *Partial trace relations beyond normal matrices*, arXiv:2507.18278, cited locally in `kronecker_sum_singular_value_note.tex:250-255`. The repository note states that their Eq. (32) gives `||tr_1 C||_F^2+||tr_2 C||_F^2 <= 3||C||_F^2` for rank-two `C` (`kronecker_sum_singular_value_note.tex:218-223`). | As locally recorded: arbitrary rank-two matrices under the same partial-trace/Frobenius conventions; no trace correction. | Gives a rigorous fallback bound leading to the weaker singular-value constant `3/4`, not the desired `1/2` (`kronecker_sum_singular_value_note.tex:224-236`). | Directly relevant but too weak for CLAIM-0001. Verify arXiv source when network is available. |
| Costa Rico--Wolf normal-case statement as locally summarized: the repository note says the corresponding rank-two inequality is open beyond the normal case and connected to two-copy distillability for Werner states (`kronecker_sum_singular_value_note.tex:91-93`; also `problem_statement_aristotle/worked_out_proof.tex:330-332`). | Normal matrices, according to the local summary. | CLAIM-0001 allows arbitrary non-normal `C`. | Not directly applicable as a proof: normality is a stronger assumption excluded by `CLAIM-0001` (`claim card:42-46`). Useful only as evidence/context. |
| Elementary rank-one reshaping inequality in local note (`kronecker_sum_singular_value_note.tex:139-182`). | Arbitrary `Y,Z in M_4(C)`; equivalently rank-one operator `|vec(Y)><vec(Z)|`; uses commuting swaps `(I-F13)(I-F24) >=0`. | Correct rank-one partial-trace control. The note explicitly records that the corrected polarization does not yield the rank-two target (`kronecker_sum_singular_value_note.tex:184-216`). | Directly applicable for rank-one pieces only; insufficient for rank-two because off-diagonal/polarization bookkeeping is the known gap. |

## B. Ordinary rank versus operator-Schmidt rank

| Result/source pointer | Hypotheses | Relation to CLAIM-0001 | Applicability verdict |
|---|---|---|---|
| Correct ordinary-rank SVD reduction in claim card (`CLAIM-0001-rank-two-partial-trace.md:97-100`). | Ordinary matrix rank `<=2`: `C=sum_i s_i |x_i><y_i|`, `i<=2`; reshape vectors `x_i,y_i` into `4x4` matrices `X_i,Y_i`. | Partial traces of each rank-one operator are `tr_2(|x_i><y_i|)=X_iY_i^*` and `tr_1(|x_i><y_i|)=X_i^*Y_i`. This is the safe reduction. | Directly applicable and should replace any operator-Schmidt shortcut. |
| Prior operator-Schmidt-style proof route in `trace_inequality/rank_two_partial_trace_proof.tex:90-96` asserted ordinary rank two gives a two-term operator-Schmidt/tensor-product expansion `C=s_1 A_1⊗B_1+s_2 A_2⊗B_2`. | That assertion is an operator-Schmidt-rank condition, not a consequence of ordinary matrix rank `<=2`. | CLAIM-0001 constrains ordinary rank only. A rank-one ordinary operator `|x><y|` can have operator-Schmidt rank as large as `Schmidt(x) Schmidt(y)`, up to `16` in the `4x4` bipartite setting. | Not applicable; this is the exact confusion to avoid. Use the SVD/reshaping formula instead. |

## C. Singular-value and projection/compression tools

| Result/source pointer | Hypotheses | Relation to CLAIM-0001 | Applicability verdict |
|---|---|---|---|
| Eckart--Young/Mirsky variational principle, as used locally in `kronecker_sum_singular_value_note.tex:128-136`. | Arbitrary complex matrix `X`; top two singular values; maximization over ordinary rank `<=2` matrices of Frobenius norm `1`. | Converts the Kronecker-sum singular-value problem to maximizing against rank-two test matrices `C`, then projects to the Kronecker-sum subspace. | Directly applicable. This is a bridge, not a proof of the missing partial-trace inequality. Bibliographic anchors: Eckart--Young (1936), Mirsky (1960), or Horn--Johnson. |
| Orthogonal projection onto traceless Kronecker-sum subspace `S`, locally derived in `kronecker_sum_singular_value_note.tex:99-126`. | Unnormalized partial traces on `M_4⊗M_4`; subspace `S={A⊗I+I⊗B: tr A=tr B=0}`. | `||P_S(C)||_F^2 = 1/4(||tr_1 C||_F^2+||tr_2 C||_F^2 - 1/2|tr C|^2)`. Thus CLAIM-0001 is exactly the missing estimate needed for the sharp `1/2` singular-value constant. | Directly applicable and locally checked. |
| Projected Compression Lemma (PCL), locally recorded in `CLAIM-0001` loop summaries: `Phi=tr_1^*tr_1+tr_2^*tr_2-(1/2)tr^*tr-2I` should be negative semidefinite on `Hom(QH,PH)` for all rank-two support projections `P,Q` (`CLAIM-0001-rank-two-partial-trace.md:221-230`; full matrix formula at `:244-256`; equivalence audit at `:301-306`). | Universal over all rank-two domain/range support planes in `H=C^4⊗C^4`; arbitrary operators `C=PCQ` in the four-dimensional compression space. | Equivalent reformulation of CLAIM-0001, not an external theorem. | Directly applicable as an exact reformulation. Do not cite it as independent literature. |
| Hermitian compression/interlacing/principal-minor facts. Bibliographic anchors requiring external verification: Horn--Johnson, *Matrix Analysis*; Bhatia, *Matrix Analysis*. | Hermitian matrix/compression. `K<=0` iff every quadratic form is nonpositive; for finite fixed Hermitian matrices PSD can be checked by all principal minors, but tested subsets or special coordinate atlases do not prove universal Grassmannian quantifiers. | Relevant to PCL because each fixed PCL matrix is Hermitian. | Applicable only after forming the exact Hermitian PCL compression matrix for arbitrary support frames. Cannot replace the universal proof by coordinate cases or `D`-only submatrices; local loops found `D`-only routes false (`CLAIM card:283-290`, `:482-487`). |

## D. Quantum-information inequalities and why most are not importable

| Result family/source pointer | Typical hypotheses | Why it does not prove CLAIM-0001 |
|---|---|---|
| Monotonicity/data processing/contractivity of trace distance or relative entropy under partial trace. Bibliographic anchors requiring verification: Nielsen--Chuang; Watrous, *The Theory of Quantum Information*. | Density operators or Hermitian trace-class inputs; completely positive trace-preserving maps; trace norm/relative entropy, not Hilbert-Schmidt squared partial traces of arbitrary matrices. | CLAIM-0001 has arbitrary complex non-Hermitian `C` and uses Hilbert-Schmidt norms of unnormalized partial traces. Positivity, trace one, and CP-channel assumptions are stronger/different and cannot be added. |
| Schatten-norm bounds for partial trace such as `||tr_B X||_2 <= sqrt(dim B)||X||_2`. | Arbitrary matrices can be covered by elementary norm bounds; constants depend on subsystem dimension. | In dimension `4`, this gives only very coarse bounds (e.g. each partial trace may gain factor `sqrt(4)`) and does not exploit rank two or the trace correction. Not enough for CLAIM-0001. |
| Entropic inequalities: subadditivity, strong subadditivity, Araki--Lieb. | Positive semidefinite density matrices with unit trace; von Neumann entropy. | Different object and hypotheses; not about arbitrary rank-two operators or Frobenius partial traces. Not applicable except as high-level context. |
| Positive-map/separability/distillability criteria for Werner states. Local source says Rico--Wolf relate the rank-two inequality to `2`-distillability for Werner states (`kronecker_sum_singular_value_note.tex:91-93`). | Usually density matrices/states, positivity, and often structured symmetry; some criteria quantify Schmidt-rank vectors rather than ordinary-rank operators. | Useful context only. Any theorem phrased for states, positive maps, or Schmidt-rank vectors must be translated before use; it cannot directly prove arbitrary non-Hermitian ordinary-rank `C` inequality. |

## E. Safe report wording

1. The only locally source-backed directly relevant external inequality is the Rico--Wolf weaker rank-two bound as recorded in the repository; it yields the fallback `3/4` singular-value bound, not the target `1/2`.
2. Normal-matrix, positivity/density-matrix, complete-positivity, and operator-Schmidt-rank results have stronger or different hypotheses than CLAIM-0001 and must not be imported as proofs.
3. The safe algebraic bridge is: ordinary-rank SVD/reshaping -> partial-trace formulas -> PAL/PCL exact reformulations. This remains open/fail-closed.
4. The literature search in this run was limited by unavailable network access; external theorem statements beyond local repository source pointers require later verification.
