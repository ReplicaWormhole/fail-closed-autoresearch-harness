#!/usr/bin/env python3
"""LOOP-0008 scalar PAL/crossed-PCL certificate probe.

This script is a reproducible algebra/numerics aid, not a proof engine.  It
attacks the scalar crossed minor

    det(D_S + 1/2 t t*)

with the trace rank-one update retained.  It records:

1. exact numerical verification of the rank-one-update expansion;
2. exact numerical verification of the one-pair row/column wedge SOS identities;
3. a negative test for a tempting but false bilinearization of those diagonal
   wedge identities into a two-frame Gram certificate;
4. sparse coordinate enumeration and random/BFGS-style local search sanity checks.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np

try:
    from scipy.optimize import minimize
except Exception:  # pragma: no cover - scipy may be unavailable
    minimize = None

n = 4
N = n * n
BASIS = [(0, 0), (0, 1), (1, 0), (1, 1)]
CROSS = (0, 3)
SEED = 8008


def mat(u: np.ndarray) -> np.ndarray:
    return u.reshape(n, n)


def hs(A: np.ndarray, B: np.ndarray) -> complex:
    return complex(np.vdot(A, B))


def rand_frame(k: int, rng: np.random.Generator) -> np.ndarray:
    A = rng.normal(size=(N, k)) + 1j * rng.normal(size=(N, k))
    Q, _ = np.linalg.qr(A)
    return Q[:, :k]


def frame_from_unconstrained(w: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    z = w[: 4 * N] + 1j * w[4 * N :]
    Uraw = z[: 2 * N].reshape(N, 2)
    Vraw = z[2 * N :].reshape(N, 2)
    U, _ = np.linalg.qr(Uraw)
    V, _ = np.linalg.qr(Vraw)
    return U[:, :2], V[:, :2]


def pt1_rank(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    return U.T @ np.conjugate(V)


def pt2_rank(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    return U @ V.conj().T


def blocks(Uframe: np.ndarray, Vframe: np.ndarray):
    A = np.zeros((4, 4), complex)
    B = np.zeros((4, 4), complex)
    T = np.zeros((4, 4), complex)
    tr = np.zeros(4, complex)
    mats = []
    for (i, a) in BASIS:
        U = mat(Uframe[:, i])
        V = mat(Vframe[:, a])
        mats.append((U, V))
        tr[len(mats) - 1] = np.vdot(V.reshape(-1), U.reshape(-1))
    for p, (U, V) in enumerate(mats):
        for q, (X, Y) in enumerate(mats):
            A[p, q] = hs(pt1_rank(U, V), pt1_rank(X, Y))
            B[p, q] = hs(pt2_rank(U, V), pt2_rank(X, Y))
            T[p, q] = np.conjugate(tr[p]) * tr[q]
    D = 2 * np.eye(4) - A - B
    M = D + 0.5 * T
    return (A + A.conj().T) / 2, (B + B.conj().T) / 2, T, (D + D.conj().T) / 2, (M + M.conj().T) / 2, tr


def crossed_scalar(Uframe: np.ndarray, Vframe: np.ndarray) -> dict:
    A, B, T, D, M, tr = blocks(Uframe, Vframe)
    S = list(CROSS)
    D2 = D[np.ix_(S, S)]
    M2 = M[np.ix_(S, S)]
    t = tr[S]
    x = D2[0, 0].real
    y = D2[1, 1].real
    c = D2[0, 1]
    det_D = (x * y - abs(c) ** 2).real
    update = 0.5 * (y * abs(t[0]) ** 2 + x * abs(t[1]) ** 2 - 2 * np.real(c * t[0] * np.conjugate(t[1])))
    delta_formula = det_D + update
    delta_direct = np.linalg.det(M2).real
    return {
        "x": float(x),
        "y": float(y),
        "c": c,
        "t1": t[0],
        "t2": t[1],
        "det_D": float(det_D),
        "trace_update": float(update),
        "delta": float(delta_direct),
        "formula_error": float(abs(delta_direct - delta_formula)),
        "eig_D2": np.linalg.eigvalsh(D2),
        "eig_M2": np.linalg.eigvalsh(M2),
        "D2": D2,
        "M2": M2,
    }


def row_wedge_defect(X: np.ndarray, Y: np.ndarray) -> float:
    total = 0.0
    for i in range(n):
        a = X[i, :]
        for j in range(n):
            b = Y[j, :]
            gram_det = np.vdot(a, a).real * np.vdot(b, b).real - abs(np.vdot(a, b)) ** 2
            total += gram_det
    return float(total)


def col_wedge_defect(X: np.ndarray, Y: np.ndarray) -> float:
    total = 0.0
    for i in range(n):
        a = X[:, i]
        for j in range(n):
            b = Y[:, j]
            gram_det = np.vdot(a, a).real * np.vdot(b, b).real - abs(np.vdot(a, b)) ** 2
            total += gram_det
    return float(total)


def naive_row_wedge_bilinear(X1, Y1, X2, Y2) -> complex:
    # Bilinear polarization of sum_{row i,row j} ||X_i-row wedge Y_j-row||^2.
    total = 0j
    for i in range(n):
        a = X1[i, :]
        c = X2[i, :]
        for j in range(n):
            b = Y1[j, :]
            d = Y2[j, :]
            total += np.vdot(a, c) * np.vdot(b, d) - np.vdot(a, d) * np.vdot(b, c)
    return total


def naive_col_wedge_bilinear(X1, Y1, X2, Y2) -> complex:
    total = 0j
    for i in range(n):
        a = X1[:, i]
        c = X2[:, i]
        for j in range(n):
            b = Y1[:, j]
            d = Y2[:, j]
            total += np.vdot(a, c) * np.vdot(b, d) - np.vdot(a, d) * np.vdot(b, c)
    return total


def product_example():
    F = np.zeros((N, 2), complex)
    F[0, 0] = 1.0
    F[1, 1] = 1.0
    return F, F


def traceless_example():
    F = np.zeros((N, 2), complex)
    F[0, 0] = 1.0
    F[5, 1] = 1.0
    return F, F


def complex_json(z):
    return {"re": float(np.real(z)), "im": float(np.imag(z))}


def arr_json(a):
    a = np.asarray(a)
    if np.iscomplexobj(a):
        if a.ndim == 1:
            return [complex_json(z) for z in a]
        return [[complex_json(z) for z in row] for row in a]
    return [float(x) for x in a.ravel()] if a.ndim == 1 else [[float(x) for x in row] for row in a]


def scalar_json(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, np.ndarray):
            out[k] = arr_json(v)
        elif isinstance(v, complex) or np.iscomplexobj(v):
            out[k] = complex_json(v)
        else:
            out[k] = v
    return out


def sparse_summary():
    coords = list(itertools.combinations(range(N), 2))
    total = 0
    min_delta = (float("inf"), None)
    min_detD = (float("inf"), None)
    negative_detD = 0
    zero_delta = 0
    zero_delta_negative_detD = 0
    for us in coords:
        U = np.zeros((N, 2), complex)
        U[us[0], 0] = 1.0
        U[us[1], 1] = 1.0
        for vs in coords:
            V = np.zeros((N, 2), complex)
            V[vs[0], 0] = 1.0
            V[vs[1], 1] = 1.0
            d = crossed_scalar(U, V)
            total += 1
            if d["delta"] < min_delta[0]:
                min_delta = (d["delta"], (us, vs))
            if d["det_D"] < min_detD[0]:
                min_detD = (d["det_D"], (us, vs))
            if d["det_D"] < -1e-12:
                negative_detD += 1
            if abs(d["delta"]) < 1e-12:
                zero_delta += 1
                if d["det_D"] < -1e-12:
                    zero_delta_negative_detD += 1
    return {
        "total": total,
        "min_delta": min_delta,
        "min_det_D": min_detD,
        "negative_det_D_count": negative_detD,
        "zero_delta_count": zero_delta,
        "zero_delta_with_negative_det_D_count": zero_delta_negative_detD,
    }


def random_summary(rng):
    samples = 5000
    min_delta = (float("inf"), None)
    min_detD = (float("inf"), None)
    max_formula_error = 0.0
    max_wedge_diag_error = 0.0
    max_naive_bilin_mismatch = 0.0
    for s in range(samples):
        U, V = rand_frame(2, rng), rand_frame(2, rng)
        d = crossed_scalar(U, V)
        max_formula_error = max(max_formula_error, d["formula_error"])
        if d["delta"] < min_delta[0]:
            min_delta = (d["delta"], s)
        if d["det_D"] < min_detD[0]:
            min_detD = (d["det_D"], s)
        X1, X2 = mat(U[:, 0]), mat(U[:, 1])
        Y1, Y2 = mat(V[:, 0]), mat(V[:, 1])
        for X, Y in [(X1, Y1), (X2, Y2)]:
            left_diag = 1 - np.linalg.norm(X @ Y.conj().T, "fro") ** 2
            right_diag = 1 - np.linalg.norm(X.conj().T @ Y, "fro") ** 2
            max_wedge_diag_error = max(max_wedge_diag_error, abs(left_diag - row_wedge_defect(X, Y)))
            max_wedge_diag_error = max(max_wedge_diag_error, abs(right_diag - col_wedge_defect(X, Y)))
        A, B, T, Dfull, Mfull, tr = blocks(U, V)
        left_K12 = -A[0, 3]
        right_K12 = -B[0, 3]
        # These are the tempting diagonal-SOS polarizations; mismatch confirms
        # the diagonal wedge SOS does not directly give the off-diagonal PAL block.
        max_naive_bilin_mismatch = max(max_naive_bilin_mismatch, abs(left_K12 - naive_row_wedge_bilinear(X1, Y1, X2, Y2)))
        max_naive_bilin_mismatch = max(max_naive_bilin_mismatch, abs(right_K12 - naive_col_wedge_bilinear(X1, Y1, X2, Y2)))
    return {
        "samples": samples,
        "min_delta": min_delta,
        "min_det_D": min_detD,
        "max_trace_update_formula_error": max_formula_error,
        "max_one_pair_wedge_diag_error": max_wedge_diag_error,
        "max_naive_wedge_bilinear_mismatch": max_naive_bilin_mismatch,
    }


def local_opt_summary(rng):
    if minimize is None:
        return {"scipy_available": False}
    starts = 8
    best = (float("inf"), None)
    for k in range(starts):
        w0 = rng.normal(size=8 * N)
        def obj(w):
            U, V = frame_from_unconstrained(w)
            return crossed_scalar(U, V)["delta"]
        res = minimize(obj, w0, method="BFGS", options={"maxiter": 120, "gtol": 1e-7})
        if float(res.fun) < best[0]:
            best = (float(res.fun), {"start": k, "success": bool(res.success), "message": str(res.message), "nit": int(res.nit)})
    return {"scipy_available": True, "starts": starts, "best_delta": best}


def main():
    rng = np.random.default_rng(SEED)
    examples = {}
    for name, maker in [("product", product_example), ("traceless", traceless_example)]:
        U, V = maker()
        d = crossed_scalar(U, V)
        X1, X2 = mat(U[:, 0]), mat(U[:, 1])
        Y1, Y2 = mat(V[:, 0]), mat(V[:, 1])
        A, B, T, Dfull, Mfull, tr = blocks(U, V)
        d["left_K12"] = -A[0, 3]
        d["naive_row_wedge_bilinear"] = naive_row_wedge_bilinear(X1, Y1, X2, Y2)
        d["right_K12"] = -B[0, 3]
        d["naive_col_wedge_bilinear"] = naive_col_wedge_bilinear(X1, Y1, X2, Y2)
        examples[name] = scalar_json(d)

    results = {
        "seed": SEED,
        "status": "probe_not_proof",
        "examples": examples,
        "random_summary": random_summary(rng),
        "sparse_coordinate_summary": sparse_summary(),
        "local_optimization_summary": local_opt_summary(rng),
    }
    out = Path("research_harness/logs/LOOP-0008_scalar_certificate_probe_seed8008.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "random_summary": results["random_summary"],
        "sparse_coordinate_summary": results["sparse_coordinate_summary"],
        "local_optimization_summary": results["local_optimization_summary"],
        "wrote": str(out),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
