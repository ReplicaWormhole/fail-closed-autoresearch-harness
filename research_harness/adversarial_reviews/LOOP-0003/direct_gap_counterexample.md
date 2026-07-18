# LOOP-0003 direct original-gap rank-two counterexample search

## Target

CLAIM-0001: for C in M_4(C) tensor M_4(C), rank(C) <= 2 implies

    gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2 - 2||C||_F^2 - (1/2)|tr C|^2 <= 0.

A positive gap is a counterexample.  Partial traces are unnormalized, with row/column tensor indices row=(i,a), col=(j,b):

    (tr_1 C)[a,b] = sum_i C[(i,a),(i,b)]
    (tr_2 C)[i,j] = sum_a C[(i,a),(j,a)]

## Executable artifact

Script:

    ./research_harness/experiments/LOOP-0003_direct_gap_search.py

The script parametrizes C directly as

    C = U V^*,  U,V in C^{16 x r}, r in {1,2},

then normalizes ||C||_F = 1 before evaluating the original CLAIM-0001 gap.  This guarantees numerical rank <= r by construction.  Optimization uses PyTorch float64/complex128 Adam followed by LBFGS polishing.  The JSON logs include per-restart seed, gap, rank check, leading singular values, trace/partial-trace terms, and a reconstructable best C as real/imag arrays; NPZ logs also store the best C.

## Commands run

Smoke test:

    cd .
    python3 research_harness/experiments/LOOP-0003_direct_gap_search.py --rank 2 --restarts 2 --steps 20 --lbfgs-steps 5 --seed-base 3003 --out-json research_harness/logs/LOOP-0003_smoke.json --out-npz research_harness/logs/LOOP-0003_smoke_best.npz > research_harness/logs/LOOP-0003_smoke.stdout.log 2>&1

Main rank-two run:

    cd .
    python3 research_harness/experiments/LOOP-0003_direct_gap_search.py --rank 2 --restarts 96 --steps 3000 --lbfgs-steps 100 --seed-base 3003 --lr 0.03 --out-json research_harness/logs/LOOP-0003_direct_gap_search_seed3003_rank2.json --out-npz research_harness/logs/LOOP-0003_direct_gap_search_seed3003_rank2_best.npz > research_harness/logs/LOOP-0003_direct_gap_search_seed3003_rank2.stdout.log 2>&1

Separate rank-one check:

    cd .
    python3 research_harness/experiments/LOOP-0003_direct_gap_search.py --rank 1 --restarts 48 --steps 2000 --lbfgs-steps 80 --seed-base 4003 --lr 0.03 --out-json research_harness/logs/LOOP-0003_direct_gap_search_seed4003_rank1.json --out-npz research_harness/logs/LOOP-0003_direct_gap_search_seed4003_rank1_best.npz > research_harness/logs/LOOP-0003_direct_gap_search_seed4003_rank1.stdout.log 2>&1

Independent NPZ recomputation check was also run with NumPy on the saved best candidates.

## Positive/equality controls

The script includes deterministic controls evaluated before optimization:

| control | rank | normalized gap | notes |
|---|---:|---:|---|
| rank1_basis_projector_E00 | 1 | -0.5 | C = |00><00| |
| rank1_basis_offdiag_E00_11 | 1 | -2.0 | C = |00><11| |
| rank2_diag_difference_E00_minus_E11 | 2 | 0.0 | normalized C = (|00><00| - |11><11|)/sqrt(2), equality-family sanity check |

The equality control is important: it confirms the implementation can realize gap 0 at rank 2 for the original claim, not only negative values.

## Main rank-two numerical result

Log:

    ./research_harness/logs/LOOP-0003_direct_gap_search_seed3003_rank2.json
    ./research_harness/logs/LOOP-0003_direct_gap_search_seed3003_rank2.stdout.log
    ./research_harness/logs/LOOP-0003_direct_gap_search_seed3003_rank2_best.npz

Summary from the JSON/NPZ recomputation:

    restarts: 96
    max final gap: 8.881784094140483e-16
    positive restarts at threshold 1e-10: 0
    near-zero restarts with gap > -1e-8: 95
    worst/min final gap: -3.8503533766171515e-08

Best saved candidate:

    gap: 8.881784094140483e-16
    ||C||_F: 1.0
    numerical rank, tol=1e-10: 2
    numerical rank, tol=1e-8: 2
    leading singular values:
        [0.7071067811896656, 0.7071067811834296,
         9.633198289182102e-17, 6.521952207065591e-17,
         4.191049967237077e-17, 2.8801602074535003e-17,
         2.0634793862712078e-17, 1.702884421818344e-17]
    |tr C|: 4.535653633915694e-12
    ||tr_1 C||_F^2: 1.2891886831943036
    ||tr_2 C||_F^2: 0.7108113168056971

The best value is positive only at double-precision roundoff scale.  The script's positivity threshold is 1e-10, and this candidate is not marked positive.  It is numerically consistent with the known rank-two equality boundary gap = 0, not with a robust counterexample.

## Rank-one check

Log:

    ./research_harness/logs/LOOP-0003_direct_gap_search_seed4003_rank1.json
    ./research_harness/logs/LOOP-0003_direct_gap_search_seed4003_rank1.stdout.log
    ./research_harness/logs/LOOP-0003_direct_gap_search_seed4003_rank1_best.npz

Summary:

    restarts: 48
    max final gap: -0.49999999999999956
    min final gap: -0.500000000489244
    positive restarts at threshold 1e-10: 0

Best rank-one candidate had numerical rank 1, ||C||_F = 1.0, |tr C| approximately 1, and gap approximately -0.5.

## Conclusion

No reconstructable positive-gap counterexample was found.

The direct rank-two optimizer repeatedly converged to gap 0 up to floating-point roundoff, with rank 2 and singular values essentially (1/sqrt(2), 1/sqrt(2), 0, ...).  The maximum recorded gap, 8.88e-16, is far below the 1e-10 positivity threshold and should be treated as numerical zero.  The saved best candidate is reconstructable from the JSON/NPZ artifacts but is not a positive-gap counterexample.

Caveats: this is a nonconvex numerical search, not a proof.  It gives additional adversarial evidence against an easily found direct rank<=2 counterexample and confirms the optimizer reaches the equality boundary, but it cannot certify CLAIM-0001 globally.
