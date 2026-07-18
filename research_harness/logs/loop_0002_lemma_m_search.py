#!/usr/bin/env python3
"""LOOP-0002 numerical counterexample hunt for Lemma M.

Search variables: two Hilbert-Schmidt orthonormal 4x4 pairs X1,X2 and Y1,Y2.
Objectives:
  * lambda_max(H - 2I)
  * determinant violation |H12|^2 - D1 D2 for K=2I-H
If a positive Lemma M violation is found, reconstruct a rank-two SVD-form C along
its top violating vector and compute the original CLAIM-0001 partial-trace gap.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

N = 4
D = N * N


def cmat_from_real(x: np.ndarray, rows: int = D, cols: int = 2) -> np.ndarray:
    n = rows * cols
    return (x[:n] + 1j * x[n:2*n]).reshape(rows, cols)


def real_from_cmat(z: np.ndarray) -> np.ndarray:
    return np.concatenate([z.real.ravel(), z.imag.ravel()])


def orth_frame_from_real(x: np.ndarray) -> np.ndarray:
    """Map unconstrained real vector to a complex D x 2 orthonormal frame."""
    z = cmat_from_real(x)
    q, r = np.linalg.qr(z)
    # Fix QR column phases for a mostly deterministic chart.
    diag = np.diag(r)
    phase = np.ones(2, dtype=np.complex128)
    nz = np.abs(diag) > 1e-14
    phase[nz] = diag[nz] / np.abs(diag[nz])
    return q[:, :2] * phase.conj()[None, :]


def random_frame(rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(D, 2)) + 1j * rng.normal(size=(D, 2))
    q, _ = np.linalg.qr(z)
    return q[:, :2]


def frames_from_param(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return orth_frame_from_real(x[:2*D*2]), orth_frame_from_real(x[2*D*2:])


def param_from_frames(Xf: np.ndarray, Yf: np.ndarray) -> np.ndarray:
    return np.concatenate([real_from_cmat(Xf), real_from_cmat(Yf)])


def mats_from_frames(Xf: np.ndarray, Yf: np.ndarray):
    X = [Xf[:, i].reshape(N, N) for i in range(2)]
    Y = [Yf[:, i].reshape(N, N) for i in range(2)]
    return X, Y


def inner(A: np.ndarray, B: np.ndarray) -> complex:
    return np.vdot(A, B)  # tr(A^* B)


def lemma_quantities(Xf: np.ndarray, Yf: np.ndarray) -> dict[str, Any]:
    X, Y = mats_from_frames(Xf, Yf)
    L = [X[i] @ Y[i].conj().T for i in range(2)]
    R = [X[i].conj().T @ Y[i] for i in range(2)]
    t = np.array([np.trace(X[i].conj().T @ Y[i]) for i in range(2)], dtype=np.complex128)
    H = np.empty((2, 2), dtype=np.complex128)
    for i in range(2):
        for j in range(2):
            H[i, j] = inner(L[i], L[j]) + inner(R[i], R[j]) - 0.5 * np.conj(t[i]) * t[j]
    H = (H + H.conj().T) / 2.0
    evals, evecs = np.linalg.eigh(H)
    Dv = np.array([2.0 - H[i, i].real for i in range(2)])
    det_violation = float(abs(H[0, 1])**2 - Dv[0] * Dv[1])
    K = 2*np.eye(2) - H
    return {
        "H": H,
        "K": K,
        "evals": evals,
        "evecs": evecs,
        "lambda_violation": float(evals[-1].real - 2.0),
        "det_violation": det_violation,
        "D": Dv,
        "H12_abs2": float(abs(H[0, 1])**2),
        "t_abs2": [float(abs(v)**2) for v in t],
        "diag_H": [float(H[i, i].real) for i in range(2)],
        "orth_X_err": float(np.linalg.norm(Xf.conj().T @ Xf - np.eye(2))),
        "orth_Y_err": float(np.linalg.norm(Yf.conj().T @ Yf - np.eye(2))),
    }


def partial_traces(C: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    T = C.reshape(N, N, N, N)
    tr1 = np.einsum("abac->bc", T)
    tr2 = np.einsum("abcb->ac", T)
    return tr1, tr2


def claim_metrics(C: np.ndarray) -> dict[str, Any]:
    tr1, tr2 = partial_traces(C)
    pt1 = float(np.vdot(tr1, tr1).real)
    pt2 = float(np.vdot(tr2, tr2).real)
    norm2 = float(np.vdot(C, C).real)
    trace_abs2 = float(abs(np.trace(C))**2)
    sv = np.linalg.svd(C, compute_uv=False)
    return {
        "rank_num_1e-9": int((sv > 1e-9).sum()),
        "singular_values_first4": [float(v) for v in sv[:4]],
        "pt1": pt1,
        "pt2": pt2,
        "lhs": pt1 + pt2,
        "norm2": norm2,
        "trace_abs2": trace_abs2,
        "gap_alpha_0.5": float(pt1 + pt2 - 2*norm2 - 0.5*trace_abs2),
    }


def reconstruct_C(Xf: np.ndarray, Yf: np.ndarray, coeff_vec: np.ndarray) -> tuple[np.ndarray, list[float], list[float]]:
    """Build C in SVD form from a complex coefficient vector.

    Phases are absorbed into Y_i so the returned singular coefficients are nonnegative.
    """
    Xcols = [Xf[:, i] for i in range(2)]
    Ycols = []
    svals = []
    phases = []
    for i, z in enumerate(coeff_vec):
        phi = float(np.angle(z))
        phases.append(phi)
        svals.append(float(abs(z)))
        Ycols.append(np.exp(-1j * phi) * Yf[:, i])
    C = np.zeros((D, D), dtype=np.complex128)
    for s, x, y in zip(svals, Xcols, Ycols):
        C += s * np.outer(x, y.conj())
    return C, svals, phases


def compact(q: dict[str, Any]) -> dict[str, Any]:
    return {
        "lambda_violation": q["lambda_violation"],
        "det_violation": q["det_violation"],
        "lambda_max_H": float(q["evals"][-1].real),
        "lambda_min_K": float(np.linalg.eigvalsh(q["K"])[0].real),
        "D": [float(x) for x in q["D"]],
        "H12_abs2": q["H12_abs2"],
        "diag_H": q["diag_H"],
        "t_abs2": q["t_abs2"],
        "orth_X_err": q["orth_X_err"],
        "orth_Y_err": q["orth_Y_err"],
        "H": [[{"re": float(z.real), "im": float(z.imag)} for z in row] for row in q["H"]],
    }


@dataclass
class Candidate:
    label: str
    source: str
    lemma: dict[str, Any]
    claim: dict[str, Any] | None = None
    coeff_singular_values: list[float] | None = None
    coeff_phases: list[float] | None = None


def equality_frames(kind: str) -> tuple[np.ndarray, np.ndarray]:
    Xf = np.zeros((D, 2), dtype=np.complex128)
    Yf = np.zeros((D, 2), dtype=np.complex128)
    if kind == "traceless_diag":
        # X1=Y1=E00; X2=-E11, Y2=E11 gives sharp H eigenvalue 2.
        Xf[0*N + 0, 0] = 1; Yf[0*N + 0, 0] = 1
        Xf[1*N + 1, 1] = -1; Yf[1*N + 1, 1] = 1
    elif kind == "product_projection":
        # X1=Y1=E00; X2=Y2=E10 gives C=(P2 tensor E00)/sqrt2 along (1,1)/sqrt2.
        Xf[0*N + 0, 0] = 1; Yf[0*N + 0, 0] = 1
        Xf[1*N + 0, 1] = 1; Yf[1*N + 0, 1] = 1
    elif kind == "phase_gauge_violation":
        # Exact counterexample to the operator Lemma M as stated:
        # X1=Y1=E00, X2=E01, Y2=i E01. Then H has diagonal 3/2 and
        # off-diagonal -3i/2, so lambda_max(H)=3 and |H12|^2-D1D2=2.
        # The corresponding top complex coefficient vector does not directly
        # give positive singular values without rephasing Y2; the reconstructed
        # rank-two C is therefore used below as a CLAIM-0001 consistency test.
        Xf[0*N + 0, 0] = 1; Yf[0*N + 0, 0] = 1
        Xf[0*N + 1, 1] = 1; Yf[0*N + 1, 1] = 1j
    else:
        raise ValueError(kind)
    return Xf, Yf


def evaluate_candidate(label: str, source: str, Xf: np.ndarray, Yf: np.ndarray) -> Candidate:
    q = lemma_quantities(Xf, Yf)
    top_vec = q["evecs"][:, -1]
    C, svals, phases = reconstruct_C(Xf, Yf, top_vec)
    return Candidate(label=label, source=source, lemma=compact(q), claim=claim_metrics(C),
                     coeff_singular_values=svals, coeff_phases=phases)


def optimize_seed(x0: np.ndarray, objective: str, maxiter: int) -> tuple[np.ndarray, dict[str, Any]]:
    from scipy.optimize import minimize

    def fun(x: np.ndarray) -> float:
        Xf, Yf = frames_from_param(x)
        q = lemma_quantities(Xf, Yf)
        if objective == "lambda":
            return -q["lambda_violation"]
        if objective == "det":
            return -q["det_violation"]
        raise ValueError(objective)

    res = minimize(fun, x0, method="Powell", options={"maxiter": maxiter, "ftol": 1e-12, "xtol": 1e-12, "disp": False})
    return np.asarray(res.x), {"success": bool(res.success), "nit": int(getattr(res, "nit", -1)), "nfev": int(getattr(res, "nfev", -1)), "message": str(res.message), "final_objective": objective, "final_value": -float(res.fun)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=2002)
    ap.add_argument("--samples", type=int, default=30000)
    ap.add_argument("--restarts", type=int, default=8)
    ap.add_argument("--maxiter", type=int, default=120)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    report: dict[str, Any] = {"seed": args.seed, "samples": args.samples, "restarts": args.restarts, "maxiter": args.maxiter, "candidates": [], "opt_logs": []}

    for kind in ["traceless_diag", "product_projection", "phase_gauge_violation"]:
        Xf, Yf = equality_frames(kind)
        label_prefix = "known_equality" if kind != "phase_gauge_violation" else "exact_lemma_m_counterexample"
        report["candidates"].append(asdict(evaluate_candidate(f"{label_prefix}_{kind}", "exact_seed", Xf, Yf)))

    best: dict[str, tuple[float, np.ndarray, np.ndarray]] = {"lambda": (-1e99, None, None), "det": (-1e99, None, None)}  # type: ignore
    lam_vals = []
    det_vals = []
    for k in range(args.samples):
        Xf = random_frame(rng)
        Yf = random_frame(rng)
        q = lemma_quantities(Xf, Yf)
        lam_vals.append(q["lambda_violation"])
        det_vals.append(q["det_violation"])
        if q["lambda_violation"] > best["lambda"][0]:
            best["lambda"] = (q["lambda_violation"], Xf.copy(), Yf.copy())
        if q["det_violation"] > best["det"][0]:
            best["det"] = (q["det_violation"], Xf.copy(), Yf.copy())

    report["random_summary"] = {
        "lambda_violation_max": float(np.max(lam_vals)),
        "lambda_violation_q99": float(np.quantile(lam_vals, 0.99)),
        "det_violation_max": float(np.max(det_vals)),
        "det_violation_q99": float(np.quantile(det_vals, 0.99)),
        "positive_lambda_count_gt_1e-10": int(np.sum(np.array(lam_vals) > 1e-10)),
        "positive_det_count_gt_1e-10": int(np.sum(np.array(det_vals) > 1e-10)),
    }

    seeds: list[tuple[str, str, np.ndarray]] = []
    for obj in ["lambda", "det"]:
        _, Xf, Yf = best[obj]
        report["candidates"].append(asdict(evaluate_candidate(f"random_best_{obj}", "random", Xf, Yf)))
        seeds.append((f"random_best_{obj}", obj, param_from_frames(Xf, Yf)))
    for i in range(args.restarts):
        seeds.append((f"fresh_{i}_lambda", "lambda", param_from_frames(random_frame(rng), random_frame(rng))))
        seeds.append((f"fresh_{i}_det", "det", param_from_frames(random_frame(rng), random_frame(rng))))

    for label, obj, x0 in seeds:
        try:
            xopt, log = optimize_seed(x0, obj, args.maxiter)
            Xf, Yf = frames_from_param(xopt)
            report["candidates"].append(asdict(evaluate_candidate(f"optimized_{label}_{obj}", "scipy_powell", Xf, Yf)))
            report["opt_logs"].append({"label": f"optimized_{label}_{obj}", **log})
        except Exception as e:
            report["opt_logs"].append({"label": label, "objective": obj, "error": repr(e)})

    # Identify best final records.
    cands = report["candidates"]
    report["best_by_lambda"] = max(cands, key=lambda c: c["lemma"]["lambda_violation"])
    report["best_by_det"] = max(cands, key=lambda c: c["lemma"]["det_violation"])
    report["violation_found_tol_1e-8"] = bool(report["best_by_lambda"]["lemma"]["lambda_violation"] > 1e-8 or report["best_by_det"]["lemma"]["det_violation"] > 1e-8)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True))
    print(json.dumps({
        "seed": report["seed"],
        "samples": report["samples"],
        "random_summary": report["random_summary"],
        "best_by_lambda": {"label": report["best_by_lambda"]["label"], "lemma": report["best_by_lambda"]["lemma"], "claim": report["best_by_lambda"]["claim"]},
        "best_by_det": {"label": report["best_by_det"]["label"], "lemma": report["best_by_det"]["lemma"], "claim": report["best_by_det"]["claim"]},
        "violation_found_tol_1e-8": report["violation_found_tol_1e-8"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
