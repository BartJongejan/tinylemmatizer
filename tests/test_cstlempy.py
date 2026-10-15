# Tests for the cstlempy module. Run with: python -m pytest tests

import pathlib
import threading

import pytest

import cstlempy

RULES = pathlib.Path(__file__).parent / "flexrules.en"


@pytest.fixture(scope="module")
def lemmatizer():
    return cstlempy.Lemmatizer(RULES)


def test_lemmatize(lemmatizer):
    assert lemmatizer.lemmatize("went") == ["go"]
    assert lemmatizer.lemmatize("mice") == ["mouse"]


def test_ambiguous(lemmatizer):
    assert lemmatizer.lemmatize("leaves") == ["leaf", "leave"]


def test_empty_word(lemmatizer):
    assert lemmatizer.lemmatize("") == []


def test_str_path():
    assert cstlempy.Lemmatizer(str(RULES)).lemmatize("went") == ["go"]


def test_word_must_be_str(lemmatizer):
    with pytest.raises(TypeError):
        lemmatizer.lemmatize(b"went")


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        cstlempy.Lemmatizer(tmp_path / "nonexistent")


@pytest.mark.parametrize("content", [b"", b"abc", b"This is not a rule file"])
def test_not_a_rules_file(tmp_path, content):
    path = tmp_path / "rules"
    path.write_bytes(content)
    with pytest.raises(ValueError):
        cstlempy.Lemmatizer(path)


def test_threads(lemmatizer):
    words = ["went", "mice", "leaves", "houses"] * 1000
    expected = [lemmatizer.lemmatize(w) for w in words]
    results = []

    def work():
        results.append([lemmatizer.lemmatize(w) for w in words] == expected)

    threads = [threading.Thread(target=work) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert results == [True] * 8


def test_legacy_api():
    with pytest.raises(RuntimeError):
        cstlempy.lemmatize("went")
    assert cstlempy.init(str(RULES)) == 0
    assert cstlempy.lemmatize("leaves") == "leaf leave "
    cstlempy.final()
    assert cstlempy.init("nonexistent") == 1
