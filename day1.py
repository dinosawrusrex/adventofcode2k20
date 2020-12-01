import itertools
import math


def multiply_combination_if_sum_to_2020(numbers, number_in_combination):

    for combo in itertools.combinations(numbers, number_in_combination):
        if sum(combo) == 2020:
            return math.prod(combo)


if __name__ == '__main__':

    test = (1721, 979, 366, 299, 675, 1456)
    assert multiply_combination_if_sum_to_2020(test, 2) == 514579
    assert multiply_combination_if_sum_to_2020(test, 3) == 241861950

    with open('inputs/day1.txt') as f:
        numbers = tuple(int(n) for n in f.read().split('\n') if n)

    assert multiply_combination_if_sum_to_2020(numbers, 2) == 1006875
    assert multiply_combination_if_sum_to_2020(numbers, 3) == 165026160

