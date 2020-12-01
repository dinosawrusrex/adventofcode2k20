def multiply_pairwise_sum_to_2020(numbers, total=2020):

    for number in numbers:
        balance = total - number
        if balance in numbers:
            return number * balance

def multiply_triples_to_2020(numbers):

    for i, number in enumerate(numbers):
        balance = 2020 - number

        multiple = multiply_pairwise_sum_to_2020(numbers[i+1:], total=balance)

        if isinstance(multiple, int):
            return multiple * number


if __name__ == '__main__':

    test = [1721, 979, 366, 299, 675, 1456]
    assert multiply_pairwise_sum_to_2020(test) == 514579
    assert multiply_triples_to_2020(test) == 241861950

    with open('inputs/day1.txt') as f:
        numbers = [int(n) for n in f.read().split('\n') if n]

    print(multiply_pairwise_sum_to_2020(numbers))
    print(multiply_triples_to_2020(numbers))

