# Approved goals

These goals replace the obsolete fixed LOOP-0003 lane list.  Each automated loop should advance one or more goals through persistent workstreams.

## G1. Scalar crossed-minor certificate

Prove or refute the scalar crossed PAL/PCL determinant inequality

```text
Delta = D1D2 - |m|^2 = GramSlack - ExchangePenalty >= 0.
```

Hard constraints:

- Retain the trace-coupled terms.
- Do not use false shortcuts `N12<=D1`, `N21<=D2`, `D1D2>=N12N21`, `D>=0`, or `detD>=0`.
- Do not promote scalar success to full PCL without a bridge.

## G2. Full PCL certificate

Find a direct trace-coupled proof that the full `4 x 4` PCL compression matrix `M` is positive semidefinite for arbitrary rank-two supports.

Hard constraints:

- Work with `M = D + (1/2) trace-rank-one-update`, not D alone.
- Coordinate atlases, random searches, and local Schur diagnostics are only guardrails.
- A scalar crossed-minor proof is not a full PCL proof.

## G3. Equality geometry and local-to-global structure

Turn local equality/tangent classifications into exact equality-family statements.

Hard constraints:

- Local Hessian zero-mode classification is not global proof.
- Product-projection and traceless two-product-atom equality mechanisms must both be accounted for.

## G4. Certified counterexample search

Search for a reconstructable rank-two `C` with positive original gap.

Hard constraints:

- Any positive candidate must be checked under the original gap and corrected partial traces.
- Use high precision, interval, or rational verification before promotion.
- Numerical roundoff equality is not a counterexample.

## G5. Literature and related inequalities

Build a source-backed map of relevant matrix/operator/quantum-information inequalities.

Hard constraints:

- Record exact statements and hypotheses.
- Watch for operator-Schmidt-rank versus ordinary-rank confusion.
- Do not import theorems whose assumptions exceed CLAIM-0001.

## G6. Working paper / derivation note

Maintain a living mathematical artifact explaining the claim, equivalences, refuted routes, current bottlenecks, and evidence.

Hard constraints:

- Mark every lemma as proved, refuted, numerical-only, or open.
- Include provenance links to loops/workstreams/scripts/logs.
- Do not typeset an unresolved proof gap as a theorem.
