from __future__ import print_function, division

from sympy.core.function import Function
from sympy.core.singleton import S


class q_pochhammer(Function):
    r"""The q-Pochhammer symbol ``(a; q)_n``.

    This is defined as :math:`\prod_{k=0}^{n-1} (1 - a q^k)` for
    non-negative integer ``n`` with ``(a; q)_0 = 1``. The symbolic form is
    left unevaluated for general ``n`` while preserving the normalization at
    ``n = 0``.
    """

    nargs = 3

    @classmethod
    def eval(cls, a, q, n):
        if n.is_zero:
            return S.One

    def _eval_rewrite_as_Product(self, a, q, n, **kwargs):
        from sympy.concrete.products import Product
        from sympy.core.symbol import Dummy

        k = Dummy('k')
        return Product(1 - a*q**k, (k, 0, n - 1))
