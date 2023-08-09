"""
Write function which receives list of text lines (which is space separated words) and word number.
It should enumerate unique words from each line and then build string from all words of given number.
Restriction: word_number >= 0
Examples:
    >>> build_from_unique_words('a b c', '1 1 1 2 3', 'cat dog milk', word_number=1)
    'b 2 dog'
    >>> build_from_unique_words('a b c', '', 'cat dog milk', word_number=0)
    'a cat'
    >>> build_from_unique_words('1 2', '1 2 3', word_number=10)
    ''
    >>> build_from_unique_words(word_number=10)
    ''
"""
from typing import Iterable


def build_from_unique_words(*lines: Iterable[str], word_number: int) -> str:
    unique_words = ''
    last_word = ''
    if len(lines) > 0 and word_number <= len(lines):
        last_word = lines[-1].split(' ')[word_number]

        for line in lines[:-1]:
            if len(line) > 0 and word_number <= len(line):
                sorted_line = sorted(set(line.replace(" ", "")), key=line.index)
                unique_words += f'{sorted_line[word_number]} '
    return f'{unique_words}{last_word}'