import itertools

def neighbour_delta(coord):
    for y in range(coord[1]-1, coord[1]+2):
        for x in range(coord[0]-1, coord[0]+2):
            if (x, y) != coord:
                yield x, y

def change_coord(coord, delta):
    return (coord[0]+delta[0], coord[1]+delta[1])

def neighbours(coord, raw_map):
    x_bound = len(raw_map[0])
    y_bound = len(raw_map)
    return [
        (x, y) for x, y in neighbour_delta(coord)
        if (
            0 <= x < x_bound and
            0 <= y < y_bound and
            raw_map[y][x] != '.'
        )
    ]

def seat_neighbours(coord, raw_map):
    x_bound = len(raw_map[0])
    y_bound = len(raw_map)
    neighbours = []
    for delta in neighbour_delta((0, 0)):
        new_coord = change_coord(coord, delta)
        while True:
            if 0 <= new_coord[0] < x_bound and 0 <= new_coord[1] < y_bound:
                if raw_map[new_coord[1]][new_coord[0]] == '.':
                    new_coord = change_coord(new_coord, delta)
                else:
                    neighbours.append(new_coord)
                    break
            else:
                break
    return neighbours

class Seat:
    def __init__(self, x, y, neighbours, seat_neighbours):
        self.x = x
        self.y = y
        self.neighbours = neighbours
        self.seat_neighbours = seat_neighbours
        self.alive = False
        self.alive_next = None

    def reset(self):
        self.alive = False
        self.alive_next = None

    def next_state(self, seating, latter):
        living_count = len(list(filter(
            lambda c: seating[c].alive,
            self.seat_neighbours if latter else self.neighbours
        )))

        if ((self.alive and living_count < (5 if latter else 4)) or
            (not self.alive and not living_count)):
            self.alive_next = True
        else:
            self.alive_next = False

    def stable(self):
        return self.alive == self.alive_next

    def update_state(self):
        self.alive = self.alive_next
        self.alive_next = None


def initialise_seating(raw_map):
    return {
        (x, y): Seat(
            x, y,
            neighbours((x, y), raw_map),
            seat_neighbours((x, y), raw_map)
        )
        for y, row in enumerate(raw_map)
        for x, seat in enumerate(row)
        if seat != '.'
    }

def occupied_at_stable_seating(seating, latter=False):

    stable = True
    for seat in seating.values():
        seat.next_state(seating, latter=latter)
        if seat.stable() is False:
            stable = False

    if stable:
        return len(list(filter(
            lambda s: s.alive,
            seating.values()
        )))

    for seat in seating.values():
        seat.update_state()
    return occupied_at_stable_seating(seating, latter=latter)

if __name__ == '__main__':
    test = [
        'L.LL.LL.LL',
        'LLLLLLL.LL',
        'L.L.L..L..',
        'LLLL.LL.LL',
        'L.LL.LL.LL',
        'L.LLLLL.LL',
        '..L.L.....',
        'LLLLLLLLLL',
        'L.LLLLLL.L',
        'L.LLLLL.LL'
    ]
    seating = initialise_seating(test)
    assert occupied_at_stable_seating(seating) == 37
    for s in seating.values():
        s.reset()
    assert occupied_at_stable_seating(seating, latter=True) == 26

    with open('inputs/day11.txt') as f:
        seating = initialise_seating([l.strip() for l in f.readlines() if l])

    assert occupied_at_stable_seating(seating) == 2344
    for s in seating.values():
        s.reset()
    assert occupied_at_stable_seating(seating, latter=True) == 2076
