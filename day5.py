def binary_search(bsp):
    return int(
        bsp.replace('F', '0').replace('L', '0').replace('B', '1').replace('R', '1'),
        2
    )

def seat_id(bsp):
    return (binary_search(bsp[:7]) * 8) + binary_search(bsp[7:])

def get_my_seat_id(all_seat_ids):
    # 1024 derivation:
    # max for row is 127 (2**7 - 1), max for col is 7 (2**3 - 1)
    # (127 * 8) + 8 = 1024
    for seat in range(1024):
        if all((
            seat not in all_seat_ids,
            seat-1 in all_seat_ids,
            seat+1 in all_seat_ids
        )):
            return seat


if __name__ == '__main__':
    test = 'FBFBBFFRLR'
    assert binary_search(test[:7]) == 44
    assert binary_search(test[7:]) == 5
    assert seat_id(test) == 357

    assert seat_id('BFFFBBFRRR') == 567
    assert seat_id('FFFBBBFRRR') == 119
    assert seat_id('BBFFBBFRLL') == 820

    with open('inputs/day5.txt') as f:
        bsps = (bsp.strip() for bsp in f.readlines() if bsp)

    all_seat_ids = [seat_id(bsp) for bsp in bsps]

    assert max(all_seat_ids) == 838
    assert get_my_seat_id(all_seat_ids) == 714
