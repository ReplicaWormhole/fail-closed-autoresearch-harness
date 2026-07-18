#!/usr/bin/env python3
"""LOOP-0007 PAL determinant identity/regression probes.

This script is not a proof.  It checks exact algebraic decompositions of the
phase-aware PAL 2x2 block and records guardrail examples: separated defect
kernels are indefinite, the m>=3 all-frame promotion is false, and the old
fixed-gauge a+b target is overstrong while the phase-aware a+conj(b) target is
sharp.
"""
import json
from pathlib import Path
import numpy as np

n = 4
N = n*n


def E(i, j):
    A = np.zeros((n, n), complex)
    A[i, j] = 1.0
    return A


def hs(A, B):
    return np.vdot(A, B)  # tr(A^* B)


def rand_frame(rng, m):
    Z = rng.normal(size=(N, m)) + 1j*rng.normal(size=(N, m))
    Q, _ = np.linalg.qr(Z)
    return [Q[:, k].reshape(n, n) for k in range(m)]


def pal_components(Xs, Ys):
    m = len(Xs)
    KL = np.zeros((m, m), complex)
    KR = np.zeros((m, m), complex)
    TT = np.zeros((m, m), complex)
    K = np.zeros((m, m), complex)
    fixed = np.zeros((m, m), complex)
    for i in range(m):
        Xi, Yi = Xs[i], Ys[i]
        Li = Xi @ Yi.conj().T
        Ri = Xi.conj().T @ Yi
        ti = np.trace(Ri)
        for j in range(m):
            Xj, Yj = Xs[j], Ys[j]
            Lj = Xj @ Yj.conj().T
            Rj = Xj.conj().T @ Yj
            tj = np.trace(Rj)
            delta = 1.0 if i == j else 0.0
            lgram = hs(Li, Lj)
            rgram = hs(Ri, Rj)
            # Phase-aware PAL block.
            K[i, j] = 2*delta - lgram - np.conj(rgram) + 0.5*ti*np.conj(tj)
            # Determinant-lane decomposition: left partial-trace defect,
            # right partial-trace defect (with PAL conjugation), trace update.
            KL[i, j] = delta - lgram
            KR[i, j] = delta - np.conj(rgram)
            TT[i, j] = 0.5*ti*np.conj(tj)
            # Old fixed-gauge overstrengthening: uses rgram, not conj(rgram).
            fixed[i, j] = 2*delta - lgram - rgram + 0.5*np.conj(ti)*tj
    # Hermitize to remove roundoff when taking eigs.
    def H(A): return (A + A.conj().T)/2
    return H(K), H(KL), H(KR), H(TT), H(fixed)


def eig(A):
    return [float(x) for x in np.linalg.eigvalsh((A + A.conj().T)/2)]


def mat_to_pairs(A):
    return [[[float(z.real), float(z.imag)] for z in row] for row in A]


def residual_identity_random(seed=7007, trials=200, m=2):
    rng = np.random.default_rng(seed)
    max_res = 0.0
    min_eig_K = 1e9
    min_eig_KL = 1e9
    min_eig_KR = 1e9
    best_det_slack = 1e9
    for _ in range(trials):
        Xs = rand_frame(rng, m)
        Ys = rand_frame(rng, m)
        K, KL, KR, TT, _ = pal_components(Xs, Ys)
        max_res = max(max_res, float(np.max(np.abs(K - (KL + KR + TT)))))
        min_eig_K = min(min_eig_K, float(np.linalg.eigvalsh(K)[0]))
        min_eig_KL = min(min_eig_KL, float(np.linalg.eigvalsh(KL)[0]))
        min_eig_KR = min(min_eig_KR, float(np.linalg.eigvalsh(KR)[0]))
        if m == 2:
            best_det_slack = min(best_det_slack, float(np.linalg.det(K).real))
    return {
        "seed": seed,
        "trials": trials,
        "m": m,
        "max_identity_residual": max_res,
        "min_eig_K": min_eig_K,
        "min_eig_left_defect": min_eig_KL,
        "min_eig_right_defect": min_eig_KR,
        "min_det_slack_m2": best_det_slack if m == 2 else None,
    }


def named_examples():
    out = {}
    examples = {
        "product_equality_two_frame": ([E(0,0), E(0,1)], [E(0,0), E(0,1)]),
        "traceless_diagonal_two_frame": ([E(0,0), -E(1,1)], [E(0,0), E(1,1)]),
        "loop0002_fixed_gauge_witness": ([E(0,0), E(0,1)], [E(0,0), 1j*E(0,1)]),
        "m3_all_frame_obstruction": ([E(0,0), E(0,1), E(0,2)], [E(0,0), E(0,1), E(0,2)]),
        "right_defect_indefinite_two_frame": ([E(0,0), E(1,0)], [E(0,0), E(1,0)]),
    }
    for name, (Xs, Ys) in examples.items():
        K, KL, KR, TT, fixed = pal_components(Xs, Ys)
        rec = {
            "K": mat_to_pairs(K),
            "eig_K": eig(K),
            "KL_left": mat_to_pairs(KL),
            "eig_KL_left": eig(KL),
            "KR_right": mat_to_pairs(KR),
            "eig_KR_right": eig(KR),
            "TT_trace": mat_to_pairs(TT),
            "eig_TT_trace": eig(TT),
            "fixed_gauge_K": mat_to_pairs(fixed),
            "eig_fixed_gauge_K": eig(fixed),
        }
        if len(Xs) == 2:
            rec["det_K"] = float(np.linalg.det(K).real)
            rec["det_fixed_gauge_K"] = float(np.linalg.det(fixed).real)
        out[name] = rec
    return out


def main():
    out = {
        "identity_random_m2": residual_identity_random(m=2),
        "identity_random_m3": residual_identity_random(seed=7010, trials=200, m=3),
        "examples": named_examples(),
    }
    path = Path("research_harness/logs/LOOP-0007_pal_determinant_identities.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2))
    print(json.dumps({
        "m2": out["identity_random_m2"],
        "m3": out["identity_random_m3"],
        "example_eigs": {k: v["eig_K"] for k, v in out["examples"].items()},
        "fixed_gauge_eigs": {k: v["eig_fixed_gauge_K"] for k, v in out["examples"].items()},
    }, indent=2))


if __name__ == "__main__":
    main()
