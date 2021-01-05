from typing import Iterable, Tuple


def find_frequent_substrings_slow(text: str, min_support: int, min_length: int = 1) -> Iterable[Tuple[str, int]]:
    """Find frequent substrings of text.

    Slower but an "obviously correct" version of
    find_frequent_substrings().
    """
    substrings = (
        x for x in find_substrings_slow(text)
        if len(x[0]) >= min_length and x[1] >= min_support)
    substrings_sorted = sorted(substrings)

    temp = []
    for candidate, next_candidate in zip(substrings_sorted[:-1], substrings_sorted[1:]):
        if not next_candidate[0].startswith(candidate[0]):
            temp.append(candidate)

    if substrings_sorted:
        temp.append(substrings_sorted[-1])

    frequent = []
    temp = sorted(temp, key=lambda x: reversed_string(x[0]))
    for candidate, next_candidate in zip(temp[:-1], temp[1:]):
        if not next_candidate[0].endswith(candidate[0]):
            frequent.append(candidate)

    if temp:
        frequent.append(temp[-1])

    return frequent


def reversed_string(s):
    return s[::-1]


def find_substrings_slow(text: str) -> Iterable[Tuple[str, int]]:
    """Get all substrings of text and their frequencies.

    Slower but an "obviously correct" version of find_substrings().
    """
    substrings = set(text[i:j]
                     for i in range(len(text))
                     for j in range(i+1, len(text)+1))
    return ((s, count_overlapping(text, s)) for s in substrings)


def count_overlapping(text: str, sub: str) -> int:
    """The number of overlapping occurrences of the substring sub in text."""
    count = 0
    start = 0
    i = 0
    while i >= 0:
        i = text.find(sub, start)
        if i >= 0:
            count += 1
            start = i+1

    return count
