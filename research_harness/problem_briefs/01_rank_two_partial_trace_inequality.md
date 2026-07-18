# Problem Brief: Rank-Two Partial-Trace Inequality

## Statement

Let `C in M_4(C) tensor M_4(C)`, regarded as an operator on `C^4 tensor C^4`. If `rank(C) <= 2`, prove or refute

```text
||tr_1 C||_F^2 + ||tr_2 C||_F^2
  <= 2 ||C||_F^2 + (1/2) |tr C|^2.
```

Here `tr_1` and `tr_2` are the two partial traces and `||.||_F` is the Frobenius norm.

## Diagnostic

Define

```text
gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
         - 2 ||C||_F^2 - (1/2) |tr C|^2.
```

A positive gap is a violation.

## Known equality witness

```text
C = (1/sqrt(2)) ( |0,0><0,0| - |1,1><1,1| ).
```

This has rank 2, Frobenius norm squared 1, trace 0, and both partial traces equal to `(1/sqrt(2)) diag(1, -1, 0, 0)`, so `gap(C) = 0`.

Any proposed stronger inequality must handle this witness.

## Non-assumptions

Do not assume any of the following unless a subclaim explicitly states it:

- `C` is Hermitian.
- `C` is normal.
- `C` is positive semidefinite.
- `C` is a pure bipartite vector rather than an operator.
- The set of rank-two operators is convex.
- A normal/Hermitian/positive special case is dense in the needed sense.

## Useful parametrizations to test

Rank-factorization:

```text
C = U V^*,    U,V in C^{16 x r},    r <= 2.
```

Singular-value/SVD form:

```text
C = s_1 |x_1><y_1| + s_2 |x_2><y_2|,
```

where `x_i, y_i in C^4 tensor C^4` are orthonormal families.

Operator-Schmidt expansions of the vectors `x_i`, `y_i` may expose how the two partial traces interact.

## First attack surfaces

1. Reduce the inequality to a statement about two-dimensional Gram matrices associated with the columns of `U` and `V`.
2. Classify or partially classify equality cases.
3. Try to refute stronger statements:
   - smaller coefficient than `1/2` on `|tr C|^2`;
   - rank 3 instead of rank 2;
   - one partial trace alone;
   - dimension-independent strengthening.
4. Determine whether the Kronecker-sum singular-value theorem needs the full claim or only a weaker projected version.

## Promotion criterion

A proof attempt for this claim is not accepted until it survives:

- skeptic review for hidden positivity/normality/convexity assumptions;
- equality-witness constant check;
- numerical tests of any stronger intermediate lemma;
- derivation note with all nontrivial inequalities sourced;
- eventually formalization of the core algebraic lemma.
