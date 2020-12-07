import re


def parse_individual_rule(rules):
    if 'no other bags' in rules:
        return {}

    rules = rules.replace('.', '').replace(' bags', '').replace(' bag', '')

    if ',' in rules:
        rules = rules.split(', ')
        return {r[2:]: int(r[0]) for r in rules}

    return {rules[2:]: int(rules[0])}

def parse_rules(raw_rules):
    bag_rules = {}

    for rules in raw_rules:
        bag, rule = rules.split(' contain ')
        bag_rules[bag.replace(' bags', '').replace(' bag', '')] = parse_individual_rule(rule)

    return bag_rules


def bags_that_hold(rules, target='shiny gold'):
    # Breadth-first search?
    # Start with one layer - find bags that hold target.
    # Then for each of these bags, find bags that hold them.
    bags = {bag for bag, rule in rules.items() if target in rule}
    bags.update(*(bags_that_hold(rules, bag) for bag in bags))
    return bags


def number_of_bags_needed(rules, current='shiny gold'):
    total = 0
    total += sum(rules[current].values())
    for bag, number in rules[current].items():
        total += number_of_bags_needed(rules, bag) * number
    return total


if __name__ == "__main__":
    test = [
        'light red bags contain 1 bright white bag, 2 muted yellow bags.',
        'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
        'bright white bags contain 1 shiny gold bag.',
        'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
        'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
        'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
        'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
        'faded blue bags contain no other bags.',
        'dotted black bags contain no other bags.'
    ]

    rules = parse_rules(test)
    assert len(bags_that_hold(rules)) == 4
    assert number_of_bags_needed(rules) == 32

    test = [
        'shiny gold bags contain 2 dark red bags.',
        'dark red bags contain 2 dark orange bags.',
        'dark orange bags contain 2 dark yellow bags.',
        'dark yellow bags contain 2 dark green bags.',
        'dark green bags contain 2 dark blue bags.',
        'dark blue bags contain 2 dark violet bags.',
        'dark violet bags contain no other bags.'
    ]
    rules = parse_rules(test)
    assert number_of_bags_needed(rules) == 126

    with open('inputs/day7.txt') as f:
        rules = parse_rules((l.strip() for l in f.readlines() if l))
    assert len(bags_that_hold(rules)) == 296
    assert number_of_bags_needed(rules) == 9339
