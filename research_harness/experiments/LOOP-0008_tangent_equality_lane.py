#!/usr/bin/env python3
"""LOOP-0008 tangent/equality lane for CLAIM-0001.

Parameterizes the rank-two tangent space at sharp equality controls and computes
first/second variation evidence for the original gap(C), using the corrected
partial-trace convention:
  tr_1(C)[a,b] = sum_i C[i,a,i,b]
  tr_2(C)[i,j] = sum_a C[i,a,j,a]

This is numerical evidence only, not a proof/certificate.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable

import numpy as np

N = 16
D = 4


def as_tensor(C: np.ndarray) -> np.ndarray:
    return C.reshape(D, D, D, D)


def tr1(C: np.ndarray) -> np.ndarray:
    T = as_tensor(C)
    out = np.zeros((D, D), dtype=np.complex128)
    for a in range(D):
        for b in range(D):
            out[a, b] = sum(T[i, a, i, b] for i in range(D))
    return out


def tr2(C: np.ndarray) -> np.ndarray:
    T = as_tensor(C)
    out = np.zeros((D, D), dtype=np.complex128)
    for i in range(D):
        for j in range(D):
            out[i, j] = sum(T[i, a, j, a] for a in range(D))
    return out


def fro2(X: np.ndarray) -> float:
    return float(np.vdot(X, X).real)


def hs(X: np.ndarray, Y: np.ndarray) -> complex:
    return complex(np.vdot(X, Y))


def gap(C: np.ndarray) -> float:
    return fro2(tr1(C)) + fro2(tr2(C)) - 2.0 * fro2(C) - 0.5 * abs(np.trace(C)) ** 2


def normalized_gap(C: np.ndarray) -> float:
    n = fro2(C)
    return float(gap(C) / n) if n else float("-inf")


def gap_polar(X: np.ndarray, Y: np.ndarray) -> complex:
    # Hermitian sesquilinear polarization q(C)=<C,Phi(C)>.
    return (
        hs(tr1(X), tr1(Y))
        + hs(tr2(X), tr2(Y))
        - 2.0 * hs(X, Y)
        - 0.5 * np.conjugate(np.trace(X)) * np.trace(Y)
    )


def ketbra(row_i: int, row_a: int, col_j: int, col_b: int) -> np.ndarray:
    C = np.zeros((N, N), dtype=np.complex128)
    C[D * row_i + row_a, D * col_j + col_b] = 1.0
    return C


def equality_examples() -> dict[str, np.ndarray]:
    diag_difference = (ketbra(0, 0, 0, 0) - ketbra(1, 1, 1, 1)) / math.sqrt(2)
    product_projection = (ketbra(0, 0, 0, 0) + ketbra(1, 0, 1, 0)) / math.sqrt(2)
    return {
        "diag_difference": diag_difference,
        "product_projection": product_projection,
    }


def svd_support(C0: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    U, s, Vh = np.linalg.svd(C0, full_matrices=True)
    rank = int(np.sum(s > 1e-12))
    assert rank == 2
    U2 = U[:, :2]
    V2 = Vh.conj().T[:, :2]
    Uperp = U[:, 2:]
    Vperp = Vh.conj().T[:, 2:]
    return U2, s[:2], V2, Uperp, Vperp


def tangent_complex_basis(C0: np.ndarray) -> list[np.ndarray]:
    # Tangent to rank-2 variety at C0: P dC Q + P dC Qperp + Pperp dC Q.
    U2, _s, V2, Uperp, Vperp = svd_support(C0)
    basis: list[np.ndarray] = []
    for a in range(2):
        for b in range(2):
            basis.append(np.outer(U2[:, a], V2[:, b].conj()))
    for a in range(2):
        for b in range(N - 2):
            basis.append(np.outer(U2[:, a], Vperp[:, b].conj()))
    for a in range(N - 2):
        for b in range(2):
            basis.append(np.outer(Uperp[:, a], V2[:, b].conj()))
    return basis


def orthonormalize_real_tangent_sphere(complex_basis: list[np.ndarray], C0: np.ndarray) -> list[np.ndarray]:
    # Real vector space spanned by B and iB, with Re<C0,D>=0 constraint.
    raw: list[np.ndarray] = []
    for B in complex_basis:
        for z in (1.0, 1.0j):
            Dv = z * B
            # Project out real radial component C0 so Re<C0,Dv>=0.
            Dv = Dv - np.real(hs(C0, Dv)) * C0 / fro2(C0)
            raw.append(Dv)
    ortho: list[np.ndarray] = []
    for v in raw:
        w = v.copy()
        for e in ortho:
            w = w - np.real(hs(e, w)) * e
        n = math.sqrt(max(fro2(w), 0.0))
        if n > 1e-11:
            ortho.append(w / n)
    return ortho


def real_quadratic_matrix(real_basis: list[np.ndarray]) -> np.ndarray:
    m = len(real_basis)
    H = np.zeros((m, m), dtype=np.float64)
    for i, Ei in enumerate(real_basis):
        for j, Ej in enumerate(real_basis[: i + 1]):
            val = np.real(gap_polar(Ei, Ej))
            H[i, j] = H[j, i] = val
    return H


def linear_coeffs(C0: np.ndarray, real_basis: list[np.ndarray]) -> np.ndarray:
    return np.array([2.0 * np.real(gap_polar(C0, E)) for E in real_basis], dtype=np.float64)


def rank2_retract(C: np.ndarray) -> np.ndarray:
    U, s, Vh = np.linalg.svd(C, full_matrices=False)
    return (U[:, :2] * s[:2]) @ Vh[:2, :]


def tangent_path(C0: np.ndarray, Dv: np.ndarray, eps: float) -> np.ndarray:
    # SVD truncation keeps rank<=2. If Dv is exact tangent this changes only O(eps^2).
    C = rank2_retract(C0 + eps * Dv)
    return C / math.sqrt(fro2(C))


def random_rank2(rng: np.random.Generator) -> np.ndarray:
    A = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    B = rng.normal(size=(N, 2)) + 1j * rng.normal(size=(N, 2))
    C = A @ B.conj().T
    return C / math.sqrt(fro2(C))


def analyze_control(name: str, C0: np.ndarray, rng: np.random.Generator, random_dirs: int) -> dict:
    cbasis = tangent_complex_basis(C0)
    rbasis = orthonormalize_real_tangent_sphere(cbasis, C0)
    H = real_quadratic_matrix(rbasis)
    ell = linear_coeffs(C0, rbasis)
    evals, evecs = np.linalg.eigh(H)
    max_idx = int(np.argmax(evals))
    min_idx = int(np.argmin(evals))
    Dmax = np.zeros_like(C0)
    Dmin = np.zeros_like(C0)
    for k in range(len(rbasis)):
        Dmax = Dmax + evecs[k, max_idx] * rbasis[k]
        Dmin = Dmin + evecs[k, min_idx] * rbasis[k]
    # First derivative finite difference along a few deterministic extremal directions.
    eps_sweep = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]

    def sweep(Dv: np.ndarray) -> list[dict]:
        out = []
        for eps in eps_sweep:
            Cp = tangent_path(C0, Dv, eps)
            Cm = tangent_path(C0, Dv, -eps)
            out.append(
                {
                    "eps": eps,
                    "plus_ngap": normalized_gap(Cp),
                    "minus_ngap": normalized_gap(Cm),
                    "central_first": (normalized_gap(Cp) - normalized_gap(Cm)) / (2 * eps),
                    "central_second": (normalized_gap(Cp) + normalized_gap(Cm) - 2 * normalized_gap(C0)) / (eps * eps),
                    "plus_rank": int(np.linalg.matrix_rank(Cp, tol=1e-10)),
                    "minus_rank": int(np.linalg.matrix_rank(Cm, tol=1e-10)),
                }
            )
        return out

    # Random exact tangent directions via real-basis coefficients, plus ambient SVD-truncated controls.
    best_tangent = {"normalized_gap": -1e99}
    best_ambient = {"normalized_gap": -1e99}
    eps_for_search = [1e-3, 1e-2, 1e-1]
    for t in range(random_dirs):
        coeff = rng.normal(size=len(rbasis))
        coeff /= np.linalg.norm(coeff)
        Dv = np.zeros_like(C0)
        for k in range(len(rbasis)):
            Dv = Dv + coeff[k] * rbasis[k]
        for eps in eps_for_search:
            C = tangent_path(C0, Dv, eps)
            ng = normalized_gap(C)
            if ng > best_tangent["normalized_gap"]:
                best_tangent = {
                    "normalized_gap": float(ng),
                    "gap": float(gap(C)),
                    "eps": eps,
                    "trial": t,
                    "rank": int(np.linalg.matrix_rank(C, tol=1e-10)),
                    "fro2": fro2(C),
                }
        R = random_rank2(rng)
        for eps in eps_for_search:
            C = tangent_path(C0, R, eps)
            ng = normalized_gap(C)
            if ng > best_ambient["normalized_gap"]:
                best_ambient = {
                    "normalized_gap": float(ng),
                    "gap": float(gap(C)),
                    "eps": eps,
                    "trial": t,
                    "rank": int(np.linalg.matrix_rank(C, tol=1e-10)),
                    "fro2": fro2(C),
                }

    return {
        "name": name,
        "rank": int(np.linalg.matrix_rank(C0, tol=1e-10)),
        "fro2": fro2(C0),
        "gap": gap(C0),
        "normalized_gap": normalized_gap(C0),
        "trace_abs2": float(abs(np.trace(C0)) ** 2),
        "tr1_fro2": fro2(tr1(C0)),
        "tr2_fro2": fro2(tr2(C0)),
        "complex_tangent_dim": len(cbasis),
        "real_sphere_tangent_dim": len(rbasis),
        "projected_first_variation_l2": float(np.linalg.norm(ell)),
        "projected_first_variation_linf": float(np.max(np.abs(ell))) if len(ell) else 0.0,
        "second_variation_eigs_qD": {
            "min": float(evals[min_idx]),
            "max": float(evals[max_idx]),
            "positive_count_tol_1e-10": int(np.sum(evals > 1e-10)),
            "near_zero_count_tol_1e-10": int(np.sum(np.abs(evals) <= 1e-10)),
            "negative_count_tol_1e-10": int(np.sum(evals < -1e-10)),
            "top10": [float(x) for x in evals[-10:][::-1]],
            "bottom10": [float(x) for x in evals[:10]],
        },
        "finite_difference_max_eigen_direction": sweep(Dmax),
        "finite_difference_min_eigen_direction": sweep(Dmin),
        "random_exact_tangent_rank2_retracted": best_tangent,
        "random_ambient_rank2_retracted": best_ambient,
        "positive_direction_tol_1e-10": bool(evals[max_idx] > 1e-10 or best_tangent["normalized_gap"] > 1e-10 or best_ambient["normalized_gap"] > 1e-10),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=8008)
    ap.add_argument("--random-dirs", type=int, default=5000)
    ap.add_argument("--out", type=Path, default=Path("research_harness/logs/LOOP-0008_tangent_equality_seed8008.json"))
    args = ap.parse_args()
    rng = np.random.default_rng(args.seed)
    controls = equality_examples()
    results = {name: analyze_control(name, C0, rng, args.random_dirs) for name, C0 in controls.items()}
    robust_positive = any(r["positive_direction_tol_1e-10"] for r in results.values())
    summary = {
        "loop": "LOOP-0008",
        "claim": "CLAIM-0001-rank-two-partial-trace",
        "seed": args.seed,
        "random_dirs_per_control": args.random_dirs,
        "convention": {
            "tr1": "tr_1(C)[a,b]=sum_i C[i,a,i,b]",
            "tr2": "tr_2(C)[i,j]=sum_a C[i,a,j,a]",
        },
        "controls": results,
        "robust_positive_direction_or_gap_found_tol_1e-10": bool(robust_positive),
        "success_condition_met": False,
        "caveat": "Finite-dimensional floating point tangent/finite-difference evidence only; local maximality evidence is not a proof.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({
        "seed": args.seed,
        "random_dirs_per_control": args.random_dirs,
        "controls": {
            name: {
                "normalized_gap": r["normalized_gap"],
                "first_variation_l2": r["projected_first_variation_l2"],
                "second_variation_max_qD": r["second_variation_eigs_qD"]["max"],
                "second_variation_positive_count": r["second_variation_eigs_qD"]["positive_count_tol_1e-10"],
                "best_random_tangent_ngap": r["random_exact_tangent_rank2_retracted"]["normalized_gap"],
                "best_random_ambient_ngap": r["random_ambient_rank2_retracted"]["normalized_gap"],
            }
            for name, r in results.items()
        },
        "robust_positive_direction_or_gap_found_tol_1e-10": robust_positive,
        "log": str(args.out),
    }, indent=2))


if __name__ == "__main__":
    main()
