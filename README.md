# Frequent substrings

A Python library for finding frequent substrings.

Example:

```python
from freqsubs import find_frequent_substrings

find_frequent_substrings('national banana', min_support=3, min_length=1)

# The output is
#
# [('na', 4)]
#
# It indicates that the substring 'na' occurs 4 times and that it is
# the only substring with three (the min_support parameter) or more
# occurrences (except for its own substrings 'n' and 'a').
```

The input can also be a list of strings.

## Testing

```
python -m pytest tests
```

## Acknowledgements

The suffix tree implementation is based on https://github.com/Reddy2/suffix-tree by [Reddy2](https://github.com/Reddy2). It is shared under the MIT license.

## License

MIT