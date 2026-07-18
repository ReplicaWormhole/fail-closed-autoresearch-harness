#!/usr/bin/env python3
"""
LOOP-0003 direct optimizer/counterexample hunter for CLAIM-0001.

Searches rank <= 2 complex matrices C in M_4(C) tensor M_4(C), represented as
16 x 16 matrices, for positive original gap

    gap(C) = ||tr_1 C||_F^2 + ||tr_2 C||_F^2
             - 2 ||C||_F^2 - (1/2) |tr C|^2.

Parametrization: C = U V^*, U,V in C^{16 x r}, r <= 2, followed by
Frobenius normalization ||C||_F = 1. This guarantees rank(C) <= r.
Uses torch Adam plus optional LBFGS polishing, with deterministic seeds.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import platform
import sys
import time
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import torch

DTYPE = torch.float64


def make_complex_params(x: torch.Tensor, rank: int) -> tuple[torch.Tensor, torch.Tensor]:
    n = 16 * rank
    ur = x[:n].reshape(16, rank)
    ui = x[n:2*n].reshape(16, rank)
    vr = x[2*n:3*n].reshape(16, rank)
    vi = x[3*n:4*n].reshape(16, rank)
    return torch.complex(ur, ui), torch.complex(vr, vi)


def partial_traces_torch(C: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    X = C.reshape(4, 4, 4, 4)  # row=(i,a), col=(j,b)
    tr1 = torch.einsum("iaib->ab", X)  # trace first tensor factor
    tr2 = torch.einsum("iaja->ij", X)  # trace second tensor factor
    return tr1, tr2


def gap_torch_from_C(C: torch.Tensor) -> torch.Tensor:
    tr1, tr2 = partial_traces_torch(C)
    fro2 = torch.real(torch.sum(torch.conj(C) * C))
    trC = torch.trace(C)
    g = torch.real(torch.sum(torch.conj(tr1) * tr1))
    g = g + torch.real(torch.sum(torch.conj(tr2) * tr2))
    g = g - 2.0 * fro2 - 0.5 * (torch.real(trC) ** 2 + torch.imag(trC) ** 2)
    return g


def normalized_C_from_params(x: torch.Tensor, rank: int, eps: float = 1e-30) -> tuple[torch.Tensor, torch.Tensor]:
    U, V = make_complex_params(x, rank)
    C = U @ torch.conj(V).T
    fro = torch.linalg.norm(C)
    Cn = C / torch.clamp(fro, min=eps)
    return Cn, fro


def objective(x: torch.Tensor, rank: int) -> torch.Tensor:
    Cn, _ = normalized_C_from_params(x, rank)
    return -gap_torch_from_C(Cn)


def partial_traces_np(C: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X = C.reshape(4, 4, 4, 4)
    tr1 = np.einsum("iaib->ab", X)
    tr2 = np.einsum("iaja->ij", X)
    return tr1, tr2


def gap_np(C: np.ndarray) -> float:
    tr1, tr2 = partial_traces_np(C)
    return float(np.vdot(tr1, tr1).real + np.vdot(tr2, tr2).real - 2*np.vdot(C, C).real - 0.5*abs(np.trace(C))**2)


def rank_np(C: np.ndarray, tol: float = 1e-10) -> tuple[int, list[float]]:
    s = np.linalg.svd(C, compute_uv=False)
    return int(np.sum(s > tol)), [float(v) for v in s[:8]]


def C_np_from_x(x_np: np.ndarray, rank: int) -> np.ndarray:
    n = 16 * rank
    U = x_np[:n].reshape(16, rank) + 1j*x_np[n:2*n].reshape(16, rank)
    V = x_np[2*n:3*n].reshape(16, rank) + 1j*x_np[3*n:4*n].reshape(16, rank)
    C = U @ V.conj().T
    return C / np.linalg.norm(C, "fro")


@dataclass
class RestartResult:
    seed: int
    rank_param: int
    init_gap: float
    final_gap: float
    polished_gap: float | None
    fro_norm: float
    numerical_rank_tol_1e_10: int
    leading_singular_values: list[float]
    trace_abs: float
    tr1_fro2: float
    tr2_fro2: float
    positive: bool
    elapsed_sec: float


def control_cases() -> list[dict[str, Any]]:
    cases: list[tuple[str, np.ndarray]] = []
    C = np.zeros((16, 16), dtype=np.complex128); C[0, 0] = 1.0
    cases.append(("rank1_basis_projector_E00", C))
    C = np.zeros((16, 16), dtype=np.complex128); C[0, 5] = 1.0
    cases.append(("rank1_basis_offdiag_E00_11", C))
    C = np.zeros((16, 16), dtype=np.complex128); C[0, 0] = 1.0; C[5, 5] = -1.0
    C = C / np.linalg.norm(C, "fro")
    cases.append(("rank2_diag_difference_E00_minus_E11", C))
    out = []
    for name, C0 in cases:
        Cn = C0 / np.linalg.norm(C0, "fro")
        tr1, tr2 = partial_traces_np(Cn)
        r, s = rank_np(Cn)
        out.append({
            "name": name,
            "gap": gap_np(Cn),
            "fro_norm": float(np.linalg.norm(Cn, "fro")),
            "rank_tol_1e_10": r,
            "leading_singular_values": s,
            "trace_abs": float(abs(np.trace(Cn))),
            "tr1_fro2": float(np.vdot(tr1, tr1).real),
            "tr2_fro2": float(np.vdot(tr2, tr2).real),
        })
    return out


def run_one(seed: int, rank: int, steps: int, lr: float, lbfgs_steps: int, device: str) -> tuple[RestartResult, np.ndarray]:
    t0 = time.time()
    torch.manual_seed(seed)
    np.random.seed(seed % (2**32 - 1))
    dim = 4 * 16 * rank
    x = torch.randn(dim, dtype=DTYPE, device=device, requires_grad=True)
    with torch.no_grad():
        init_C, _ = normalized_C_from_params(x, rank)
        init_gap = float(gap_torch_from_C(init_C).detach().cpu())
    opt = torch.optim.Adam([x], lr=lr)
    for _ in range(steps):
        opt.zero_grad(set_to_none=True)
        loss = objective(x, rank)
        loss.backward()
        opt.step()
    polished_gap = None
    if lbfgs_steps > 0:
        opt2 = torch.optim.LBFGS([x], lr=0.5, max_iter=lbfgs_steps, line_search_fn="strong_wolfe")
        def closure():
            opt2.zero_grad(set_to_none=True)
            loss = objective(x, rank)
            loss.backward()
            return loss
        opt2.step(closure)
        with torch.no_grad():
            Ctmp, _ = normalized_C_from_params(x, rank)
            polished_gap = float(gap_torch_from_C(Ctmp).detach().cpu())
    with torch.no_grad():
        x_np = x.detach().cpu().numpy().copy()
    C_np = C_np_from_x(x_np, rank)
    final_gap = gap_np(C_np)
    tr1, tr2 = partial_traces_np(C_np)
    r, s = rank_np(C_np)
    res = RestartResult(
        seed=seed,
        rank_param=rank,
        init_gap=init_gap,
        final_gap=final_gap,
        polished_gap=polished_gap,
        fro_norm=float(np.linalg.norm(C_np, "fro")),
        numerical_rank_tol_1e_10=r,
        leading_singular_values=s,
        trace_abs=float(abs(np.trace(C_np))),
        tr1_fro2=float(np.vdot(tr1, tr1).real),
        tr2_fro2=float(np.vdot(tr2, tr2).real),
        positive=bool(final_gap > 1e-10),
        elapsed_sec=time.time()-t0,
    )
    return res, C_np


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rank", type=int, default=2, choices=[1, 2])
    p.add_argument("--restarts", type=int, default=64)
    p.add_argument("--seed-base", type=int, default=3003)
    p.add_argument("--steps", type=int, default=2500)
    p.add_argument("--lr", type=float, default=0.03)
    p.add_argument("--lbfgs-steps", type=int, default=80)
    p.add_argument("--out-json", required=True)
    p.add_argument("--out-npz", default=None)
    p.add_argument("--device", default="cpu")
    args = p.parse_args()

    torch.set_default_dtype(DTYPE)
    if args.device != "cpu" and not torch.cuda.is_available():
        raise RuntimeError(f"Requested device {args.device!r}, but CUDA is unavailable")

    all_results: list[RestartResult] = []
    best_C = None
    best_gap = -math.inf
    print(f"LOOP-0003 direct original gap search rank={args.rank} restarts={args.restarts} steps={args.steps} lbfgs={args.lbfgs_steps}", flush=True)
    controls = control_cases()
    print("controls:")
    for c in controls:
        print(json.dumps(c, sort_keys=True), flush=True)
    for k in range(args.restarts):
        seed = args.seed_base + k
        res, C = run_one(seed, args.rank, args.steps, args.lr, args.lbfgs_steps, args.device)
        all_results.append(res)
        if res.final_gap > best_gap:
            best_gap = res.final_gap
            best_C = C.copy()
        print(json.dumps(asdict(res), sort_keys=True), flush=True)

    assert best_C is not None
    best_rank, best_s = rank_np(best_C)
    best_tr1, best_tr2 = partial_traces_np(best_C)
    best_gap_recomputed = gap_np(best_C)
    summary = {
        "claim": "CLAIM-0001 rank(C)<=2 implies original gap(C)<=0",
        "method": "C=U V^*, U,V complex 16xr; Frobenius normalize C; torch Adam + LBFGS polish; direct original gap objective",
        "argv": sys.argv,
        "python": sys.version,
        "platform": platform.platform(),
        "numpy_version": np.__version__,
        "torch_version": torch.__version__,
        "config": vars(args),
        "controls": controls,
        "restarts": [asdict(r) for r in all_results],
        "best": {
            "gap": best_gap_recomputed,
            "fro_norm": float(np.linalg.norm(best_C, "fro")),
            "rank_tol_1e_10": best_rank,
            "rank_tol_1e_8": int(np.sum(np.linalg.svd(best_C, compute_uv=False) > 1e-8)),
            "leading_singular_values": best_s,
            "trace_abs": float(abs(np.trace(best_C))),
            "tr1_fro2": float(np.vdot(best_tr1, best_tr1).real),
            "tr2_fro2": float(np.vdot(best_tr2, best_tr2).real),
            "positive_threshold_1e_10": bool(best_gap_recomputed > 1e-10),
            "C_real": best_C.real.tolist(),
            "C_imag": best_C.imag.tolist(),
        },
    }
    os.makedirs(os.path.dirname(args.out_json), exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
    if args.out_npz:
        os.makedirs(os.path.dirname(args.out_npz), exist_ok=True)
        np.savez(args.out_npz, C=best_C, gap=np.array([best_gap_recomputed]), singular_values=np.linalg.svd(best_C, compute_uv=False))
    print("SUMMARY " + json.dumps({k: summary["best"][k] for k in ["gap", "fro_norm", "rank_tol_1e_10", "rank_tol_1e_8", "leading_singular_values", "positive_threshold_1e_10"]}, sort_keys=True), flush=True)
    print(f"wrote_json={args.out_json}", flush=True)
    if args.out_npz:
        print(f"wrote_npz={args.out_npz}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
