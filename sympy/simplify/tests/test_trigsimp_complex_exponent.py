from sympy import I, cos, simplify, sin, symbols, tan, trigsimp


def test_trigsimp_complex_exponent_no_change():
    x = symbols('x')
    expressions = [
        cos(x) ** I,
        sin(x) ** I,
        (cos(x) + sin(x)) ** I,
    ]

    for expr in expressions:
        assert simplify(expr) == expr
        assert simplify(trigsimp(expr) - expr) == 0
        assert simplify(trigsimp(expr, method='fu') - expr) == 0


def test_trigsimp_integer_exponent_behaviour_preserved():
    x = symbols('x')

    assert simplify(trigsimp(cos(x) ** 2, method='fu') - (1 - sin(x) ** 2)) == 0
    assert simplify(trigsimp(sin(x) ** 4, method='fu') - (1 - cos(x) ** 2) ** 2) == 0
    assert simplify(trigsimp(1 / cos(x) ** 2 - 1, method='fu') - tan(x) ** 2) == 0


def test_trigsimp_symbolic_non_integer_exponent_skipped():
    x = symbols('x')
    a = symbols('a', real=True)

    assert simplify(trigsimp(cos(x) ** a) - cos(x) ** a) == 0
    assert simplify(trigsimp(sin(x) ** a) - sin(x) ** a) == 0
    assert trigsimp(cos(x) ** a, method='fu') == cos(x) ** a
    assert trigsimp(sin(x) ** a, method='fu') == sin(x) ** a
