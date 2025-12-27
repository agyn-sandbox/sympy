from sympy.core.basic import Basic
from sympy.core.symbol import Str

from sympy.codegen.ast import String, QuotedString, Comment


def _assert_positional_invariance(expr, expected_text):
    assert expr.text == expected_text
    assert isinstance(expr.text, str)
    assert expr.args == (Str(expected_text),)
    assert isinstance(expr.args[0], Basic)
    assert expr.func(*expr.args) == expr


def test_String_args_are_positional_and_basic():
    _assert_positional_invariance(String('foo'), 'foo')


def test_QuotedString_args_are_positional_and_basic():
    _assert_positional_invariance(QuotedString('bar'), 'bar')


def test_Comment_args_are_positional_and_basic():
    _assert_positional_invariance(Comment('baz'), 'baz')
