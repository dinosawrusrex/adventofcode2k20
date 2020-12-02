from collections import namedtuple
import re

ENTRY = namedtuple('ENTRY', 'min, max, character, password')
RULE = re.compile('(\d+)-(\d+) ([a-z]): ([a-z]+)')

def parse_passwords(database: list) -> list:
    return (
        ENTRY(
            int(RULE.match(entry).group(1)),
            int(RULE.match(entry).group(2)),
            RULE.match(entry).group(3),
            RULE.match(entry).group(4)
        ) for entry in database
    )

def count_valid_rule_one(database: list) -> int:
    count = 0
    for entry in parse_passwords(database):
        if entry.min <= entry.password.count(entry.character) <= entry.max:
            count += 1
    return count

def count_valid_rule_two(database: list) -> int:
    count = 0
    for entry in parse_passwords(database):
        # Exclusive or: bool(a) != bool(b)
        if (
            (entry.password[entry.min-1] == entry.character) !=
            (entry.password[entry.max-1] == entry.character)
        ):
            count += 1

    return count


if __name__ == '__main__':

    test = [
        '1-3 a: abcde',
        '1-3 b: cdefg',
        '2-9 c: ccccccccc'
    ]

    assert count_valid_rule_one(test) == 2
    assert count_valid_rule_two(test) == 1

    with open('inputs/day2.txt') as f:
        database = [l.strip() for l in f.readlines() if l]

    assert count_valid_rule_one(database) == 456
    assert count_valid_rule_two(database) == 308
