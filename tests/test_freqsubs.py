import pytest
from collections import Counter
from functools import reduce
from operator import add
from freqsubs import find_substrings, find_frequent_substrings
from utils import find_substrings_slow, find_frequent_substrings_slow

doppler_text = "Doppler spectroscopy (also known as the radial-velocity method, or colloquially, the wobble method) is an indirect method for finding extrasolar planets and brown dwarfs from radial-velocity measurements via observation of Doppler shifts in the spectrum of the planet's parent star."

tabby_text = "Tabby's Star\nTabby's Star (also known as Boyajian's Star and WTF Star, and designated KIC 8462852 in the Kepler Input Catalog) is an F-type main-sequence star in the constellation Cygnus approximately 1,470 light-years (450 pc) from Earth. Unusual light fluctuations of the star, including up to a 22% dimming in brightness, were discovered by citizen scientists as part of the Planet Hunters project."


def test_empty():
    assert list(find_substrings('')) == []


def test_empty_list():
    assert list(find_substrings([])) == []


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


def test_substrings_multi_input():
    inputs = [
        'banana',
        'national',
        'barbarian',
    ]

    merged = reduce(add, (Counter(dict(find_substrings(x))) for x in inputs))
    assert dict(find_substrings(inputs)) == merged


def test_frequent_empty():
    assert list(find_frequent_substrings('', 1)) == []


def test_frequent_empty_list():
    assert list(find_frequent_substrings([], 1)) == []


def test_frequent_one():
    assert list(find_frequent_substrings('A', 1)) == [('A', 1)]
    assert list(find_frequent_substrings('A', 2)) == []
    assert list(find_frequent_substrings('A', 3)) == []


def test_frequent_banana():
    banana_1 = [
        ('banana', 1),
    ]
    banana_2 = [
        ('ana', 2),
    ]
    banana_3 = [
        ('a', 3)
    ]

    assert sorted(find_frequent_substrings('banana', 1)) == banana_1
    assert sorted(find_frequent_substrings('banana', 2)) == banana_2
    assert sorted(find_frequent_substrings('banana', 3)) == banana_3
    assert sorted(find_frequent_substrings('banana', 4)) == []


def test_frequent_bananaey():
    text = 'banana banana banane banany'
    assert sorted(find_frequent_substrings(text, 1)) == [(text, 1)]
    assert sorted(find_frequent_substrings(text, 2)) == [('banana banan', 2)]
    assert sorted(find_frequent_substrings(text, 3)) == [(' banan', 3)]
    assert sorted(find_frequent_substrings(text, 4)) == [('banan', 4)]
    assert sorted(find_frequent_substrings(text, 5)) == [('ana', 6)]
    assert sorted(find_frequent_substrings(text, 6)) == [('ana', 6)]
    assert sorted(find_frequent_substrings(text, 7)) == [('an', 8)]
    assert sorted(find_frequent_substrings(text, 8)) == [('an', 8)]
    assert sorted(find_frequent_substrings(text, 9)) == [('a', 10)]
    assert sorted(find_frequent_substrings(text, 10)) == [('a', 10)]
    assert sorted(find_frequent_substrings(text, 11)) == []


def test_frequent_nanny_ogg():
    assert sorted(find_frequent_substrings('bananana', 2)) == [('anana', 2)]


def test_frequent_bananatural():
    text = 'bananabananaturalnatural-natural:natural'
    expected = [
        ('banana', 2),
        ('natural', 4)
    ]
    assert sorted(find_frequent_substrings(text, 2)) == expected


@pytest.mark.parametrize("min_support,min_length",
                         [(1, 1), (2, 1), (4, 1), (39, 1), (40, 1),
                          (2, 19), (2, 20), (3, 6), (3, 8)])
def test_frequent_doppler(min_support, min_length):
    assert sorted(find_frequent_substrings(doppler_text, min_support, min_length)) == \
        sorted(find_frequent_substrings_slow(doppler_text, min_support, min_length))


def test_frequent_multi_input():
    counts = dict(find_frequent_substrings([doppler_text, tabby_text],
                                           min_support=2, min_length=6))
    assert counts[' (also known as '] == 2
    assert counts[' of the '] ==  3
