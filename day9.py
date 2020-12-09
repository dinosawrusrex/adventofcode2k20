def first_number_without_summable_pair(xmas, preamble=25):
    head = preamble
    while head < len(xmas):
        start = head - preamble
        print(start, head)
        for i in range(start, head):
            balance = xmas[head] - xmas[i]
            try:
                index = xmas.index(balance, start, head)
            except ValueError:
                pass
            else:
                head += 1
                break

        # This else clause will only be executed
        # if loop not terminated by break.
        else:
            return xmas[head]

def encryption_weakness(xmas, invalid):
    start, end = 0, 1

    while (total := sum(
        contiguous_set := [xmas[x] for x in range(start, end)]
    )) != invalid:
        if total < invalid:
            end += 1
        else:
            start += 1

    return min(contiguous_set) + max(contiguous_set)


if __name__ == '__main__':
    test = [
        35,20,15,25,47,40,62,55,
        65,95,102,117,150,182,127,
        219,299,277,309,576
    ]

    assert first_number_without_summable_pair(test, preamble=5) == 127
    # assert encryption_weakness(test, 127) == 62

    # with open('inputs/day9.txt') as f:
    #     xmas = [int(l.strip()) for l in f.readlines() if l]

    # invalid = first_number_without_summable_pair(xmas)
    # assert invalid == 542529149
    # assert encryption_weakness(xmas, invalid) == 75678618


