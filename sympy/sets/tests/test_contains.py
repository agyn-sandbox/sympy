from sympy.core.expr import unchanged
from sympy.core.numbers import oo
from sympy.core.relational import Eq
from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy.functions.elementary.piecewise import Piecewise
from sympy.sets import ConditionSet
from sympy.sets.contains import Contains
from sympy.sets.sets import (FiniteSet, Interval)
from sympy.testing.pytest import raises

def test_contains_basic():
    raises(TypeError, lambda: Contains(S.Integers, 1))
    assert Contains(2, S.Integers) is S.true
    assert Contains(-2, S.Naturals) is S.false

    i = Symbol('i', integer=True)
    assert Contains(i, S.Naturals) == Contains(i, S.Naturals, evaluate=False)


def test_issue_6194():
    x = Symbol('x')
    assert unchanged(Contains, x, Interval(0, 1))
    assert Interval(0, 1).contains(x) == (S.Zero <= x) & (x <= 1)
    assert Contains(x, FiniteSet(0)) != S.false
    assert Contains(x, Interval(1, 1)) != S.false
    assert Contains(x, S.Integers) != S.false


def test_issue_10326():
    assert Contains(oo, Interval(-oo, oo)) == False
    assert Contains(-oo, Interval(-oo, oo)) == False


def test_binary_symbols():
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    assert Contains(x, FiniteSet(y, Eq(z, True))
        ).binary_symbols == {y, z}


def test_as_set_basic_sets():
    x = Symbol('x')

    assert Contains(x, S.Reals).as_set() is S.Reals
    assert Contains(x, Interval(0, 1)).as_set() == Interval(0, 1)


def test_as_set_condition_set_fallback():
    x = Symbol('x')

    dependent = Contains(x, Interval(x, oo)).as_set()
    assert isinstance(dependent, ConditionSet)
    assert dependent.sym == x
    assert dependent.condition == Contains(x, Interval(x, oo))
    assert dependent.base_set is S.UniversalSet

    shifted = Contains(x + 1, Interval(0, 1)).as_set()
    assert isinstance(shifted, ConditionSet)
    assert shifted.sym == x
    assert shifted.condition == Contains(x + 1, Interval(0, 1))
    assert shifted.base_set is S.UniversalSet


def test_piecewise_contains_condition():
    x = Symbol('x')

    pw = Piecewise((6, Contains(x, S.Reals)), (7, True))
    pairs = pw.as_expr_set_pairs()
    assert pairs == [(6, S.Reals)]

def test_type_error():
    # Pass in a parameter not of type "set"
    raises(TypeError, lambda: Contains(2, None))
