import math

DIRECTIONS = ['E', 'S', 'W', 'N']
# DELTA corresponds with the DIRECTIONS index
DELTA = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def apply_delta(coord, direction, distance):
    return (
        coord[0] + DELTA[direction][0] * distance,
        coord[1] + DELTA[direction][1] * distance
    )


def apply_waypoint(coord, waypoint, distance):
    for direction, w_distance in waypoint:
        coord = apply_delta(coord, direction, distance*w_distance)
    return coord


def change_direction(rotation, angle, facing):
    delta = int((angle - (math.floor(angle / 360) * 360)) / 90)
    if 0 <= delta <= 3:
        facing += delta * (-1 if rotation == 'L' else 1)

    if not (0 <= facing < 4):
        facing += 4 * (-1 if facing >= 4 else 1)

    return facing


def change_waypoint(rotation, value, waypoint):
    for w in waypoint:
        w[0] = change_direction(rotation, value, w[0])
    return waypoint


def destination_from_origin(instruction, waypoint=False):
    coord = (0, 0)
    change_coord = apply_waypoint if waypoint else apply_delta

    facing = [[0, 10], [3, 1]] if waypoint else 0
    change_facing = change_waypoint if waypoint else change_direction

    for actions in instruction:
        direction_or_rotation, value = actions[0], int(actions[1:])

        if direction_or_rotation in DIRECTIONS:
            direction = DIRECTIONS.index(direction_or_rotation)
            if waypoint:
                facing.append([direction, value])
            else:
                coord = change_coord(coord, direction, value)

        if direction_or_rotation == 'F':
            coord = change_coord(coord, facing, value)

        if direction_or_rotation in 'LR':
            facing = change_facing(direction_or_rotation, value, facing)

    return abs(coord[0]) + abs(coord[1])


if __name__ == '__main__':
    instruction = ['F10', 'N3', 'F7', 'R90', 'F11']
    assert destination_from_origin(instruction) == 25
    assert destination_from_origin(instruction, waypoint=True) == 286

    with open('inputs/day12.txt') as f:
        instruction = [l.strip() for l in f.readlines() if l]

    assert destination_from_origin(instruction) == 1482
    assert destination_from_origin(instruction, waypoint=True) == 48739
