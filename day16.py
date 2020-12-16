import itertools
import math


def parse_notes(notes):
    rules = {}
    ticket = None
    nearby = []

    for l in notes:
        if '-' in l and 'or' in l:
            field, values = l.split(': ')
            a, b = values.split(' or ')
            rules[field] = tuple(
                tuple(int(v) for v in min_max.split('-'))
                for min_max in values.split(' or ')
            )

        elif l not in ['your ticket:', 'nearby tickets:']:
            if ticket is None:
                ticket = tuple(int(v) for v in l.split(','))
            else:
                nearby.append(tuple(int(v) for v in l.split(',')))

    return rules, ticket, nearby


def get_matching_rule(ticket, rules):
    possible = []
    for value in ticket:
        fields = set()
        for field, rule in rules.items():
            if any(_min <= value <= _max for _min, _max in rule):
                fields.add(field)
        possible.append(fields)
    return possible


def sum_invalid_values_and_possible_fields(rules, nearby):
    values = []
    fields = []

    for ticket in nearby:
        invalid = False
        for value in ticket:
            if not any(
                _min <= value <= _max
                for _min, _max in itertools.chain.from_iterable(rules.values())
            ):
                values.append(value)
                break
        else:
            possible_fields = get_matching_rule(ticket, rules)
            if not fields:
                fields = possible_fields
            else:
                for i in range(len(fields)):
                    if fields[i] != possible_fields[i]:
                        fields[i] &= possible_fields[i]

    while not all(len(f) == 1 for f in fields):
        for f in fields:
            if len(f) == 1:
                for f_2 in fields:
                    if f_2 != f:
                        f_2 -= f

    fields = [list(f)[0] for f in fields]
    return sum(values), fields


if __name__ == '__main__':
    test = [
        'class: 1-3 or 5-7',
        'row: 6-11 or 33-44',
        'seat: 13-40 or 45-50',
        'your ticket:',
        '7,1,14',
        'nearby tickets:',
        '7,3,47',
        '40,4,50',
        '55,2,20',
        '38,6,12'
    ]
    rules, ticket, nearby = parse_notes(test)
    total, valid = sum_invalid_values_and_possible_fields(rules, nearby)
    assert total == 71

    test = [
        'class: 0-1 or 4-19',
        'row: 0-5 or 8-19',
        'seat: 0-13 or 16-19',
        'your ticket:',
        '11,12,13',
        'nearby tickets:',
        '3,9,18',
        '15,1,5',
        '5,14,9'
    ]

    rules, ticket, nearby = parse_notes(test)
    total, fields = sum_invalid_values_and_possible_fields(rules, nearby)
    assert fields == ['row', 'class', 'seat']

    with open('inputs/day16.txt') as f:
        notes = [l.strip() for l in f.readlines() if l.strip()]

    rules, ticket, nearby = parse_notes(notes)
    total, fields = sum_invalid_values_and_possible_fields(rules, nearby)
    assert total == 29851
    assert math.prod(ticket[i] for i, f in enumerate(fields) if f.startswith('departure')) == 3029180675981
