#!/usr/bin/env python3
"""Independent negative-control verifier for V-Bitwen-LR recoveries.

Every equation in a harness log's ``Verified (n):`` block was **already
symbolically proven** by the upstream SymPy verifier (proof-by-simplification;
see the ``proved: True`` lines and the authors' ``verify()`` in
``upstream/src/bitween/analyzer.py``). This script provides the **independent
second mechanism**: a numeric falsifier that ``lambdify``s the equation's LHS
with the *numeric* implementation of ``f`` and evaluates the residual over ~1e4
random inputs in the function's domain. A true identity has max|residual| < eps;
this is wholly independent of SymPy.

It also runs **false-positive controls** (deliberately wrong identities) that the
falsifier MUST reject, proving it actually catches non-identities.

Two independent confirmations per recovered identity = upstream SymPy + our numeric
falsifier. Output: a table to stdout and ``independent_verification.csv``.
"""
import argparse
import csv
import os
import re
import sys

import numpy as np
import sympy

# --------------------------------------------------------------------------- #
# Registry: test_id -> function metadata for independent numeric falsification.
# numeric_f uses numpy (vectorized); sampler(k, n) returns k arrays of length n.
# --------------------------------------------------------------------------- #
U = lambda lo, hi: (lambda k, n: [np.random.uniform(lo, hi, n) for _ in range(k)])


def _nf_exp(x):
    return np.exp(x)


def _nf_inverse(x):
    return 1.0 / x


def _nf_sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def _nf_logistic(x, L=1, k=2, x0=0):
    return L / (1.0 + np.exp(-k * (x - x0)))


REGISTRY = {
    "01_identity":  dict(nf=lambda x: 5 * x,   sp=lambda x: 5 * x,                  domain="Real",          sampler=U(-5, 5)),
    "02_exp":       dict(nf=_nf_exp,           sp=lambda x: sympy.exp(x),           domain="Real",          sampler=U(-5, 5)),
    "12_inverse":   dict(nf=_nf_inverse,       sp=lambda x: 1 / x,                  domain="Real",          sampler=U(0.5, 5)),
    "18_cos":       dict(nf=np.cos,            sp=lambda x: sympy.cos(x),           domain="Real",          sampler=U(-5, 5)),
    "19_cosh":      dict(nf=np.cosh,           sp=lambda x: sympy.cosh(x),          domain="Real",          sampler=U(-5, 5)),
    "20_squared":   dict(nf=lambda x: x ** 2,  sp=lambda x: x ** 2,                 domain="Integer",       sampler=U(-5, 5)),
    "22_sinh":      dict(nf=np.sinh,           sp=lambda x: sympy.sinh(x),          domain="Real",          sampler=U(-5, 5)),
    "32_tanh":      dict(nf=np.tanh,           sp=lambda x: sympy.tanh(x),          domain="Real",          sampler=U(-5, 5)),
    "33_sigmoid":   dict(nf=_nf_sigmoid,       sp=lambda x: 1 / (1 + sympy.exp(-x)), domain="Real",         sampler=U(-5, 5)),
    "36_logistic":  dict(nf=_nf_logistic,      sp=lambda x: 1 / (1 + sympy.exp(-2 * x)), domain="Real",     sampler=U(-5, 5)),
    "43_arctan":    dict(nf=np.arctan,         sp=lambda x: sympy.atan(x),          domain="Real",          sampler=U(-2, 2)),
    "54_sqrt":      dict(nf=np.sqrt,           sp=lambda x: sympy.sqrt(x),          domain="Positive_Real", sampler=U(0.1, 5)),
}

def parse_verified_eqs(txt_path: str) -> list[str]:
    """Return the list of 'Eq(...)' strings from a harness log's Verified block.

    Line-based (the harness .txt logs are large and verbose; a regex with a
    nested quantifier backtracks catastrophically on them).
    """
    eqs: list[str] = []
    in_block = False
    with open(txt_path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            s = raw.strip()
            if not in_block:
                if s.startswith("Verified (") and s.endswith(":"):
                    in_block = True
                continue
            if s.startswith("Eq("):
                eqs.append(s)
            elif s == "":
                continue
            else:
                break
    return eqs


def numeric_falsify(eq_str, numeric_f, sampler, constants=None, n=10000, eps=1e-3):
    """Evaluate eq LHS numerically over random samples; True if max|residual| < eps."""
    constants = constants or {}
    expr = sympy.sympify(eq_str)
    if isinstance(expr, sympy.Eq):
        expr = expr.lhs
    expr = expr.subs({sympy.Symbol(c): sympy.sympify(v) for c, v in constants.items()})
    free = sorted(expr.free_symbols, key=lambda s: s.name)
    fn = sympy.lambdify(free, expr, modules=[{"f": numeric_f}, "numpy"])
    arrays = sampler(len(free), n)
    vals = np.asarray(fn(*arrays), dtype=float)
    vals = vals[np.isfinite(vals)]
    if vals.size == 0:
        return False, float("nan"), 0
    return bool(np.abs(vals).max() < eps), float(np.abs(vals).max()), int(vals.size)


def false_positive_controls():
    return [
        ("exp: f(x+y) - f(x) - f(y) (false)", _nf_exp, U(-5, 5), "f(x+y) - f(x) - f(y)"),
        ("sigmoid: f(x) - 1/2 (false)", _nf_sigmoid, U(-5, 5), "f(x) - 1/2"),
        ("squared: f(x+y) - f(x) - f(y) (false)", lambda x: x ** 2, U(-5, 5),
         "f(x+y) - f(x) - f(y)"),
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--res_dir", required=True)
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--eps", type=float, default=1e-3)
    args = ap.parse_args()
    np.random.seed(0)

    rows = []
    n_checked = n_confirmed = 0
    print("=" * 80, flush=True)
    print("Independent numeric falsifier on V-Bitwen-LR recoveries", flush=True)
    print("(each was already SymPy-proven by the upstream harness)", flush=True)
    print("=" * 80, flush=True)
    print(f"{'test_id':14s} {'eq#':>3s} {'numeric':>8s} {'max|resid|':>11s} {'n':>7s}  equation", flush=True)
    print("-" * 80, flush=True)

    for test_id, meta in REGISTRY.items():
        txt = os.path.join(args.res_dir, f"{test_id}.txt")
        if not os.path.exists(txt):
            continue
        for i, eq in enumerate(parse_verified_eqs(txt)):
            try:
                ok, mr, nv = numeric_falsify(eq, meta["nf"], meta["sampler"], n=args.n, eps=args.eps)
            except Exception as e:  # isolate one bad equation
                ok, mr, nv = False, float("nan"), 0
                eq = f"{eq}  [falsifier error: {e}]"
            n_checked += 1
            n_confirmed += int(ok)
            short = eq if len(eq) <= 46 else eq[:43] + "..."
            print(f"{test_id:14s} {i+1:>3d} {str(ok):>8s} {mr:>11.3e} {nv:>7d}  {short}", flush=True)
            rows.append(dict(test_id=test_id, eq_i=i + 1, equation=eq,
                             upstream_sympy="verified (harness)", numeric_verify=ok,
                             max_abs_residual=mr, n_valid_samples=nv))

    print("-" * 80, flush=True)
    print("False-positive controls (numeric falsifier MUST reject):", flush=True)
    fp_ok = 0
    for label, nf, samp, lhs in false_positive_controls():
        try:
            ok, mr, nv = numeric_falsify(lhs, nf, samp, n=args.n, eps=args.eps)
        except Exception:
            ok, mr, nv = False, float("nan"), 0
        rejected = not ok
        fp_ok += int(rejected)
        print(f"  [{'REJECT' if rejected else 'ACCEPT!!'}] {label}  (max|resid|={mr:.3e}, n={nv})", flush=True)
        rows.append(dict(test_id="_control", eq_i=0, equation=label,
                         upstream_sympy="n/a", numeric_verify=bool(ok),
                         max_abs_residual=mr, n_valid_samples=nv))

    out_csv = os.path.join(args.res_dir, "independent_verification.csv")
    with open(out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["test_id", "eq_i", "equation",
                                           "upstream_sympy", "numeric_verify",
                                           "max_abs_residual", "n_valid_samples"])
        w.writeheader()
        w.writerows(rows)

    print("-" * 80, flush=True)
    print(f"Recovered identities independently checked : {n_checked}", flush=True)
    print(f"Numeric falsifier CONFIRMS                  : {n_confirmed}/{n_checked}", flush=True)
    print(f"False-positive controls rejected            : {fp_ok}/3", flush=True)
    print(f"wrote {out_csv}", flush=True)


if __name__ == "__main__":
    main()
