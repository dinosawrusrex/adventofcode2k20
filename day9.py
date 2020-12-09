def first_number_without_summable_pair(xmas, head=None, preamble=25):
    head = preamble if head is None else head
    chunk = xmas[head - preamble: head]

    if any(xmas[head]-i in chunk for i in chunk):
        return first_number_without_summable_pair(xmas, head+1, preamble)

    return xmas[head]


def encryption_weakness(xmas, invalid):
    start, end = 0, 2

    # Cannot recurse.. Keep hitting max recursion
    while (total := sum((chunk := xmas[start:end]))) != invalid:
        if total < invalid:
            end += 1
        else:
            start += 1

    return min(chunk) + max(chunk)


if __name__ == '__main__':
    test = [
        35,20,15,25,47,40,62,55,
        65,95,102,117,150,182,127,
        219,299,277,309,576
    ]

    assert first_number_without_summable_pair(test, preamble=5) == 127
    assert encryption_weakness(test, 127) == 62

    with open('inputs/day9.txt') as f:
        xmas = [int(l.strip()) for l in f.readlines() if l]

    invalid = first_number_without_summable_pair(xmas)
    assert invalid == 542529149
    assert encryption_weakness(xmas, invalid) == 75678618
