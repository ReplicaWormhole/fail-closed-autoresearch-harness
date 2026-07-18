#!/usr/bin/env python3
"""LOOP-0010 scalar crossed-minor certificate lane.

This diagnostic attacks the determinant-level scalar crossed PAL/PCL minor

    Delta = M_00 M_33 - |M_03|^2 >= 0

using the LOOP-0009 exact mixed Plucker off-diagonal identity.  It records the
exact determinant correction obtained by applying Cauchy to the mixed Plucker
vectors W12 and W21:

    m = M_03 = <W12,W21>
    N12 = ||W12||^2,  N21 = ||W21||^2
    Delta = (N12*N21 - |m|^2) - (N12*N21 - D1*D2).

The first term is the Gram/Cauchy slack of the mixed vectors; the second is the
"exchange penalty" incurred because the actual crossed minor uses the same-pair
PAL diagonals D(X1,Y1), D(X2,Y2), not the mixed diagonals D(X1,Y2), D(X2,Y1).

This is not a proof.  It checks whether natural determinant-level refinements
such as D1*D2 >= N12*N21 or simple positive correction terms survive random,
coordinate, and local-optimization probes.
"""
from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import time
from pathlib import Path
from typing import Any

import numpy as np

try:
    from scipy.optimize import minimize
except Exception:  # pragma: no cover
    minimize = None

ROOT = Path(__file__).resolve().parents[2]
LOOP9_PATH = ROOT / "research_harness/experiments/LOOP-0009_mixed_plucker_probe.py"
spec = importlib.util.spec_from_file_location("loop9", LOOP9_PATH)
assert spec is not None and spec.loader is not None
loop9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop9)

N = loop9.N
CROSS = loop9.CROSS


def cjson(z: complex) -> dict[str, float]:
    return {"re": float(np.real(z)), "im": float(np.imag(z))}


def to_jsonable(x: Any) -> Any:
    if isinstance(x, dict):
        return {k: to_jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [to_jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        if np.iscomplexobj(x):
            return [cjson(complex(z)) for z in x.reshape(-1)] if x.ndim == 1 else [[cjson(complex(z)) for z in row] for row in x]
        return x.tolist()
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, complex) or np.iscomplexobj(x):
        return cjson(complex(x))
    return x


def frame_from_unconstrained(w: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return loop9.frame_from_unconstrained(w)


def mixed_decomposition(U: np.ndarray, V: np.ndarray) -> dict[str, Any]:
    d = loop9.scalar_data(U, V)
    D1 = float(d["D1"])
    D2 = float(d["D2"])
    m = complex(d["M03"])
    N12 = float(d["mixed_norm_12"])
    N21 = float(d["mixed_norm_21"])
    gram_slack = float(N12 * N21 - abs(m) ** 2)
    exchange_penalty = float(N12 * N21 - D1 * D2)
    delta_from_terms = float(gram_slack - exchange_penalty)
    delta_direct = float(d["delta"])
    return {
        **d,
        "N12_times_N21": float(N12 * N21),
        "D1_times_D2": float(D1 * D2),
        "gram_cauchy_slack_N12N21_minus_abs_m_sq": gram_slack,
        "exchange_penalty_N12N21_minus_D1D2": exchange_penalty,
        "det_identity_residual_abs": float(abs(delta_direct - delta_from_terms)),
        "exchange_product_margin_D1D2_minus_N12N21": float(D1 * D2 - N12 * N21),
        "penalty_minus_slack_equals_negative_delta": float(exchange_penalty - gram_slack),
        "penalty_to_slack_ratio_if_positive_slack": (float(exchange_penalty / gram_slack) if gram_slack > 1e-14 else None),
    }


def coordinate_frame(pair: tuple[int, int]) -> np.ndarray:
    F = np.zeros((N, 2), dtype=np.complex128)
    F[pair[0], 0] = 1.0
    F[pair[1], 1] = 1.0
    return F


def coordinate_scan() -> dict[str, Any]:
    pairs = list(itertools.combinations(range(N), 2))
    total = 0
    min_delta = (float("inf"), None)
    min_exchange_margin = (float("inf"), None)
    max_identity_resid = 0.0
    positive_exchange_penalty_count = 0
    positive_penalty_with_zero_delta_examples = []
    max_ratio = (-float("inf"), None)
    max_penalty_minus_slack = (-float("inf"), None)
    for up in pairs:
        U = coordinate_frame(up)
        for vp in pairs:
            V = coordinate_frame(vp)
            r = mixed_decomposition(U, V)
            total += 1
            max_identity_resid = max(max_identity_resid, r["det_identity_residual_abs"])
            if r["delta"] < min_delta[0]:
                min_delta = (r["delta"], {"U_pair": up, "V_pair": vp, "record": r})
            if r["exchange_product_margin_D1D2_minus_N12N21"] < min_exchange_margin[0]:
                min_exchange_margin = (r["exchange_product_margin_D1D2_minus_N12N21"], {"U_pair": up, "V_pair": vp, "record": r})
            if r["exchange_penalty_N12N21_minus_D1D2"] > 1e-12:
                positive_exchange_penalty_count += 1
                if abs(r["delta"]) < 1e-12 and len(positive_penalty_with_zero_delta_examples) < 5:
                    positive_penalty_with_zero_delta_examples.append({"U_pair": up, "V_pair": vp, "record": r})
            ratio = r["penalty_to_slack_ratio_if_positive_slack"]
            if ratio is not None and ratio > max_ratio[0]:
                max_ratio = (ratio, {"U_pair": up, "V_pair": vp, "record": r})
            pms = r["penalty_minus_slack_equals_negative_delta"]
            if pms > max_penalty_minus_slack[0]:
                max_penalty_minus_slack = (pms, {"U_pair": up, "V_pair": vp, "record": r})
    return {
        "total": total,
        "max_det_identity_residual_abs": max_identity_resid,
        "min_delta": min_delta,
        "min_exchange_product_margin_D1D2_minus_N12N21": min_exchange_margin,
        "positive_exchange_penalty_count": positive_exchange_penalty_count,
        "positive_penalty_with_zero_delta_examples": positive_penalty_with_zero_delta_examples,
        "max_penalty_to_slack_ratio": max_ratio,
        "max_penalty_minus_slack_equals_negative_delta": max_penalty_minus_slack,
    }


def random_scan(rng: np.random.Generator, samples: int) -> dict[str, Any]:
    min_delta = (float("inf"), None)
    min_exchange_margin = (float("inf"), None)
    max_identity_resid = 0.0
    max_ratio = (-float("inf"), None)
    max_penalty_minus_slack = (-float("inf"), None)
    positive_exchange_penalty_count = 0
    for j in range(samples):
        U, V = loop9.rand_frame(2, rng), loop9.rand_frame(2, rng)
        r = mixed_decomposition(U, V)
        max_identity_resid = max(max_identity_resid, r["det_identity_residual_abs"], r["mixed_offdiag_error"])
        if r["delta"] < min_delta[0]:
            min_delta = (r["delta"], j)
        if r["exchange_product_margin_D1D2_minus_N12N21"] < min_exchange_margin[0]:
            min_exchange_margin = (r["exchange_product_margin_D1D2_minus_N12N21"], j)
        if r["exchange_penalty_N12N21_minus_D1D2"] > 1e-12:
            positive_exchange_penalty_count += 1
        ratio = r["penalty_to_slack_ratio_if_positive_slack"]
        if ratio is not None and ratio > max_ratio[0]:
            max_ratio = (ratio, j)
        pms = r["penalty_minus_slack_equals_negative_delta"]
        if pms > max_penalty_minus_slack[0]:
            max_penalty_minus_slack = (pms, j)
    return {
        "samples": samples,
        "max_identity_or_offdiag_residual_abs": max_identity_resid,
        "min_delta": min_delta,
        "min_exchange_product_margin_D1D2_minus_N12N21": min_exchange_margin,
        "positive_exchange_penalty_count": positive_exchange_penalty_count,
        "max_penalty_to_slack_ratio": max_ratio,
        "max_penalty_minus_slack_equals_negative_delta": max_penalty_minus_slack,
    }


def local_opt(seed: int, starts: int, maxiter: int) -> dict[str, Any]:
    if minimize is None:
        return {"scipy_available": False}
    rng = np.random.default_rng(seed)
    targets = {
        "min_delta": lambda r: r["delta"],
        "min_exchange_product_margin": lambda r: r["exchange_product_margin_D1D2_minus_N12N21"],
        "max_penalty_minus_slack": lambda r: -r["penalty_minus_slack_equals_negative_delta"],
    }
    out: dict[str, Any] = {"scipy_available": True, "starts": starts, "maxiter": maxiter}
    for name, getter in targets.items():
        best = (float("inf"), None)
        for k in range(starts):
            w0 = rng.normal(size=8 * N)

            def obj(w: np.ndarray) -> float:
                U, V = frame_from_unconstrained(w)
                return float(getter(mixed_decomposition(U, V)))

            res = minimize(obj, w0, method="BFGS", options={"maxiter": maxiter, "gtol": 1e-7})
            if float(res.fun) < best[0]:
                U, V = frame_from_unconstrained(res.x)
                rec = mixed_decomposition(U, V)
                best = (float(res.fun), {"start": k, "success": bool(res.success), "message": str(res.message), "nit": int(res.nit), "record": rec})
        out[name] = best
    return out


def controls() -> dict[str, Any]:
    return {
        "product_LOOP9": mixed_decomposition(*loop9.product_example()),
        "traceless_LOOP9": mixed_decomposition(*loop9.traceless_example()),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=10010)
    ap.add_argument("--samples", type=int, default=5000)
    ap.add_argument("--opt-starts", type=int, default=8)
    ap.add_argument("--maxiter", type=int, default=160)
    ap.add_argument("--out", type=Path, default=ROOT / "research_harness/logs/LOOP-0010_scalar_crossed_minor_certificate_lane_seed10010.json")
    args = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(args.seed)
    res = {
        "loop": "LOOP-0010",
        "lane": "scalar crossed PAL/PCL minor determinant certificate diagnostics",
        "claim": "CLAIM-0001",
        "status": "exact_cauchy_minus_exchange_identity_recorded; determinant_level_simple_exchange_product_ansatz_obstructed; no proof_or_counterexample",
        "identity": "Delta = (N12*N21-|m|^2) - (N12*N21-D1*D2), m=<W12,W21> from LOOP-0009 mixed Plucker identity",
        "fail_closed_caveat": "Numerical diagnostics only; scalar crossed minor is not full PCL; no Hermitian/positive/normal assumptions are imposed.",
        "controls": controls(),
        "coordinate_scan": coordinate_scan(),
        "random_scan": random_scan(rng, args.samples),
        "local_optimization": local_opt(args.seed + 1, args.opt_starts, args.maxiter),
        "elapsed_sec": time.time() - t0,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(to_jsonable(res), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": res["status"],
        "coordinate_min_delta": res["coordinate_scan"]["min_delta"][0],
        "coordinate_min_exchange_product_margin": res["coordinate_scan"]["min_exchange_product_margin_D1D2_minus_N12N21"][0],
        "coordinate_positive_exchange_penalty_count": res["coordinate_scan"]["positive_exchange_penalty_count"],
        "random_min_delta": res["random_scan"]["min_delta"],
        "random_min_exchange_product_margin": res["random_scan"]["min_exchange_product_margin_D1D2_minus_N12N21"],
        "random_max_penalty_minus_slack": res["random_scan"]["max_penalty_minus_slack_equals_negative_delta"],
        "local_opt_keys": {k: (v[0] if isinstance(v, list | tuple) else v) for k, v in res["local_optimization"].items() if k != "scipy_available"},
        "wrote": str(args.out),
        "elapsed_sec": res["elapsed_sec"],
    }
    print(json.dumps(to_jsonable(summary), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
