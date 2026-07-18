# LOOP-0002 Coordinator Report

status: completed
claim_focus:
  - `CLAIM-0001-rank-two-partial-trace.md`

## Goal

Attack the LOOP-0001 bottleneck Lemma M for the rank-two partial-trace inequality.

## Artifacts produced

- `sos_gram_proposer.md`
- `determinant_bound_proposer.md`
- `lemma_m_counterexample.md`
- `skeptic.md`
- `auditor.md`

Numerical/exact-search artifacts:

- `research_harness/logs/loop_0002_lemma_m_search.py`
- `research_harness/logs/loop_0002_lemma_m_search_seed2002.json`
- `research_harness/logs/loop_0002_lemma_m_search_seed2002.stdout.log`
- `research_harness/logs/loop_0002_smoke.json`
- `research_harness/logs/loop_0002_smoke.stdout.log`

## Main result

LOOP-0002 refuted Lemma M as stated.

The exact counterexample is

```text
X_1 = Y_1 = E_00,
X_2 = E_01,
Y_2 = i E_01.
```

These satisfy the Hilbert-Schmidt two-frame hypotheses. For

```text
L_i = X_iY_i^*,
R_i = X_i^*Y_i,
t_i = tr(X_i^*Y_i),
H_ij = <L_i,L_j>_F + <R_i,R_j>_F - (1/2) overline(t_i)t_j,
```

the verified values are

```text
t = [1, i]
H = [[3/2, -3i/2],
     [3i/2,  3/2]]
eig(H) = [0, 3]
```

So `H <= 2I_2` is false. Equivalently,

```text
D = [1/2, 1/2]
|H_12|^2 = 9/4
D_1D_2 = 1/4
|H_12|^2 - D_1D_2 = 2
```

## Does this refute CLAIM-0001?

No.

The refuted Lemma M controlled arbitrary complex coefficient vectors in a fixed singular-vector gauge. The original rank-two SVD problem uses nonnegative real singular coefficients and permits phase absorption into singular vectors. After phase absorption, the associated rank-two operator gives equality for CLAIM-0001 to numerical precision:

```text
rank = 2
singular values = [1/sqrt(2), 1/sqrt(2)]
claim gap alpha=1/2 = -2.22e-16
```

Therefore CLAIM-0001 remains fail-closed/open: no accepted proof and no accepted counterexample.

## Lane outcomes

### SOS/Gram proposer

No complete proof. The lane produced useful reformulations and correctly noted that ambient projection positivity is indefinite, but any proof based on fixed-gauge `H <= 2I` is obsolete because that target is false.

### Determinant-bound proposer

No complete proof. The natural separated Cauchy-Schwarz route fails because individual defect kernels are not PSD. LOOP-0002 further shows the full fixed-gauge determinant target is false.

### Counterexample hunter

Decisive for the loop. Refuted Lemma M as stated, while preserving the distinction from CLAIM-0001.

### Skeptic/auditor

Both independently verified the counterexample and agreed:

- Lemma M as stated: refuted.
- Determinant bound as stated: refuted.
- CLAIM-0001: still open / proof_gap_found.

## Claim-card updates applied

`research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md` was updated to record:

- Lemma M as stated was refuted in LOOP-0002.
- The refutation does not refute CLAIM-0001.
- The current proof gap is now a phase-aware rank-two/SVD replacement lemma or an alternative complete proof.
- Open attack surfaces now include direct rank-two gap search independent of the refuted fixed-gauge matrix inequality.

## LOOP-0003 recommendation

Run LOOP-0003 on a corrected phase-aware SVD target.

Recommended lanes:

1. Phase-aware lemma proposer
   - Formulate the exact two-term SVD inequality with `s_1,s_2 >= 0`.
   - Track `y_i -> e^{i theta_i} y_i` gauge freedom.
   - Replace `H <= 2I` by the weakest scalar/gauge-invariant inequality actually needed.

2. Direct rank-two gap optimizer
   - Optimize original `gap(C)` directly over rank-two factorizations.
   - Avoid using Lemma M as an objective except as a diagnostic.
   - Attempt exact reconstruction for any positive gap.

3. Equality-family classifier
   - Analyze equality families from LOOP-0001 and LOOP-0002.
   - Determine whether sharp cases are product-projection, traceless diagonal, or part of a larger phase-normalized family.

4. Skeptic/auditor
   - Reject any proof that silently upgrades nonnegative singular coefficients to arbitrary complex coefficients.
   - Reject any fixed-gauge lemma unless equivalence to the original SVD problem is proved.

## Coordinator verdict

LOOP-0002 made negative but important progress: it killed the overstrong Lemma M bottleneck and exposed the missing phase-gauge issue. The problem remains open, but the next loop is sharper: formulate and attack the correct phase-aware rank-two SVD inequality.
