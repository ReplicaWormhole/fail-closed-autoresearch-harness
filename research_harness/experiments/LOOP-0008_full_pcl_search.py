#!/usr/bin/env python3
"""LOOP-0008 full PCL/search lane for CLAIM-0001.

Fail-closed numerical/regression tool.  It probes the full 4x4 PCL matrix

    M(U,V)=2I_4-A(U,V)-B(U,V)+(1/2)T(U,V)

for two support frames U,V in C^4 tensor C^4.  PCL asks M>=0.  A violation is a
negative eigenvalue of M, equivalently a positive eigenvalue of K=-M and an
explicit rank-at-most-two operator C=P C Q with positive original gap(C).

The script always converts the worst compression eigenvector into C and checks
rank/gap with the corrected partial-trace convention:
    tr_1(C)[a,b] = sum_i C[i,a,i,b]
    tr_2(C)[i,j] = sum_a C[i,a,j,a]
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np

try:
    from scipy.optimize import minimize
    SCIPY = True
except Exception:
    SCIPY = False

n = 4
N = n * n


def cvec(i: int, a: int) -> np.ndarray:
    v = np.zeros(N, dtype=np.complex128)
    v[n * i + a] = 1.0
    return v


def ketbra(row_i: int, row_a: int, col_j: int, col_b: int) -> np.ndarray:
    C = np.zeros((N, N), dtype=np.complex128)
    C[n * row_i + row_a, n * col_j + col_b] = 1.0
    return C


def mat(u: np.ndarray) -> np.ndarray:
    return u.reshape(n, n)


def hs(A: np.ndarray, B: np.ndarray) -> complex:
    return complex(np.vdot(A, B))


def orth(Z: np.ndarray) -> np.ndarray:
    Q, R = np.linalg.qr(Z)
    # Fix phases only for reproducibility; the plane is unchanged.
    d = np.diag(R)[:2]
    ph = np.where(np.abs(d) > 0, d / np.abs(d), 1.0)
    return Q[:, :2] * ph.conj()


def random_frame(rng: np.random.Generator, support: list[int] | None = None) -> np.ndarray:
    if support is None:
        Z = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    else:
        Z = np.zeros((N, 2), dtype=np.complex128)
        W = rng.normal(size=(len(support), 2)) + 1j * rng.normal(size=(len(support), 2))
        for k, idx in enumerate(support):
            Z[idx, :] = W[k, :]
    return orth(Z)


def pt1_rank(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    # tr_1(|vec(U)><vec(V)|)[a,b] = sum_i U[i,a] conjugate(V[i,b])
    return U.T @ np.conjugate(V)


def pt2_rank(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    # tr_2(|vec(U)><vec(V)|)[i,j] = sum_a U[i,a] conjugate(V[j,a])
    return U @ V.conj().T


def partials(C: np.ndarray) -> tuple[np.ndarray, np.ndarray, complex]:
    T4 = C.reshape(n, n, n, n)
    tr1 = np.einsum("iaib->ab", T4)
    tr2 = np.einsum("iaja->ij", T4)
    return tr1, tr2, np.trace(C)


def fro2(X: np.ndarray) -> float:
    return float(np.vdot(X, X).real)


def gap(C: np.ndarray) -> float:
    tr1, tr2, tr = partials(C)
    return fro2(tr1) + fro2(tr2) - 2.0 * fro2(C) - 0.5 * abs(tr) ** 2


def normalized_gap(C: np.ndarray) -> float:
    den = fro2(C)
    return gap(C) / den if den else float("nan")


def pcl_matrices(Uframe: np.ndarray, Vframe: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[np.ndarray]]:
    A = np.zeros((4, 4), dtype=np.complex128)
    B = np.zeros((4, 4), dtype=np.complex128)
    T = np.zeros((4, 4), dtype=np.complex128)
    Es: list[np.ndarray] = []
    data: list[tuple[np.ndarray, np.ndarray]] = []
    for i in range(2):
        for a in range(2):
            U = mat(Uframe[:, i])
            V = mat(Vframe[:, a])
            data.append((U, V))
            Es.append(np.outer(Uframe[:, i], Vframe[:, a].conj()))
    traces = [np.vdot(V.reshape(-1), U.reshape(-1)) for U, V in data]
    for p, (U, V) in enumerate(data):
        for q, (X, Y) in enumerate(data):
            A[p, q] = hs(pt1_rank(U, V), pt1_rank(X, Y))
            B[p, q] = hs(pt2_rank(U, V), pt2_rank(X, Y))
            T[p, q] = np.conjugate(traces[p]) * traces[q]
    M = 2.0 * np.eye(4) - A - B + 0.5 * T
    M = (M + M.conj().T) / 2.0
    return A, B, T, M, Es


def principal_minors(M: np.ndarray) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k in range(1, 5):
        vals = []
        for I in itertools.combinations(range(4), k):
            sub = M[np.ix_(I, I)]
            vals.append({"I": list(I), "det": float(np.linalg.det(sub).real)})
        vals.sort(key=lambda x: x["det"])
        out[str(k)] = {"min": vals[0], "max": vals[-1], "negative_count_tol_1e-10": sum(v["det"] < -1e-10 for v in vals)}
    return out


def eval_frames(U: np.ndarray, V: np.ndarray) -> dict[str, Any]:
    A, B, T, M, Es = pcl_matrices(U, V)
    w, Q = np.linalg.eigh(M)
    imin = int(np.argmin(w))
    coeff = Q[:, imin]
    C = np.zeros((N, N), dtype=np.complex128)
    for j in range(4):
        C += coeff[j] * Es[j]
    C_fro2 = fro2(C)
    if C_fro2 > 0:
        C = C / math.sqrt(C_fro2)
    ng = normalized_gap(C)
    rayleigh_M = float(np.real(np.vdot(coeff, M @ coeff)))
    gap_identity_error = float(abs(ng + rayleigh_M))
    return {
        "eig_M": [float(x) for x in w],
        "min_eig_M": float(w[imin]),
        "max_gap_eig_K": float(-w[imin]),
        "top_original_normalized_gap": float(ng),
        "top_original_rank": int(np.linalg.matrix_rank(C, tol=1e-10)),
        "gap_plus_rayleigh_M_abs_error": gap_identity_error,
        "principal_minors": principal_minors(M),
    }


def equality_controls() -> dict[str, Any]:
    controls: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    # Product equality support span |00>,|10>.
    P = np.column_stack([cvec(0, 0), cvec(1, 0)])
    controls["product_projection_support_00_10"] = (P, P.copy())
    # Diagonal/traceless equality support span |00>,|11>.
    D = np.column_stack([cvec(0, 0), cvec(1, 1)])
    controls["diagonal_traceless_support_00_11"] = (D, D.copy())
    # LOOP-0007 product convention span |00>,|01> as additional regression.
    R = np.column_stack([cvec(0, 0), cvec(0, 1)])
    controls["right_product_support_00_01"] = (R, R.copy())
    return {name: eval_frames(U, V) for name, (U, V) in controls.items()}


def coordinate_plane_scan() -> dict[str, Any]:
    planes = []
    for I in itertools.combinations(range(N), 2):
        F = np.zeros((N, 2), dtype=np.complex128)
        F[I[0], 0] = 1.0
        F[I[1], 1] = 1.0
        planes.append((I, F))
    best: dict[str, Any] | None = None
    neg_count = 0
    total = 0
    minor_neg_counts = {"1": 0, "2": 0, "3": 0, "4": 0}
    for IP, P in planes:
        for IQ, Q in planes:
            total += 1
            r = eval_frames(P, Q)
            if r["min_eig_M"] < -1e-10:
                neg_count += 1
            for k in minor_neg_counts:
                if r["principal_minors"][k]["negative_count_tol_1e-10"]:
                    minor_neg_counts[k] += 1
            if best is None or r["min_eig_M"] < best["min_eig_M"]:
                best = dict(r)
                best["plane_P"] = list(IP)
                best["plane_Q"] = list(IQ)
    return {"total_pairs": total, "negative_min_eig_count_tol_1e-10": neg_count, "pair_count_with_negative_minor_by_size": minor_neg_counts, "worst": best}


def random_scan(rng: np.random.Generator, trials: int) -> dict[str, Any]:
    best: dict[str, Any] | None = None
    positive_gap_count = 0
    max_gap_identity_error = 0.0
    min_minor_by_size = {"1": (float("inf"), None), "2": (float("inf"), None), "3": (float("inf"), None), "4": (float("inf"), None)}
    for t in range(trials):
        P = random_frame(rng)
        Q = random_frame(rng)
        r = eval_frames(P, Q)
        max_gap_identity_error = max(max_gap_identity_error, r["gap_plus_rayleigh_M_abs_error"])
        positive_gap_count += int(r["top_original_normalized_gap"] > 1e-10)
        if best is None or r["min_eig_M"] < best["min_eig_M"]:
            best = dict(r)
            best["trial"] = t
        for k in min_minor_by_size:
            det = r["principal_minors"][k]["min"]["det"]
            if det < min_minor_by_size[k][0]:
                min_minor_by_size[k] = (det, t)
    return {
        "trials": trials,
        "worst_min_eig": best,
        "positive_original_gap_count_tol_1e-10": positive_gap_count,
        "max_gap_identity_error": max_gap_identity_error,
        "min_principal_minor_by_size": {k: {"det": float(v[0]), "trial": v[1]} for k, v in min_minor_by_size.items()},
    }


def optimize_min_eig(seed: int, restarts: int, maxiter: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)

    def frames_from_x(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        z1 = x[0:16] + 1j * x[16:32]
        z2 = x[32:48] + 1j * x[48:64]
        w1 = x[64:80] + 1j * x[80:96]
        w2 = x[96:112] + 1j * x[112:128]
        return orth(np.column_stack([z1, z2])), orth(np.column_stack([w1, w2]))

    def obj(x: np.ndarray) -> float:
        P, Q = frames_from_x(x)
        return eval_frames(P, Q)["min_eig_M"]

    best: dict[str, Any] | None = None
    for r in range(restarts):
        x0 = rng.normal(size=128)
        success = False
        fun = None
        nit = None
        if SCIPY:
            res = minimize(obj, x0, method="BFGS", options={"maxiter": maxiter, "gtol": 1e-7})
            x = res.x
            success = bool(res.success)
            fun = float(res.fun)
            nit = int(getattr(res, "nit", -1))
        else:
            x = x0.copy()
            val = obj(x)
            step = 0.25
            for it in range(maxiter):
                y = x + step * rng.normal(size=128)
                vy = obj(y)
                if vy < val:
                    x, val = y, vy
                step *= 0.99
            fun = float(val)
            nit = maxiter
        P, Q = frames_from_x(x)
        rr = eval_frames(P, Q)
        rr.update({"restart": r, "optimizer_success": success, "optimizer_fun": fun, "nit": nit})
        if best is None or rr["min_eig_M"] < best["min_eig_M"]:
            best = rr
    return {"scipy": SCIPY, "restarts": restarts, "maxiter": maxiter, "best": best}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=8008)
    ap.add_argument("--random-trials", type=int, default=5000)
    ap.add_argument("--opt-restarts", type=int, default=8)
    ap.add_argument("--maxiter", type=int, default=200)
    ap.add_argument("--out", type=Path, default=Path("research_harness/logs/LOOP-0008_full_pcl_search_seed8008.json"))
    args = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(args.seed)
    result: dict[str, Any] = {
        "claim": "CLAIM-0001-rank-two-partial-trace",
        "loop": "LOOP-0008",
        "seed": args.seed,
        "convention": {
            "tr1": "tr_1(C)[a,b]=sum_i C[i,a,i,b]",
            "tr2": "tr_2(C)[i,j]=sum_a C[i,a,j,a]",
            "pcl_target": "M=2I-A-B+(1/2)T should be PSD; violation is min_eig(M)<0 and original gap(C)>0",
        },
        "equality_controls": equality_controls(),
        "coordinate_two_plane_scan": coordinate_plane_scan(),
        "random_scan": random_scan(rng, args.random_trials),
        "optimize_min_eig_M": optimize_min_eig(args.seed + 17, args.opt_restarts, args.maxiter),
    }
    candidates = [
        result["coordinate_two_plane_scan"]["worst"],
        result["random_scan"]["worst_min_eig"],
        result["optimize_min_eig_M"]["best"],
    ]
    worst = min(candidates, key=lambda d: d["min_eig_M"])
    result["worst_overall"] = worst
    result["robust_pcl_violation_found"] = bool(worst["min_eig_M"] < -1e-8 and worst["top_original_normalized_gap"] > 1e-8)
    result["success_condition_met"] = False
    result["caveat"] = "Numerical search/regression only; no proof of full PCL PSD and no certified positive-gap counterexample."
    result["elapsed_sec"] = time.time() - t0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    summary = {
        "seed": args.seed,
        "random_trials": args.random_trials,
        "coordinate_pairs": result["coordinate_two_plane_scan"]["total_pairs"],
        "control_min_eigs": {k: v["min_eig_M"] for k, v in result["equality_controls"].items()},
        "coordinate_worst_min_eig_M": result["coordinate_two_plane_scan"]["worst"]["min_eig_M"],
        "random_worst_min_eig_M": result["random_scan"]["worst_min_eig"]["min_eig_M"],
        "optimized_worst_min_eig_M": result["optimize_min_eig_M"]["best"]["min_eig_M"],
        "worst_overall_min_eig_M": result["worst_overall"]["min_eig_M"],
        "worst_overall_original_normalized_gap": result["worst_overall"]["top_original_normalized_gap"],
        "robust_pcl_violation_found": result["robust_pcl_violation_found"],
        "log": str(args.out),
        "elapsed_sec": result["elapsed_sec"],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
