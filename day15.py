def get_2020th_number(starting, iteration=2020):
    numbers_and_turn = {n: [i+1] for i, n in enumerate(starting)}
    last = starting[-1]

    for i in range(len(starting)+1, iteration+1):
        indices = numbers_and_turn[last]
        last = 0 if len(indices) == 1 else indices[-1] - indices[-2]
        new = numbers_and_turn.setdefault(last, [])
        new.append(i)

    return last


if __name__ == '__main__':
    fucking_iteration = 30000000
    test = [0, 3, 6]
    assert get_2020th_number(test) == 436

    test = [1,3,2]
    assert get_2020th_number(test) == 1
    test = [2,1,3]
    assert get_2020th_number(test) == 10
    test = [1,2,3]
    assert get_2020th_number(test) == 27
    test = [2,3,1]
    assert get_2020th_number(test) == 78
    test = [3,2,1]
    assert get_2020th_number(test) == 438
    test = [3,1,2]
    assert get_2020th_number(test) == 1836

    current_input = [1,20,11,6,12,0]
    assert get_2020th_number(current_input) == 1085
    assert get_2020th_number(current_input, iteration=fucking_iteration) == 10652
