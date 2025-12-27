Title: Fix IndexError in minimal_blocks used by sylow_subgroup for even-order dihedral groups

Context
The fork branch sympy__sympy-19954 exhibits an IndexError when calling DihedralGroup(18).sylow_subgroup(p=2) and DihedralGroup(50).sylow_subgroup(p=2). The traceback points to combinatorics/perm_groups.py minimal_blocks() deleting from lists while iterating, leading to out-of-range indexing.

Observed Failure
- File: sympy/combinatorics/perm_groups.py
- Function: minimal_blocks(randomized=True)
- Approx lines: 2160–2240
- Error line: around 2201 (del num_blocks[i], blocks[i])

Repro steps (local):
- From this branch, import DihedralGroup and call sylow_subgroup(2) for n even (e.g., 18 and 50). The IndexError is raised consistently.

Root Cause
- minimal_blocks builds three parallel lists: blocks, num_blocks, rep_blocks (representative block sets).
- During a forward loop over rep_blocks (for i, r in enumerate(rep_blocks)), the code deletes entries at the same index i from num_blocks and blocks when it determines a previously discovered system is non-minimal:
  - del num_blocks[i], blocks[i]
  - It defers removing from rep_blocks by collecting to_remove and filtering rep_blocks after the loop.
- This in-loop deletion breaks positional alignment and list length invariants across the three lists. Multiple deletions shift indices and eventually make i refer to a valid position in rep_blocks but an out-of-range index in num_blocks/blocks, causing IndexError.
- The condition occurs notably for DihedralGroup of even order where multiple candidate block systems exist and subset relations cause more than one prior block system to be removed.

Implementation-ready Fix (spec)
1) In minimal_blocks(), replace the in-loop deletion of num_blocks and blocks with deferred removals applied uniformly across all three lists after completing the subset checks for the current candidate.
   - Instead of:
     - del num_blocks[i], blocks[i]
     - collecting to_remove = [rep_blocks[i], ...] and later doing rep_blocks = [r for r in rep_blocks if r not in to_remove]
   - Do:
     - Maintain a set of indices idx_to_remove for entries found non-minimal (i where len(r) > len(rep) and rep.issubset(r)).
     - After the inner loop terminates, rebuild all three lists by excluding those indices (or delete in descending index order):
       - blocks = [b for j, b in enumerate(blocks) if j not in idx_to_remove]
       - num_blocks = [nb for j, nb in enumerate(num_blocks) if j not in idx_to_remove]
       - rep_blocks = [rb for j, rb in enumerate(rep_blocks) if j not in idx_to_remove]
     - Alternatively and equivalently, perform: for j in sorted(idx_to_remove, reverse=True): del blocks[j]; del num_blocks[j]; del rep_blocks[j]
   - This ensures all three lists remain aligned and prevents index mismatches.

2) Keep the minimality check logic intact:
   - If len(r) < len(rep) and r.issubset(rep), mark the current system as non-minimal (minimal = False) and do not add it.
   - If len(r) > len(rep) and rep.issubset(r), mark r’s index for removal in idx_to_remove.

3) No changes to algorithmic semantics: minimal_blocks should still return a list of block numberings (e.g., [0,1,0,1,...]) for each minimal block system.

4) In sylow_subgroup(p), add a minor guard for empty block systems:
   - After blocks = self.minimal_blocks(), explicitly handle blocks being empty to skip the block_homomorphism reduction path. Current code naturally falls through, but an explicit check improves clarity:
     - If not blocks: proceed to element-of-order-p path (no functional change).

Test Plan (add under sympy/combinatorics/tests)
1) Test dihedral even order, 2-Sylow:
   - DihedralGroup(18).sylow_subgroup(2).order() == 4
   - DihedralGroup(2*25).sylow_subgroup(2).order() == 4

2) Ensure no IndexError when computing minimal blocks used by sylow_subgroup for these cases. The tests should call sylow_subgroup directly; the failure in current HEAD is an exception.

3) Additional edge cases:
   - DihedralGroup(6).minimal_blocks() returns two minimal block systems as documented (e.g., [[0,1,0,1,0,1], [0,1,2,0,1,2]]). This asserts that the refactor preserves existing behavior.
   - Primitive group path: for SymmetricGroup(5), minimal_blocks() may be empty; calling sylow_subgroup(3) should succeed (order == 3), exercising the explicit empty-blocks guard.

Suggested test file: sympy/combinatorics/tests/test_perm_groups_sylow_blocks.py
- Test: test_sylow_2_dihedral_even_orders() — asserts orders and no exceptions for n=18, 50.
- Test: test_minimal_blocks_dihedral6() — asserts expected block systems for D6.
- Test: test_sylow_fallback_no_blocks() — SymmetricGroup(5).sylow_subgroup(3) order == 3.

Local Verification (without CI)
Commands:
- Use Python 3.10 with venv to avoid distutils import error; install mpmath:
  - python3 -m venv .venv310
  - .venv310/bin/python -m pip install mpmath setuptools
- Run a quick script:
  - PYTHONPATH=$PWD/. .venv310/bin/python - <<'PY'
    import sys
    sys.path.insert(0, '/workspace/sympy')
    from sympy.combinatorics.named_groups import DihedralGroup
    from sympy.combinatorics.named_groups import SymmetricGroup
    print('D18 2-Sylow order:', DihedralGroup(18).sylow_subgroup(2).order())
    print('D50 2-Sylow order:', DihedralGroup(50).sylow_subgroup(2).order())
    print('D6 minimal_blocks:', DihedralGroup(6).minimal_blocks())
    print('S5 3-Sylow order:', SymmetricGroup(5).sylow_subgroup(3).order())
    PY
Expected output:
- D18 2-Sylow order: 4
- D50 2-Sylow order: 4
- D6 minimal_blocks: two block systems as documented
- S5 3-Sylow order: 3

Notes
- The fix modifies only list-handling in minimal_blocks, avoiding in-loop deletions, and adds a harmless guard in sylow_subgroup for empty blocks.
- No API changes; behavior is preserved except the elimination of the IndexError.

