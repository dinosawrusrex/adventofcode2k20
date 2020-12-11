def distribution_of_differences(adapters, start=0, distribution=None):
    distribution = {1: 0, 2: 0, 3: 1} if distribution is None else distribution

    for i in range(1, 4):
        if (next_joltage := start+i) in adapters:
            distribution[i] += 1
            return distribution_of_differences(adapters, next_joltage, distribution)

    return distribution

def number_of_paths(adapters, start=None, count=0):

    start = max(adapters) + 3 if start is None else start

    for i in range(1, 4):
        next_joltage = start - i
        if next_joltage == 0:
            return count + 1
        elif next_joltage > 0 and next_joltage in adapters:
            count = number_of_paths(adapters, next_joltage, count)

    return count


if __name__ == '__main__':
    adapters = [1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19]
    distribution = distribution_of_differences(adapters)
    assert distribution[1] == 7
    assert distribution[3] == 5
    assert distribution[1] * distribution[3] == 35
    assert number_of_paths(adapters) == 8

    adapters = [
        28,33,18,42,31,14,46,20,48,47,24,23,49,45,
        19,38,39,11,1,32,25,35,8,17,7,9,4,2,34,10,3
    ]
    distribution = distribution_of_differences(adapters)
    assert distribution[1] == 22
    assert distribution[3] == 10
    assert distribution[1] * distribution[3] == 220
    assert number_of_paths(adapters) == 19208

    with open('inputs/day10.txt') as f:
        adapters = [int(l.strip()) for l in f.readlines() if l]

    distribution = distribution_of_differences(adapters)
    assert distribution[1] * distribution[3] == 2516
    # print(number_of_paths(adapters))
