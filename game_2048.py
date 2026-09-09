"""Terminal 2048. Run with Python 3; no extra packages required."""

import random

SIZE = 4


def add_tile(board):
    """Place a 2 (90% chance) or 4 in a random empty square."""
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE)
             if board[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        board[r][c] = 2 if random.random() < 0.9 else 4


def new_game():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_tile(board)
    add_tile(board)
    return board


def merge_row(row):
    """Slide left, merging each tile at most once, and return points earned."""
    tiles = [value for value in row if value != 0]
    merged = []
    points = 0
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            value = tiles[i] * 2
            merged.append(value)
            points += value
            i += 2
        else:
            merged.append(tiles[i])
            i += 1
    return merged + [0] * (SIZE - len(merged)), points


def move(board, direction):
    """Read each row/column from the moving edge, then merge toward it."""
    result = [row[:] for row in board]
    points = 0
    for index in range(SIZE):
        if direction == 'a':
            cells = [(index, c) for c in range(SIZE)]
        elif direction == 'd':
            cells = [(index, c) for c in reversed(range(SIZE))]
        elif direction == 'w':
            cells = [(r, index) for r in range(SIZE)]
        elif direction == 's':
            cells = [(r, index) for r in reversed(range(SIZE))]
        else:
            raise ValueError('Use w, a, s, or d.')
        merged, earned = merge_row([board[r][c] for r, c in cells])
        for (r, c), value in zip(cells, merged):
            result[r][c] = value
        points += earned
    return result, points


def can_move(board):
    return any(move(board, key)[0] != board for key in 'wasd')


def display(board, score):
    width = max(6, len(str(max(map(max, board)))) + 2)
    border = '+' + ('-' * width + '+') * SIZE
    print('\n2048 | Score:', score)
    print(border)
    for row in board:
        print('|' + '|'.join(str(value or '.').center(width)
                             for value in row) + '|')
        print(border)
    print('W: up | A: left | S: down | D: right | R: restart | Q: quit')


def main():
    board = new_game()
    score = 0
    won = False
    print('Combine matching tiles to reach 2048!')
    print('Type a control letter and press Enter.')
    while True:
        display(board, score)
        if not won and any(value >= 2048 for row in board for value in row):
            print('You reached 2048! You can keep playing.')
            won = True
        game_over = not can_move(board)
        if game_over:
            print('Game over! Press R to restart or Q to quit.')
        try:
            command = input('Your move: ').strip().lower()
        except (EOFError, KeyboardInterrupt):
            print('\nThanks for playing!')
            break
        if command == 'q':
            print('Thanks for playing!')
            break
        if command == 'r':
            board = new_game()
            score = 0
            won = False
            continue
        if command not in ('w', 'a', 's', 'd'):
            print('Please enter W, A, S, D, R, or Q.')
            continue
        if game_over:
            continue
        updated, earned = move(board, command)
        if updated != board:
            board = updated
            score += earned
            add_tile(board)
        else:
            print('No tiles can move in that direction. Try another direction.')


if __name__ == '__main__':
    main()
