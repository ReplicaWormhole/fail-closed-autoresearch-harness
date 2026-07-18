#!/usr/bin/env python3
"""LOOP-0007 certified search lane for CLAIM-0001.

Searches for violations of
  gap(C)=||tr_1 C||_F^2+||tr_2 C||_F^2-2||C||_F^2-(1/2)|tr C|^2 <= 0
for rank(C)<=2 in M_4(C) tensor M_4(C), using the corrected partial-trace
convention from LOOP-0006:
  tr_1(C)[a,b] = sum_i C[i,a,i,b]
  tr_2(C)[i,j] = sum_a C[i,a,j,a]

This is not a proof. It is a fail-closed reproducible search/regression script.
"""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np

def as_tensor(C: np.ndarray) -> np.ndarray:
    return C.reshape(4, 4, 4, 4)

def tr1(C: np.ndarray) -> np.ndarray:
    T = as_tensor(C); out = np.zeros((4, 4), dtype=np.complex128)
    for a in range(4):
        for b in range(4):
            out[a, b] = sum(T[i, a, i, b] for i in range(4))
    return out

def tr2(C: np.ndarray) -> np.ndarray:
    T = as_tensor(C); out = np.zeros((4, 4), dtype=np.complex128)
    for i in range(4):
        for j in range(4):
            out[i, j] = sum(T[i, a, j, a] for a in range(4))
    return out

def fro2(X: np.ndarray) -> float:
    return float(np.vdot(X, X).real)

def gap(C: np.ndarray) -> float:
    return fro2(tr1(C)) + fro2(tr2(C)) - 2.0 * fro2(C) - 0.5 * abs(np.trace(C)) ** 2

def normalized_gap(C: np.ndarray) -> float:
    n = fro2(C)
    return gap(C) / n if n else float('-inf')

def random_rank2(rng: np.random.Generator) -> np.ndarray:
    A = rng.normal(size=(16, 2)) + 1j * rng.normal(size=(16, 2))
    B = rng.normal(size=(16, 2)) + 1j * rng.normal(size=(16, 2))
    C = A @ B.conj().T
    return C / math.sqrt(fro2(C))

def ketbra(row_i: int, row_a: int, col_j: int, col_b: int) -> np.ndarray:
    C = np.zeros((16, 16), dtype=np.complex128)
    C[4 * row_i + row_a, 4 * col_j + col_b] = 1.0
    return C

def equality_examples() -> dict[str, np.ndarray]:
    C1 = (ketbra(0, 0, 0, 0) - ketbra(1, 1, 1, 1)) / math.sqrt(2)
    C2 = (ketbra(0, 0, 0, 0) + ketbra(1, 0, 1, 0)) / math.sqrt(2)
    C3 = (ketbra(0, 0, 0, 0) + 1j * ketbra(0, 1, 0, 1)) / math.sqrt(2)
    return {'diag_difference': C1, 'product_projection': C2, 'phase_sparse_control': C3}

def perturb_around(C0: np.ndarray, rng: np.random.Generator, eps: float, trials: int) -> dict:
    best = {'normalized_gap': -1e99, 'gap': -1e99, 'rank': None, 'trial': None}
    for t in range(trials):
        R = random_rank2(rng)
        C = C0 + eps * R
        U, s, Vh = np.linalg.svd(C, full_matrices=False)
        C2 = (U[:, :2] * s[:2]) @ Vh[:2, :]
        C2 = C2 / math.sqrt(fro2(C2))
        ng = normalized_gap(C2)
        if ng > best['normalized_gap']:
            best = {'normalized_gap': float(ng), 'gap': float(gap(C2)), 'rank': int(np.linalg.matrix_rank(C2, tol=1e-10)), 'trial': t}
    return best

def coordinate_rank2_scan() -> dict:
    units = [ketbra(i, a, j, b) for i in range(4) for a in range(4) for j in range(4) for b in range(4)]
    phases = [1, -1, 1j, -1j]
    best = {'normalized_gap': -1e99, 'pair': None, 'phase': None, 'rank': None}
    count_positive = 0; count_zeroish = 0; total = 0
    for p, E in enumerate(units):
        total += 1; ng = normalized_gap(E)
        if ng > best['normalized_gap']:
            best = {'normalized_gap': float(ng), 'pair': [p], 'phase': None, 'rank': int(np.linalg.matrix_rank(E))}
        count_positive += int(ng > 1e-10); count_zeroish += int(abs(ng) <= 1e-10)
        for q in range(p + 1, len(units)):
            F = units[q]
            for ph in phases:
                total += 1
                C = (E + ph * F) / math.sqrt(fro2(E + ph * F))
                ng = normalized_gap(C)
                if ng > best['normalized_gap']:
                    best = {'normalized_gap': float(ng), 'pair': [p, q], 'phase': str(ph), 'rank': int(np.linalg.matrix_rank(C, tol=1e-10))}
                count_positive += int(ng > 1e-10); count_zeroish += int(abs(ng) <= 1e-10)
    return {'total': total, 'best': best, 'count_positive': count_positive, 'count_zeroish': count_zeroish}

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=7007)
    ap.add_argument('--random-trials', type=int, default=20000)
    ap.add_argument('--perturb-trials', type=int, default=2000)
    ap.add_argument('--out', type=Path, default=Path('research_harness/logs/LOOP-0007_certified_search_seed7007.json'))
    args = ap.parse_args(); rng = np.random.default_rng(args.seed)
    equality = {}
    for name, C in equality_examples().items():
        equality[name] = {'rank': int(np.linalg.matrix_rank(C, tol=1e-10)), 'fro2': fro2(C), 'trace_abs2': float(abs(np.trace(C)) ** 2), 'tr1_fro2': fro2(tr1(C)), 'tr2_fro2': fro2(tr2(C)), 'gap': gap(C), 'normalized_gap': normalized_gap(C)}
    best_random = {'normalized_gap': -1e99, 'gap': -1e99, 'trial': None, 'rank': None}; positive_random = 0
    for t in range(args.random_trials):
        C = random_rank2(rng); ng = normalized_gap(C)
        if ng > best_random['normalized_gap']:
            best_random = {'normalized_gap': float(ng), 'gap': float(gap(C)), 'trial': t, 'rank': int(np.linalg.matrix_rank(C, tol=1e-10))}
        positive_random += int(ng > 1e-10)
    perturb = {}
    for eps in [1e-4, 1e-3, 1e-2, 1e-1, 5e-1]:
        for name, C0 in equality_examples().items():
            perturb[f'{name}_eps_{eps:g}'] = perturb_around(C0, rng, eps, args.perturb_trials)
    coord = coordinate_rank2_scan()
    result = {'claim': 'CLAIM-0001-rank-two-partial-trace', 'loop': 'LOOP-0007', 'seed': args.seed, 'convention': {'tr1': 'tr_1(C)[a,b]=sum_i C[i,a,i,b]', 'tr2': 'tr_2(C)[i,j]=sum_a C[i,a,j,a]'}, 'equality_regressions': equality, 'random_rank2': {'trials': args.random_trials, 'best': best_random, 'positive_count_tol_1e-10': positive_random}, 'equality_perturbations_rank2_truncated': perturb, 'coordinate_two_unit_scan': coord, 'robust_positive_gap_found': bool(positive_random > 0 or coord['count_positive'] > 0 or any(v['normalized_gap'] > 1e-10 for v in perturb.values())), 'success_condition_met': False, 'caveat': 'Numerical search/regression only; absence of positives is not a proof.'}
    args.out.parent.mkdir(parents=True, exist_ok=True); args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'seed': args.seed, 'equality_gaps': {k: v['normalized_gap'] for k, v in equality.items()}, 'random_best_normalized_gap': best_random['normalized_gap'], 'random_positive_count_tol_1e-10': positive_random, 'coordinate_best_normalized_gap': coord['best']['normalized_gap'], 'coordinate_positive_count_tol_1e-10': coord['count_positive'], 'best_perturbation_normalized_gap': max(v['normalized_gap'] for v in perturb.values()), 'robust_positive_gap_found': result['robust_positive_gap_found'], 'log': str(args.out)}, indent=2))
if __name__ == '__main__':
    main()
