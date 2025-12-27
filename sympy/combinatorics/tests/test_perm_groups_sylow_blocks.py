from sympy.combinatorics.named_groups import DihedralGroup, SymmetricGroup


def _normalize_block_systems(blocks):
    normalized = []
    for block in blocks:
        # block is a sequence describing block membership per point
        normalized.append(tuple(block))
    return set(normalized)


def test_sylow_2_dihedral_even_orders():
    assert DihedralGroup(18).sylow_subgroup(2).order() == 4
    assert DihedralGroup(50).sylow_subgroup(2).order() == 4


def test_minimal_blocks_dihedral6():
    blocks = DihedralGroup(6).minimal_blocks(randomized=False)
    assert len(blocks) == 2
    normalized = _normalize_block_systems(blocks)
    expected = {
        (0, 1, 0, 1, 0, 1),
        (0, 1, 2, 0, 1, 2),
    }
    assert normalized == expected


def test_sylow_fallback_no_blocks():
    assert SymmetricGroup(5).sylow_subgroup(3).order() == 3
