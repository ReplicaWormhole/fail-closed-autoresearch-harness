#!/usr/bin/env python3
"""
LOOP-0005 PCL numerical/eigenvalue lane.

For rank-two projections P,Q on H=C^4 tensor C^4, form the compression of

    Phi = tr_1^* tr_1 + tr_2^* tr_2 - (1/2) tr^* tr - 2 I

on Hom(QH,PH).  With orthonormal bases p1,p2 and q1,q2, the four basis
operators are E_ij=|p_i><q_j|.  The 4x4 Hermitian compression matrix is
K_ab=<E_a,Phi(E_b)>; a robust positive largest eigenvalue would give a
positive-gap rank <=2 counterexample.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

try:
    from scipy.optimize import minimize as scipy_minimize
    SCIPY = True
except Exception:
    scipy_minimize = None
    SCIPY = False

N = 16
D = 4


def vec_unit(i: int, a: int) -> np.ndarray:
    v = np.zeros(N, dtype=np.complex128)
    v[i * D + a] = 1.0
    return v


def mat_unit(i: int, j: int) -> np.ndarray:
    M = np.zeros((D, D), dtype=np.complex128)
    M[i, j] = 1.0
    return M


def mat_to_vec(M: np.ndarray) -> np.ndarray:
    return np.asarray(M, dtype=np.complex128).reshape(N)


def partial_traces(C: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X = C.reshape(D, D, D, D)  # row=(i,a), col=(j,b)
    tr1 = np.einsum("iaib->ab", X)  # trace first tensor factor
    tr2 = np.einsum("iaja->ij", X)  # trace second tensor factor
    return tr1, tr2


def phi(C: np.ndarray) -> np.ndarray:
    tr1, tr2 = partial_traces(C)
    tr = np.trace(C)
    Y = np.zeros_like(C, dtype=np.complex128)
    Y4 = Y.reshape(D, D, D, D)
    # tr_1^*: (tr1)_{ab} placed where first row/col indices agree.
    for i in range(D):
        Y4[i, :, i, :] += tr1
    # tr_2^*: (tr2)_{ij} placed where second row/col indices agree.
    for a in range(D):
        Y4[:, a, :, a] += tr2
    Y -= 0.5 * tr * np.eye(N, dtype=np.complex128)
    Y -= 2.0 * C
    return Y


def gap(C: np.ndarray) -> float:
    tr1, tr2 = partial_traces(C)
    return float((np.vdot(tr1, tr1) + np.vdot(tr2, tr2) - 0.5 * abs(np.trace(C)) ** 2 - 2.0 * np.vdot(C, C)).real)


def rank_and_sv(C: np.ndarray, tol: float = 1e-10) -> tuple[int, list[float]]:
    s = np.linalg.svd(C, compute_uv=False)
    return int(np.sum(s > tol)), [float(x) for x in s[:8]]


def orthonormalize(Z: np.ndarray) -> np.ndarray:
    Q, R = np.linalg.qr(Z)
    # deterministic phase convention for reproducibility
    for k in range(Q.shape[1]):
        diag = R[k, k]
        if abs(diag) > 0:
            Q[:, k] *= diag / abs(diag)
    return Q[:, :2]


def random_frame(rng: np.random.Generator) -> np.ndarray:
    Z = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    return orthonormalize(Z)


def frame_from_real(z: np.ndarray) -> np.ndarray:
    Z = z[: 2 * N].reshape(N, 2) + 1j * z[2 * N : 4 * N].reshape(N, 2)
    # avoid singular all-zero starts deterministically
    if np.linalg.norm(Z) < 1e-14:
        Z = np.eye(N, 2, dtype=np.complex128)
    return orthonormalize(Z)


def basis_ops(P: np.ndarray, Q: np.ndarray) -> list[np.ndarray]:
    return [np.outer(P[:, i], Q[:, j].conj()) for i in range(2) for j in range(2)]


def compression(P: np.ndarray, Q: np.ndarray) -> np.ndarray:
    Es = basis_ops(P, Q)
    Phis = [phi(E) for E in Es]
    K = np.array([[np.vdot(Es[a], Phis[b]) for b in range(4)] for a in range(4)], dtype=np.complex128)
    return 0.5 * (K + K.conj().T)


def compression_summary(P: np.ndarray, Q: np.ndarray, name: str | None = None) -> dict[str, Any]:
    K = compression(P, Q)
    w, V = np.linalg.eigh(K)
    imax = int(np.argmax(w))
    coeff = V[:, imax]
    Es = basis_ops(P, Q)
    C = np.zeros((N, N), dtype=np.complex128)
    for k in range(4):
        C += coeff[k] * Es[k]
    C /= np.linalg.norm(C, "fro")
    g = gap(C)
    r, sv = rank_and_sv(C)
    return {
        "name": name,
        "eigvals": [float(x) for x in w],
        "lambda_max": float(w[imax]),
        "hermitian_residual_fro": float(np.linalg.norm(K - K.conj().T, "fro")),
        "top_eigenvector_coeffs": [[float(z.real), float(z.imag)] for z in coeff],
        "reconstructed_gap": g,
        "reconstructed_rank_tol_1e_10": r,
        "reconstructed_leading_singular_values": sv,
        "gap_minus_lambda_max": float(g - w[imax]),
    }


def support_from_C(C: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    U, s, Vh = np.linalg.svd(C, full_matrices=False)
    return U[:, :2], Vh.conj().T[:, :2]


def equality_cases() -> list[dict[str, Any]]:
    cases: list[tuple[str, np.ndarray]] = []
    # Known traceless diagonal equality: (|00><00|-|11><11|)/sqrt(2).
    C = (np.outer(vec_unit(0, 0), vec_unit(0, 0).conj()) - np.outer(vec_unit(1, 1), vec_unit(1, 1).conj())) / math.sqrt(2)
    cases.append(("traceless_diagonal_E00_minus_E11", C))
    # Product-projection equality: (diag(1,1,0,0) tensor |0><0|)/sqrt(2).
    C = (np.outer(vec_unit(0, 0), vec_unit(0, 0).conj()) + np.outer(vec_unit(1, 0), vec_unit(1, 0).conj())) / math.sqrt(2)
    cases.append(("product_projection_P2_tensor_00", C))
    # LOOP-0002 phase-absorbed equality support: X1=Y1=E00, X2=E01,
    # with the coefficient phase absorbed so the original gap is equality.
    x1 = mat_to_vec(mat_unit(0, 0)); y1 = mat_to_vec(mat_unit(0, 0))
    x2 = mat_to_vec(mat_unit(0, 1)); y2 = mat_to_vec(mat_unit(0, 1))
    C = (np.outer(x1, y1.conj()) + np.outer(x2, y2.conj())) / math.sqrt(2)
    cases.append(("LOOP-0002_phase_absorbed_equality", C))

    out = []
    for name, C in cases:
        P, Q = support_from_C(C)
        item = compression_summary(P, Q, name)
        tr1, tr2 = partial_traces(C)
        r, sv = rank_and_sv(C)
        item["witness_gap"] = gap(C)
        item["witness_rank_tol_1e_10"] = r
        item["witness_leading_singular_values"] = sv
        item["witness_tr1_fro2"] = float(np.vdot(tr1, tr1).real)
        item["witness_tr2_fro2"] = float(np.vdot(tr2, tr2).real)
        item["witness_trace_abs2"] = float(abs(np.trace(C)) ** 2)
        out.append(item)
    return out


def random_search(samples: int, seed: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    best: dict[str, Any] | None = None
    positives = 0
    t0 = time.time()
    for k in range(samples):
        P = random_frame(rng); Q = random_frame(rng)
        s = compression_summary(P, Q)
        s["iter"] = k
        if s["lambda_max"] > 1e-10:
            positives += 1
        if best is None or s["lambda_max"] > best["lambda_max"]:
            best = s
    return {"samples": samples, "seed": seed, "positive_count_tol_1e_10": positives, "best": best, "elapsed_sec": time.time() - t0}


def optimize(seed: int, restarts: int, maxiter: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    best: dict[str, Any] | None = None
    t0 = time.time()

    def obj(z: np.ndarray) -> float:
        P = frame_from_real(z[: 4 * N])
        Q = frame_from_real(z[4 * N :])
        return -compression_summary(P, Q)["lambda_max"]

    records = []
    for r in range(restarts):
        z0 = rng.normal(size=8 * N)
        if SCIPY:
            assert scipy_minimize is not None
            res = scipy_minimize(obj, z0, method="BFGS", options={"maxiter": maxiter, "gtol": 1e-8})
            z = res.x
            success = bool(res.success)
            message = str(res.message)
            nit = int(getattr(res, "nit", -1))
        else:
            z = z0.copy()
            val = -obj(z)
            step = 0.2
            for _ in range(maxiter):
                cand = z + step * rng.normal(size=z.shape)
                cval = -obj(cand)
                if cval > val:
                    z, val = cand, cval
                step *= 0.995
            success = False
            message = "scipy unavailable; used deterministic random hill climb fallback"
            nit = maxiter
        P = frame_from_real(z[: 4 * N]); Q = frame_from_real(z[4 * N :])
        rec = compression_summary(P, Q)
        rec.update({"restart": r, "optimizer_success": success, "optimizer_message": message, "nit": nit})
        records.append({k: rec[k] for k in ["restart", "lambda_max", "reconstructed_gap", "optimizer_success", "optimizer_message", "nit"]})
        if best is None or rec["lambda_max"] > best["lambda_max"]:
            best = rec
    return {"seed": seed, "scipy": SCIPY, "restarts": restarts, "maxiter": maxiter, "best": best, "records": records, "elapsed_sec": time.time() - t0}


def self_check_adjoint(seed: int = 5005) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    C = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
    Dm = rng.normal(size=(N, N)) + 1j * rng.normal(size=(N, N))
    lhs = np.vdot(C, phi(Dm))
    rhs = (np.vdot(partial_traces(C)[0], partial_traces(Dm)[0]) +
           np.vdot(partial_traces(C)[1], partial_traces(Dm)[1]) -
           0.5 * np.conj(np.trace(C)) * np.trace(Dm) - 2.0 * np.vdot(C, Dm))
    qdiff = np.vdot(C, phi(C)).real - gap(C)
    return {"sesquilinear_abs_error": float(abs(lhs - rhs)), "quadratic_abs_error": float(abs(qdiff))}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=5005)
    ap.add_argument("--random", type=int, default=5000)
    ap.add_argument("--opt-restarts", type=int, default=8)
    ap.add_argument("--maxiter", type=int, default=200)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    t0 = time.time()
    out: dict[str, Any] = {
        "script": "LOOP-0005_pcl_compression_search.py",
        "claim": "PCL: every rank-two support compression of Phi is negative semidefinite",
        "seed": args.seed,
        "numpy_version": np.__version__,
        "python": sys.version,
        "platform": platform.platform(),
        "scipy_available": SCIPY,
        "self_check_adjoint": self_check_adjoint(args.seed),
        "equality_regressions": equality_cases(),
    }
    print("LOOP-0005 PCL compression search")
    print(json.dumps({"scipy_available": SCIPY, "self_check_adjoint": out["self_check_adjoint"]}, indent=2), flush=True)
    print("equality regressions:")
    for c in out["equality_regressions"]:
        print(json.dumps({"name": c["name"], "witness_gap": c["witness_gap"], "lambda_max": c["lambda_max"], "eigvals": c["eigvals"], "reconstructed_gap": c["reconstructed_gap"]}, sort_keys=True), flush=True)

    out["random_search"] = random_search(args.random, args.seed)
    print("random best:")
    print(json.dumps(out["random_search"]["best"], indent=2), flush=True)

    out["optimization"] = optimize(args.seed + 17, args.opt_restarts, args.maxiter)
    print("optimization best:")
    print(json.dumps(out["optimization"]["best"], indent=2), flush=True)

    # Best overall and robust-positive reconstruction check.
    candidates = [out["random_search"]["best"], out["optimization"]["best"]] + out["equality_regressions"]
    best_overall = max(candidates, key=lambda x: x["lambda_max"])
    out["best_overall"] = best_overall
    out["positive_robust_tol_1e_8"] = bool(best_overall["lambda_max"] > 1e-8 and best_overall["reconstructed_gap"] > 1e-8)
    out["elapsed_sec"] = time.time() - t0

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(out, indent=2, sort_keys=True))
    print("summary:")
    print(json.dumps({"best_lambda_max": best_overall["lambda_max"], "best_reconstructed_gap": best_overall["reconstructed_gap"], "positive_robust_tol_1e_8": out["positive_robust_tol_1e_8"], "out": args.out, "elapsed_sec": out["elapsed_sec"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
