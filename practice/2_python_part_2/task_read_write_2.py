"""
Use function 'generate_words' to generate random words.
Write them to a new file encoded in UTF-8. Separator - '\n'.
Write second file encoded in CP1252, reverse words order. Separator - ','.

Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""


def generate_words(n=20):
    import string
    import random

    words = list()
    for _ in range(n):
        word = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
        words.append(word)

    return words


def write_to_file(filename, words, encoding, spacer, needs_reverse):
    with open(filename, 'w', encoding=encoding) as file_to_write:
        file_to_write.write(f'content: \"{spacer.join(reversed(words) if needs_reverse else words)}\"')


if __name__ == '__main__':
    random_words = generate_words(3)
    write_to_file('file_utf.txt', random_words, 'utf-8', '\n', False)
    write_to_file('file_cp.txt', random_words, 'cp1252', ',', True)

