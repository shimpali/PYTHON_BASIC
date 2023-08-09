"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
import tempfile
from pathlib import Path
from tasks.task_read_write import task_read_write


def test_read_write():
    path = '../2_python_part_2/files'
    result = task_read_write(path)
    with tempfile.TemporaryDirectory() as tmp_dirname:
        temp_dir = Path(tmp_dirname)
        file_name = temp_dir / "test_result.txt"
        file_name.write_text(f'content: \"{", ".join(result)}\"')

        assert temp_dir.exists() == True
        assert file_name.open().read() == 'content: "59, 99, 14, 1, 95, 99, 80, 66, 37, 15, 91, 74, 67, 39, 90, 40, ' \
                                          '32, 69, 48, 82"'
