# LOOP-0003 Skeptic Report

status: fail_closed
claim_focus: CLAIM-0001-rank-two-partial-trace
reviewed:
  - research_harness/adversarial_reviews/LOOP-0003/phase_aware_lemma_proposer.md
  - research_harness/adversarial_reviews/LOOP-0003/direct_gap_counterexample.md
  - research_harness/adversarial_reviews/LOOP-0003/equality_family_classifier.md
  - research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md
  - selected LOOP-0002 skeptic/auditor notes

## Executive verdict

Fail closed.

LOOP-0003 improves the LOOP-0002 state by isolating a plausible phase-aware scalar bottleneck, but it does not prove CLAIM-0001 and does not produce a counterexample. The proposed phase-aware lemma PAL appears to be the right gauge-uniform scalar statement for the two-term SVD route, and my independent checks did not find a violation. However, PAL is still an unproved nonlinear inequality under nontrivial orthonormal two-frame constraints. Therefore it cannot be promoted to a proof of CLAIM-0001.

The direct numerical search is useful evidence only: it optimizes the original gap over rank <= 2 factorizations and finds no robust positive gap, but nonconvex floating-point optimization cannot certify the universal claim. The equality-family note is appropriately framed as partial; any complete-classification interpretation must be rejected unless a proof is supplied.

Current status:

```text
CLAIM-0001: open / proof_gap_found / fail_closed
Lemma M fixed-gauge H <= 2I: refuted in LOOP-0002
PAL phase-aware scalar lemma: plausible, numerically supported, unproved
Direct rank-two counterexample: none found
Equality classification: partial only, not complete
```

## 1. Phase-aware lemma review

### 1.1 SVD reduction and sign/phase audit

For an SVD-form rank-two operator

```text
C = s_1 |x_1><y_1| + s_2 |x_2><y_2|,     s_i >= 0,
```

with reshapes `X_i,Y_i in M_4(C)`, the proposer's formulas are consistent with the standard unnormalized partial traces under the row convention `row=(i,a), col=(j,b)`:

```text
tr_2(|x_i><y_i|) = X_i Y_i^*,
tr_1(|x_i><y_i|) = X_i^* Y_i,
tr(|x_i><y_i|) = tr(X_i^*Y_i).
```

Thus, defining

```text
L_i = X_iY_i^*,
R_i = X_i^*Y_i,
t_i = tr(X_i^*Y_i),
H_ij = <L_i,L_j> + <R_i,R_j> - (1/2) conjugate(t_i)t_j,
```

CLAIM-0001 for this fixed SVD data is equivalent to

```text
s^* H s <= 2(s_1^2+s_2^2),     s_i >= 0 real.
```

For two terms this is the real-cone condition

```text
D_1 s_1^2 + D_2 s_2^2 - 2 Re(H_12) s_1s_2 >= 0,
D_i = 2-H_ii.
```

Given `D_i >= 0`, the fixed-gauge requirement is

```text
Re(H_12) <= sqrt(D_1D_2),
```

not the refuted full Hermitian determinant condition `|H_12|^2 <= D_1D_2`.

I also checked the right-vector phase law. If

```text
Y_i' = eta_i Y_i,     |eta_i|=1,
delta = arg(eta_1)-arg(eta_2),
```

then

```text
L_i' = conjugate(eta_i)L_i,
R_i' = eta_i R_i,
t_i' = eta_i t_i,
H_12' = e^{i delta} a + e^{-i delta} b,
```

where

```text
a = <L_1,L_2>,
b = <R_1,R_2> - (1/2)conjugate(t_1)t_2.
```

Therefore

```text
max_delta Re(H_12') = |a + conjugate(b)|.
```

This supports the proposer's phase correction. It correctly separates the invalid fixed-gauge complex-coefficient direction from valid SVD data with nonnegative singular values.

### 1.2 PAL sufficiency and equivalence status

The proposed PAL is

```text
|a + conjugate(b)|^2 <= D_1D_2,
```

with

```text
D_i = 2 - ||X_iY_i^*||_F^2 - ||X_i^*Y_i||_F^2 + (1/2)|t_i|^2.
```

Sufficiency for CLAIM-0001 via the two-term SVD route looks correct:

1. In a fixed SVD gauge, only `Re(H_12)` matters.
2. For that fixed gauge, `Re(H_12)=Re(a+b) <= |a+conjugate(b)|`.
3. PAL gives `|a+conjugate(b)| <= sqrt(D_1D_2)`.
4. Hence the real nonnegative singular-value quadratic is nonnegative.

The gauge-uniform interpretation is also reasonable: universal validity of CLAIM-0001 over all rank-two operators must tolerate arbitrary right-singular-vector phase choices, and optimizing those phases yields exactly the PAL off-diagonal magnitude.

Important limitation: this is an equivalence only for the SVD-proof strategy after making the statement gauge-uniform. CLAIM-0001 itself for one fixed `C` only needs the fixed-gauge real-cone inequality for that SVD data. PAL is a stronger uniform scalar lemma, though apparently the natural one because every right-phase choice is valid SVD data for some rank-two operator. The report should not be read as saying PAL has been proved equivalent to CLAIM-0001 as a theorem in both directions.

### 1.3 Hidden-assumption audit

I did not find a hidden Hermitian/normal/positive assumption in the PAL formulation. It works with arbitrary complex singular-vector reshapes.

The diagonal nonnegativity statement is acceptable:

```text
D_i = (1-||X_iY_i^*||_F^2) + (1-||X_i^*Y_i||_F^2) + (1/2)|t_i|^2 >= 0,
```

because `||X_i||_F=||Y_i||_F=1` implies both contraction norms are at most 1.

The main unresolved issue is not a normalization or phase error; it is that no proof of PAL is supplied. Any later proof must avoid reverting to a Hermitian PSD kernel for `2I-H`, since that kernel was exactly refuted in LOOP-0002.

### 1.4 Could PAL be false?

I found no PAL violation, but the search is not decisive.

Independent checks I ran:

```text
random PAL n=4 N=200000 bad 0 min 1.6007353918001705
unit PAL bad 0 min 0.0 num_eq 528
PAL torch minimize slack best (seed 8, slack -5.551115123125783e-16)
```

Interpretation:

- 200,000 random orthonormal two-frame samples found no negative slack.
- An exhaustive matrix-unit two-frame sweep found no violation and many exact equality cases.
- A small PyTorch minimization of PAL slack over Gram-Schmidt-parametrized frames reached only roundoff-scale negative values, consistent with equality rather than a robust counterexample.

These tests increase confidence that PAL may be true, but they are not a proof. Sparse/equality cases are numerous, and a false inequality may require structured non-sparse frames not reached by random or local searches.

## 2. Direct original-gap counterexample search review

The direct search lane is better targeted than the LOOP-0002 Lemma M search because it optimizes the original quantity

```text
gap(C)=||tr_1 C||_F^2+||tr_2 C||_F^2-2||C||_F^2-(1/2)|tr C|^2
```

over matrices parametrized as

```text
C = U V^*,     U,V in C^{16 x r},     r in {1,2},
```

then normalizes `||C||_F=1`. This construction really enforces numerical rank `<= r` and does not rely on the refuted fixed-gauge matrix lemma.

I inspected the script and recomputed summaries from the JSON/NPZ logs. The reported controls and logs are consistent:

```text
rank-two main run:
  restarts: 96
  max final gap: 8.881784094140483e-16
  min final gap: -3.8503533766171515e-08
  positive restarts at threshold 1e-10: 0
  near-zero restarts with gap > -1e-8: 95
  best rank tol 1e-10: 2
  best singular values begin: [0.7071067811896656, 0.7071067811834296, 9.633198289182102e-17]

rank-one check:
  restarts: 48
  max final gap: -0.49999999999999956
  min final gap: -0.500000000489244
  positive restarts at threshold 1e-10: 0
  best rank tol 1e-10: 1

controls:
  rank1_basis_projector_E00: gap -0.5
  rank1_basis_offdiag_E00_11: gap -2.0
  rank2_diag_difference_E00_minus_E11: gap 0.0
```

Independent NPZ recomputation gave:

```text
rank2 best NPZ gap 8.881784094140483e-16, fro 1.0, rank1e-10 2
rank1 best NPZ gap -0.49999999999999956, fro 1.0, rank1e-10 1
```

Skeptical conclusion: no positive-gap counterexample is supported. The only positive value is roundoff-scale and below the lane's own `1e-10` positivity threshold. The optimizer appears to find the equality boundary repeatedly.

But this remains numerical evidence only. It does not prove global nonpositivity, and it does not prove that the equality boundary found exhausts all possible maximizers.

## 3. Equality-family classifier review

The equality-family report is mostly appropriately scoped: it says `completed_partial_classification` and explicitly states that it does not claim a complete classification of all rank-two equality cases. That caveat is essential and should be preserved.

Accepted as useful partial information:

1. Product-type equality:

```text
C = A tensor B,
rank(A)=1,
rank(B)=2,
|tr B|^2 = 2||B||_F^2,
```

or with tensor factors swapped, gives equality. The formula

```text
gap(A tensor B)=||A||_F^2||B||_F^2(alpha+beta-2-alpha beta/2)
```

is correct under the stated definitions.

2. Disjoint two-product-atom diagonal equality:

```text
C = a P tensor Q + b R tensor S
```

with both local supports orthogonal gives

```text
gap(C)=-(1/2)|a+b|^2,
```

so equality occurs at `a+b=0`.

3. Shared-local-index diagonal case reduces to product projection equality when equality holds.

4. The two headline witnesses are separated by invariants such as trace, spectrum, and partial-trace norm multiset, so they are not in the same local-unitary orbit.

Rejected/blocked if overstated:

- This is not a complete classification. It does not rule out nonnormal, non-diagonal, entangled-singular-vector, or other structured equality cases.
- It should not be used to infer a strict defect away from these visible families.
- It should not justify a reduction to positive/Hermitian/normal `C`; even visible equality includes arbitrary complex rank-one factors in the product family.

## 4. Main blockers before any promotion

1. Prove or refute PAL:

```text
| <X_1Y_1^*,X_2Y_2^*> + conjugate(<X_1^*Y_1,X_2^*Y_2> - (1/2)conjugate(t_1)t_2) |^2
<= D_1D_2
```

for Hilbert-Schmidt orthonormal two-frames `X_i` and `Y_i` in `M_4(C)`.

2. If PAL is not the final route, provide an alternative complete proof of the original rank-two inequality that does not assume Hermitian, normal, positive, or convex reductions.

3. If searching for counterexamples, require a reconstructable `C` with robust positive gap above numerical tolerance, verified independently from saved artifacts.

4. Any equality classification must remain partial unless it includes a proof covering arbitrary rank-two complex operators, not merely diagonal/product examples.

5. Any Gram/SOS attempt must encode the real singular coefficients or phase optimization explicitly. A fixed-gauge complex PSD statement equivalent to `H <= 2I` is already refuted.

## 5. Final fail-closed status

No LOOP-0003 artifact proves CLAIM-0001. No LOOP-0003 artifact refutes CLAIM-0001.

The strongest current formulation is:

```text
CLAIM-0001 would follow from PAL, and PAL has survived the tested numerical and sparse cases, but PAL remains unproved.
```

Therefore the correct repository status remains:

```text
CLAIM-0001: proof_gap_found / fail_closed / open
```
