"""Unit tests for the independent verifier (known-true and known-false identities)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__) + "/../src")
from verify_independent import numeric_falsify, parse_verified_eqs, REGISTRY  # noqa: E402

U = lambda lo, hi: (lambda k, n: [np.random.uniform(lo, hi, n) for _ in range(k)])


def test_known_true_identity_passes():
    # exp law recovered by the harness: f(x) - f(x-y)*f(y) = 0  (e^x = e^{x-y} * e^y)
    ok, mr, n = numeric_falsify("f(x) - f(x-y)*f(y)", np.exp, U(-5, 5), n=5000, eps=1e-3)
    assert ok, f"true identity rejected (max|resid|={mr})"
    assert n > 0


def test_known_false_identity_rejected():
    # false: f(x+y) - f(x) - f(y) = 0 is NOT true for exp
    ok, mr, n = numeric_falsify("f(x+y) - f(x) - f(y)", np.exp, U(-5, 5), n=5000, eps=1e-3)
    assert not ok, f"false identity accepted (max|resid|={mr})"


def test_sigmoid_identity_passes():
    # one of the recovered sigmoid RSRs (cross-multiplied), must verify
    eq = ("f(x)*f(x+y) + f(x)*f(x-y) - f(x) - 2*f(x+y)*f(x-y)"
          " - f(x+y)*f(y) + f(x+y) + f(x-y)*f(y)")
    ok, mr, n = numeric_falsify(eq, REGISTRY["33_sigmoid"]["nf"],
                                REGISTRY["33_sigmoid"]["sampler"], n=5000, eps=1e-3)
    assert ok, f"sigmoid RSR rejected (max|resid|={mr})"


def test_parse_verified_eqs_extracts_eq_strings(tmp_path):
    log = tmp_path / "33_sigmoid.txt"
    log.write_text("Starting 33_sigmoid\nVerified (2):\nEq(f(x)-f(y), 0)\nEq(f(x)+f(y)-1, 0)\nTook time: 1.0s\nEnding 33_sigmoid\n")
    eqs = parse_verified_eqs(str(log))
    assert len(eqs) == 2
    assert eqs[0].startswith("Eq(")
