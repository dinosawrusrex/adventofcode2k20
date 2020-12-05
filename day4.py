import re


def process_passport(passport):
    passport_values = {}

    for field_value in passport.split(' '):
        field, value = field_value.split(':')
        passport_values[field] = value

    return passport_values

def parse_input(input_file):
    passports = []

    passport = ''
    for line in input_file.readlines():
        line = line.strip('\n')
        if line.strip() == '' and passport != '':
            passports.append(process_passport(passport))
            passport = ''

        if passport != '':
            passport += ' '

        passport += line

    return passports


COLOR = re.compile('^#[0-9a-f]{6}$')
VALIDATION = {
    'byr': lambda v: len(v) == 4 and 1920 <= int(v) <= 2002,
    'iyr': lambda v: len(v) == 4 and 2010 <= int(v) <= 2020,
    'eyr': lambda v: len(v) == 4 and 2020 <= int(v) <= 2030,
    'ecl': lambda v: v in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
    'hcl': lambda v: bool(COLOR.match(v)),
    'pid': lambda v: len(v) == 9 and v.isdigit(),
    'hgt': lambda v: validate_height(v)
}

HEIGHT = re.compile('^(\d+)(cm|in)$')
def validate_height(value):
    if (match := HEIGHT.match(value)):
        lower, higher = (150, 193) if match.group(2) == 'cm' else (59, 76)
        return lower <= int(match.group(1)) <= higher
    return False


def loose_criteria(passport):
    return any((
        len(passport) == 8,
        len(passport) == 7 and 'cid' not in passport
    ))

def strict_criteria(passport):
    for field, validate in VALIDATION.items():
        if validate(passport.get(field)) is False:
            return False
    return True

def count_valid(passports, strictly=False):
    count = 0
    for passport in passports:
        if loose_criteria(passport):
            if strictly:
                if strict_criteria(passport):
                    count += 1
            else:
                count += 1
    return count


if __name__ == '__main__':
    pass

    test = [
        'ecl:gry pid:860033327 eyr:2020 hcl:#fffffd byr:1937 iyr:2017 cid:147 hgt:183cm',
        'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884 hcl:#cfa07d byr:1929',
        'hcl:#ae17e1 iyr:2013 eyr:2024 ecl:brn pid:760753108 byr:1931 hgt:179cm',
        'hcl:#cfa07d eyr:2025 pid:166559648 iyr:2011 ecl:brn hgt:59in'
    ]

    test = [process_passport(p) for p in test]

    assert count_valid(test) == 2

    assert VALIDATION['byr']('1920')
    assert VALIDATION['byr']('2002')
    assert VALIDATION['byr']('2003') is False

    assert VALIDATION['hgt']('60in')
    assert VALIDATION['hgt']('190cm')
    assert VALIDATION['hgt']('190in') is False
    assert VALIDATION['hgt']('190') is False

    assert VALIDATION['hcl']('#123abc')
    assert VALIDATION['hcl']('#123abz') is False
    assert VALIDATION['hcl']('123abc') is False

    assert VALIDATION['ecl']('brn')
    assert VALIDATION['ecl']('wat') is False

    assert VALIDATION['pid']('000000001')
    assert VALIDATION['pid']('0123456789') is False

    test = [process_passport(p) for p in [
        'eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
        'iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946',
        'hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
        'hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007'
    ]]

    assert count_valid(test, strictly=True) == 0

    test = [process_passport(p) for p in [
        'pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f',
        'eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
        'hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022',
        'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'
    ]]

    assert count_valid(test, strictly=True) == 4

    with open('inputs/day4.txt') as f:
        passports = parse_input(f)

    assert count_valid(passports) == 196
    assert count_valid(passports, strictly=True) == 114
