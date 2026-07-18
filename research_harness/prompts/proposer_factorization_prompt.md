# Proposer Prompt: Factorization Lane

You are the Proposer in an adversarial mathematical research loop.

## Claim

Work on `research_harness/claim_cards/CLAIM-0001-rank-two-partial-trace.md`.

Prove, reduce, or sharply localize the claim:

```text
For C in M_4(C) tensor M_4(C), rank(C) <= 2,
||tr_1 C||_F^2 + ||tr_2 C||_F^2
  <= 2 ||C||_F^2 + (1/2) |tr C|^2.
```

## Preferred attack

Use rank factorization

```text
C = U V^*,    U,V in C^{16 x r},    r <= 2.
```

Try to express both partial traces and the Frobenius/trace terms through small Gram matrices, contractions, or 2x2 PSD inequalities.

## Hard constraints

Do not assume:

- C is Hermitian;
- C is normal;
- C is positive semidefinite;
- the rank-two set is convex;
- a special class is dense in a way that preserves the needed inequality.

## Required output

Write your result as if it will be attacked by a skeptic.

Include:

1. Exact statement attempted.
2. Definitions and tensor-index conventions.
3. Step-by-step derivation.
4. Every nontrivial inequality with hypotheses.
5. Explicit check against the equality witness
   `C = (1/sqrt(2))(|00><00| - |11><11|)`.
6. If incomplete, state the exact missing lemma.

Acceptable endings:

- complete proof attempt;
- reduction to a precise lemma;
- failed attempt with a clear obstruction.

Do not claim the theorem is solved unless every step is explicit.
