import functools
import itertools

def parse_input(seed, extra_dimension=False):
    dead = set()
    live = set()

    for y, row in enumerate(seed):
        for x, cell in enumerate(row):
            c = (x, y, 0, 0) if extra_dimension else (x, y, 0)
            if cell == '#':
                live.add(c)
            else:
                dead.add(c)

    return live, dead

@functools.cache
def neighbours(cell):
    if len(cell) == 3:
        return {
            (x, y, z)
            for z in range(cell[2]-1, cell[2]+2)
            for y in range(cell[1]-1, cell[1]+2)
            for x in range(cell[0]-1, cell[0]+2)
            if (x, y, z) != cell
        }
    return {
        (x, y, z, w)
        for w in range(cell[3]-1, cell[3]+2)
        for z in range(cell[2]-1, cell[2]+2)
        for y in range(cell[1]-1, cell[1]+2)
        for x in range(cell[0]-1, cell[0]+2)
        if (x, y, z, w) != cell
    }



def next_boundary(living, dead):
    for c in living:
        dimension = len(c)
        break
    if dimension == 3:
        return {
            cell
            for x in range(
                min(c[0] for c in itertools.chain(living, dead))-1,
                max(c[0] for c in itertools.chain(living, dead))+2,
            )
            for y in range(
                min(c[1] for c in itertools.chain(living, dead))-1,
                max(c[1] for c in itertools.chain(living, dead))+2,
            )
            for z in range(
                min(c[2] for c in itertools.chain(living, dead))-1,
                max(c[2] for c in itertools.chain(living, dead))+2,
            )
            if (cell := (x, y, z)) not in living and cell not in dead
        }

    return {
        cell
        for x in range(
            min(c[0] for c in itertools.chain(living, dead))-1,
            max(c[0] for c in itertools.chain(living, dead))+2,
        )
        for y in range(
            min(c[1] for c in itertools.chain(living, dead))-1,
            max(c[1] for c in itertools.chain(living, dead))+2,
        )
        for z in range(
            min(c[2] for c in itertools.chain(living, dead))-1,
            max(c[2] for c in itertools.chain(living, dead))+2,
        )
        for w in range(
            min(c[3] for c in itertools.chain(living, dead))-1,
            max(c[3] for c in itertools.chain(living, dead))+2,
        )
        if (cell := (x, y, z, w)) not in living and cell not in dead
    }


def next_iteration(living, dead):
    next_living = set()
    next_dead = set()

    for live in living:
        if len(neighbours(live).intersection(living)) in [2, 3]:
            next_living.add(live)
        else:
            next_dead.add(live)

    for d in itertools.chain(dead, next_boundary(living, dead)):
        if len(neighbours(d).intersection(living)) == 3:
            next_living.add(d)
        else:
            next_dead.add(d)

    return next_living, next_dead

def run(live, dead, iteration=6):
    for i in range(iteration):
        print(i)
        live, dead = next_iteration(live, dead)
    return live, dead


if __name__ == '__main__':
    test = [
        '.#.',
        '..#',
        '###'
    ]

    living, dead = parse_input(test)
    living, dead = run(living, dead)
    assert len(living) == 112

    living, dead = parse_input(test, True)
    living, dead = run(living, dead, 1)
    assert len(living) == 29

    living, dead = run(living, dead, 5)
    assert len(living) == 848


    with open('inputs/day17.txt') as f:
        seed = [l.strip() for l in f.readlines() if l]

    living, dead = parse_input(seed)
    living, dead = run(living, dead)
    assert len(living) == 317

    living, dead = parse_input(seed, True)
    living, dead = run(living, dead)
    assert len(living) == 1692

