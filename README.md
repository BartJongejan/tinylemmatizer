# tinylemmatizer
Simple lemmatizer for inclusion in Python programs that uses the same lemmatization rules as CSTlemma. 

This project consists of a Python3 wrapper around a small C-program that lemmatizes full forms using a rule set ('flexrules') that is in the same binary format as the rule sets used by cstlemma (https://github.com/kuhumcst/cstlemma).
Rule sets can be trained using the affixtrain program (https://github.com/kuhumcst/affixtrain). Alternatively, rule sets can be downloaded from https://github.com/kuhumcst/texton-linguistic-resources. Look for files in folders such as

    https://github.com/kuhumcst/texton-linguistic-resources/blob/master/da/lemmatiser/notags/c21/0/flexrules

or

    https://github.com/kuhumcst/texton-linguistic-resources/blob/master/en/lemmatiser/notags/2/flexrules

In these paths, the names of the subdirectories named '0' and '2' indicate the pruning level. '0' means unpruned.

## Installation

    python -m pip install cstlempy

Wheels are available for Linux, macOS and Windows and for Python 3.9 and later, including free-threaded Python.

## Usage

    import cstlempy

    lemmatizer = cstlempy.Lemmatizer("flexrules")  # path to a flexrules file
    lemmatizer.lemmatize("køer")                   # -> ['kø', 'ko']

`lemmatize()` returns a list, because a full form can have more than one lemma. `Lemmatizer()` raises `OSError` if the file cannot be read and `ValueError` if it is not a flexrules file. You can create several lemmatizers, e.g. one per language, and share them between threads.

The older functions `cstlempy.init(filename)`, `cstlempy.lemmatize(fullform)` and `cstlempy.final()` still work.

## Building from source

Prerequisites: Python 3.9 or later and a C compiler. In the project folder:

    python -m pip install .

To test, edit the file 'launch.py' and make sure that 'filename' is the path to a flexrule file. Then run `build-launch.sh` (Linux/macOS) or `build-launch.bat` (Windows); these need setuptools and Cython:

    python -m pip install setuptools Cython

To run the tests:

    python -m pip install pytest
    python -m pytest tests

## Releasing

Every push to master builds and tests the wheels with GitHub Actions (`.github/workflows/wheels.yml`). Publishing a GitHub release uploads the wheels and the source distribution to PyPI. Increase `version` in `pyproject.toml` before each release.

