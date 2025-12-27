from sympy import Symbol, posify


def test_posify_preserves_compatible_assumptions():
    cases = (
        (Symbol('a_finite', finite=True), 'is_finite'),
        (Symbol('a_integer', integer=True), 'is_integer'),
        (Symbol('a_rational', rational=True), 'is_rational'),
        (Symbol('a_even', even=True), 'is_even'),
        (Symbol('a_odd', odd=True), 'is_odd'),
        (Symbol('a_nonzero', nonzero=True), 'is_nonzero'),
        (Symbol('a_nonnegative', nonnegative=True), 'is_nonnegative'),
        (Symbol('a_real', real=True), 'is_real'),
        (Symbol('a_complex', complex=True), 'is_complex'),
    )

    for sym, attr in cases:
        posified, reps = posify(sym)

        assert posified.is_positive is True
        assert getattr(posified, attr) is True
        assert reps == {posified: sym}


def test_posify_skips_conflicting_assumptions():
    conflicting = (
        Symbol('m_negative', negative=True),
        Symbol('m_nonpositive', nonpositive=True),
        Symbol('m_zero', zero=True),
        Symbol('m_imaginary', imaginary=True),
        Symbol('m_prime', prime=True),
    )

    for sym in conflicting:
        posified, reps = posify(sym)

        assert posified == sym
        assert reps == {}


def test_posify_preserves_noncommutative():
    nc = Symbol('nc', commutative=False)
    posified, reps = posify(nc)

    assert posified == nc
    assert posified.is_commutative is False
    assert reps == {}
