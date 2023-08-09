"""
Write function which receives list of integers. Calculate power of each integer and
subtract difference between original previous value and it's power. For first value subtract nothing.
Restriction:
Examples:
    >>> calculate_power_with_difference([1, 2, 3])
    [1, 4, 7]  # because [1^2, 2^2 - (1^2 - 1), 3^2 - (2^2 - 2)]
"""
from typing import List


def calculate_power_with_difference(ints: List[int]) -> List[int]:
    diff = []
    powers = []
    for index, value in enumerate(ints):
        power = pow(value, 2)
        powers.append(power)
        if len(powers) == len(ints):
            for index, pow_value in enumerate(powers):
                if index == 0:
                    diff = [pow_value]
                if index - 1 >= 0:
                    diff.append(pow_value - (powers[index - 1] - ints[index - 1]))

    return diff
