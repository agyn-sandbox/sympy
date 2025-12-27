from sympy.testing.pytest import raises

from sympy.core.symbol import Symbol
from sympy.matrices import Matrix
from sympy.polys.matrices.normalforms import (
    invariant_factors, smith_normal_form,
    hermite_normal_form, _hermite_normal_form, _hermite_normal_form_modulo_D)
from sympy.polys.domains import ZZ, QQ
from sympy.polys.matrices import DomainMatrix, DM
from sympy.polys.matrices.exceptions import DMDomainError, DMShapeError


def _column_data_from_row_style(rows):
    flipped = [list(reversed(row)) for row in reversed(rows)]
    return [list(col) for col in zip(*flipped)]


def test_smith_normal():

    m = DM([[12, 6, 4, 8], [3, 9, 6, 12], [2, 16, 14, 28], [20, 10, 10, 20]], ZZ)
    smf = DM([[1, 0, 0, 0], [0, 10, 0, 0], [0, 0, -30, 0], [0, 0, 0, 0]], ZZ)
    assert smith_normal_form(m).to_dense() == smf

    x = Symbol('x')
    m = DM([[x-1,  1, -1],
            [  0,  x, -1],
            [  0, -1,  x]], QQ[x])
    dx = m.domain.gens[0]
    assert invariant_factors(m) == (1, dx-1, dx**2-1)

    zr = DomainMatrix([], (0, 2), ZZ)
    zc = DomainMatrix([[], []], (2, 0), ZZ)
    assert smith_normal_form(zr).to_dense() == zr
    assert smith_normal_form(zc).to_dense() == zc

    assert smith_normal_form(DM([[2, 4]], ZZ)).to_dense() == DM([[2, 0]], ZZ)
    assert smith_normal_form(DM([[0, -2]], ZZ)).to_dense() == DM([[-2, 0]], ZZ)
    assert smith_normal_form(DM([[0], [-2]], ZZ)).to_dense() == DM([[-2], [0]], ZZ)

    m =   DM([[3, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0]], ZZ)
    snf = DM([[1, 0, 0, 0], [0, 6, 0, 0], [0, 0, 0, 0]], ZZ)
    assert smith_normal_form(m).to_dense() == snf

    raises(ValueError, lambda: smith_normal_form(DM([[1]], ZZ[x])))


def test_hermite_normal():
    m = DM([[2, 7, 17, 29, 41], [3, 11, 19, 31, 43], [5, 13, 23, 37, 47]], ZZ)
    hnf = DM([[1, 0, 0], [0, 2, 1], [0, 0, 1]], ZZ)
    assert hermite_normal_form(m) == hnf
    assert hermite_normal_form(m, D=ZZ(2)) == hnf
    assert hermite_normal_form(m, D=ZZ(2), check_rank=True) == hnf

    m = m.transpose()
    hnf = DM([[37, 0, 19], [222, -6, 113], [48, 0, 25], [0, 2, 1], [0, 0, 1]], ZZ)
    assert hermite_normal_form(m) == hnf
    raises(DMShapeError, lambda: _hermite_normal_form_modulo_D(m, ZZ(96)))
    raises(DMDomainError, lambda: _hermite_normal_form_modulo_D(m, QQ(96)))

    m = DM([[8, 28, 68, 116, 164], [3, 11, 19, 31, 43], [5, 13, 23, 37, 47]], ZZ)
    hnf = DM([[4, 0, 0], [0, 2, 1], [0, 0, 1]], ZZ)
    assert hermite_normal_form(m) == hnf
    assert hermite_normal_form(m, D=ZZ(8)) == hnf
    assert hermite_normal_form(m, D=ZZ(8), check_rank=True) == hnf

    m = DM([[10, 8, 6, 30, 2], [45, 36, 27, 18, 9], [5, 4, 3, 2, 1]], ZZ)
    hnf = DM([[26, 2], [0, 9], [0, 1]], ZZ)
    assert hermite_normal_form(m) == hnf

    m = DM([[2, 7], [0, 0], [0, 0]], ZZ)
    hnf = DM([[], [], []], ZZ)
    assert hermite_normal_form(m) == hnf
    assert _hermite_normal_form(m) == hnf

    m = DM([[-2, 1], [0, 1]], ZZ)
    hnf = DM([[2, 1], [0, 1]], ZZ)
    assert hermite_normal_form(m) == hnf

    m = DomainMatrix([[QQ(1)]], (1, 1), QQ)
    raises(DMDomainError, lambda: hermite_normal_form(m))
    raises(DMDomainError, lambda: _hermite_normal_form(m))
    raises(DMDomainError, lambda: _hermite_normal_form_modulo_D(m, ZZ(1)))


def test__hermite_normal_form_rectangular_scan_rows():
    data = _column_data_from_row_style([[5, 8, 12], [0, 0, 1]])
    m = DM(data, ZZ)
    h = hermite_normal_form(m)
    expected = DM([[1, 0], [0, 8], [0, 5]], ZZ)
    assert h.shape == (3, 2)
    assert h == expected
    ht = h.to_Matrix().T
    row_h = Matrix([list(reversed(row)) for row in reversed(ht.tolist())])
    assert row_h == Matrix([[5, 8, 0], [0, 0, 1]])
    assert _hermite_normal_form(m) == expected


def test__hermite_normal_form_unit_positions():
    cases = [
        ([[5, 8, 12], [0, 1, 0]], DM([[0, 12], [1, 0], [0, 5]], ZZ), Matrix([[5, 0, 12], [0, 1, 0]])),
        ([[5, 8, 12], [1, 0, 0]], DM([[12, 0], [8, 0], [0, 1]], ZZ), Matrix([[1, 0, 0], [0, 8, 12]])),
    ]
    for rows, expected_dm, expected_row in cases:
        m = DM(_column_data_from_row_style(rows), ZZ)
        h = hermite_normal_form(m)
        assert h == expected_dm
        assert _hermite_normal_form(m) == expected_dm
        ht = h.to_Matrix().T
        row_h = Matrix([list(reversed(row)) for row in reversed(ht.tolist())])
        assert row_h == expected_row


def test__hermite_normal_form_top_pivots():
    m = DM([[0, 5], [1, 0], [0, 0], [0, 0]], ZZ)
    expected = DM([[5, 0], [0, 1], [0, 0], [0, 0]], ZZ)
    h = hermite_normal_form(m)
    assert h.shape == (4, 2)
    assert h == expected
    assert _hermite_normal_form(m) == expected
