#!/usr/bin/env python3
"""LOOP-0011 full-PCL lift / Schur-certificate diagnostics.

Fail-closed numerical diagnostic for CLAIM-0001/PCL.  It does not assume
D=2I-A-B is PSD.  It explicitly tracks the trace rank-one update

    M = D + (1/2) conjugate(t) t^T

on all principal minors and on Schur/pivot structures.  The purpose is to test
whether the LOOP-0010 coordinate rank-one-update patterns persist under
arbitrary two-frames, and to produce reproducible hints/obstructions for a
future trace-coupled Gram/Schur certificate.
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


def adjugate(A: np.ndarray) -> np.ndarray:
    n = A.shape[0]
    adj = np.zeros_like(A)
    if n == 1:
        adj[0, 0] = 1.0
        return adj
    for r in range(n):
        for c in range(n):
            rows = [x for x in range(n) if x != c]
            cols = [x for x in range(n) if x != r]
            adj[r, c] = ((-1) ** (r + c)) * np.linalg.det(A[np.ix_(rows, cols)])
    return adj


def matrices(U: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    A, B, T, M, _ = loop8.pcl_matrices(U, V)
    D = 2.0 * np.eye(4) - A - B
    D = (D + D.conj().T) / 2.0
    t = trace_vec(U, V)
    # Reconstruct M from D and t to force the convention under test.
    M2 = D + 0.5 * np.outer(np.conjugate(t), t)
    M2 = (M2 + M2.conj().T) / 2.0
    return D, t, M2, A, B


def eig_min(H: np.ndarray) -> float:
    return float(np.linalg.eigvalsh((H + H.conj().T) / 2.0)[0])


def principal_update_stats(D: np.ndarray, t: np.ndarray, M: np.ndarray) -> dict[str, Any]:
    out: dict[str, Any] = {}
    max_err = 0.0
    for k in range(1, 5):
        rows = []
        negD = negM = 0
        min_detD = math.inf
        min_detM = math.inf
        min_update = math.inf
        max_update = -math.inf
        repaired = 0
        for S in itertools.combinations(range(4), k):
            I = list(S)
            DS = D[np.ix_(I, I)]
            MS = M[np.ix_(I, I)]
            u = t[I]
            detD_c = np.linalg.det(DS)
            detM_c = np.linalg.det(MS)
            upd_c = 0.5 * (u @ adjugate(DS) @ np.conjugate(u))
            err = abs(detM_c - (detD_c + upd_c))
            max_err = max(max_err, float(err))
            detD = float(detD_c.real)
            detM = float(detM_c.real)
            upd = float(upd_c.real)
            negD += int(detD < -TOL)
            negM += int(detM < -TOL)
            repaired += int(detD < -TOL and detM >= -TOL)
            min_detD = min(min_detD, detD)
            min_detM = min(min_detM, detM)
            min_update = min(min_update, upd)
            max_update = max(max_update, upd)
            rows.append({"S": I, "detD": detD, "update": upd, "detM": detM})
        rows.sort(key=lambda r: r["detM"])
        out[str(k)] = {
            "negative_detD": negD,
            "negative_detM": negM,
            "repaired_negative_D_by_update": repaired,
            "min_detD": min_detD,
            "min_update": min_update,
            "max_update": max_update,
            "min_detM": min_detM,
            "worst_detM_subset": rows[0],
        }
    out["max_update_identity_error"] = max_err
    return out


def schur_complement(H: np.ndarray, S: tuple[int, ...]) -> np.ndarray | None:
    S = tuple(S)
    R = tuple(i for i in range(4) if i not in S)
    if not R:
        return np.zeros((0, 0), dtype=np.complex128)
    A = H[np.ix_(S, S)]
    # Use inverse only for well-conditioned pivots; otherwise report singular.
    svals = np.linalg.svd(A, compute_uv=False)
    if svals[-1] < 1e-9:
        return None
    B = H[np.ix_(S, R)]
    C = H[np.ix_(R, R)]
    return (C - B.conj().T @ np.linalg.solve(A, B) + (C - B.conj().T @ np.linalg.solve(A, B)).conj().T) / 2.0


def block_schur_stats(D: np.ndarray, M: np.ndarray) -> dict[str, Any]:
    rows = []
    counts = {"M_schur_negative": 0, "D_schur_negative": 0, "M_singular_pivot": 0, "D_singular_pivot": 0}
    for k in (1, 2, 3):
        for S in itertools.combinations(range(4), k):
            row: dict[str, Any] = {"S": list(S)}
            for name, H in (("M", M), ("D", D)):
                SC = schur_complement(H, S)
                if SC is None:
                    counts[f"{name}_singular_pivot"] += 1
                    row[f"{name}_schur_min_eig"] = None
                elif SC.size == 0:
                    row[f"{name}_schur_min_eig"] = None
                else:
                    mn = eig_min(SC)
                    row[f"{name}_schur_min_eig"] = mn
                    counts[f"{name}_schur_negative"] += int(mn < -TOL)
            rows.append(row)
    rows.sort(key=lambda r: (float("inf") if r.get("M_schur_min_eig") is None else r["M_schur_min_eig"]))
    return {"counts": counts, "worst_by_M_schur": rows[:5]}


def pivot_sequence(H: np.ndarray, perm: tuple[int, ...]) -> list[float] | None:
    A = H[np.ix_(perm, perm)].copy()
    pivots: list[float] = []
    for k in range(4):
        p = float(A[k, k].real)
        pivots.append(p)
        if k == 3:
            break
        if abs(p) < 1e-9:
            return None
        v = A[k + 1 :, k].copy()
        A[k + 1 :, k + 1 :] -= np.outer(v, np.conjugate(v)) / p
        A[k + 1 :, k + 1 :] = (A[k + 1 :, k + 1 :] + A[k + 1 :, k + 1 :].conj().T) / 2.0
    return pivots


def pivot_stats(D: np.ndarray, M: np.ndarray) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name, H in (("M", M), ("D", D)):
        seqs = []
        singular = 0
        has_negative = 0
        for perm in itertools.permutations(range(4)):
            piv = pivot_sequence(H, perm)
            if piv is None:
                singular += 1
                continue
            mn = min(piv)
            has_negative += int(mn < -TOL)
            seqs.append({"perm": list(perm), "pivots": piv, "min_pivot": mn})
        seqs.sort(key=lambda r: r["min_pivot"])
        out[name] = {
            "permutations": 24,
            "singular_or_zero_pivot": singular,
            "negative_pivot_sequence_count": has_negative,
            "worst_sequences": seqs[:3],
            "best_sequences": list(reversed(seqs[-3:])),
        }
    return out


def summarize_case(label: str, U: np.ndarray, V: np.ndarray) -> dict[str, Any]:
    D, t, M, A, B = matrices(U, V)
    wM = np.linalg.eigvalsh(M)
    wD = np.linalg.eigvalsh(D)
    return {
        "label": label,
        "min_eig_M": float(wM[0]),
        "eig_M": [float(x) for x in wM],
        "min_eig_D": float(wD[0]),
        "eig_D": [float(x) for x in wD],
        "trace_norm2": float(np.vdot(t, t).real),
        "principal_update": principal_update_stats(D, t, M),
        "block_schur": block_schur_stats(D, M),
        "pivots": pivot_stats(D, M),
    }


def coordinate_frame(i: int, j: int) -> np.ndarray:
    F = np.zeros((16, 2), dtype=np.complex128)
    F[i, 0] = 1.0
    F[j, 1] = 1.0
    return F


def coordinate_schur_scan() -> dict[str, Any]:
    """Finite coordinate Schur/update atlas; diagnostic only, not a proof."""
    planes = list(itertools.combinations(range(16), 2))
    out: dict[str, Any] = {
        "total_pairs": 0,
        "negative_min_eig_M": 0,
        "negative_min_eig_D": 0,
        "min_eig_M": math.inf,
        "min_eig_D": math.inf,
        "negative_detM_by_size": {str(k): 0 for k in range(1, 5)},
        "negative_detD_by_size": {str(k): 0 for k in range(1, 5)},
        "repaired_negative_D_by_size": {str(k): 0 for k in range(1, 5)},
        "M_schur_negative_splits": 0,
        "D_schur_negative_splits": 0,
        "M_singular_pivots": 0,
        "D_singular_pivots": 0,
        "examples": [],
    }
    for IP in planes:
        U = coordinate_frame(*IP)
        for IQ in planes:
            V = coordinate_frame(*IQ)
            D, t, M, _, _ = matrices(U, V)
            out["total_pairs"] += 1
            mnM = eig_min(M)
            mnD = eig_min(D)
            out["min_eig_M"] = min(out["min_eig_M"], mnM)
            out["min_eig_D"] = min(out["min_eig_D"], mnD)
            out["negative_min_eig_M"] += int(mnM < -TOL)
            out["negative_min_eig_D"] += int(mnD < -TOL)
            ps = principal_update_stats(D, t, M)
            for k in range(1, 5):
                rec = ps[str(k)]
                out["negative_detM_by_size"][str(k)] += rec["negative_detM"]
                out["negative_detD_by_size"][str(k)] += rec["negative_detD"]
                out["repaired_negative_D_by_size"][str(k)] += rec["repaired_negative_D_by_update"]
                if rec["repaired_negative_D_by_update"] and len(out["examples"]) < 8:
                    out["examples"].append({
                        "plane_P": list(IP),
                        "plane_Q": list(IQ),
                        "size": k,
                        "worst_subset": rec["worst_detM_subset"],
                    })
            bs = block_schur_stats(D, M)["counts"]
            out["M_schur_negative_splits"] += bs["M_schur_negative"]
            out["D_schur_negative_splits"] += bs["D_schur_negative"]
            out["M_singular_pivots"] += bs["M_singular_pivot"]
            out["D_singular_pivots"] += bs["D_singular_pivot"]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=250)
    ap.add_argument("--seed", type=int, default=11011)
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)

    # Rebuild the standard LOOP-0008 equality/control frames.  The helper in
    # LOOP-0008 returns evaluated dictionaries rather than the raw frames.
    Pprod = np.column_stack([loop8.cvec(0, 0), loop8.cvec(1, 0)])
    Ddiag = np.column_stack([loop8.cvec(0, 0), loop8.cvec(1, 1)])
    Rprod = np.column_stack([loop8.cvec(0, 0), loop8.cvec(0, 1)])
    controls = [
        ("product_projection_support_00_10", Pprod, Pprod.copy()),
        ("diagonal_traceless_support_00_11", Ddiag, Ddiag.copy()),
        ("right_product_support_00_01", Rprod, Rprod.copy()),
        ("coordinate_negative_D_repaired_LOOP0010_example", coordinate_frame(0, 1), coordinate_frame(0, 4)),
    ]

    case_summaries = [summarize_case(name, U, V) for name, U, V in controls]
    coord_scan = coordinate_schur_scan()

    aggregate: dict[str, Any] = {
        "trials": args.trials,
        "negative_min_eig_M": 0,
        "negative_principal_detM_cases": 0,
        "negative_principal_detD_cases": 0,
        "repaired_negative_D_principal_cases": 0,
        "max_update_identity_error": 0.0,
        "random_min_eig_M_min": math.inf,
        "random_min_detM_min_by_size": {str(k): math.inf for k in range(1, 5)},
        "random_min_detD_min_by_size": {str(k): math.inf for k in range(1, 5)},
        "random_schur_M_negative_splits": 0,
        "random_schur_D_negative_splits": 0,
        "random_pivot_M_negative_sequences": 0,
        "random_pivot_D_negative_sequences": 0,
    }
    worst_random: dict[str, Any] | None = None
    for trial in range(args.trials):
        U = loop8.random_frame(rng)
        V = loop8.random_frame(rng)
        r = summarize_case(f"random_{trial}", U, V)
        aggregate["negative_min_eig_M"] += int(r["min_eig_M"] < -TOL)
        aggregate["random_min_eig_M_min"] = min(aggregate["random_min_eig_M_min"], r["min_eig_M"])
        ps = r["principal_update"]
        aggregate["max_update_identity_error"] = max(aggregate["max_update_identity_error"], ps["max_update_identity_error"])
        for k in range(1, 5):
            rec = ps[str(k)]
            aggregate["negative_principal_detM_cases"] += rec["negative_detM"]
            aggregate["negative_principal_detD_cases"] += rec["negative_detD"]
            aggregate["repaired_negative_D_principal_cases"] += rec["repaired_negative_D_by_update"]
            aggregate["random_min_detM_min_by_size"][str(k)] = min(aggregate["random_min_detM_min_by_size"][str(k)], rec["min_detM"])
            aggregate["random_min_detD_min_by_size"][str(k)] = min(aggregate["random_min_detD_min_by_size"][str(k)], rec["min_detD"])
        aggregate["random_schur_M_negative_splits"] += r["block_schur"]["counts"]["M_schur_negative"]
        aggregate["random_schur_D_negative_splits"] += r["block_schur"]["counts"]["D_schur_negative"]
        aggregate["random_pivot_M_negative_sequences"] += r["pivots"]["M"]["negative_pivot_sequence_count"]
        aggregate["random_pivot_D_negative_sequences"] += r["pivots"]["D"]["negative_pivot_sequence_count"]
        if worst_random is None or r["min_eig_M"] < worst_random["min_eig_M"]:
            worst_random = r

    result = {
        "loop": "LOOP-0011",
        "lane": "full-PCL lift / Schur-certificate diagnostics",
        "claim": "CLAIM-0001-rank-two-partial-trace",
        "seed": args.seed,
        "caveat": "Numerical diagnostics only. No proof. Does not use D>=0 or det(D)>=0 as a certificate.",
        "success_condition_met": False,
        "aggregate_random": aggregate,
        "coordinate_schur_scan": coord_scan,
        "controls": case_summaries,
        "worst_random_case": worst_random,
    }
    outp = ROOT / "research_harness/logs/LOOP-0011_full_pcl_schur_diagnostics_seed11011.json"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "loop": result["loop"],
        "seed": args.seed,
        "trials": args.trials,
        "negative_min_eig_M": aggregate["negative_min_eig_M"],
        "negative_principal_detM_cases": aggregate["negative_principal_detM_cases"],
        "negative_principal_detD_cases": aggregate["negative_principal_detD_cases"],
        "repaired_negative_D_principal_cases": aggregate["repaired_negative_D_principal_cases"],
        "random_min_eig_M_min": aggregate["random_min_eig_M_min"],
        "random_min_detM_min_by_size": aggregate["random_min_detM_min_by_size"],
        "random_min_detD_min_by_size": aggregate["random_min_detD_min_by_size"],
        "random_schur_M_negative_splits": aggregate["random_schur_M_negative_splits"],
        "random_schur_D_negative_splits": aggregate["random_schur_D_negative_splits"],
        "random_pivot_M_negative_sequences": aggregate["random_pivot_M_negative_sequences"],
        "random_pivot_D_negative_sequences": aggregate["random_pivot_D_negative_sequences"],
        "coordinate_negative_min_eig_M": coord_scan["negative_min_eig_M"],
        "coordinate_negative_min_eig_D": coord_scan["negative_min_eig_D"],
        "coordinate_negative_detD_by_size": coord_scan["negative_detD_by_size"],
        "coordinate_repaired_negative_D_by_size": coord_scan["repaired_negative_D_by_size"],
        "coordinate_M_schur_negative_splits": coord_scan["M_schur_negative_splits"],
        "coordinate_D_schur_negative_splits": coord_scan["D_schur_negative_splits"],
        "max_update_identity_error": aggregate["max_update_identity_error"],
        "log": str(outp),
    }, indent=2))


if __name__ == "__main__":
    main()
