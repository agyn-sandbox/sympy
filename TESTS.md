TESTS: Local Execution Guide

Prerequisites:
- Python >= 3.11
- pip
- Dependencies: pytest, pytest-xdist, pytest-timeout, pytest-split, pytest-doctestplus, hypothesis

Setup:
- Install package in editable mode:

```
pip install -e .
```

- Install development requirements:

```
pip install -r requirements-dev.txt
```

Run tests:
- Unit tests (use all CPU cores):

```
pytest -n auto
```

- Doctests:

```
bin/doctest --force-colors
```

Troubleshooting:
- Skip slow tests locally if needed:

```
pytest -m "not slow"
```

- Ensure hypothesis is installed to avoid skipped property-based tests.
