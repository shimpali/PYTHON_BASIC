import random
import re
import time
from uuid import uuid4


def get_choices(value: str) -> str:
    choices = value.strip('[]').split(',')
    for index, choice in enumerate(choices):
        choices[index] = choice.replace('\'', '').replace('\"', '').strip()
    return random.choice(choices)


def get_rand_in_range(value: str):
    lst = re.findall(r'\d+', value)
    a, b = int(lst[0]), int(lst[1])
    return random.randint(a, b)


def gen_timestamp() -> float:
    return time.time()


def gen_int(value: str) -> None | int | list[str] | str:
    if value == '':
        return None
    elif value == 'rand':
        return random.randint(0, 100000)
    elif value.startswith('[') and value.endswith(']'):
        return int(get_choices(value))
    elif re.search(r'^rand\(\d+, \d+\)$', value):
        return get_rand_in_range(value)
    else:
        try:
            value = int(value)
        except ValueError:
            return f'Wrong type of data, {value} cannot be converted to int'
    return value


def gen_str(value: str) -> str | list[str]:
    if value == '':
        return ''
    elif value == 'rand':
        return str(uuid4())
    elif value.startswith('[') and value.endswith(']'):
        return get_choices(value)
    elif re.search(r'^rand\(\d+, \d+\)$', value):
        return 'Wrong type of data'
    else:
        return value
