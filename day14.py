import itertools


SUBSTR_TO_REMOVE = ['mem', '[', ']']

def set_bit(value, bit, bit_index):
    if bit == 1:
        return value | (1 << bit_index)
    return value & ~(1 << bit_index)

def process_mask(line):
    return {
        index: int(bit) if bit != 'X' else bit
        for index, bit in enumerate(line[7:][::-1])
    }

def decode_address(address, mask):
    addresses = []

    # Update address with 1's from mask or make 0 if X
    for index, bit in mask.items():
        if bit == 1:
            address = set_bit(address, bit, index)
        if bit == 'X':
            address = set_bit(address, 0, index)

    # For all X's, we create the binaries with combinations of 0s and 1s
    # E.g. X000X -> [00000, 00001, 10000, 10001]
    xs = ''.join('{}' if c == 'X' else '0' for _, c in reversed(sorted(mask.items())))
    for c in itertools.product(*['01' for _ in range(list(mask.values()).count('X'))]):
        addresses.append(address + int(xs.format(*c), 2))

    return addresses

def address_and_value(line, mask, floating=False):
    for substr in SUBSTR_TO_REMOVE:
        line = line.replace(substr, '')

    address, value = [int(c) for c in line.split(' = ')]

    if floating is False:
        for index, bit in mask.items():
            if bit != 'X':
                value = set_bit(value, bit, index)
        return [(address, value)]

    return [(a, value) for a in decode_address(address, mask)]

def process_instructions(instructions, floating=False):
    mask = None
    memory = {}
    for l in instructions:
        if 'mask' in l:
            mask = process_mask(l)
            continue
        for address, value in address_and_value(l, mask, floating=floating):
            memory[address] = value
    return memory


if __name__ == '__main__':
    test = [
        'mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X',
        'mem[8] = 11',
        'mem[7] = 101',
        'mem[8] = 0'
    ]

    memory = process_instructions(test)
    assert sum(memory.values()) == 165

    test = [
        'mask = 000000000000000000000000000000X1001X',
        'mem[42] = 100',
        'mask = 00000000000000000000000000000000X0XX',
        'mem[26] = 1'
    ]
    memory = process_instructions(test, True)
    assert sum(memory.values()) == 208

    with open('inputs/day14.txt') as f:
        instructions = [l.strip() for l in f.readlines() if l]

    memory = process_instructions(instructions)
    assert sum(memory.values()) == 10717676595607
    memory = process_instructions(instructions, True)
    assert sum(memory.values()) == 3974538275659
