import math

def parse_map(grid):
    return (
        len(grid),
        len(grid[0]),
        {
            (x, y)
            for y, row in enumerate(grid) for x, col in enumerate(row)
            if col == '#'
        }
    )

def x_path_generator(width, width_step):
    # Start at width_step.
    # Start counting trees from first step after origin.
    x = width_step
    while True:
        yield x
        if (x := x+width_step) >= width:
            x -= width


def traverse_and_count_trees(height, width, trees, height_step, width_step):
    # Start at height_step.
    # Start counting trees from first step after origin.
    path = {
        coord
        for coord in zip(
            x_path_generator(width, width_step),
            range(height_step, height, height_step)
        )
    }
    return len(path.intersection(trees))

def multiply_with_different_steps(height, width, trees):
    return math.prod((
        traverse_and_count_trees(
            height, width, trees, height_step, width_step
        )
        for height_step, width_step in (
            (1, 1), (1, 3), (1, 5), (1, 7), (2, 1)
        )
    ))


if __name__ == '__main__':

    test = [
        '..##.......',
        '#...#...#..',
        '.#....#..#.',
        '..#.#...#.#',
        '.#...##..#.',
        '..#.##.....',
        '.#.#.#....#',
        '.#........#',
        '#.##...#...',
        '#...##....#',
        '.#..#...#.#'
    ]

    height, width, trees = parse_map(test)
    assert traverse_and_count_trees(height, width, trees, 1, 1) == 2
    assert traverse_and_count_trees(height, width, trees, 1, 3) == 7
    assert traverse_and_count_trees(height, width, trees, 1, 5) == 3
    assert traverse_and_count_trees(height, width, trees, 1, 7) == 4
    assert traverse_and_count_trees(height, width, trees, 2, 1) == 2
    assert multiply_with_different_steps(height, width, trees) == 336

    with open('inputs/day3.txt') as f:
        raw = [f.strip() for f in f.readlines() if f]

    height, width, trees = parse_map(raw)
    assert traverse_and_count_trees(height, width, trees, 1, 3) == 191
    assert multiply_with_different_steps(height, width, trees) == 1478615040
