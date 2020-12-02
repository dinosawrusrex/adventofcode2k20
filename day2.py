from collections import namedtuple
import re
import typing

ENTRY = namedtuple('ENTRY', 'min, max, character, password')
RULE = re.compile('(\d+)-(\d+) ([a-z]): ([a-z]+)')

def parse_database(database: typing.List[str]) -> typing.Generator:
    return (
        ENTRY(
            int(RULE.match(entry).group(1)),
            int(RULE.match(entry).group(2)),
            RULE.match(entry).group(3),
            RULE.match(entry).group(4)
        ) for entry in database
    )

def count_valid_rule_one(database: typing.List[str]) -> int:
    return len(list(filter(
        lambda e: e.min <= e.password.count(e.character) <= e.max,
        parse_database(database)
    )))

def count_valid_rule_two(database: typing.List[str]) -> int:
    return len(list(filter(
        lambda e: (
            (e.password[e.min-1] == e.character) !=
            (e.password[e.max-1] == e.character)
        ),
        parse_database(database)
    )))


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
