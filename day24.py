import collections
import copy
import functools
import itertools


DELTA = {
    # double-width horizontal layout, doubles column values
    # https://www.redblobgames.com/grids/hexagons/
    'e': (2, 0), 'ne': (1, 1), 'se': (1, -1),
    'w': (-2, 0), 'nw': (-1, 1), 'sw': (-1, -1)
}


def parse_individual_steps(steps):
    current = ''
    while (steps := collections.deque(steps)):
        current += steps.popleft()
        if current in ['s', 'n']:
            continue

        yield current
        current = ''


def get_coordinates(steps):
    coordinate = (0, 0)
    for step in parse_individual_steps(steps):
        coordinate = (coordinate[0]+DELTA[step][0], coordinate[1]+DELTA[step][1])
    return coordinate


def black_coordinates(lines_of_steps):
    black = set()

    for steps in lines_of_steps:
        if (coordinate := get_coordinates(steps)) not in black:
            black.add(coordinate)
        else:
            black.remove(coordinate)

    return black


@functools.cache
def neighbours(coordinate):
    return set((coordinate[0] + d[0], coordinate[1] + d[1]) for d in DELTA.values())


def run(blacks, iterations=100):

    for _ in range(iterations):
        next_blacks = set()
        inspected = set()
        for c in blacks:
            inspected.add(c)
            if 0 < len(neighbours(c).intersection(blacks)) < 3:
                next_blacks.add(c)

        for c in itertools.chain.from_iterable(neighbours(c) for c in blacks):
            if c not in inspected and c not in blacks:
                inspected.add(c)
                if len(neighbours(c).intersection(blacks)) == 2:
                    next_blacks.add(c)

        blacks = copy.copy(next_blacks)

    return blacks



if __name__ == '__main__':
    test = 'esew'
    assert get_coordinates(test) == (1, -1)

    test = 'nwwswee'
    assert get_coordinates(test) == (0, 0)

    test = [
        'sesenwnenenewseeswwswswwnenewsewsw',
        'neeenesenwnwwswnenewnwwsewnenwseswesw',
        'seswneswswsenwwnwse',
        'nwnwneseeswswnenewneswwnewseswneseene',
        'swweswneswnenwsewnwneneseenw',
        'eesenwseswswnenwswnwnwsewwnwsene',
        'sewnenenenesenwsewnenwwwse',
        'wenwwweseeeweswwwnwwe',
        'wsweesenenewnwwnwsenewsenwwsesesenwne',
        'neeswseenwwswnwswswnw',
        'nenwswwsewswnenenewsenwsenwnesesenew',
        'enewnwewneswsewnwswenweswnenwsenwsw',
        'sweneswneswneneenwnewenewwneswswnese',
        'swwesenesewenwneswnwwneseswwne',
        'enesenwswwswneneswsenwnewswseenwsese',
        'wnwnesenesenenwwnenwsewesewsesesew',
        'nenewswnwewswnenesenwnesewesw',
        'eneswnwswnwsenenwnwnwwseeswneewsenese',
        'neswnwewnwnwseenwseesewsenwsweewe',
        'wseweeenwnesenwwwswnew'
    ]
    blacks = black_coordinates(test)
    assert len(blacks) == 10
    assert len((run(blacks))) == 2208

    with open('inputs/day24.txt') as f:
        lines_of_steps = [l.strip() for l in f.readlines() if l.strip()]

    blacks = black_coordinates(lines_of_steps)
    assert len(blacks) == 420
    assert len(run(blacks)) == 4206
