import sys
sys.path.insert(0, '.')
from sympy import symbols
from sympy.printing import srepr
x, y = symbols('x y')
print('Actual srepr for set:', srepr({x, y}))
print('Actual srepr for dict:', srepr({x: y}))
# Expected recursive printing of Symbols
expected_set_1 = "{Symbol('x'), Symbol('y')}"
expected_set_2 = "{Symbol('y'), Symbol('x')}"
expected_dict = "{Symbol('x'): Symbol('y')}"
assert srepr({x, y}) in (expected_set_1, expected_set_2)
assert srepr({x: y}) == expected_dict
