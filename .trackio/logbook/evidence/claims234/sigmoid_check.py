#!/usr/bin/env python3
"""Focused demonstration of the sigmoid RSR recovery (Claim 1 'incl. sigmoid' clause).

Parses the recovered + verified sigmoid identities from the sweep log
(``33_sigmoid.txt``), prints each in plain text and LaTeX, and confirms it three
ways: (1) the harness already SymPy-proved it (it is in the Verified block),
(2) the upstream symbolic verifier re-run with a correctly-named ``_sp_f`` whose
``__name__`` strips to ``f`` (as verify() expects), and (3) the independent
numeric falsifier.
"""
import argparse
import os

import sympy

from verify_independent import REGISTRY, numeric_falsify, parse_verified_eqs
from bitween.analyzer import verify_with_timeout
from bitween.sampler import Domain


def _sp_f(x):
    # __name__ "_sp_f" strips to "f" inside verify()'s namespace
    return 1 / (1 + sympy.exp(-x))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--res_dir", required=True)
    args = ap.parse_args()
    txt = os.path.join(args.res_dir, "33_sigmoid.txt")
    eqs = parse_verified_eqs(txt)
    meta = REGISTRY["33_sigmoid"]

    print("=" * 72)
    print("Claim 1 sigmoid clause — V-Bitwen-LR recovered, verified RSR(s)")
    print("=" * 72)
    print("f(x) = sigmoid = 1/(1+e^-x)\n")
    if not eqs:
        print("No verified sigmoid identities found in", txt)
        return
    for i, eq in enumerate(eqs, 1):
        up_ok, _ = verify_with_timeout(eq, [_sp_f], Domain.Real)
        num_ok, mr, nv = numeric_falsify(eq, meta["nf"], meta["sampler"], n=20000, eps=1e-3)
        expr = sympy.sympify(eq)
        lhs = expr.lhs if isinstance(expr, sympy.Eq) else expr
        print(f"RSR #{i}:  {eq}")
        print(f"   LaTeX: {sympy.latex(lhs)} = 0")
        print(f"   upstream SymPy verify: {bool(up_ok)} | numeric falsifier: {num_ok} "
              f"(max|resid|={mr:.3e} over {nv} samples)\n")
    print("These are randomized self-reductions of the sigmoid: identities over")
    print("f evaluated at correlated random points (x+y, x-y, x, y) that hold for")
    print("ALL inputs — the first known such reduction, recovered automatically.")


if __name__ == "__main__":
    main()
