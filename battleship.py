import os
import time
from random import randint


ROWS = 10  # number of rows
COLS = 10  # number of columns


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def init_board(ROWS, COLS):
    board = [[0 for _ in range(ROWS)] for _ in range(COLS)]
    return board


def checking_sunked_ships(table):
    counter = 0
    for elements in table:
        counter += elements.count('S')
    if counter == 3:
        return True
    else:
        return False


def convert_coordinates(coordinate):
    alphabet = {'A': 1, 'B': 2, 'C': 3, 'D': 4,
                'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9}
    try:
        row = alphabet[coordinate[0].upper()]-1
        col = int(coordinate[1:])-1
    except KeyError:
        row = 9999  # it will cause out of range error
        col = int(coordinate[1])-1
    return row, col


def validate_input(board, use_for_what):
    while True:
        coordinate = input('Please choose a coordinate !\n')
        if len(coordinate) < 2:
            print('That is not a coordinate')
        elif coordinate[0].isalpha() and coordinate[1:].isnumeric():
            row, col = convert_coordinates(coordinate)
            if use_for_what == 'shot':
                if is_in_range(row, col, board):
                    return row, col
                else:
                    print('Out of range')
            elif is_in_range(row, col, board):
                if check_position_is_available(board, row, col):
                    return row, col
                else:
                    print('It`s already taken')
            else:
                print('Out of range')
        else:
            print('That is not a coordinate')


def ai_move(board):
    while True:
        row = randint(0, ROWS-1)
        col = randint(0, COLS-1)
        if board[row][col] == 0 or board[row][col] == 'X':
            return row, col


def ai_placing_ships(board, ship, player):
    row, col = ai_move(board)
    if is_ship_around(row, col, board):
        ai_placing_ships(board, ship, player)
    elif ship == 1:
        mark(board, row, col, 'ship')
    else:
        direction = randint(0, 1)
        try:
            if direction == 0:
                mark(board, row, col+1, 'ship')
                mark(board, row, col, 'ship')

            elif direction == 1:
                mark(board, row+1, col, 'ship')
                mark(board, row, col, 'ship')
        except IndexError:
            ai_placing_ships(board, ship, player)
    print_board(board1, board2)
    return board1, board2


def is_in_range(row, col, board):
    if row in range(ROWS) and col in range(COLS):
        return True
    else:
        return False


def make_a_shot(player, board):
    print('player ', player, 'turn to shot')
    if player == 'AI':
        row, col = ai_move(board)
    else:
        row, col = validate_input(board, 'shot')
    print('player ', player, 'turn to shot')
    if board[row][col] == 'X':
        if is_ship_around(row, col, board):
            marked_cell = 'hit'
        else:
            marked_cell = 'sunk'
            try:
                mark(board, row, col, marked_cell)
                row, col = where_is_the_hole(row, col, board)
            except TypeError:
                pass

    else:
        marked_cell = 'missed'
    mark(board, row, col, marked_cell)
    print_action(marked_cell)


def where_is_the_hole(row, col, board):
    alist = [1, -1]
    for i in alist:
        try:
            if board[row+i][col] == 'H':
                return row+i, col
        except IndexError:
            pass
    for i in alist:
        try:
            if board[row][col+i] == 'H':
                return row, col+i
        except IndexError:
            pass


def print_action(marked_cell):
    if marked_cell == 'missed':
        print('You`ve missed!')
    elif marked_cell == 'hit':
        print('You`ve hit a ship!')
    elif marked_cell == 'sunk':
        print('You`ve sunk a ship!')
    time.sleep(0.8)


def mark(board, row, col, marked_cell):
    if marked_cell == 'ship':
        board[row][col] = 'X'
    elif marked_cell == 'missed':
        board[row][col] = 'M'
    elif marked_cell == 'hit':
        board[row][col] = 'H'
    elif marked_cell == 'sunk':
        board[row][col] = 'S'
    else:
        print('sthg')


def check_position_is_available(board, row, col):
    if board[row][col] == 0:
        return True
    else:
        return False


def has_won(table1, table2):
    if checking_sunked_ships(table1) is True:
        winner = 2
        print('Player ', winner, ' wins!')
        return True

    elif checking_sunked_ships(table2) is True:
        winner = 1
        print('Player ', winner, ' wins!')
        return True
    else:
        return False


def making_fancy(board, when):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'X':
                if when == 'placing':
                    board[row][col] = '🚢'
                else:
                    board[row][col] = '🌊'
            elif board[row][col] == 0:
                board[row][col] = '🌊'
            elif board[row][col] == 'S':
                board[row][col] = '💨'
            elif board[row][col] == 'H':
                board[row][col] = '🔥'
            elif board[row][col] == 'M':
                board[row][col] = '⛔'


def tracing_ships_places(board):
    ship_places = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 'X':
                ship_places.append([row, col])
    return ship_places


def placing_ships_back(board, ship_places):
    for element in ship_places:
        board[element[0]][element[1]] = 'X'


def making_normal(board):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == '🚢':
                board[row][col] = 'X'
            elif board[row][col] == '🌊':
                board[row][col] = 0
            elif board[row][col] == '💨':
                board[row][col] = 'S'
            elif board[row][col] == '🔥':
                board[row][col] = 'H'
            elif board[row][col] == '⛔':
                board[row][col] = 'M'


def print_board(board1, board2, when='battle'):
    clear()
    ship_places1 = tracing_ships_places(board1)
    ship_places2 = tracing_ships_places(board2)
    if len(ship_places1) > 2:
        making_fancy(board1, 'battle')
    else:
        making_fancy(board1, when)
    making_fancy(board2, when)
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    print('    Player1              Player2')
    for i in range(COLS):
        if i == COLS-1:
            print(i+1, end='    ')
        elif i == 0:
            print(' ', i+1, end='   ')
        else:
            print(i+1, end='   ')
    for i in range(COLS):
        if i == 0:
            print('   ', i+1, end='   ')
        else:
            print(i+1, end='   ')
    for line1, line2, letter in zip(board1, board2, alphabet):
        print('\n'+letter, end=' ')
        for element, i in zip(line1, range(COLS)):
            if i == COLS-1:
                print(element, end='    '+letter+' ')
            else:
                print(element, end='  ')
        for element in line2:
            print(element, end='  ')
    print('\n')
    placing_ships_back(board1, ship_places1)
    placing_ships_back(board2, ship_places2)
    making_normal(board1)
    making_normal(board2)


def is_ship_around(row, col, board):
    plus_minus = [1, -1]
    for i in plus_minus:
        if is_in_range(row+i, col, board) and board[row+i][col] == 'X':
            return True
        elif is_in_range(row, col+i, board) and board[row][col+i] == 'X':
            return True
    return False


def placing_ships(board, ship, player):
    if player == 'AI':
        ai_placing_ships(board, ship, player)
        return True
    print('player ', player, 'turn')
    print('placing ship:', ship)
    row, col = validate_input(board, 'placing_ships')
    if is_ship_around(row, col, board):
        print('Ships are too close')
        placing_ships(board, 2, player)
    elif ship == 1:
        board[row][col] = 'X'
    else:
        direction = input('Please choose a direction v or h !')
        try:
            if direction.upper() == 'H':
                mark(board, row, col+1, 'ship')
                mark(board, row, col, 'ship')
                if player == 1:
                    clear()
                    input('Next player`s placement phase press enter to continue')

            elif direction.upper() == 'V':
                mark(board, row+1, col, 'ship')
                mark(board, row, col, 'ship')
                if player == 1:
                    clear()
                    input('Next player`s placement phase press enter to continue')
            else:
                print('v or h !')
        except IndexError:
            print('too close to edge')
            placing_ships(board, 2, player)
    print_board(board1, board2, 'placing')
    return board1, board2


def battleship_game(board1, board2):
    print_board(board1, board2)
    play_type = input('1. Single player, 2. Multiplayer\n')
    turn_limit = int(input(' please choose a turn limit between 5-50\n'))
    if turn_limit > 50 or turn_limit < 5:
        print('must be between 5-50')
        battleship_game(board1, board2)
    for i in range(2):
        for l in range(2):
            if play_type == '1':
                if i == 0:
                    player = i+1
                else:
                    player = 'AI'
            elif play_type == '2':
                player = i+1
            else:
                print('please input 1 or 2!')
                battleship_game(board1, board2)
            ship = l+1
            if player == 1:
                board = board1
            else:
                board = board2
            placing_ships(board, ship, player)
    for i in range((turn_limit*2)):
        if i % 2 == 1:
            player = 1
            board = board2
        else:
            if play_type == '1':
                player = 'AI'
            elif play_type == '2':
                player = 2
            board = board1
        make_a_shot(player, board)
        print_board(board1, board2)
        if has_won(board1, board2):
            quit()
    print('No more turns, it`s a draw!')
    quit()


ROWS = int(input('please choose a board size between 5-10\n'))
COLS = ROWS
board1 = init_board(ROWS, COLS)
board2 = init_board(ROWS, COLS)
battleship_game(board1, board2)
