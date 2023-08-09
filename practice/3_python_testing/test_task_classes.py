"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""
import pytest
from tasks.task_classes import *


@pytest.fixture
def setup():
    teacher = Teacher('Dmitry', 'Orlyakov')
    student = Student('Vladislav', 'Popov')
    homework = Homework('Learn functions', 10)
    new_homework = teacher.create_homework('Learn functions', 10)
    assigned_homework = student.do_homework(new_homework)

    return dict(
        teacher=teacher,
        student=student,
        homework=homework,
        new_homework=new_homework,
        assigned_homework=assigned_homework
    )


def test_teacher_details(setup):
    assert setup.get('teacher').first_name == 'Dmitry'
    assert setup.get('teacher').last_name == 'Orlyakov'


def test_student_details(setup):
    assert setup.get('student').first_name == 'Vladislav'
    assert setup.get('student').last_name == 'Popov'


def test_create_homework(setup):
    assert setup.get('new_homework').text == setup.get('homework').text


def test_homework_details(setup):
    homework = setup.get('homework')
    assert homework.text == 'Learn functions'
    assert homework.deadline == datetime.timedelta(10)


def test_do_homework(setup):
    assert setup.get('assigned_homework') == setup.get('new_homework').text


def test_expired_homework(setup):
    expired_homework = setup.get('teacher').create_homework('Write unit tests', 0)
    assigned_homework = setup.get('student').do_homework(expired_homework)
    assert assigned_homework == 'You are late'


def test_negative_homework_deadline(setup):
    with pytest.raises(ValueError) as error:
        invalid_homework = setup.get('teacher').create_homework('Write integration tests', -2)
        setup.get('student').do_homework(invalid_homework)
        assert 'Number of days should be positive' in str(error.value)