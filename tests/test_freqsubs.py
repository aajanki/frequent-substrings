from src.freqsubs import substring_frequencies, substring_frequencies_slow


def test_empty():
    assert list(substring_frequencies('')) == []


def test_one():
    assert list(substring_frequencies('A')) == [('A', 1)]


def test_bbc():
    bbc_substrings = [
        ('B', 2),
        ('BB', 1),
        ('BBC', 1),
        ('BC', 1),
        ('C', 1)
    ]

    assert sorted(substring_frequencies('BBC')) == bbc_substrings


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

    assert sorted(substring_frequencies('banana')) == banana_substrings


def test_nefernefernefer():
    substrings = list(substring_frequencies('nefernefernefer'))

    assert ('e', 6) in substrings
    assert ('n', 3) in substrings
    assert ('efer', 3) in substrings
    assert ('ern', 2) in substrings


def test_longer_text():
    text = "Doppler spectroscopy (also known as the radial-velocity method, or colloquially, the wobble method) is an indirect method for finding extrasolar planets and brown dwarfs from radial-velocity measurements via observation of Doppler shifts in the spectrum of the planet's parent star."

    assert sorted(substring_frequencies(text)) == sorted(substring_frequencies_slow(text))
