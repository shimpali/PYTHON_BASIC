"""
Create 3 classes with interconnection between them (Student, Teacher,
Homework)
Use datetime module for working with date/time
1. Homework takes 2 attributes for __init__: tasks text and number of days to complete
Attributes:
    text - task text
    deadline - datetime.timedelta object with date until task should be completed
    created - datetime.datetime object when the task was created
Methods:
    is_active - check if task already closed
2. Student
Attributes:
    last_name
    first_name
Methods:
    do_homework - request Homework object and returns it,
    if Homework is expired, prints 'You are late' and returns None
3. Teacher
Attributes:
     last_name
     first_name
Methods:
    create_homework - request task text and number of days to complete, returns Homework object
    Note that this method doesn't need object itself
PEP8 comply strictly.
"""
import datetime
from datetime import date


class Teacher:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def create_homework(text, no_of_days):
        return Homework(text, no_of_days)


class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def do_homework(homework):
        return homework.is_active()


class Homework:

    def __init__(self, text, no_of_days):
        if no_of_days >= 0:
            self.text = text
            self.created = datetime.datetime.now()
            self.deadline = datetime.timedelta(days=no_of_days)
        else:
            raise ValueError('Number of days should be positive')

    def is_active(self):
        active = self.created - self.deadline
        if active.date() < date.today():
            return self.text
        else:
            return 'You are late'


if __name__ == '__main__':
    teacher = Teacher('Dmitry', 'Orlyakov')
    student = Student('Vladislav', 'Popov')
    print(teacher.last_name)
    print(student.first_name)

    expired_homework = teacher.create_homework('Learn functions', 0)
    print(expired_homework.created)  # Example: 2019-05-26 16:44:30.688762
    print(expired_homework.deadline)  # 0:00:00
    print(expired_homework.text)  # 'Learn functions'

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too('Create 2 simple classes', 5)
    print(oop_homework.created)
    print(oop_homework.deadline)  # 5 days, 0:00:00
    print(oop_homework.text)

    student.do_homework(expired_homework) # You are late
    student.do_homework(oop_homework)  # Create 2 simple classes
    print(student)
