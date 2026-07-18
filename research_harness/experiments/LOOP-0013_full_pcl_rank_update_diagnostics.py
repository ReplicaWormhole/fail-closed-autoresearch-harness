#!/usr/bin/env python3
"""LOOP-0013 full-PCL trace-coupled rank-one-update diagnostics.

Fail-closed lane artifact for U-0002 / WS-full-pcl-certificate.

The admissible target is the full 4x4 Hermitian matrix

    M = D + (1/2) conjugate(t) t^T,      D = 2I - A - B,

not D alone.  This script checks reproducible coordinate/random diagnostics for
(1) the rank-one determinant identity on every principal subset,
(2) the sign behavior of det(D_S), update term t_S^T adj(D_S)conj(t_S), and
    det(M_S),
(3) full-M LDL pivot-order behavior, while explicitly recording D-only failures.

It does not certify PCL; it records the exact trace-coupled objects that remain
to be proved by a symbolic Gram/SOS/Schur certificate.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
LOOP12_PATH = ROOT / "research_harness/experiments/LOOP-0012_trace_coupled_pivot_candidate.py"
spec = importlib.util.spec_from_file_location("loop12", LOOP12_PATH)
assert spec is not None and spec.loader is not None
loop12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop12)

TOL = 1e-10


def adjugate(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    if n == 1:
        return np.ones((1, 1), dtype=np.complex128)
    Adj = np.empty_like(A, dtype=np.complex128)
    for i in range(n):
        for j in range(n):
            # adj(A)[i,j] = cofactor(A)[j,i]
            minor = np.delete(np.delete(A, j, axis=0), i, axis=1)
            Adj[i, j] = ((-1) ** (i + j)) * np.linalg.det(minor)
    return Adj


def det_identity_terms(D: np.ndarray, t: np.ndarray, M: np.ndarray, S: tuple[int, ...]) -> dict[str, Any]:
    Ds = D[np.ix_(S, S)]
    Ms = M[np.ix_(S, S)]
    ts = t[list(S)]
    detD = complex(np.linalg.det(Ds))
    detM = complex(np.linalg.det(Ms))
    q = complex(ts @ adjugate(Ds) @ np.conjugate(ts))
    rhs = detD + 0.5 * q
    return {
        "S": list(S),
        "detD": float(detD.real),
        "update_q": float(q.real),
        "detM": float(detM.real),
        "identity_abs_residual": float(abs(detM - rhs)),
    }


def empty_size_stats() -> dict[str, Any]:
    return {
        str(k): {
            "min_detM": {"value": math.inf, "case": None},
            "min_detD": {"value": math.inf, "case": None},
            "min_update_q": {"value": math.inf, "case": None},
            "negative_detM_count": 0,
            "negative_detD_count": 0,
            "negative_update_q_count": 0,
            "zero_detM_count": 0,
            "max_identity_abs_residual": 0.0,
        }
        for k in range(1, 5)
    }


def update_stats(stats: dict[str, Any], terms: dict[str, Any], case: dict[str, Any]) -> None:
    st = stats[str(len(terms["S"]))]
    for key, field in [("min_detM", "detM"), ("min_detD", "detD"), ("min_update_q", "update_q")]:
        val = terms[field]
        if val < st[key]["value"]:
            st[key] = {"value": val, "case": {**case, **terms}}
    st["negative_detM_count"] += int(terms["detM"] < -TOL)
    st["negative_detD_count"] += int(terms["detD"] < -TOL)
    st["negative_update_q_count"] += int(terms["update_q"] < -TOL)
    st["zero_detM_count"] += int(abs(terms["detM"]) <= TOL)
    st["max_identity_abs_residual"] = max(st["max_identity_abs_residual"], terms["identity_abs_residual"])


def coordinate_frame(i: int, j: int) -> np.ndarray:
    F = np.zeros((16, 2), dtype=np.complex128)
    F[i, 0] = 1.0
    F[j, 1] = 1.0
    return F


def coordinate_scan() -> dict[str, Any]:
    planes = [(I, coordinate_frame(*I)) for I in itertools.combinations(range(16), 2)]
    stats = empty_size_stats()
    fixed_perm_stats = {str(list(p)): {"bad_count": 0, "min_success_pivot": math.inf, "first_bad_case": None} for p in itertools.permutations(range(4))}
    summary = {
        "total_plane_pairs": 0,
        "M_negative_eig_count": 0,
        "D_negative_eig_count": 0,
        "D_no_nonnegative_pivot_order_count": 0,
        "M_no_nonnegative_pivot_order_count": 0,
        "min_eig_M": {"value": math.inf, "case": None},
        "min_eig_D": {"value": math.inf, "case": None},
    }
    for IP, U in planes:
        for IQ, V in planes:
            D, t, M = loop12.matrices(U, V)
            case = {"P": list(IP), "Q": list(IQ)}
            summary["total_plane_pairs"] += 1
            eigM = np.linalg.eigvalsh(M)
            eigD = np.linalg.eigvalsh(D)
            minM = float(eigM[0])
            minD = float(eigD[0])
            summary["M_negative_eig_count"] += int(minM < -TOL)
            summary["D_negative_eig_count"] += int(minD < -TOL)
            if minM < summary["min_eig_M"]["value"]:
                summary["min_eig_M"] = {"value": minM, "case": {**case, "eig_M": [float(x) for x in eigM]}}
            if minD < summary["min_eig_D"]["value"]:
                summary["min_eig_D"] = {"value": minD, "case": {**case, "eig_D": [float(x) for x in eigD]}}
            rpM = loop12.pivot_report(M)
            rpD = loop12.pivot_report(D)
            summary["M_no_nonnegative_pivot_order_count"] += int(rpM["nonnegative_sequence_count"] == 0)
            summary["D_no_nonnegative_pivot_order_count"] += int(rpD["nonnegative_sequence_count"] == 0)
            for perm in itertools.permutations(range(4)):
                piv = loop12.ldl_pivots(M, perm)
                pst = fixed_perm_stats[str(list(perm))]
                if piv is None or min(piv) < -TOL:
                    pst["bad_count"] += 1
                    if pst["first_bad_case"] is None:
                        pst["first_bad_case"] = {**case, "perm": list(perm), "pivots": piv, "eig_M": [float(x) for x in eigM]}
                else:
                    pst["min_success_pivot"] = min(pst["min_success_pivot"], float(min(piv)))
            for k in range(1, 5):
                for S in itertools.combinations(range(4), k):
                    update_stats(stats, det_identity_terms(D, t, M, S), case)
    good_fixed = [p for p, st in fixed_perm_stats.items() if st["bad_count"] == 0]
    return {"summary": summary, "principal_subset_stats": stats, "fixed_M_pivot_order_stats": fixed_perm_stats, "coordinate_good_fixed_M_pivot_orders": good_fixed}


def random_scan(seed: int, trials: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    stats = empty_size_stats()
    out: dict[str, Any] = {
        "seed": seed,
        "trials": trials,
        "M_negative_eig_count": 0,
        "D_negative_eig_count": 0,
        "M_no_nonnegative_pivot_order_count": 0,
        "D_no_nonnegative_pivot_order_count": 0,
        "worst_M_min_eig": {"value": math.inf, "case": None},
        "worst_D_min_eig": {"value": math.inf, "case": None},
    }
    for trial in range(trials):
        U = loop12.loop8.random_frame(rng)
        V = loop12.loop8.random_frame(rng)
        D, t, M = loop12.matrices(U, V)
        case = {"trial": trial}
        eigM = np.linalg.eigvalsh(M)
        eigD = np.linalg.eigvalsh(D)
        minM = float(eigM[0])
        minD = float(eigD[0])
        out["M_negative_eig_count"] += int(minM < -TOL)
        out["D_negative_eig_count"] += int(minD < -TOL)
        out["M_no_nonnegative_pivot_order_count"] += int(loop12.pivot_report(M)["nonnegative_sequence_count"] == 0)
        out["D_no_nonnegative_pivot_order_count"] += int(loop12.pivot_report(D)["nonnegative_sequence_count"] == 0)
        if minM < out["worst_M_min_eig"]["value"]:
            out["worst_M_min_eig"] = {"value": minM, "case": {"trial": trial, "eig_M": [float(x) for x in eigM]}}
        if minD < out["worst_D_min_eig"]["value"]:
            out["worst_D_min_eig"] = {"value": minD, "case": {"trial": trial, "eig_D": [float(x) for x in eigD]}}
        for k in range(1, 5):
            for S in itertools.combinations(range(4), k):
                update_stats(stats, det_identity_terms(D, t, M, S), case)
    out["principal_subset_stats"] = stats
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=13013)
    ap.add_argument("--trials", type=int, default=500)
    args = ap.parse_args()

    coordinate = coordinate_scan()
    random = random_scan(args.seed, args.trials)
    result = {
        "loop": "LOOP-0013",
        "lane": "WS-full-pcl-certificate / trace-coupled Schur-Gram-SOS-rank-one-update diagnostics",
        "success_condition_met": False,
        "D_only_route_status": "explicitly rejected: D-only pivots/minors are false and are not used as a certificate target",
        "proved_algebraic_identity": "For every principal S, det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S), the matrix determinant lemma/adjugate polynomial identity for M_S=D_S+(1/2)conj(t_S)t_S^T.",
        "unproved_certificate_target": "Need a symbolic Gram/SOS/Schur proof that det(D_S)+(1/2)q_S >= 0 for all principal S, or an equivalent full Hermitian Schur complement certificate for M itself.",
        "coordinate_scan": coordinate,
        "random_scan": random,
    }
    outp = ROOT / f"research_harness/logs/LOOP-0013_full_pcl_rank_update_seed{args.seed}.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(result, indent=2) + "\n")

    print(json.dumps({
        "loop": "LOOP-0013",
        "seed": args.seed,
        "trials": args.trials,
        "coordinate_total_pairs": coordinate["summary"]["total_plane_pairs"],
        "coordinate_M_negative_eig_count": coordinate["summary"]["M_negative_eig_count"],
        "coordinate_D_negative_eig_count": coordinate["summary"]["D_negative_eig_count"],
        "coordinate_M_no_nonnegative_pivot_order_count": coordinate["summary"]["M_no_nonnegative_pivot_order_count"],
        "coordinate_D_no_nonnegative_pivot_order_count": coordinate["summary"]["D_no_nonnegative_pivot_order_count"],
        "coordinate_good_fixed_M_pivot_orders": coordinate["coordinate_good_fixed_M_pivot_orders"],
        "coordinate_size4_min_detM": coordinate["principal_subset_stats"]["4"]["min_detM"],
        "coordinate_size4_min_detD": coordinate["principal_subset_stats"]["4"]["min_detD"],
        "coordinate_max_det_identity_residual_size4": coordinate["principal_subset_stats"]["4"]["max_identity_abs_residual"],
        "random_M_negative_eig_count": random["M_negative_eig_count"],
        "random_D_negative_eig_count": random["D_negative_eig_count"],
        "random_worst_M_min_eig": random["worst_M_min_eig"],
        "random_size4_min_detM": random["principal_subset_stats"]["4"]["min_detM"],
        "random_size4_min_update_q": random["principal_subset_stats"]["4"]["min_update_q"],
        "log": str(outp),
    }, indent=2))


if __name__ == "__main__":
    main()
