from suffix_trees import STree  # type: ignore
from typing import Iterable, Tuple, Union


def find_frequent_substrings(
        inputs: Union[str, Iterable[str]],
        min_support: int,
        min_length: int = 1
) -> Iterable[Tuple[str, int]]:
    """Find frequent substrings of text.

    Returns an unsorted iterable of (substring, frequency) tuples. The
    output contains substrings that occur at least min_support times
    and are at least min_length characters long. The output includes
    only the longest possible substrings, that is no substring in the
    output is a prefix of another.

    The runtime and memory requirement are linear O(n), where n is the
    length of the input text.
    """
    if inputs == '':
        return []

    tree = STree.STree(inputs)
    for (prefix, suffix, freq) in _find_substrings(tree, min_support, only_dominating_substrings=True):
        text = prefix + suffix
        if len(text) >= min_length:
            yield (text, freq)


def find_substrings(inputs: Union[str, Iterable[str]]) -> Iterable[Tuple[str, int]]:
    """Find all substrings of text and their frequencies.

    The input can be either a string or an iterable of strings.

    Returns an unsorted iterable of (substring, frequency) tuples. The
    frequencies include all overlapping occurrences of a substring. If
    the input is an iterable of strings, the output contains
    substrings from any of the inputs and the frequencies are the
    combined occurrence counts.
    
    The runtime is O(n^2) in the input text length n.
    """
    if inputs == '':
        return []

    tree = STree.STree(inputs)
    for (prefix, suffix, freq) in _find_substrings(tree):
        for s in prefixes(suffix):
            yield (prefix + s, freq)


def _find_substrings(
        tree: STree.STree,
        min_support: int = 1,
        only_dominating_substrings: bool = False
) -> Iterable[Tuple[str, str, int]]:
    root = tree.root
    # Stack: (node, tree level, is pre step)
    stack = [(root, 0, True)]
    # Accumulator for frequencies: freq_acc[i] is the (partial) sum of
    # substring frequencies at tree depth i. It is the total frequency
    # at depth i at post-step phase when every descendant node has
    # been processed.
    freq_acc = []
    # path_label[i] is the label on the i:th edge along the path from
    # the root to the current node.
    path_labels = []
    # child_has_yielded[i] is True if we have already returned a
    # substring from any child node below tree depth i. Useful when
    # returnign only dominating substrings.
    child_has_yielded = []
    prev_level = -1

    while stack:
        node, level, prestep = stack.pop()
        edge_label = tree._edgeLabel(node, node.parent)

        if prestep:
            # pre-step: push the post-step and children to the stack
            #
            # The root node is skipped as a minor optimization.
            if node is not root:
                stack.append((node, level, False))

            if node.transition_links:
                stack.extend(
                    (child, level + 1, True) for child in node.transition_links.values()
                )
                freq_acc.append(0)
                path_labels.append(edge_label)
                child_has_yielded.append(False)

        else:
            # post-step: all children have been processed and we have
            # the frequency. Yield current node's label and frequency.
            freq = 0
            dominated = False
            if level < prev_level:
                freq = freq_acc.pop()
                path_labels.pop()
                dominated = child_has_yielded.pop() and only_dominating_substrings
            elif node.is_leaf():
                freq = 1

                # TODO: fix the tree builder so that the edge label
                # stops at the first terminator.
                i = _find_terminator(edge_label)
                edge_label = edge_label[:i]

            freq_acc[-1] += freq

            text = ''.join(path_labels)
            if freq >= min_support and not dominated and edge_label:
                child_has_yielded = [True for _ in child_has_yielded]
                yield (text, edge_label, freq)

            prev_level = level


def _is_terminator(c: str) -> bool:
    i = ord(c)
    return (i in range(0xE000, 0xF8FF+1) or
            i in range(0xF0000, 0xFFFFD+1) or
            i in range(0x100000, 0x10FFFD+1))


def _find_terminator(s: str) -> int:
    return next(i for i, c in enumerate(s) if _is_terminator(c))


def find_frequent_substrings_slow(text: str, min_support: int, min_length: int = 1) -> Iterable[Tuple[str, int]]:
    """Find frequent substrings of text.

    Like find_frequent_substrings() but asymptotically slower O(n^2).
    """
    substrings = (
        x for x in find_substrings_slow(text)
        if len(x[0]) >= min_length and x[1] >= min_support)
    substrings_sorted = sorted(substrings)

    frequent = []
    for candidate, next_candidate in zip(substrings_sorted[:-1], substrings_sorted[1:]):
        if not next_candidate[0].startswith(candidate[0]):
            frequent.append(candidate)

    if substrings_sorted:
        frequent.append(substrings_sorted[-1])

    return frequent


def find_substrings_slow(text: str) -> Iterable[Tuple[str, int]]:
    """Get all substrings of text and their frequencies.

    The output equals to find_substrings() but this is asymptotically
    slower and uses more memory.
    """
    substrings = set(text[i:j]
                     for i in range(len(text))
                     for j in range(i+1, len(text)+1))
    return ((s, count_overlapping(text, s)) for s in substrings)


def prefixes(s: str) -> Iterable[str]:
    for i in range(1, len(s) + 1):
        yield s[:i]


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
