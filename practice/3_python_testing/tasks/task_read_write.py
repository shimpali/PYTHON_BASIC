"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

import os


def task_read_write(files_path: str):
    result = []
    for root, dirs, files in os.walk(files_path):
        for name in files:
            with open(os.path.join(root, name)) as opened_file:
                for line in opened_file:
                    result.append(line)

    return result


if __name__ == '__main__':
    path = 'files'
    data = task_read_write(path)

    with open('result.txt', 'w') as result_file:
        result_file.write(f'content: \"{", ".join(data)}\"')
