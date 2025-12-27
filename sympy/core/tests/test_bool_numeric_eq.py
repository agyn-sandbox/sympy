from sympy import S


def test_boolean_float_zero_equality_is_symmetric():
    # Reproduces current asymmetry:
    # Before fix: S(0.0) == S.false is True, S.false == S(0.0) is False
    # Expected after fix: both should be False
    assert (S(0.0) == S.false) is False
    assert (S.false == S(0.0)) is False


def test_boolean_integer_zero_equality_is_symmetric():
    assert (S(0) == S.false) is False
    assert (S.false == S(0)) is False


def test_boolean_true_numeric_non_equality():
    assert (S(1.0) == S.true) is False
    assert (S.true == S(1.0)) is False
    assert (S(1) == S.true) is False
    assert (S.true == S(1)) is False


def test_numeric_equality_remains_correct():
    assert (S(0.0) == S(0)) is True
    assert (S(0) == S(0.0)) is True
    assert (S(1.0) == S(1)) is True
    assert (S(1) == S(1.0)) is True
