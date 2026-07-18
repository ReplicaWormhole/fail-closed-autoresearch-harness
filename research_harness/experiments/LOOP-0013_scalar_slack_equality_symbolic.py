#!/usr/bin/env python3
"""LOOP-0013 scalar-slack/equality symbolic family probe.

This script is deliberately fail-closed.  It does two things:

1. Exact SymPy checks on parametrized versions of the three LOOP-0012
   coordinate equality signatures.  The parameters are real rotations inside
   the active two-dimensional row/column support.  They are not a global
   equality classification, but they prove non-coordinate equality curves
   through each coordinate signature.
2. Numeric complex-unitary stress tests of the same promoted families using
   the LOOP-0011 scalar bookkeeping.

It does *not* prove the universal scalar inequality GramSlack >= ExchangePenalty
and does not prove CLAIM-0001/full PCL.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import time
from pathlib import Path
from typing import Any

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
LOOP11_PATH = ROOT / "research_harness/experiments/LOOP-0011_scalar_slack_domination_lane.py"


def load_loop11():
    spec = importlib.util.spec_from_file_location("loop11", LOOP11_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cjson(z: complex) -> dict[str, float]:
    return {"re": float(z.real), "im": float(z.imag)}


def to_jsonable(x: Any) -> Any:
    try:
        import numpy as np
    except Exception:  # pragma: no cover
        np = None
    if isinstance(x, dict):
        return {k: to_jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [to_jsonable(v) for v in x]
    if np is not None and isinstance(x, np.ndarray):
        return x.tolist()
    if np is not None and isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, complex):
        return cjson(x)
    return x


# ---------- exact SymPy scalar machinery ----------

def hs(A: sp.Matrix, B: sp.Matrix):
    # Real symbolic families only here, so conjugation is identity.
    return sum(A[i, j] * B[i, j] for i in range(A.rows) for j in range(A.cols))


def pt1_rank(U: sp.Matrix, V: sp.Matrix) -> sp.Matrix:
    return U.T * V


def pt2_rank(U: sp.Matrix, V: sp.Matrix) -> sp.Matrix:
    return U * V.T


def wedge_inner(a: sp.Matrix, b: sp.Matrix, c: sp.Matrix, d: sp.Matrix):
    return (a.dot(c) * b.dot(d)) - (a.dot(d) * b.dot(c))


def row_wedge_bilinear(Xa: sp.Matrix, Ya: sp.Matrix, Xb: sp.Matrix, Yb: sp.Matrix):
    total = 0
    for i in range(4):
        for j in range(4):
            total += wedge_inner(Xa.row(i), Ya.row(j), Xb.row(i), Yb.row(j))
    return sp.simplify(total)


def col_wedge_bilinear(Xa: sp.Matrix, Ya: sp.Matrix, Xb: sp.Matrix, Yb: sp.Matrix):
    total = 0
    for i in range(4):
        for j in range(4):
            total += wedge_inner(Xa.col(i), Ya.col(j), Xb.col(i), Yb.col(j))
    return sp.simplify(total)


def row_wedge_norm2(X: sp.Matrix, Y: sp.Matrix):
    return row_wedge_bilinear(X, Y, X, Y)


def col_wedge_norm2(X: sp.Matrix, Y: sp.Matrix):
    return col_wedge_bilinear(X, Y, X, Y)


def scalar_record(X1: sp.Matrix, X2: sp.Matrix, Y1: sp.Matrix, Y2: sp.Matrix) -> dict[str, str]:
    pairs = [(X1, Y1), (X1, Y2), (X2, Y1), (X2, Y2)]
    A = sp.zeros(4)
    B = sp.zeros(4)
    tr = []
    for U, V in pairs:
        tr.append(hs(U, V))
    for p, (U, V) in enumerate(pairs):
        for q, (X, Y) in enumerate(pairs):
            A[p, q] = hs(pt1_rank(U, V), pt1_rank(X, Y))
            B[p, q] = hs(pt2_rank(U, V), pt2_rank(X, Y))
    D = 2 * sp.eye(4) - A - B
    T = sp.Matrix(4, 4, lambda i, j: tr[i] * tr[j])
    M = D + sp.Rational(1, 2) * T
    m_plucker = (
        row_wedge_bilinear(X1, Y2, X2, Y1)
        + col_wedge_bilinear(X1, Y2, X2, Y1)
        + sp.Rational(1, 2) * tr[0] * tr[3]
    )
    N12 = row_wedge_norm2(X1, Y2) + col_wedge_norm2(X1, Y2) + sp.Rational(1, 2) * tr[1] ** 2
    N21 = row_wedge_norm2(X2, Y1) + col_wedge_norm2(X2, Y1) + sp.Rational(1, 2) * tr[2] ** 2
    D1 = sp.simplify(M[0, 0])
    D2 = sp.simplify(M[3, 3])
    m = sp.simplify(M[0, 3])
    Nprod = sp.simplify(N12 * N21)
    abs_m_sq = sp.simplify(m * m)  # real families
    gram_slack = sp.factor(Nprod - abs_m_sq)
    exchange_penalty = sp.factor(Nprod - D1 * D2)
    delta = sp.factor(D1 * D2 - abs_m_sq)
    return {
        "D1": str(sp.factor(D1)),
        "D2": str(sp.factor(D2)),
        "M03": str(sp.factor(m)),
        "mixed_plucker_M03_residual": str(sp.factor(m - m_plucker)),
        "N12": str(sp.factor(N12)),
        "N21": str(sp.factor(N21)),
        "N12_times_N21": str(sp.factor(Nprod)),
        "abs_m_sq": str(sp.factor(abs_m_sq)),
        "GramSlack": str(gram_slack),
        "ExchangePenalty": str(exchange_penalty),
        "Delta": str(delta),
        "slack_minus_penalty": str(sp.factor(gram_slack - exchange_penalty)),
    }


def zero_mat() -> sp.Matrix:
    return sp.zeros(4, 4)


def row_outer(r: int, q: sp.Matrix) -> sp.Matrix:
    M = zero_mat()
    for c in range(4):
        M[r, c] = q[c]
    return M


def col_outer(c: int, q: sp.Matrix) -> sp.Matrix:
    M = zero_mat()
    for r in range(4):
        M[r, c] = q[r]
    return M


def exact_parametric_families() -> dict[str, Any]:
    c, s = sp.symbols("c s", real=True)
    q1 = sp.Matrix([c, s, 0, 0])
    q2 = sp.Matrix([-s, c, 0, 0])
    # Reduction modulo c^2+s^2=1 by substitution after expansion.
    def reduce_unit_circle_record(rec: dict[str, str]) -> dict[str, str]:
        out = {}
        gb = sp.groebner([c**2 + s**2 - 1], c, s, order="grlex", domain=sp.QQ)
        for k, v in rec.items():
            expr = sp.sympify(v, locals={"c": c, "s": s})
            # Exact normal form modulo the unit-circle constraint c^2+s^2=1.
            poly_expr = sp.Poly(sp.expand(expr), c, s, domain=sp.QQ).as_expr()
            _, rem = gb.reduce(poly_expr)
            out[k] = str(sp.factor(rem))
        return out

    row_id = reduce_unit_circle_record(scalar_record(row_outer(0, q1), row_outer(0, q2), row_outer(0, q1), row_outer(0, q2)))
    row_translate = reduce_unit_circle_record(scalar_record(row_outer(0, q1), row_outer(0, q2), row_outer(1, q1), row_outer(1, q2)))
    col_id = reduce_unit_circle_record(scalar_record(col_outer(0, q1), col_outer(0, q2), col_outer(0, q1), col_outer(0, q2)))
    col_translate = reduce_unit_circle_record(scalar_record(col_outer(0, q1), col_outer(0, q2), col_outer(1, q1), col_outer(1, q2)))
    diagonal_id = reduce_unit_circle_record(scalar_record(row_outer(0, q1), row_outer(1, q2), row_outer(0, q1), row_outer(1, q2)))

    return {
        "parameters": "real c,s with c^2+s^2=1; q1=(c,s,0,0), q2=(-s,c,0,0)",
        "same_row_identical_support_family": row_id,
        "same_row_parallel_translate_family": row_translate,
        "same_column_identical_support_family": col_id,
        "same_column_parallel_translate_family": col_translate,
        "diagonal_identical_support_family": diagonal_id,
        "certificate_status": (
            "exact on these families: mixed Plucker residual=0 and Delta=0 while "
            "GramSlack=ExchangePenalty>0; this is guardrail evidence, not a universal SOS certificate"
        ),
    }


# ---------- numeric complex-unitary family stress tests ----------

def numeric_complex_family_tests(seed: int, samples: int) -> dict[str, Any]:
    import numpy as np

    loop11 = load_loop11()
    rng = np.random.default_rng(seed)
    n = 4
    N = 16

    def randQ(k: int = 2):
        A = rng.normal(size=(n, k)) + 1j * rng.normal(size=(n, k))
        Q, _ = np.linalg.qr(A)
        return Q[:, :k]

    def pack(mats):
        F = np.zeros((N, 2), dtype=complex)
        for j, M in enumerate(mats):
            F[:, j] = M.reshape(-1)
        return F

    def row_family(r: int, Q):
        er = np.eye(n)[r]
        return pack([er[:, None] @ Q[:, i][None, :] for i in range(2)])

    def col_family(c: int, Q):
        ec = np.eye(n)[c]
        return pack([Q[:, i][:, None] @ ec[None, :] for i in range(2)])

    def diag_family(r: int, s: int, Q):
        er = np.eye(n)[r]
        es = np.eye(n)[s]
        return pack([er[:, None] @ Q[:, 0][None, :], es[:, None] @ Q[:, 1][None, :]])

    constructors = {
        "same_row_identical": lambda Q: (row_family(0, Q), row_family(0, Q)),
        "same_row_translate": lambda Q: (row_family(0, Q), row_family(1, Q)),
        "same_column_identical": lambda Q: (col_family(0, Q), col_family(0, Q)),
        "same_column_translate": lambda Q: (col_family(0, Q), col_family(1, Q)),
        "diagonal_identical": lambda Q: (diag_family(0, 1, Q), diag_family(0, 1, Q)),
    }
    out = {}
    for name, ctor in constructors.items():
        max_abs_delta = 0.0
        max_abs_ratio_minus_one = 0.0
        min_slack = float("inf")
        max_identity = 0.0
        first = None
        for _ in range(samples):
            Q = randQ(2)
            U, V = ctor(Q)
            r = loop11.enriched(U, V)
            max_abs_delta = max(max_abs_delta, abs(float(r["delta"])))
            ratio = r["penalty_to_slack_ratio"]
            if ratio is not None:
                max_abs_ratio_minus_one = max(max_abs_ratio_minus_one, abs(float(ratio) - 1.0))
            min_slack = min(min_slack, float(r["gram_cauchy_slack_N12N21_minus_abs_m_sq"]))
            max_identity = max(max_identity, float(r["det_identity_residual_abs"]), float(r["mixed_offdiag_error"]))
            if first is None:
                first = {
                    "D1": r["D1"],
                    "D2": r["D2"],
                    "GramSlack": r["gram_cauchy_slack_N12N21_minus_abs_m_sq"],
                    "ExchangePenalty": r["exchange_penalty_N12N21_minus_D1D2"],
                    "Delta": r["delta"],
                    "ratio": r["penalty_to_slack_ratio"],
                }
        out[name] = {
            "samples": samples,
            "max_abs_delta": max_abs_delta,
            "max_abs_ratio_minus_one": max_abs_ratio_minus_one,
            "min_GramSlack": min_slack,
            "max_identity_residual": max_identity,
            "first_record": first,
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=13013)
    ap.add_argument("--samples", type=int, default=100)
    ap.add_argument("--out", type=Path, default=ROOT / "research_harness/logs/LOOP-0013_scalar_slack_equality_symbolic_seed13013.json")
    args = ap.parse_args()
    t0 = time.time()
    exact = exact_parametric_families()
    numeric = numeric_complex_family_tests(args.seed, args.samples)
    result = {
        "loop": "LOOP-0013",
        "claim": "CLAIM-0001",
        "workstreams": ["WS-scalar-slack", "WS-equality-geometry"],
        "status": "parametric equality families certified in restricted charts; no universal scalar SOS/Plucker certificate; fail_closed",
        "exact_real_rotation_families": exact,
        "numeric_complex_unitary_family_tests": numeric,
        "adversarial_caveat": "Coordinate/local equality signatures were globalized only to explicit families, not classified globally on Gr(2,16)xGr(2,16).",
        "elapsed_sec": time.time() - t0,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(to_jsonable(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": result["status"],
        "wrote": str(args.out),
        "families": list(exact.keys()),
        "numeric_max_abs_delta_by_family": {k: v["max_abs_delta"] for k, v in numeric.items()},
        "elapsed_sec": result["elapsed_sec"],
    }
    print(json.dumps(to_jsonable(summary), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
