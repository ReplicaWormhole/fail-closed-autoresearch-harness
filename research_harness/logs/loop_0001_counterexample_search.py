#!/usr/bin/env python3
"""Counterexample/stronger-variant search for CLAIM-0001.

Positive gap_alpha = ||tr1 C||_F^2 + ||tr2 C||_F^2 - 2||C||_F^2 - alpha |tr C|^2
means violation of the variant with coefficient alpha.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

N = 4
D = N * N


def random_complex_matrix(rng, shape):
    return rng.normal(size=shape) + 1j * rng.normal(size=shape)


def normalize(C):
    n = math.sqrt(float(np.vdot(C, C).real))
    return C if n == 0 else C / n


def partial_traces(C):
    T = C.reshape(N, N, N, N)
    tr1 = np.einsum("abac->bc", T)
    tr2 = np.einsum("abcb->ac", T)
    return tr1, tr2


def metrics(C, alpha=0.5):
    tr1, tr2 = partial_traces(C)
    pt1 = float(np.vdot(tr1, tr1).real)
    pt2 = float(np.vdot(tr2, tr2).real)
    norm2 = float(np.vdot(C, C).real)
    trace_abs2 = float(abs(np.trace(C)) ** 2)
    gap_alpha = pt1 + pt2 - 2.0 * norm2 - alpha * trace_abs2
    alpha_needed = None
    if trace_abs2 > 1e-12:
        alpha_needed = (pt1 + pt2 - 2.0 * norm2) / trace_abs2
    return dict(pt1=pt1, pt2=pt2, lhs=pt1+pt2, norm2=norm2, trace_abs2=trace_abs2,
                alpha=alpha, gap_alpha=float(gap_alpha), alpha_needed=alpha_needed)


def factor_to_matrix(x, rank):
    n = D * rank
    U = (x[:n] + 1j*x[n:2*n]).reshape(D, rank)
    V = (x[2*n:3*n] + 1j*x[3*n:4*n]).reshape(D, rank)
    return normalize(U @ V.conj().T)


def matrix_to_factor(C, rank):
    U, s, Vh = np.linalg.svd(C, full_matrices=False)
    s = s[:rank]
    U = U[:, :rank] * np.sqrt(s)
    V = Vh.conj().T[:, :rank] * np.sqrt(s)
    return np.concatenate([U.real.ravel(), U.imag.ravel(), V.real.ravel(), V.imag.ravel()])


def random_rank_matrix(rng, rank):
    U = random_complex_matrix(rng, (D, rank))
    V = random_complex_matrix(rng, (D, rank))
    return normalize(U @ V.conj().T)


@dataclass
class Candidate:
    label: str
    rank_param: int
    objective: float
    metrics: dict
    singular_values: list[float]


def summarize(label, rank, C, objective):
    s = np.linalg.svd(C, compute_uv=False)
    return Candidate(label, rank, float(objective), metrics(C, 0.5), [float(x) for x in s[:8]])


def equality_witness():
    C = np.zeros((D, D), dtype=np.complex128)
    C[0*N + 0, 0*N + 0] = 1/math.sqrt(2)
    C[1*N + 1, 1*N + 1] = -1/math.sqrt(2)
    return C


def diagonal_witness(vals):
    C = np.zeros((D, D), dtype=np.complex128)
    for i, v in enumerate(vals):
        C[i*N + i, i*N + i] = v
    return normalize(C)


def optimize(seedC, rank, objective_name, alpha, maxiter):
    from scipy.optimize import minimize
    x0 = matrix_to_factor(seedC, rank)

    def obj(x):
        C = factor_to_matrix(x, rank)
        m = metrics(C, alpha)
        if objective_name == "gap_alpha":
            val = float(m["gap_alpha"])
        elif objective_name == "alpha_needed":
            # Penalize tiny trace: we want variants with nonzero trace that force coefficient.
            val = float(m["alpha_needed"]) if m["alpha_needed"] is not None else -1e6
        elif objective_name == "pt1_minus_norm":
            val = float(m["pt1"]) - float(m["norm2"])
        elif objective_name == "sum_minus_2norm":
            val = float(m["lhs"]) - 2*float(m["norm2"])
        else:
            raise ValueError(objective_name)
        return -val

    res = minimize(obj, x0, method="Powell", options={"maxiter": maxiter, "ftol": 1e-12, "xtol": 1e-12, "disp": False})
    C = factor_to_matrix(res.x, rank)
    return C, -float(res.fun), dict(success=bool(res.success), nit=int(getattr(res, "nit", -1)), message=str(res.message))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=1001)
    ap.add_argument("--samples", type=int, default=5000)
    ap.add_argument("--restarts", type=int, default=6)
    ap.add_argument("--maxiter", type=int, default=250)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    report = {"seed": args.seed, "samples": args.samples, "restarts": args.restarts, "maxiter": args.maxiter, "candidates": [], "opt_logs": []}

    special = [("known_rank2_equality", 2, equality_witness()),
               ("rank3_diagonal_traceless", 3, diagonal_witness([1, 1, -2])),
               ("rank3_diagonal_nonzero_trace", 3, diagonal_witness([1, 1, 1]))]
    for label, rank, C in special:
        report["candidates"].append(asdict(summarize(label, rank, C, metrics(C, 0.5)["gap_alpha"])))

    tasks = []
    for rank in [1, 2, 3]:
        random_best = {"gap_alpha": (-1e9, None), "alpha_needed": (-1e9, None), "sum_minus_2norm": (-1e9, None), "pt1_minus_norm": (-1e9, None)}
        for _ in range(args.samples):
            C = random_rank_matrix(rng, rank)
            m05 = metrics(C, 0.5)
            vals = {
                "gap_alpha": m05["gap_alpha"],
                "alpha_needed": m05["alpha_needed"] if m05["alpha_needed"] is not None else -1e9,
                "sum_minus_2norm": m05["lhs"] - 2*m05["norm2"],
                "pt1_minus_norm": m05["pt1"] - m05["norm2"],
            }
            for k, v in vals.items():
                if v > random_best[k][0]:
                    random_best[k] = (float(v), C.copy())
        for objname, (val, C) in random_best.items():
            report["candidates"].append(asdict(summarize(f"random_rank{rank}_{objname}", rank, C, val)))
            tasks.append((rank, objname, C))

    # Optimize selected seeds. Alpha=0.25 tests smaller trace coefficient; alpha irrelevant for alpha_needed objective.
    for rank, objname, seedC in tasks:
        alpha = 0.25 if objname == "gap_alpha" else 0.5
        try:
            Copt, val, optlog = optimize(seedC, rank, objname, alpha, args.maxiter)
            cand = asdict(summarize(f"optimized_rank{rank}_{objname}_alpha{alpha}", rank, Copt, val))
            cand["variant_alpha_used_in_objective"] = alpha
            report["candidates"].append(cand)
            report["opt_logs"].append({"label": cand["label"], **optlog})
        except Exception as e:
            report["opt_logs"].append({"rank": rank, "objective": objname, "error": repr(e)})

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    print(json.dumps(report, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
