class Cup:

    def __init__(self, number):
        self.number = number
        self.next = None

    def __repr__(self):
        return f'{self.number}({self.next.number if isinstance(self.next, Cup) else None})'

    def neighbour(self, n=1):
        c = None
        for _ in range(n):
            c = c.next if isinstance(c, Cup) else self.next
        return c

    @property
    def next_three(self):
        return [self.neighbour(), self.neighbour(2), self.neighbour(3)]


def parse_cups(cups, extend=False):

    first = Cup(int(cups[0]))
    current = first
    last = None

    for i, c in enumerate(cups[1:], start=1):
        current.next = Cup(int(c))
        current = current.next
        if i == len(cups) - 1:
            last = current
            current.next = first

    if extend is False:
        return first

    current = last
    for i in range(max(int(c) for c in cups)+1, 1000001):
        new = Cup(i)
        current.next = new
        current = new

        if i == 1000000:
            current.next = first

    return first


def get_all_cups(first):
    cups = {}

    current = first
    while current.number not in cups:
        cups[current.number] = current
        current = current.next

    return cups


def destination(current, cups, reduction_factor=None):
    reduction_factor = reduction_factor if reduction_factor else 1
    next_three = current.next_three

    if (current_n := current.number - reduction_factor) in cups:
        if cups[current_n] in next_three:
            return destination(current, cups, reduction_factor + 1)
        else:
            return cups[current_n]
    return max(
        (c for c in cups.values() if c not in next_three and c != current),
        key=lambda c: c.number
    )


def run(first, moves=100):
    cups = get_all_cups(first)

    minimum = min(cups.keys())
    current = first
    for _ in range(moves):
        dest = destination(current, cups)
        temp = current.neighbour(3).next
        current.neighbour(3).next = dest.next
        dest.next = current.next
        current.next = temp
        current = current.next
    return cups


def final_order(cups):
    order = []
    current = cups[1].next
    while current.number != 1:
        order.append(str(current.number))
        current = current.next
    return ''.join(order)


if __name__ == '__main__':
    test = '389125467'

    first = parse_cups(test)
    result = run(first)
    assert final_order(result) == '67384529'

    board = parse_cups(test, True)
    result = run(board, 10000000)
    n = result[1].next
    assert n.number == 934001
    assert n.next.number == 159792
    assert n.number * n.next.number == 149245887792

    original = '467528193'
    first = parse_cups(original)
    result = run(first)
    assert final_order(result) == '43769582'

    board = parse_cups(original, True)
    result = run(board, 10000000)
    n = result[1].next
    assert n.number == 489710
    assert n.next.number == 540509
    assert n.number * n.next.number == 264692662390
