def binary_search(bsp):
    return sum(
        2**exponent
        for exponent, char in zip(range(len(bsp)-1, -1, -1), bsp)
        if char in 'BR'
    )

def row_and_column(bsp):
    return binary_search(bsp[:7]), binary_search(bsp[7:])

def seat_id(row_column):
    return (row_column[0] * 8) + row_column[1]

def empty_remaining_seats(seats):
    return {(row, col) for row in range(1, 127) for col in range(0, 6)}.difference(seats)

def get_my_seat_id(all_seat_ids, remaining_seats):
    for row_column in remaining_seats:
        seat = seat_id(row_column)
        if seat-1 in all_seat_ids and seat+1 in all_seat_ids:
            return seat


if __name__ == '__main__':
    test = 'FBFBBFFRLR'
    assert binary_search(test[:7]) == 44
    assert binary_search(test[7:]) == 5
    assert seat_id(row_and_column(test)) == 357

    assert seat_id(row_and_column('BFFFBBFRRR')) == 567
    assert seat_id(row_and_column('FFFBBBFRRR')) == 119
    assert seat_id(row_and_column('BBFFBBFRLL')) == 820

    with open('inputs/day5.txt') as f:
        bsps = (bsp.strip() for bsp in f.readlines() if bsp)

    seats = {row_and_column(bsp) for bsp in bsps}
    all_seat_ids = [seat_id(seat) for seat in seats]

    assert max(all_seat_ids) == 838
    assert get_my_seat_id(all_seat_ids, empty_remaining_seats(seats)) == 714
