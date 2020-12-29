from suffix_trees import STree


def substring_frequencies(text):
    """Returns all substrings of text and their frequencies.

    Returns an unsorted iterable of (substring, frequency) tuples. The
    frequencies include all overlapping occurrences of a substring.
    
    The runtime is O(n^2) in the input text length n.
    """
    if text == '':
        return []

    tree = STree.STree(text)
    for (prefix, suffix, freq) in _find_substrings(tree):
        for s in prefixes(suffix):
            yield (prefix + s, freq)


def _find_substrings(tree):
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

        else:
            # post-step: all children have been processed and we have
            # the frequency. Yield current node's label and frequency.

            freq = 0
            if level < prev_level:
                freq = freq_acc.pop()
                path_labels.pop()
            elif node.is_leaf():
                freq = 1

                assert edge_label and _is_terminator(edge_label[-1])
                edge_label = edge_label[:-1]

            freq_acc[-1] += freq

            text = ''.join(path_labels)
            if text or edge_label:
                yield (text, edge_label, freq)

            prev_level = level


def _is_terminator(c):
    i = ord(c)
    return (i in range(0xE000, 0xF8FF+1) or
            i in range(0xF0000, 0xFFFFD+1) or
            i in range(0x100000, 0x10FFFD+1))


def substring_frequencies_slow(text):
    """Get all substrings of text and their frequencies.

    The output equals to substring_frequencies() but this is
    asymptotically slower and uses more memory.
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
