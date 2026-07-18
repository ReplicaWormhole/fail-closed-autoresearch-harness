#!/usr/bin/env python3
"""LOOP-0011 scalar slack-domination lane.

Attacks the refined scalar crossed-minor inequality from LOOP-0010:

    GramSlack := N12*N21 - |m|^2
    ExchangePenalty := N12*N21 - D1*D2
    target: GramSlack >= ExchangePenalty.

Equivalently, whenever N12*N21 > 0,

    D1*D2/(N12*N21) >= |m|^2/(N12*N21).

The right-hand side is the squared mixed-Plucker correlation cos^2(W12,W21),
and the left-hand side is the same-pair diagonal ratio q.  This script records
slack, penalty, ratio, equality/near-equality controls, coordinate signatures,
and local searches for penalty approaching/exceeding slack.

Fail closed: this is only the scalar crossed PAL/PCL minor diagnostic, not a
proof of full PCL/CLAIM-0001.  No Hermitian/positive/normal assumptions are used.
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
LOOP10_PATH = ROOT / "research_harness/experiments/LOOP-0010_scalar_crossed_minor_certificate_lane.py"
spec = importlib.util.spec_from_file_location("loop10", LOOP10_PATH)
assert spec is not None and spec.loader is not None
loop10 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(loop10)
loop9 = loop10.loop9
N = loop10.N


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


def ij(k: int) -> tuple[int, int]:
    return divmod(k, 4)


def pair_label(pair: tuple[int, int]) -> str:
    return f"{pair[0]}={ij(pair[0])}, {pair[1]}={ij(pair[1])}"


def enriched(U: np.ndarray, V: np.ndarray) -> dict[str, Any]:
    r = loop10.mixed_decomposition(U, V)
    Nprod = float(r["N12_times_N21"])
    Dprod = float(r["D1_times_D2"])
    m_abs_sq = float(abs(complex(r["M03"])) ** 2)
    slack = float(r["gram_cauchy_slack_N12N21_minus_abs_m_sq"])
    penalty = float(r["exchange_penalty_N12N21_minus_D1D2"])
    delta = float(r["delta"])
    if Nprod > 1e-14:
        corr_sq = m_abs_sq / Nprod
        diag_ratio = Dprod / Nprod
        normalized_gap = diag_ratio - corr_sq
    else:
        corr_sq = None
        diag_ratio = None
        normalized_gap = None
    if slack > 1e-14:
        penalty_slack_ratio = penalty / slack
    else:
        penalty_slack_ratio = None
    return {
        **r,
        "abs_m_sq": m_abs_sq,
        "mixed_correlation_sq_abs_m_sq_over_Nprod": corr_sq,
        "same_pair_diagonal_ratio_Dprod_over_Nprod": diag_ratio,
        "normalized_gap_q_minus_corr_sq": normalized_gap,
        "penalty_to_slack_ratio": penalty_slack_ratio,
        "slack_minus_penalty": float(slack - penalty),
        "delta_over_Nprod": (float(delta / Nprod) if Nprod > 1e-14 else None),
        "equality_test_abs_delta": abs(delta),
    }


def coordinate_frame(pair: tuple[int, int]) -> np.ndarray:
    F = np.zeros((N, 2), dtype=np.complex128)
    F[pair[0], 0] = 1.0
    F[pair[1], 1] = 1.0
    return F


def rounded_signature(r: dict[str, Any]) -> tuple[Any, ...]:
    keys = [
        "D1", "D2", "N12_times_N21", "abs_m_sq",
        "gram_cauchy_slack_N12N21_minus_abs_m_sq",
        "exchange_penalty_N12N21_minus_D1D2", "delta",
        "mixed_correlation_sq_abs_m_sq_over_Nprod",
        "same_pair_diagonal_ratio_Dprod_over_Nprod",
    ]
    return tuple(None if r[k] is None else round(float(r[k]), 12) for k in keys)


def coordinate_scan(max_examples_per_signature: int = 4) -> dict[str, Any]:
    pairs = list(itertools.combinations(range(N), 2))
    total = 0
    max_identity_resid = 0.0
    min_delta = (float("inf"), None)
    max_penalty_minus_slack = (-float("inf"), None)
    max_ratio = (-float("inf"), None)
    min_normalized_gap = (float("inf"), None)
    equality_count = 0
    positive_penalty_count = 0
    sigs: dict[str, dict[str, Any]] = {}
    for up in pairs:
        U = coordinate_frame(up)
        for vp in pairs:
            V = coordinate_frame(vp)
            r = enriched(U, V)
            total += 1
            max_identity_resid = max(max_identity_resid, r["det_identity_residual_abs"], r["mixed_offdiag_error"])
            if r["delta"] < min_delta[0]:
                min_delta = (r["delta"], {"U_pair": up, "U_label": pair_label(up), "V_pair": vp, "V_label": pair_label(vp), "record": r})
            pms = r["penalty_minus_slack_equals_negative_delta"]
            if pms > max_penalty_minus_slack[0]:
                max_penalty_minus_slack = (pms, {"U_pair": up, "U_label": pair_label(up), "V_pair": vp, "V_label": pair_label(vp), "record": r})
            ratio = r["penalty_to_slack_ratio"]
            if ratio is not None and ratio > max_ratio[0]:
                max_ratio = (ratio, {"U_pair": up, "U_label": pair_label(up), "V_pair": vp, "V_label": pair_label(vp), "record": r})
            ng = r["normalized_gap_q_minus_corr_sq"]
            if ng is not None and ng < min_normalized_gap[0]:
                min_normalized_gap = (ng, {"U_pair": up, "U_label": pair_label(up), "V_pair": vp, "V_label": pair_label(vp), "record": r})
            if r["exchange_penalty_N12N21_minus_D1D2"] > 1e-12:
                positive_penalty_count += 1
            if abs(r["delta"]) < 1e-12:
                equality_count += 1
                sig = str(rounded_signature(r))
                if sig not in sigs:
                    sigs[sig] = {"count": 0, "signature": rounded_signature(r), "examples": []}
                sigs[sig]["count"] += 1
                if len(sigs[sig]["examples"]) < max_examples_per_signature:
                    sigs[sig]["examples"].append({"U_pair": up, "U_label": pair_label(up), "V_pair": vp, "V_label": pair_label(vp), "record": r})
    return {
        "total": total,
        "max_identity_or_offdiag_residual_abs": max_identity_resid,
        "min_delta": min_delta,
        "max_penalty_minus_slack_equals_negative_delta": max_penalty_minus_slack,
        "max_penalty_to_slack_ratio": max_ratio,
        "min_normalized_gap_q_minus_corr_sq": min_normalized_gap,
        "positive_exchange_penalty_count": positive_penalty_count,
        "equality_count_abs_delta_le_1e_12": equality_count,
        "equality_signature_count": len(sigs),
        "equality_signatures": sorted(sigs.values(), key=lambda d: (-d["count"], str(d["signature"])))[:30],
    }


def random_scan(rng: np.random.Generator, samples: int) -> dict[str, Any]:
    min_delta = (float("inf"), None)
    max_ratio = (-float("inf"), None)
    max_penalty_minus_slack = (-float("inf"), None)
    min_normalized_gap = (float("inf"), None)
    min_exchange_margin = (float("inf"), None)
    positive_penalty_count = 0
    max_identity_resid = 0.0
    for j in range(samples):
        U, V = loop9.rand_frame(2, rng), loop9.rand_frame(2, rng)
        r = enriched(U, V)
        max_identity_resid = max(max_identity_resid, r["det_identity_residual_abs"], r["mixed_offdiag_error"])
        if r["delta"] < min_delta[0]:
            min_delta = (r["delta"], j, r)
        ratio = r["penalty_to_slack_ratio"]
        if ratio is not None and ratio > max_ratio[0]:
            max_ratio = (ratio, j, r)
        pms = r["penalty_minus_slack_equals_negative_delta"]
        if pms > max_penalty_minus_slack[0]:
            max_penalty_minus_slack = (pms, j, r)
        ng = r["normalized_gap_q_minus_corr_sq"]
        if ng is not None and ng < min_normalized_gap[0]:
            min_normalized_gap = (ng, j, r)
        if r["exchange_product_margin_D1D2_minus_N12N21"] < min_exchange_margin[0]:
            min_exchange_margin = (r["exchange_product_margin_D1D2_minus_N12N21"], j, r)
        if r["exchange_penalty_N12N21_minus_D1D2"] > 1e-12:
            positive_penalty_count += 1
    return {
        "samples": samples,
        "max_identity_or_offdiag_residual_abs": max_identity_resid,
        "min_delta": min_delta,
        "max_penalty_to_slack_ratio": max_ratio,
        "max_penalty_minus_slack_equals_negative_delta": max_penalty_minus_slack,
        "min_normalized_gap_q_minus_corr_sq": min_normalized_gap,
        "min_exchange_product_margin_D1D2_minus_N12N21": min_exchange_margin,
        "positive_exchange_penalty_count": positive_penalty_count,
    }


def local_opt(seed: int, starts: int, maxiter: int) -> dict[str, Any]:
    if minimize is None:
        return {"scipy_available": False}
    rng = np.random.default_rng(seed)
    targets = {
        "min_delta": lambda r: r["delta"],
        "max_penalty_to_slack_ratio": lambda r: -(r["penalty_to_slack_ratio"] if r["penalty_to_slack_ratio"] is not None else -1e6),
        "min_normalized_gap_q_minus_corr_sq": lambda r: (r["normalized_gap_q_minus_corr_sq"] if r["normalized_gap_q_minus_corr_sq"] is not None else 1e6),
        "max_exchange_penalty": lambda r: -r["exchange_penalty_N12N21_minus_D1D2"],
    }
    out: dict[str, Any] = {"scipy_available": True, "starts": starts, "maxiter": maxiter}
    for name, getter in targets.items():
        best = (float("inf"), None)
        for k in range(starts):
            w0 = rng.normal(size=8 * N)

            def obj(w: np.ndarray) -> float:
                U, V = loop10.frame_from_unconstrained(w)
                return float(getter(enriched(U, V)))

            res = minimize(obj, w0, method="BFGS", options={"maxiter": maxiter, "gtol": 1e-7})
            if float(res.fun) < best[0]:
                U, V = loop10.frame_from_unconstrained(res.x)
                rec = enriched(U, V)
                best = (float(res.fun), {"start": k, "success": bool(res.success), "message": str(res.message), "nit": int(res.nit), "record": rec})
        out[name] = best
    return out


def controls() -> dict[str, Any]:
    return {
        "product_LOOP9": enriched(*loop9.product_example()),
        "traceless_LOOP9": enriched(*loop9.traceless_example()),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=11011)
    ap.add_argument("--samples", type=int, default=6000)
    ap.add_argument("--opt-starts", type=int, default=8)
    ap.add_argument("--maxiter", type=int, default=180)
    ap.add_argument("--out", type=Path, default=ROOT / "research_harness/logs/LOOP-0011_scalar_slack_domination_lane_seed11011.json")
    args = ap.parse_args()
    t0 = time.time()
    rng = np.random.default_rng(args.seed)
    res = {
        "loop": "LOOP-0011",
        "lane": "scalar slack-domination diagnostics for crossed PAL/PCL minor",
        "claim": "CLAIM-0001",
        "status": "refined_ratio_identity_recorded; equality/near-equality mechanisms probed; no scalar violation_or_proof; not full_PCL",
        "equivalence": "GramSlack>=ExchangePenalty iff D1*D2>=|m|^2 iff q:=D1D2/(N12N21) >= rho:=|m|^2/(N12N21) when N12N21>0",
        "fail_closed_caveat": "Scalar crossed-minor diagnostics only; no Hermitian/positive/normal assumptions are imposed and no full PCL conclusion is claimed.",
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
        "coordinate_max_ratio": res["coordinate_scan"]["max_penalty_to_slack_ratio"][0],
        "coordinate_equality_count": res["coordinate_scan"]["equality_count_abs_delta_le_1e_12"],
        "coordinate_equality_signature_count": res["coordinate_scan"]["equality_signature_count"],
        "random_min_delta": res["random_scan"]["min_delta"][:2],
        "random_max_ratio": res["random_scan"]["max_penalty_to_slack_ratio"][:2],
        "random_min_normalized_gap": res["random_scan"]["min_normalized_gap_q_minus_corr_sq"][:2],
        "local_keys": {k: (v[0] if isinstance(v, (list, tuple)) else v) for k, v in res["local_optimization"].items() if k != "scipy_available"},
        "wrote": str(args.out),
        "elapsed_sec": res["elapsed_sec"],
    }
    print(json.dumps(to_jsonable(summary), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
