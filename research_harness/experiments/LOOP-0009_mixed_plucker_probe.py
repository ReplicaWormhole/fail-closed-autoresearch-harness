#!/usr/bin/env python3
"""LOOP-0009 mixed two-frame Plucker/SOS probe.

This is a reproducible algebra/numerics aid, not a proof engine.
It attacks the scalar PAL / crossed-PCL minor

    det M[{(1,1),(2,2)}] = D1 D2 - |M_12|^2 >= 0

with the trace rank-one update retained.  LOOP-0008 showed that the
same-pair diagonal wedge polarization gives the wrong off-diagonal entry.
This script tests the next natural mixed two-frame identity:

    M_12 = <row_wedges(X1,Y2), row_wedges(X2,Y1)>
         + <col_wedges(X1,Y2), col_wedges(X2,Y1)>
         + (1/2) conjugate(tr(Y1^* X1)) tr(Y2^* X2),

where the wedge inner product is

    <a wedge b, c wedge d> = <a,c><b,d> - <a,d><b,c>.

It then checks the tempting Cauchy/SOS route using these mixed wedge vectors.
That route would need the norms of the mixed vectors to be bounded by the
actual diagonal entries D1,D2.  The script finds explicit negative margins,
so this simple mixed-Gram ansatz is obstructed even though the mixed off-diagonal
identity is exact on the orthonormal two-frame constraint manifold.
"""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any

import numpy as np

try:
    from scipy.optimize import minimize
except Exception:  # pragma: no cover
    minimize = None

n = 4
N = n * n
BASIS = [(0, 0), (0, 1), (1, 0), (1, 1)]
CROSS = (0, 3)


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
    # Corrected LOOP-0007/0008 convention: entries are row-row contractions.
    return U.T @ np.conjugate(V)


def pt2_rank(U: np.ndarray, V: np.ndarray) -> np.ndarray:
    return U @ V.conj().T


def blocks(Uframe: np.ndarray, Vframe: np.ndarray):
    A = np.zeros((4, 4), complex)
    B = np.zeros((4, 4), complex)
    T = np.zeros((4, 4), complex)
    tr = np.zeros(4, complex)
    pairs = []
    for (i, a) in BASIS:
        U = mat(Uframe[:, i])
        V = mat(Vframe[:, a])
        pairs.append((U, V))
        tr[len(pairs) - 1] = np.vdot(V.reshape(-1), U.reshape(-1))
    for p, (U, V) in enumerate(pairs):
        for q, (X, Y) in enumerate(pairs):
            A[p, q] = hs(pt1_rank(U, V), pt1_rank(X, Y))
            B[p, q] = hs(pt2_rank(U, V), pt2_rank(X, Y))
            T[p, q] = np.conjugate(tr[p]) * tr[q]
    D = 2 * np.eye(4) - A - B
    M = D + 0.5 * T
    return (A + A.conj().T) / 2, (B + B.conj().T) / 2, T, (D + D.conj().T) / 2, (M + M.conj().T) / 2, tr


def wedge_inner(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> complex:
    ac = complex(np.vdot(a, c))
    bd = complex(np.vdot(b, d))
    ad = complex(np.vdot(a, d))
    bc = complex(np.vdot(b, c))
    return ac * bd - ad * bc


def row_wedge_bilinear(Xa, Ya, Xb, Yb) -> complex:
    total = 0j
    for i in range(n):
        for j in range(n):
            total += wedge_inner(Xa[i, :], Ya[j, :], Xb[i, :], Yb[j, :])
    return total


def col_wedge_bilinear(Xa, Ya, Xb, Yb) -> complex:
    total = 0j
    for i in range(n):
        for j in range(n):
            total += wedge_inner(Xa[:, i], Ya[:, j], Xb[:, i], Yb[:, j])
    return total


def row_wedge_norm2(X, Y) -> float:
    return float(np.real(row_wedge_bilinear(X, Y, X, Y)))


def col_wedge_norm2(X, Y) -> float:
    return float(np.real(col_wedge_bilinear(X, Y, X, Y)))


def scalar_data(Uframe: np.ndarray, Vframe: np.ndarray) -> dict[str, Any]:
    A, B, T, D, M, tr = blocks(Uframe, Vframe)
    X1, X2 = mat(Uframe[:, 0]), mat(Uframe[:, 1])
    Y1, Y2 = mat(Vframe[:, 0]), mat(Vframe[:, 1])
    S = list(CROSS)
    M2 = M[np.ix_(S, S)]
    D2 = D[np.ix_(S, S)]
    delta = float(np.real(np.linalg.det(M2)))
    mixed_offdiag = (
        row_wedge_bilinear(X1, Y2, X2, Y1)
        + col_wedge_bilinear(X1, Y2, X2, Y1)
        + 0.5 * np.conjugate(tr[0]) * tr[3]
    )
    same_pair_offdiag = (
        row_wedge_bilinear(X1, Y1, X2, Y2)
        + col_wedge_bilinear(X1, Y1, X2, Y2)
        + 0.5 * np.conjugate(tr[0]) * tr[3]
    )
    mixed_norm_12 = row_wedge_norm2(X1, Y2) + col_wedge_norm2(X1, Y2) + 0.5 * abs(np.vdot(Y2, X1)) ** 2
    mixed_norm_21 = row_wedge_norm2(X2, Y1) + col_wedge_norm2(X2, Y1) + 0.5 * abs(np.vdot(Y1, X2)) ** 2
    return {
        "D1": float(np.real(M[0, 0])),
        "D2": float(np.real(M[3, 3])),
        "M03": M[0, 3],
        "delta": delta,
        "det_D": float(np.real(np.linalg.det(D2))),
        "mixed_offdiag": mixed_offdiag,
        "same_pair_offdiag": same_pair_offdiag,
        "mixed_offdiag_error": float(abs(M[0, 3] - mixed_offdiag)),
        "same_pair_mismatch": float(abs(M[0, 3] - same_pair_offdiag)),
        "mixed_norm_12": float(np.real(mixed_norm_12)),
        "mixed_norm_21": float(np.real(mixed_norm_21)),
        "margin_D1_minus_mixed12": float(np.real(M[0, 0] - mixed_norm_12)),
        "margin_D2_minus_mixed21": float(np.real(M[3, 3] - mixed_norm_21)),
        "orthogonality_U12": complex(np.vdot(Uframe[:, 0], Uframe[:, 1])),
        "orthogonality_V12": complex(np.vdot(Vframe[:, 0], Vframe[:, 1])),
        "eig_M2": np.linalg.eigvalsh(M2),
        "eig_D2": np.linalg.eigvalsh(D2),
    }


def product_example() -> tuple[np.ndarray, np.ndarray]:
    F = np.zeros((N, 2), complex)
    F[0, 0] = 1.0      # E_00
    F[1, 1] = 1.0      # E_01
    return F, F


def traceless_example() -> tuple[np.ndarray, np.ndarray]:
    F = np.zeros((N, 2), complex)
    F[0, 0] = 1.0      # E_00
    F[5, 1] = 1.0      # E_11
    return F, F


def complex_json(z: complex) -> dict[str, float]:
    return {"re": float(np.real(z)), "im": float(np.imag(z))}


def to_jsonable(x: Any) -> Any:
    if isinstance(x, dict):
        return {k: to_jsonable(v) for k, v in x.items()}
    if isinstance(x, tuple):
        return [to_jsonable(v) for v in x]
    if isinstance(x, list):
        return [to_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        if np.iscomplexobj(x):
            return [[complex_json(z) for z in row] for row in x] if x.ndim == 2 else [complex_json(z) for z in x]
        return x.tolist()
    if isinstance(x, complex) or np.iscomplexobj(x):
        return complex_json(complex(x))
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    return x


def random_summary(rng: np.random.Generator, samples: int) -> dict[str, Any]:
    max_mixed_error = 0.0
    max_same_mismatch = 0.0
    min_delta = (float("inf"), None)
    min_margin12 = (float("inf"), None)
    min_margin21 = (float("inf"), None)
    max_orth = 0.0
    for s in range(samples):
        U, V = rand_frame(2, rng), rand_frame(2, rng)
        d = scalar_data(U, V)
        max_mixed_error = max(max_mixed_error, d["mixed_offdiag_error"])
        max_same_mismatch = max(max_same_mismatch, d["same_pair_mismatch"])
        max_orth = max(max_orth, abs(d["orthogonality_U12"]), abs(d["orthogonality_V12"]))
        if d["delta"] < min_delta[0]:
            min_delta = (d["delta"], s)
        if d["margin_D1_minus_mixed12"] < min_margin12[0]:
            min_margin12 = (d["margin_D1_minus_mixed12"], s)
        if d["margin_D2_minus_mixed21"] < min_margin21[0]:
            min_margin21 = (d["margin_D2_minus_mixed21"], s)
    return {
        "samples": samples,
        "max_mixed_offdiag_identity_error": max_mixed_error,
        "max_same_pair_polarization_mismatch": max_same_mismatch,
        "min_delta": min_delta,
        "min_margin_D1_minus_mixed12": min_margin12,
        "min_margin_D2_minus_mixed21": min_margin21,
        "max_frame_orthogonality_residual": max_orth,
    }


def sparse_summary() -> dict[str, Any]:
    coords = list(itertools.combinations(range(N), 2))
    total = 0
    max_mixed_error = 0.0
    min_delta = (float("inf"), None)
    min_margin12 = (float("inf"), None)
    min_margin21 = (float("inf"), None)
    negative_margin12 = 0
    negative_margin21 = 0
    for us in coords:
        U = np.zeros((N, 2), complex)
        U[us[0], 0] = 1.0
        U[us[1], 1] = 1.0
        for vs in coords:
            V = np.zeros((N, 2), complex)
            V[vs[0], 0] = 1.0
            V[vs[1], 1] = 1.0
            d = scalar_data(U, V)
            total += 1
            max_mixed_error = max(max_mixed_error, d["mixed_offdiag_error"])
            if d["delta"] < min_delta[0]:
                min_delta = (d["delta"], (us, vs))
            if d["margin_D1_minus_mixed12"] < min_margin12[0]:
                min_margin12 = (d["margin_D1_minus_mixed12"], (us, vs))
            if d["margin_D2_minus_mixed21"] < min_margin21[0]:
                min_margin21 = (d["margin_D2_minus_mixed21"], (us, vs))
            if d["margin_D1_minus_mixed12"] < -1e-12:
                negative_margin12 += 1
            if d["margin_D2_minus_mixed21"] < -1e-12:
                negative_margin21 += 1
    return {
        "total": total,
        "max_mixed_offdiag_identity_error": max_mixed_error,
        "min_delta": min_delta,
        "min_margin_D1_minus_mixed12": min_margin12,
        "min_margin_D2_minus_mixed21": min_margin21,
        "negative_margin12_count": negative_margin12,
        "negative_margin21_count": negative_margin21,
    }


def local_opt_summary(rng: np.random.Generator, starts: int, maxiter: int) -> dict[str, Any]:
    if minimize is None:
        return {"scipy_available": False}
    targets = {
        "delta": lambda d: d["delta"],
        "margin_D1_minus_mixed12": lambda d: d["margin_D1_minus_mixed12"],
        "margin_D2_minus_mixed21": lambda d: d["margin_D2_minus_mixed21"],
    }
    out: dict[str, Any] = {"scipy_available": True, "starts": starts, "maxiter": maxiter}
    for name, getter in targets.items():
        best = (float("inf"), None)
        for k in range(starts):
            w0 = rng.normal(size=8 * N)

            def obj(w):
                U, V = frame_from_unconstrained(w)
                return float(getter(scalar_data(U, V)))

            res = minimize(obj, w0, method="BFGS", options={"maxiter": maxiter, "gtol": 1e-7})
            if float(res.fun) < best[0]:
                Ubest, Vbest = frame_from_unconstrained(res.x)
                dbest = scalar_data(Ubest, Vbest)
                best = (
                    float(res.fun),
                    {
                        "start": k,
                        "success": bool(res.success),
                        "message": str(res.message),
                        "nit": int(res.nit),
                        "delta_at_best": dbest["delta"],
                        "identity_error_at_best": dbest["mixed_offdiag_error"],
                    },
                )
        out["best_" + name] = best
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=9009)
    ap.add_argument("--samples", type=int, default=5000)
    ap.add_argument("--opt-starts", type=int, default=6)
    ap.add_argument("--maxiter", type=int, default=120)
    ap.add_argument("--out", type=Path, default=Path("research_harness/logs/LOOP-0009_mixed_plucker_probe_seed9009.json"))
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    examples = {}
    for name, maker in [("product", product_example), ("traceless", traceless_example)]:
        U, V = maker()
        examples[name] = scalar_data(U, V)

    results = {
        "seed": args.seed,
        "status": "mixed_identity_found_but_simple_cauchy_ansatz_obstructed_not_proof",
        "interpretation": {
            "exact_identity": "M03 equals mixed row wedges + mixed column wedges + 1/2 conjugate(t1)t2 to roundoff",
            "failed_ansatz": "Cauchy on these mixed wedge vectors would require D1>=||W12||^2 and D2>=||W21||^2; both margins are negative on the constraint manifold",
            "orthonormality_multipliers": "<X1,X2> and <Y1,Y2> are zero after QR; adding their multiples cannot repair negative margins on the actual constrained samples",
        },
        "examples": examples,
        "random_summary": random_summary(rng, args.samples),
        "sparse_coordinate_summary": sparse_summary(),
        "local_optimization_summary": local_opt_summary(rng, args.opt_starts, args.maxiter),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(to_jsonable(results), indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(to_jsonable({
        "status": results["status"],
        "random_summary": results["random_summary"],
        "sparse_coordinate_summary": results["sparse_coordinate_summary"],
        "local_optimization_summary": results["local_optimization_summary"],
        "wrote": str(args.out),
    }), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
