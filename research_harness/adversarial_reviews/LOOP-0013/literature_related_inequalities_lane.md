# LOOP-0013 literature-and-related-inequalities lane

Date: 2026-06-03T21:00:55+02:00

Workstream: `WS-literature-and-related-inequalities`  
Claim under review: `CLAIM-0001-rank-two-partial-trace`

## Scope and guardrail

CLAIM-0001 is the rank-two partial-trace inequality

\[
\|\operatorname{tr}_1 C\|_F^2+\|\operatorname{tr}_2 C\|_F^2
\le 2\|C\|_F^2+\tfrac12 |\operatorname{tr}C|^2,
\qquad C\in M_4(\mathbb C)\otimes M_4(\mathbb C),\ \operatorname{rank}C\le2.
\]

The admissible hypotheses are ordinary matrix rank `<=2` on the `16 x 16` matrix `C`, arbitrary complex entries, no Hermitian/normal/positive/density/channel assumption, and no operator-Schmidt-rank assumption. Partial traces are the usual unnormalized partial traces and the norm is Frobenius/Schatten-2.

This lane retries the LOOP-0012 external-source verification failure for arXiv `2507.18278` and checks whether any related inequality can be imported without exceeding those hypotheses.

## External retrieval and durable source record

Network retry succeeded.

- arXiv abs page `https://arxiv.org/abs/2507.18278`: HTTP 200; title `Partial trace relations beyond normal matrices`; authors Pablo Costa Rico and Michael M. Wolf; submitted 24 Jul 2025.
- arXiv e-print `https://arxiv.org/e-print/2507.18278`: HTTP 200; source archive extracted.
- Durable local source copy: `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex`.
- Durable local e-print copy: `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/2507.18278.eprint`.
- SHA256:
  - `2507.18278.eprint`: `3dcb51d22a3b7596c9c78f881041e3cf1f77e1dfac858ab3a7b40f6fcd1ab2c8`
  - `PTI.tex`: `38f576f8f5f82552a8f68d572855bdbe0c6fe465be841af1c8b6ed6208dce077`

## Source-backed exact findings from arXiv 2507.18278

Line references below are to `research_harness/adversarial_reviews/LOOP-0013/external_sources/arxiv_2507_18278/PTI.tex`.

### 1. The source explicitly treats general matrices, but its sharp trace-corrected rank-two inequality is stated as open beyond normal matrices

The introduction says the paper deliberately considers general matrices rather than restricting to positive or normal matrices, with rank as an occasional constraint (`PTI.tex:150`). It recalls the prior normal-matrix inequality

\[
\|\operatorname{Tr}_A[M]\|_2^2+\|\operatorname{Tr}_B[M]\|_2^2
\le r\|M\|_2^2+\frac1r|\operatorname{tr}M|^2
\]

for all normal matrices `M` of rank `r` (`PTI.tex:163-169`). The paper then states that whether this equation also holds beyond normal matrices is an open problem, especially for `r=2`, equivalent to the two-copy distillability problem for Werner states (`PTI.tex:171`).

**Applicability to CLAIM-0001:** not importable as a proof. For `r=2` the displayed normal-matrix inequality is exactly the CLAIM-0001 shape, but the source says the beyond-normal case is open. CLAIM-0001 permits arbitrary non-normal complex rank-two matrices.

### 2. The source proves a rank-two/general-rank Schatten-2 fallback bound, but it is too weak

Corollary `\ref{cor:AudenR}` states: if `M in M_{d_1 \otimes ... \otimes d_n}` has rank `r` and partial traces `M_i`, then for all `p in [1,\infty]` and `\gamma >= 1`,

\[
\sum_i \|M_i\|_p^\gamma
\le \left(1+r^{\gamma(1-1/p)}(n-1)\right)\|M\|_p^\gamma.
\]

This is in `PTI.tex:468-472`, with proof in `PTI.tex:474-479`. The Werner-application section specializes `n=r=p=\gamma=2` and records

\[
\|M_A\|_2^2+\|M_B\|_2^2\le 3\|M\|_2^2
\]

at `PTI.tex:533-536`.

**Applicability to CLAIM-0001:** source-backed and directly applicable to arbitrary rank-two complex matrices, but too weak. CLAIM-0001 requires

\[
\|M_A\|_2^2+\|M_B\|_2^2\le2\|M\|_2^2+\tfrac12|\operatorname{tr}M|^2,
\]

which can be strictly below `3||M||_2^2`, especially when `tr M = 0`. This theorem cannot close CLAIM-0001 or the sharp `1/2` Kronecker-sum singular-value bound.

### 3. The source proves the rank-one trace-corrected Schatten-2 inequality, but rank-one does not cover rank two

A proposition at `PTI.tex:506-511` states that if `M` has rank one and partial traces `A,B`, then for any `\gamma >= 2`,

\[
\|A\|_2^\gamma+\|B\|_2^\gamma\le \|M\|_2^\gamma+|\operatorname{tr}M|^\gamma.
\]

For `\gamma=2`, this is a strong trace-corrected rank-one relation, proved by a flip-positivity argument in `PTI.tex:512-521`.

**Applicability to CLAIM-0001:** not enough. CLAIM-0001 is rank `<=2`; the obstruction in the local repository is exactly the rank-two cross-term/polarization bookkeeping. A rank-one theorem may be cited as context and as a local consistency check, not as a proof of CLAIM-0001.

### 4. The source contains an ordinary-rank dilation result; it does not imply CLAIM-0001

Proposition `\ref{prop:rank2dilation}` says that for any two matrices `A,B in M_d` there exists a rank-two `M in M_{d\otimes d}` with partial traces `tr_A[M]=B` and `tr_B[M]=A` iff `tr A = tr B` (`PTI.tex:270-279`).

**Applicability to CLAIM-0001:** useful guardrail only. It confirms ordinary rank two is broad enough to realize arbitrary same-trace marginals; it does not give a Frobenius norm lower bound on the dilation and cannot prove the target inequality.

### 5. The source uses ordinary rank, not an operator-Schmidt-rank substitute, in its relevant statements

The rank and partial-trace conventions are ordinary matrix conventions. Rank-one partial traces are represented by rectangular matrices `X_i` with formulas `tr_A[M]=(X_2^*X_1)^T` and `tr_B[M]=X_1X_2^*` (`PTI.tex:244-252`). Rank-two dilation uses a sum of two such rank-one terms in equations `PTI.tex:275-279`.

**Applicability to CLAIM-0001:** compatible with the CLAIM-0001 ordinary-rank guardrail, but no theorem in the source supplies the missing rank-two trace-corrected inequality for arbitrary non-normal matrices.

## Related inequality families checked against exact hypotheses

| Family / theorem | Exact source-backed or local hypotheses | Relation to CLAIM-0001 | Import verdict |
|---|---|---|---|
| Rico--Wolf normal rank-`r` trace-corrected inequality | Normal matrices of rank `r`; Schatten/Frobenius 2; partial traces (`PTI.tex:163-171`). | For `r=2` has the same algebraic shape as CLAIM-0001. | **Do not import as proof**: normality exceeds CLAIM-0001 and source says non-normal case is open. |
| Rico--Wolf / extended Audenaert low-rank bound | Arbitrary matrix of rank `r`; all Schatten `p`; all `gamma>=1`; `n` tensor factors (`PTI.tex:468-472`). | Specializes to `||M_A||_2^2+||M_B||_2^2 <= 3||M||_2^2` for `n=r=p=gamma=2` (`PTI.tex:533-536`). | **Import only as weaker fallback/context**; too weak for CLAIM-0001. |
| Rico--Wolf rank-one trace-corrected relation | Rank-one `M`; partial traces `A,B`; `gamma>=2` (`PTI.tex:506-511`). | Strong for rank one; mirrors local rank-one flip argument. | **Do not import as rank-two proof**; rank-one hypothesis is too restrictive. |
| Kronecker-sum majorization | General matrices `C_i`; weak submajorization of singular values of Kronecker sums (`PTI.tex:364-369`). | Underlies their norm-template theorem. | **Context/tool only**; does not yield the exact trace-corrected rank-two bound. |
| Quantum-information Werner distillability criterion | Rank-two `M in M_{d\otimes d}`; Werner state parameter `alpha`; inequality `PTI.tex:529-532`. | Shows the sharp trace-corrected family is equivalent to a known open distillability boundary. | **Do not import as proof**; it is an equivalence/application, and source only extends to `alpha >= -1/3` via the weaker `3||M||^2` bound. |
| Data processing, entropy, trace-distance contractivity | Density/positive/Hermitian states, channels, trace norm or entropy. | Different norms and positivity/CP hypotheses. | **Not applicable** to arbitrary complex non-Hermitian ordinary-rank-two `C`. |
| Matrix-analysis compression/interlacing/PSD tests | Fixed Hermitian matrices/compressions; require exact compression for every support pair. | Relevant to PCL reformulation. | **Not independent literature proof**; at most verification machinery for a derived PCL certificate. |

## Consequence for the local Kronecker-sum bridge

The local bridge remains valid as a reduction/guardrail: Eckart--Young/Mirsky converts the top-two singular-value problem to rank-two test matrices, and the projection formula onto the traceless Kronecker-sum subspace converts the desired sharp constant into CLAIM-0001. However, the source-backed external result available from arXiv `2507.18278` supplies only the fallback

\[
\|\operatorname{tr}_1 C\|_F^2+\|\operatorname{tr}_2 C\|_F^2\le 3\|C\|_F^2
\]

for rank-two arbitrary `C`; it does not supply the needed trace-corrected coefficient `2` plus `1/2 |tr C|^2`.

## Verdict

**Fail-closed / no theorem imported as a proof of CLAIM-0001.**

External verification succeeded and resolved the LOOP-0012 network uncertainty for arXiv `2507.18278`. The exact source hypotheses confirm:

1. the sharp trace-corrected inequality in CLAIM-0001 is known/proved in the cited line only for **normal** matrices;
2. the source explicitly calls the beyond-normal rank-two case open;
3. the source-backed arbitrary-rank-two theorem gives only the weaker constant `3` bound;
4. rank-one and quantum-information results are useful context but have hypotheses that do not cover arbitrary non-Hermitian ordinary-rank-two `C`.

Therefore U-0004 is materially advanced but not closed as a route to success: no source-backed external theorem proves CLAIM-0001, and no bridge defect accepted by an auditor was found in this lane.
