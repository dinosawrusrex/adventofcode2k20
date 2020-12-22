import collections
import copy


def parse_cards(decks):

    parsed_decks = []
    current = None

    for c in decks:
        if 'Player' in c:
            if current:
                parsed_decks.append(current)
            current = collections.deque()
        else:
            current.appendleft(int(c))

    parsed_decks.append(current)

    return parsed_decks

def play(decks, recursive=False, a_is_winner=False):
    a, b = decks
    a = copy.copy(a)
    b = copy.copy(b)

    if recursive:
        history = {'a': [copy.copy(a)], 'b': [copy.copy(b)]}

    while a and b:
        winner, loser = (a, b) if is_a_winner(a, b, recursive) else (b, a)
        winner.rotate()
        winner.appendleft(loser.pop())

        if recursive:
            if a in history['a'] or b in history['b']:
                return True if a_is_winner else a
            else:
                history['a'].append(copy.copy(a))
                history['b'].append(copy.copy(b))

    if a_is_winner:
        return True if a else False
    return a if a else b

def is_a_winner(a, b, recursive=False):

    if recursive and len(a) > a[-1] and len(b) > b[-1]:
        a_copy = copy.copy(a)
        b_copy = copy.copy(b)

        for deck in (a_copy, b_copy):
            for _ in range(len(deck)-1-deck.pop()):
                deck.popleft()

        return play((a_copy, b_copy), recursive=recursive, a_is_winner=True)

    return a[-1] > b[-1]


if __name__ == '__main__':

    test = [
        'Player 1:', '9', '2', '6', '3', '1',
        'Player 2:', '5', '8', '4', '7', '10',
    ]

    decks = parse_cards(test)
    winner = play(decks)
    assert sum(i*c for i, c in enumerate(winner, start=1)) == 306

    winner = play(decks, recursive=True)
    assert sum(i*c for i, c in enumerate(winner, start=1)) == 291

    with open('inputs/day22.txt') as f:
        cards = [l.strip() for l in f.readlines() if l.strip()]

    decks = parse_cards(cards)
    winner = play(decks)
    assert sum(i*c for i, c in enumerate(winner, start=1)) == 33473

    winner = play(decks, recursive=True)
    assert sum(i*c for i, c in enumerate(winner, start=1)) == 31793
