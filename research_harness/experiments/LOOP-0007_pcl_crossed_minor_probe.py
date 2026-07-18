#!/usr/bin/env python3
"""LOOP-0007 PCL crossed-minor probe.

This is a regression/probe script, not a proof engine.  It checks the exact
2-by-2 crossed PCL block

    indices (1,1) and (2,2) in the basis (1,1),(1,2),(2,1),(2,2)

for random two-frames U,V in C^4 tensor C^4.  It verifies numerically the
rank-one-update determinant identity

    det(D_S + 1/2 t_S t_S^*)
      = det(D_S) + 1/2 t_S^* adj(D_S) t_S,

with the PCL convention M = D + 1/2 T, D=2I-A-B,
T_{pq}=conj(trace_p) trace_q.
"""
import itertools
import json
from pathlib import Path

import numpy as np

n = 4
N = n * n
BASIS = [(0, 0), (0, 1), (1, 0), (1, 1)]
CROSS = (0, 3)  # (1,1),(2,2) in 1-based notation


def mat(u):
    return u.reshape(n, n)


def rand_frame(k, rng):
    A = rng.normal(size=(N, k)) + 1j * rng.normal(size=(N, k))
    Q, _ = np.linalg.qr(A)
    return Q[:, :k]


def hs(A, B):
    return np.vdot(A, B)


def pt1_rank(U, V):
    # tr_1(|vec U><vec V|)[a,b] = sum_i U[i,a] conj(V[i,b])
    return U.T @ np.conjugate(V)


def pt2_rank(U, V):
    # tr_2(|vec U><vec V|)[i,j] = sum_a U[i,a] conj(V[j,a])
    return U @ V.conj().T


def blocks(Uframe, Vframe):
    A = np.zeros((4, 4), complex)
    B = np.zeros((4, 4), complex)
    T = np.zeros((4, 4), complex)
    tr = np.zeros(4, complex)
    mats = []
    for (i, a) in BASIS:
        U = mat(Uframe[:, i])
        V = mat(Vframe[:, a])
        mats.append((i, a, U, V))
        tr[len(mats) - 1] = np.vdot(V.reshape(-1), U.reshape(-1))
    for p, (_, _, U, V) in enumerate(mats):
        for q, (_, _, X, Y) in enumerate(mats):
            A[p, q] = hs(pt1_rank(U, V), pt1_rank(X, Y))
            B[p, q] = hs(pt2_rank(U, V), pt2_rank(X, Y))
            T[p, q] = np.conj(tr[p]) * tr[q]
    D = 2 * np.eye(4) - A - B
    M = D + 0.5 * T
    D = (D + D.conj().T) / 2
    M = (M + M.conj().T) / 2
    return A, B, T, D, M, tr


def example_product():
    F = np.zeros((N, 2), complex)
    F[0, 0] = 1.0   # |0,0>
    F[1, 1] = 1.0   # |0,1>
    return F, F


def example_traceless():
    F = np.zeros((N, 2), complex)
    F[0, 0] = 1.0   # |0,0>
    F[5, 1] = 1.0   # |1,1>
    return F, F


def crossed_data(U, V):
    A, B, T, D, M, tr = blocks(U, V)
    S = list(CROSS)
    D2 = D[np.ix_(S, S)]
    M2 = M[np.ix_(S, S)]
    t = tr[S]
    # T = u u^*, where u_p = conj(trace_p), on this Hermitian convention.
    u = np.conjugate(t)
    x = D2[0, 0].real
    y = D2[1, 1].real
    c = D2[0, 1]
    det_D = np.linalg.det(D2).real
    update_scalar = 0.5 * (y * abs(u[0]) ** 2 + x * abs(u[1]) ** 2
                           - c * np.conjugate(u[0]) * u[1]
                           - np.conjugate(c) * np.conjugate(u[1]) * u[0])
    delta_formula = det_D + update_scalar.real
    delta_direct = np.linalg.det(M2).real
    pal_z = A[S[0], S[1]] + B[S[0], S[1]] - 0.5 * T[S[0], S[1]]
    pal_delta = M[S[0], S[0]].real * M[S[1], S[1]].real - abs(pal_z) ** 2
    return {
        "D2": D2,
        "M2": M2,
        "tr_pair": t,
        "det_D2": float(det_D),
        "rank_one_update_term": float(update_scalar.real),
        "delta_cross_direct": float(delta_direct),
        "delta_cross_formula": float(delta_formula),
        "pal_delta": float(pal_delta),
        "identity_error": float(abs(delta_direct - delta_formula)),
        "pal_error": float(abs(delta_direct - pal_delta)),
        "eig_D2": np.linalg.eigvalsh(D2),
        "eig_M2": np.linalg.eigvalsh(M2),
        "eig_D_full": np.linalg.eigvalsh(D),
        "eig_M_full": np.linalg.eigvalsh(M),
    }


def jsonable_data(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, np.ndarray):
            if np.iscomplexobj(v):
                out[k] = [[{"re": float(z.real), "im": float(z.imag)} for z in row]
                          for row in v] if v.ndim == 2 else [{"re": float(z.real), "im": float(z.imag)} for z in v]
            else:
                out[k] = [float(x) for x in v]
        elif isinstance(v, complex):
            out[k] = {"re": float(v.real), "im": float(v.imag)}
        else:
            out[k] = v
    return out


def sparse_frame_pairs_summary():
    # Enumerate coordinate two-planes for U and V. This is a finite regression
    # class only: Gr(2,16) is continuous.
    min_delta = (float("inf"), None)
    min_det_D = (float("inf"), None)
    negative_D_count = 0
    total = 0
    coords = list(itertools.combinations(range(N), 2))
    for us in coords:
        U = np.zeros((N, 2), complex)
        U[us[0], 0] = 1.0
        U[us[1], 1] = 1.0
        for vs in coords:
            V = np.zeros((N, 2), complex)
            V[vs[0], 0] = 1.0
            V[vs[1], 1] = 1.0
            d = crossed_data(U, V)
            total += 1
            if d["delta_cross_direct"] < min_delta[0]:
                min_delta = (d["delta_cross_direct"], (us, vs))
            if d["det_D2"] < min_det_D[0]:
                min_det_D = (d["det_D2"], (us, vs))
            if min(d["eig_D2"]) < -1e-12:
                negative_D_count += 1
    return {
        "total_coordinate_plane_pairs": total,
        "min_delta_cross": min_delta,
        "min_det_D2": min_det_D,
        "negative_D2_count": negative_D_count,
    }


def main():
    rng = np.random.default_rng(7007)
    results = {
        "seed": 7007,
        "convention": {
            "tr1": "tr_1(C)[a,b]=sum_i C[i,a,i,b]",
            "tr2": "tr_2(C)[i,j]=sum_a C[i,a,j,a]",
            "crossed_indices_zero_based": CROSS,
            "basis_zero_based": BASIS,
        },
        "equality_regressions": {},
        "random_summary": {},
        "coordinate_sparse_summary": {},
    }

    for name, maker in [("product", example_product), ("traceless", example_traceless)]:
        U, V = maker()
        results["equality_regressions"][name] = jsonable_data(crossed_data(U, V))

    min_delta = (float("inf"), None)
    min_det_D = (float("inf"), None)
    max_identity_error = 0.0
    max_pal_error = 0.0
    negative_D2_count = 0
    negative_Dfull_count = 0
    samples = 2000
    for s in range(samples):
        U = rand_frame(2, rng)
        V = rand_frame(2, rng)
        d = crossed_data(U, V)
        max_identity_error = max(max_identity_error, d["identity_error"])
        max_pal_error = max(max_pal_error, d["pal_error"])
        if d["delta_cross_direct"] < min_delta[0]:
            min_delta = (d["delta_cross_direct"], s)
        if d["det_D2"] < min_det_D[0]:
            min_det_D = (d["det_D2"], s)
        if min(d["eig_D2"]) < -1e-12:
            negative_D2_count += 1
        if min(d["eig_D_full"]) < -1e-12:
            negative_Dfull_count += 1
    results["random_summary"] = {
        "samples": samples,
        "min_delta_cross": min_delta,
        "min_det_D2": min_det_D,
        "max_rank_one_update_identity_error": max_identity_error,
        "max_pal_block_identity_error": max_pal_error,
        "negative_D2_count": negative_D2_count,
        "negative_Dfull_count": negative_Dfull_count,
    }
    results["coordinate_sparse_summary"] = sparse_frame_pairs_summary()

    out = Path("research_harness/logs/LOOP-0007_pcl_crossed_minor_seed7007.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps(results["random_summary"], indent=2, sort_keys=True))
    print(json.dumps(results["coordinate_sparse_summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
