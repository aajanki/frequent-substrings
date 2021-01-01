from .suffix_tree import SuffixTree  # type: ignore
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
    if inputs == '' or inputs == []:
        return []

    if isinstance(inputs, str):
        inputs = [inputs]

    tree = SuffixTree(inputs)
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
    if inputs == '' or inputs == []:
        return []

    if isinstance(inputs, str):
        inputs = [inputs]

    tree = SuffixTree(inputs)
    for (prefix, suffix, freq) in _find_substrings(tree):
        for s in prefixes(suffix):
            yield (prefix + s, freq)


def _find_substrings(
        tree: SuffixTree,
        min_support: int = 1,
        only_dominating_substrings: bool = False
) -> Iterable[Tuple[str, str, int]]:
    root = tree._root
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
        edge_label = _edge_label(tree, node)

        if prestep:
            # pre-step: push the post-step and children to the stack
            #
            # The root node is skipped as a minor optimization.
            if node is not root:
                stack.append((node, level, False))

            if node.children:
                stack.extend(
                    (child, level + 1, True) for child in node.children.values()
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
            elif not node.children:
                freq = 1

            freq_acc[-1] += freq

            text = ''.join(path_labels)
            if freq >= min_support and not dominated and edge_label:
                child_has_yielded = [True for _ in child_has_yielded]
                yield (text, edge_label, freq)

            prev_level = level


def prefixes(s: str) -> Iterable[str]:
    for i in range(1, len(s) + 1):
        yield s[:i]


def _edge_label(tree: SuffixTree, node) -> str:
    if node is tree._root:
        return ''

    label = tree._strings[node.string_id][node.start:node.end + 1]
    if label[-1] == tree._terminal_character:
        label = label[:-1]

    return label
