# LOOP-0002 Auditor Report

status: completed_fail_closed
claim_focus:
  - `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`
lemma_m_status: refuted_as_stated
claim_0001_status: fail_closed_proof_gap_found_open
last_updated: 2026-06-03

## Executive verdict

Fail closed.

LOOP-0002 refutes the LOOP-0001 bottleneck Lemma M as stated.  The explicit
matrix-unit example in `lemma_m_counterexample.md` satisfies the stated
Hilbert-Schmidt two-frame hypotheses but has `lambda_max(H)=3>2`, so the
operator-matrix assertion `H <= 2 I_2` is false.

This does not refute CLAIM-0001.  The counterexample exploits complex
coefficient directions in a fixed singular-vector gauge.  The original rank-two
SVD reduction uses nonnegative real singular values, with phase freedom in the
singular vectors.  After phase absorption, the same construction gives equality
for the original partial-trace inequality to roundoff rather than a positive
claim gap.

Therefore:

- Lemma M as stated: rejected / refuted.
- Determinant bound `|H_12|^2 <= D_1 D_2` as stated: rejected / refuted.
- CLAIM-0001: remains open, with no accepted proof and no known counterexample
  from LOOP-0002.
- Claim-card status should remain fail-closed, but the localized bottleneck must
  be updated from "Lemma M open" to "Lemma M as stated refuted; replacement
  phase-aware SVD lemma needed".

## Inputs reviewed

Reviewed the required LOOP-0002 artifacts:

1. `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`
2. `research_harness/adversarial_reviews/LOOP-0002/coordinator.md`
3. `research_harness/adversarial_reviews/LOOP-0002/sos_gram_proposer.md`
4. `research_harness/adversarial_reviews/LOOP-0002/determinant_bound_proposer.md`
5. `research_harness/adversarial_reviews/LOOP-0002/lemma_m_counterexample.md`

I also independently reran the exact numerical check for the matrix-unit
counterexample.  It returned:

```text
XGram [[1.+0.j 0.+0.j]
 [0.+0.j 1.+0.j]]
YGram [[1.+0.j 0.+0.j]
 [0.+0.j 1.+0.j]]
t [1.+0.j 0.+1.j]
H [[1.5+0.j  0. -1.5j]
 [0. +1.5j 1.5+0.j ]]
eigH [0. 3.]
D [0.5 0.5] H12sq 2.25 Dprod 0.25 violation 2.0
eigK [-1.  2.]
```

This verifies the advertised violation of `H <= 2I` and of the determinant
form.

## Lemma M audit

The LOOP-0001/LOOP-0002 Lemma M target was:

```text
X_1,X_2,Y_1,Y_2 in M_4(C),
<X_i,X_j>_F = delta_ij,
<Y_i,Y_j>_F = delta_ij,
L_i = X_i Y_i^*,
R_i = X_i^* Y_i,
t_i = tr(X_i^*Y_i),
H_ij = <L_i,L_j>_F + <R_i,R_j>_F - (1/2) overline(t_i)t_j,
H <= 2 I_2.
```

The counterexample is:

```text
X_1 = Y_1 = E_00,
X_2 = E_01,
Y_2 = i E_01.
```

It satisfies the hypotheses and gives:

```text
t = [1, i]
H = [[3/2, -3i/2],
     [3i/2,  3/2]],
eig(H) = [0, 3].
```

Thus `H <= 2I_2` is false.  Equivalently:

```text
D_1 = D_2 = 1/2,
|H_12|^2 = 9/4,
D_1 D_2 = 1/4.
```

So the determinant/off-diagonal form fails by `2`.

Audit status for Lemma M: refuted as stated.  It should no longer be listed as
an open lemma awaiting proof; it is an invalid sufficient lemma.

## CLAIM-0001 audit

The Lemma M refutation does not by itself provide a counterexample to the
rank-two partial-trace inequality.

Reason: the false Lemma M requires positivity of the Hermitian matrix `2I-H`
against arbitrary complex coefficient vectors while keeping a fixed gauge for
`Y_i`.  In the actual rank-two SVD representation

```text
C = s_1 |x_1><y_1| + s_2 |x_2><y_2|,
s_i >= 0,
```

relative phases can be absorbed into the singular vectors.  The matrix `H` is
not invariant under this gauge choice, so the failed complex-coefficient
direction is stronger than what CLAIM-0001 requires.

The counterexample lane reports that the reconstructed rank-two operator has:

```text
rank = 2,
singular values = [1/sqrt(2), 1/sqrt(2)],
claim gap alpha=1/2 = -2.22e-16.
```

This is equality to numerical precision, not a violation.

Audit status for CLAIM-0001: still fail-closed / proof-gap-found / open.  No
proof is accepted, and LOOP-0002 has not produced a counterexample to the claim.

## Audit of proposer lanes

### SOS/Gram proposer

The SOS/Gram lane correctly did not claim a proof.  Its projection identity and
warning that `2I-4P_S` is indefinite are useful, but any proof based on the
refuted `H <= 2I` target is now obsolete unless the target is replaced by a
phase-aware or real-coefficient version.

Status: incomplete, no promotion value for CLAIM-0001.

### Determinant-bound proposer

The determinant-bound lane correctly did not claim a proof and identified that
separate positivity of `I-G^L` and `I-G^R` is false.  LOOP-0002 now goes further:
the full determinant target associated with Lemma M is false as stated.

Status: determinant target refuted as a universal complex-coefficient statement;
no promotion value for CLAIM-0001.

### Counterexample lane

The counterexample lane supplies the decisive LOOP-0002 result.  Its distinction
between refuting Lemma M and refuting CLAIM-0001 is essential and should be
carried into the claim card.

Status: accepted for refuting Lemma M as stated; not accepted as a refutation of
CLAIM-0001.

## Claim-card patch suggestions

Recommended updates to
`research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`:

### 1. Keep status fail-closed but clarify current bottleneck

Replace the current proof-status paragraph:

```text
LOOP-0001 status: proof gap localized to Lemma M. There is no accepted proof of
Lemma M and hence no accepted proof of CLAIM-0001.
```

with:

```text
LOOP-0001 status: proof gap was localized to a proposed two-pair contraction
lemma called Lemma M.

LOOP-0002 status: Lemma M as stated is refuted.  The refutation does not refute
CLAIM-0001, because the false statement controlled arbitrary complex
coefficients in a fixed SVD gauge, whereas the original SVD reduction uses
nonnegative real singular coefficients with phase freedom in the singular
vectors.  Therefore CLAIM-0001 remains open with no accepted proof and no known
counterexample from LOOP-0002.
```

### 2. Update existing evidence section

Append after the LOOP-0001 evidence bullets:

```text
LOOP-0002 evidence:

- The proposed Lemma M / determinant target `H <= 2I_2` is false as stated.
- Exact counterexample: `X_1=Y_1=E_00`, `X_2=E_01`, `Y_2=iE_01`, yielding
  `H=[[3/2,-3i/2],[3i/2,3/2]]` and `eig(H)=[0,3]`.
- This violates the Lemma M bound but, after SVD phase absorption, produces an
  equality case for CLAIM-0001 to numerical precision rather than a positive
  gap.
- The correct replacement target must respect SVD phase gauge and nonnegative
  singular coefficients.
```

### 3. Update open attack surfaces

Replace:

```text
7. Prove or disprove LOOP-0001 Lemma M / determinant bound.
```

with:

```text
7. Formulate and prove/disprove a phase-aware replacement for the refuted
   LOOP-0001 Lemma M / determinant bound, using nonnegative singular
   coefficients and SVD gauge freedom.
8. Search directly for positive `gap(C)` over rank-two `C`, independently of the
   refuted fixed-gauge matrix inequality.
```

### 4. Update adversarial history

Replace:

```text
- LOOP-0001 completed: `research_harness/adversarial_reviews/LOOP-0001/`.
```

with:

```text
- LOOP-0001 completed: `research_harness/adversarial_reviews/LOOP-0001/`.
- LOOP-0002 completed: `research_harness/adversarial_reviews/LOOP-0002/`.
  Lemma M as stated was refuted; CLAIM-0001 remains open/fail-closed.
```

### 5. Update current verdict

Replace:

```text
Fail-closed: central bottleneck remains open in this repository. Current status is
`proof_gap_found`, localized to Lemma M from LOOP-0001.
```

with:

```text
Fail-closed: no accepted proof and no accepted counterexample for CLAIM-0001.
The LOOP-0001 bottleneck Lemma M is no longer merely open; LOOP-0002 refuted it
as stated.  The current proof gap is the absence of a valid phase-aware
rank-two/SVD replacement lemma or an alternative complete proof.
```

## LOOP-0003 recommendation

Start LOOP-0003 with the following focus:

```text
LOOP-0003: Phase-aware rank-two SVD reduction for CLAIM-0001.
```

Recommended lanes:

1. Phase-aware lemma proposer
   - Formulate the exact two-term SVD inequality with `s_1,s_2 >= 0`.
   - Track allowed transformations `y_i -> e^{i theta_i} y_i` and corresponding
     changes to the off-diagonal terms.
   - Replace fixed-gauge `H <= 2I` by the weakest gauge-invariant scalar
     inequality actually needed for CLAIM-0001.

2. Direct rank-two gap optimizer / counterexample hunter
   - Optimize the original `gap(C)` directly over rank-two factorizations, not
     over the refuted Lemma M matrix cone.
   - Include exact reconstruction attempts for any positive numerical gap.

3. Equality-family classifier
   - Analyze the matrix-unit equality families exposed by LOOP-0001 and
     LOOP-0002.
   - Determine whether all sharp cases arise from phase-normalized product or
     traceless diagonal configurations.

4. Skeptic/auditor lane
   - Reject any proof that silently upgrades nonnegative singular coefficients
     to arbitrary complex coefficients.
   - Reject any lemma not invariant under SVD phase gauge unless it explicitly
     fixes a gauge and proves that the fixed gauge is without loss.

Promotion gate for LOOP-0003: do not promote CLAIM-0001 unless there is either
(a) a complete proof of the original rank-two inequality, or (b) a verified
rank-two counterexample with positive original `gap(C)`.  A proof of an
intermediate fixed-gauge matrix inequality is insufficient unless its equivalence
to the original SVD problem is explicitly established.

## Final status assignment

```text
Lemma M as stated: REFUTED.
Determinant form as stated: REFUTED.
CLAIM-0001: FAIL-CLOSED / PROOF-GAP-FOUND / OPEN.
Recommended claim-card status: keep `proof_gap_found`, update narrative to record
that Lemma M was refuted and that a phase-aware replacement is required.
```
