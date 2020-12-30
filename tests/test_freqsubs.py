import pytest
from src.freqsubs import find_substrings, find_substrings_slow, \
    find_frequent_substrings, find_frequent_substrings_slow

doppler_text = "Doppler spectroscopy (also known as the radial-velocity method, or colloquially, the wobble method) is an indirect method for finding extrasolar planets and brown dwarfs from radial-velocity measurements via observation of Doppler shifts in the spectrum of the planet's parent star."


def test_empty():
    assert list(find_substrings('')) == []


def test_one():
    assert list(find_substrings('A')) == [('A', 1)]


def test_bbc():
    bbc_substrings = [
        ('B', 2),
        ('BB', 1),
        ('BBC', 1),
        ('BC', 1),
        ('C', 1)
    ]

    assert sorted(find_substrings('BBC')) == bbc_substrings


def test_banana():
    banana_substrings = [
        ('a', 3),
        ('an', 2),
        ('ana', 2),
        ('anan', 1),
        ('anana', 1),
        ('b', 1),
        ('ba', 1),
        ('ban', 1),
        ('bana', 1),
        ('banan', 1),
        ('banana', 1),
        ('n', 2),
        ('na', 2),
        ('nan', 1),
        ('nana', 1)
    ]

    assert sorted(find_substrings('banana')) == banana_substrings


def test_nefernefernefer():
    substrings = list(find_substrings('nefernefernefer'))

    assert ('e', 6) in substrings
    assert ('n', 3) in substrings
    assert ('efer', 3) in substrings
    assert ('ern', 2) in substrings


def test_substrings_doppler():
    assert sorted(find_substrings(doppler_text)) == sorted(find_substrings_slow(doppler_text))


def test_frequent_empty():
    assert list(find_frequent_substrings('', 1)) == []


def test_frequent_one():
    assert list(find_frequent_substrings('A', 1)) == [('A', 1)]
    assert list(find_frequent_substrings('A', 2)) == []
    assert list(find_frequent_substrings('A', 3)) == []


def test_frequent_banana():
    banana_1 = [
        ('anana', 1),
        ('banana', 1),
        ('nana', 1)
    ]
    banana_2 = [
        ('ana', 2),
        ('na', 2)
    ]
    banana_3 = [
        ('a', 3)
    ]

    assert sorted(find_frequent_substrings('banana', 1)) == banana_1
    assert sorted(find_frequent_substrings('banana', 2)) == banana_2
    assert sorted(find_frequent_substrings('banana', 3)) == banana_3
    assert sorted(find_frequent_substrings('banana', 4)) == []


@pytest.mark.parametrize("min_support,min_length",
                         [(1, 1), (2, 1), (4, 1), (39, 1), (40, 1),
                          (2, 19), (2, 20), (3, 6), (3, 8)])
def test_frequent_doppler(min_support, min_length):
    assert sorted(find_frequent_substrings(doppler_text, min_support, min_length)) == \
        sorted(find_frequent_substrings_slow(doppler_text, min_support, min_length))
