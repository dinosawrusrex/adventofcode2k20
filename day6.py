def parse_groups(responses):
    groups = []

    group = []
    for i, yes in enumerate(responses):
        if yes == '':
            groups.append(group)
            group = []
        else:
            group.append({char for char in yes})

        if len(responses)-1 == i:
            groups.append(group)

    return groups

def any_yes(groups):
    return sum(len(set().union(*g)) for g in groups)

def all_yes(groups):
    return sum(len(g[0].intersection(*g)) for g in groups)


if __name__ == '__main__':
    test = [
        'abc',
        '',
        'a', 'b', 'c',
        '',
        'ab', 'ac',
        '',
        'a', 'a', 'a', 'a',
        '',
        'b'
    ]

    group_yes = parse_groups(test)
    assert any_yes(group_yes) == 11
    assert all_yes(group_yes) == 6

    with open('inputs/day6.txt') as f:
        responses = [l.strip() for l in f.readlines() if l]

    group_yes = parse_groups(responses)
    assert any_yes(group_yes) == 6443
    assert all_yes(group_yes) == 3232
