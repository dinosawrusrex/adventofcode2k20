def accumulator_until_first_repeat(instruction, debug=False):
    address = 0
    output = 0
    history = set()

    while address not in history:
        history.add(address)
        operation, value = instruction[address].split(' ')
        value = int(value)

        if operation == 'acc':
            output += value

        address += value if operation == 'jmp' else 1

        if address >= len(instruction):
            return output

    return output if debug else None

def fix_program(instruction):
    nop_or_jmp_indices = (
        index for index, operation in enumerate(instruction)
        if 'nop' in operation or 'jmp' in operation
    )

    for index in nop_or_jmp_indices:
        copy = instruction.copy()
        if 'nop' in copy[index]:
            copy[index]  = copy[index].replace('nop', 'jmp')
        else:
            copy[index] = copy[index].replace('jmp', 'nop')

        output = accumulator_until_first_repeat(copy)
        if isinstance(output, int):
            return output


if __name__ == '__main__':
    test = [
        'nop +0',
        'acc +1',
        'jmp +4',
        'acc +3',
        'jmp -3',
        'acc -99',
        'acc +1',
        'jmp -4',
        'acc +6'
    ]

    assert accumulator_until_first_repeat(test, debug=True) == 5
    assert fix_program(test) == 8

    with open('inputs/day8.txt') as f:
        instructions = [l.strip() for l in f.readlines() if l]

    assert accumulator_until_first_repeat(instructions, debug=True) == 1521
    assert fix_program(instructions) == 1016
