from suffix_trees import STree


def substring_frequencies(text):
    """Returns all substrings of text and their frequencies.

    Returns an unsorted iterable of (substring, frequency) tuples. The
    frequencies include all overlapping occurrences of a substring.
    
    The runtime is linear O(n) in the input text length n.
    """
    if text == '':
        return []

    tree = STree.STree(text)
    for (prefix, suffix, freq) in _frequent_substrings_recursive(tree, tree.root, '', 0)[1]:
        for s in prefixes(suffix):
            yield (prefix + s, freq)


def _frequent_substrings_recursive(tree, node, text, level):
    edge_label = tree._edgeLabel(node, node.parent)
    
    if node.is_leaf():
        assert edge_label and _is_terminator(edge_label[-1])

        if len(edge_label) == 1:
            return (1, [])
        else:
            return (1, [(text, edge_label[:-1], 1)])
    else:
        child_freqs = []
        freq = 0
        for n in node.transition_links.values():
            f, child_texts = _frequent_substrings_recursive(tree, n, text + edge_label, level + 1)
            freq += f
            child_freqs.extend(child_texts)

        if text or edge_label:
            return (freq, [(text, edge_label, freq)] + child_freqs)
        else:
            return (freq, child_freqs)


def _is_terminator(c):
    i = ord(c)
    return (i in range(0xE000, 0xF8FF+1) or
            i in range(0xF0000, 0xFFFFD+1) or
            i in range(0x100000, 0x10FFFD+1))


def substring_frequencies_slow(text):
    """Get all substrings of text and their frequencies.

    Like substring_frequencies(), but the runtime is asymptotically
    slower O(n^2).
    """
    substrings = set(text[i:j]
                     for i in range(len(text))
                     for j in range(i+1, len(text)+1))
    return ((s, count_overlapping(text, s)) for s in substrings)


def prefixes(s):
    for i in range(1, len(s) + 1):
        yield s[:i]


def count_overlapping(text, sub):
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
