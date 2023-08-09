"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import tempfile
from pathlib import Path
from tasks.task_read_write_2 import generate_words, write_to_file


def test_write_to_file():
    with tempfile.TemporaryDirectory() as tmp_dirname:
        temp_dir = Path(tmp_dirname)
        file1_name = temp_dir / "test_result_cp.txt"
        file2_name = temp_dir / "test_result_utf.txt"

        words = generate_words(3)
        new_line = '\n'
        write_to_file(file1_name, words, 'utf-8', new_line, False)
        write_to_file(file2_name, words, 'cp1252', ',', True)

        assert temp_dir.exists() == True
        assert file1_name.open().read() == f'content: "{new_line.join(words)}"'
        assert file2_name.open().read() == f'content: "{",".join(reversed(words))}"'