#!/usr/bin/env python3
"""LOOP-0012 trace-coupled full-PCL pivot candidate diagnostics.

This is a fail-closed diagnostic for U-0002.  It deliberately refuses the false
D-only route.  The object under test is always

    M = D + (1/2) conjugate(t) t^T,     D = 2I - A - B,

and Schur pivots are taken on M itself.  The script records whether M has a
nonnegative one-by-one pivot order in controls/coordinate/random cases, while D
can fail on the same cases.  It also emits the exact trace-coupled Schur formula
that should be attacked symbolically next.
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
LOOP8_PATH = ROOT / "research_harness/experiments/LOOP-0008_full_pcl_search.py"
spec = importlib.util.spec_from_file_location("loop8", LOOP8_PATH)
assert spec is not None and spec.loader is not None
loop8 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop8)

TOL = 1e-10


def trace_vec(Uframe: np.ndarray, Vframe: np.ndarray) -> np.ndarray:
    vals = []
    for i in range(2):
        for a in range(2):
            U = loop8.mat(Uframe[:, i])
            V = loop8.mat(Vframe[:, a])
            vals.append(np.vdot(V.reshape(-1), U.reshape(-1)))
    return np.asarray(vals, dtype=np.complex128)


def matrices(U: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    A, B, _T, _M, _ = loop8.pcl_matrices(U, V)
    D = 2.0 * np.eye(4) - A - B
    D = (D + D.conj().T) / 2.0
    t = trace_vec(U, V)
    M = D + 0.5 * np.outer(np.conjugate(t), t)
    M = (M + M.conj().T) / 2.0
    return D, t, M


def coordinate_frame(i: int, j: int) -> np.ndarray:
    F = np.zeros((16, 2), dtype=np.complex128)
    F[i, 0] = 1.0
    F[j, 1] = 1.0
    return F


def ldl_pivots(H: np.ndarray, perm: tuple[int, ...]) -> list[float] | None:
    A = H[np.ix_(perm, perm)].copy()
    pivots: list[float] = []
    for k in range(4):
        p = float(A[k, k].real)
        pivots.append(p)
        if k == 3:
            break
        if abs(p) < 1e-11:
            return None
        v = A[k + 1 :, k].copy()
        A[k + 1 :, k + 1 :] -= np.outer(v, np.conjugate(v)) / p
        A[k + 1 :, k + 1 :] = (A[k + 1 :, k + 1 :] + A[k + 1 :, k + 1 :].conj().T) / 2.0
    return pivots


def pivot_report(H: np.ndarray) -> dict[str, Any]:
    seqs = []
    singular = 0
    nonnegative = 0
    negative = 0
    for perm in itertools.permutations(range(4)):
        piv = ldl_pivots(H, perm)
        if piv is None:
            singular += 1
            continue
        mn = min(piv)
        nonnegative += int(mn >= -TOL)
        negative += int(mn < -TOL)
        seqs.append({"perm": list(perm), "pivots": piv, "min_pivot": mn})
    seqs.sort(key=lambda r: r["min_pivot"])
    return {
        "nonnegative_sequence_count": nonnegative,
        "negative_sequence_count": negative,
        "singular_or_zero_sequence_count": singular,
        "best_sequence": (seqs[-1] if seqs else None),
        "worst_sequence": (seqs[0] if seqs else None),
    }


def update_repairs_negative_D_direction(D: np.ndarray, t: np.ndarray, M: np.ndarray) -> dict[str, Any]:
    w, Q = np.linalg.eigh(D)
    i = int(np.argmin(w))
    v = Q[:, i]
    d_ray = float(np.real(np.vdot(v, D @ v)))
    update_ray = float(0.5 * abs(np.dot(t, v)) ** 2)  # v^* outer(conj(t),t) v = |t^T v|^2
    m_ray = float(np.real(np.vdot(v, M @ v)))
    return {
        "min_eig_D": float(w[i]),
        "D_min_direction_D_rayleigh": d_ray,
        "trace_update_on_D_min_direction": update_ray,
        "M_rayleigh_same_direction": m_ray,
        "repair_margin_same_direction": m_ray,
    }


def summarize_case(label: str, U: np.ndarray, V: np.ndarray) -> dict[str, Any]:
    D, t, M = matrices(U, V)
    return {
        "label": label,
        "eig_M": [float(x) for x in np.linalg.eigvalsh(M)],
        "eig_D": [float(x) for x in np.linalg.eigvalsh(D)],
        "M_pivots": pivot_report(M),
        "D_pivots": pivot_report(D),
        "D_negative_direction_trace_repair": update_repairs_negative_D_direction(D, t, M),
    }


def controls() -> list[tuple[str, np.ndarray, np.ndarray]]:
    Pprod = np.column_stack([loop8.cvec(0, 0), loop8.cvec(1, 0)])
    Ddiag = np.column_stack([loop8.cvec(0, 0), loop8.cvec(1, 1)])
    Rprod = np.column_stack([loop8.cvec(0, 0), loop8.cvec(0, 1)])
    return [
        ("product_projection_support_00_10", Pprod, Pprod.copy()),
        ("diagonal_traceless_support_00_11", Ddiag, Ddiag.copy()),
        ("right_product_support_00_01", Rprod, Rprod.copy()),
        ("coordinate_D_negative_repaired_00_01_vs_00_10", coordinate_frame(0, 1), coordinate_frame(0, 4)),
    ]


def coordinate_scan() -> dict[str, Any]:
    planes = list(itertools.combinations(range(16), 2))
    out: dict[str, Any] = {
        "total_pairs": 0,
        "M_no_nonnegative_pivot_order": 0,
        "D_no_nonnegative_pivot_order": 0,
        "M_negative_eig_count": 0,
        "D_negative_eig_count": 0,
        "worst_M_min_eig": math.inf,
        "worst_D_min_eig": math.inf,
        "examples_D_rejected": [],
        "examples_M_boundary": [],
    }
    for IP in planes:
        U = coordinate_frame(*IP)
        for IQ in planes:
            V = coordinate_frame(*IQ)
            D, t, M = matrices(U, V)
            out["total_pairs"] += 1
            minM = float(np.linalg.eigvalsh(M)[0])
            minD = float(np.linalg.eigvalsh(D)[0])
            out["worst_M_min_eig"] = min(out["worst_M_min_eig"], minM)
            out["worst_D_min_eig"] = min(out["worst_D_min_eig"], minD)
            out["M_negative_eig_count"] += int(minM < -TOL)
            out["D_negative_eig_count"] += int(minD < -TOL)
            rpM = pivot_report(M)
            rpD = pivot_report(D)
            if rpM["nonnegative_sequence_count"] == 0:
                out["M_no_nonnegative_pivot_order"] += 1
                if len(out["examples_M_boundary"]) < 5:
                    out["examples_M_boundary"].append({"P": list(IP), "Q": list(IQ), "min_eig_M": minM, "M_pivots": rpM})
            if rpD["nonnegative_sequence_count"] == 0:
                out["D_no_nonnegative_pivot_order"] += 1
                if len(out["examples_D_rejected"]) < 5:
                    out["examples_D_rejected"].append({
                        "P": list(IP), "Q": list(IQ), "min_eig_D": minD,
                        "D_pivots": rpD,
                        "trace_repair": update_repairs_negative_D_direction(D, t, M),
                    })
    return out


def random_scan(seed: int, trials: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    out: dict[str, Any] = {
        "trials": trials,
        "M_no_nonnegative_pivot_order": 0,
        "D_no_nonnegative_pivot_order": 0,
        "M_negative_eig_count": 0,
        "D_negative_eig_count": 0,
        "worst_M_min_eig": math.inf,
        "worst_D_min_eig": math.inf,
        "worst_M_case": None,
    }
    for k in range(trials):
        U = loop8.random_frame(rng)
        V = loop8.random_frame(rng)
        D, t, M = matrices(U, V)
        minM = float(np.linalg.eigvalsh(M)[0])
        minD = float(np.linalg.eigvalsh(D)[0])
        if minM < out["worst_M_min_eig"]:
            out["worst_M_min_eig"] = minM
            out["worst_M_case"] = {"trial": k, "M_pivots": pivot_report(M), "D_pivots": pivot_report(D)}
        out["worst_D_min_eig"] = min(out["worst_D_min_eig"], minD)
        out["M_negative_eig_count"] += int(minM < -TOL)
        out["D_negative_eig_count"] += int(minD < -TOL)
        out["M_no_nonnegative_pivot_order"] += int(pivot_report(M)["nonnegative_sequence_count"] == 0)
        out["D_no_nonnegative_pivot_order"] += int(pivot_report(D)["nonnegative_sequence_count"] == 0)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--seed", type=int, default=12012)
    args = ap.parse_args()

    result = {
        "loop": "LOOP-0012",
        "lane": "trace-coupled full-PCL Schur/LDL candidate diagnostics",
        "claim": "CLAIM-0001 / U-0002 Full PCL certificate",
        "success_condition_met": False,
        "D_only_route_status": "explicitly rejected; D pivot/minor positivity is false on controls/coordinate cases",
        "trace_coupled_schur_formula": (
            "For pivot i with R=complement, m=M_ii=D_ii+(1/2)|t_i|^2 and "
            "c=M_Ri=D_Ri+(1/2)conj(t_R)t_i, carry the update in "
            "S_R=M_RR-c c^*/m.  Do not replace this by a Schur complement of D."
        ),
        "candidate_next_lemma": (
            "Find an invariant choice of positive M principal pivot, or prove all principal "
            "minors det(M_S)=det(D_S)+(1/2)t_S^T adj(D_S)conj(t_S) are nonnegative by "
            "trace-coupled Gram/SOS identities."
        ),
        "controls": [summarize_case(name, U, V) for name, U, V in controls()],
        "coordinate_scan": coordinate_scan(),
        "random_scan": random_scan(args.seed, args.trials),
    }
    outp = ROOT / f"research_harness/logs/LOOP-0012_trace_coupled_pivot_candidate_seed{args.seed}.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(result, indent=2) + "\n")

    print(json.dumps({
        "loop": result["loop"],
        "seed": args.seed,
        "trials": args.trials,
        "D_only_route_status": result["D_only_route_status"],
        "coordinate_total_pairs": result["coordinate_scan"]["total_pairs"],
        "coordinate_M_negative_eig_count": result["coordinate_scan"]["M_negative_eig_count"],
        "coordinate_D_negative_eig_count": result["coordinate_scan"]["D_negative_eig_count"],
        "coordinate_M_no_nonnegative_pivot_order": result["coordinate_scan"]["M_no_nonnegative_pivot_order"],
        "coordinate_D_no_nonnegative_pivot_order": result["coordinate_scan"]["D_no_nonnegative_pivot_order"],
        "random_M_negative_eig_count": result["random_scan"]["M_negative_eig_count"],
        "random_D_negative_eig_count": result["random_scan"]["D_negative_eig_count"],
        "random_M_no_nonnegative_pivot_order": result["random_scan"]["M_no_nonnegative_pivot_order"],
        "random_D_no_nonnegative_pivot_order": result["random_scan"]["D_no_nonnegative_pivot_order"],
        "worst_random_M_min_eig": result["random_scan"]["worst_M_min_eig"],
        "log": str(outp),
    }, indent=2))


if __name__ == "__main__":
    main()
