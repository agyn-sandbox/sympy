import pytest

from sympy import Symbol
from sympy.core.basic import Basic
from sympy.core._print_helpers import Printable
from sympy.printing.str import sstr


def test_symbol_instances_have_no_dict():
    symbol = Symbol('s')

    assert not hasattr(symbol, '__dict__')
    with pytest.raises(AttributeError):
        _ = symbol.__dict__


def test_basic_instances_have_no_dict():
    basic = Basic()

    assert not hasattr(basic, '__dict__')
    with pytest.raises(AttributeError):
        _ = basic.__dict__


def test_printable_declares_empty_slots():
    assert Printable.__slots__ == ()


def test_symbol_printing_is_unchanged():
    assert sstr(Symbol('s')) == 's'
