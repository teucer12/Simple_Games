import random
from typing import List, Optional
import os
import datetime
import json

def header():
    print('---------------------------')
    print('      Connect 4 v1')
    print('---------------------------')

def show_leaderboard():
    leaders = get_leaders()

    sorted_names = list(leaders.items())
    sorted_names.sort(key=lambda l: l[1], reverse=True)
    log("Game Starting...")
    print()
    print ("LEADERS:")
    for name, wins in sorted_names[0:5]:
        print(f"{wins:,} -- {name}")
    print()
    print("---------------------------------")
    print()

def main():
    header()
    turns = 0
    active_player_index = 0
    show_leaderboard()
    # get players
    Player1 = input("What is Player 1's name? ")
    log(f"{Player1} has joined.")
    Player2 = input("What is Player 2's name (Enter for AI)? ")
    if Player2 == "":
        Player2 = "AI"
    else:
        log(f"{Player2} has joined.")
    players = [Player1, Player2, ]
    players_symbols = ["O", "X", ]
    coin = random.randint(1, 2)
    if coin == 1:
        active_player_index = 0
        print(f"{Player1} goes first!")
    else:
        active_player_index = 1
        print(f"{Player2} goes first!")

    board = [
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None]]

    # whose turn is it
    while not find_winner(board):
        player = players[active_player_index]
        symbol = players_symbols[active_player_index]
        announce_turn(player)

        # show the board
        show_board(board)
        if not choose_location(board, symbol, player):
            print("That is not an option, try again.")
            continue

        # drop a piece
        # check for a winner
        # change players
        active_player_index = (active_player_index + 1) % 2
        turns += 1
        if turns == 42:
            print("Tie Game!")
            exit()
    print(f'Game Over! {player} has won with the board: ')
    show_board(board)
    record_win(player)
    log(f"{player}) has won")

def announce_turn(player):
    print(f"{player}, drop your piece!")
    print()


def find_winner(board):
    sequences = get_winning_sequences(board)

    for cells in sequences:
        symbol1 = cells[0]
        if symbol1 and all(symbol1 == cell for cell in cells):
            return True

    return False


def get_winning_sequences(board):
    sequences = []
    winrow = [0, 1, 2, 3, 4, 5]
    for row in winrow:
        rows = [
            [board[row][0], board[row][1], board[row][2], board[row][3]],
            [board[row][4], board[row][1], board[row][2], board[row][3]],
            [board[row][5], board[row][4], board[row][2], board[row][3]],
            [board[row][6], board[row][5], board[row][4], board[row][3]]
        ]

        sequences.extend(rows)

    wincol = [0, 1, 2, 3, 4, 5, 6]
    for col in wincol:
        cols = [
            [board[0][col], board[1][col], board[2][col], board[3][col]],
            [board[1][col], board[2][col], board[3][col], board[4][col]],
            [board[2][col], board[3][col], board[4][col], board[5][col]]
        ]
        sequences.extend(cols)

    diagonals = [
        [board[2][0], board[3][1], board[4][2], board[5][3]],
        [board[1][0], board[2][1], board[3][2], board[4][3], board[5][4]],
        [board[0][0], board[1][1], board[2][2], board[3][3], board[4][4], board[5][5]],
        [board[0][1], board[1][2], board[2][3], board[3][4], board[4][5], board[5][6]],
        [board[0][2], board[1][3], board[2][4], board[3][5], board[4][6]],
        [board[0][3], board[1][4], board[2][5], board[3][6]],
        #    ]

        # diag_row2 = [board[0][3], board[1][2], board[2][1], board[3][0]],
        [board[0][4], board[1][3], board[2][2], board[3][1], board[4][0]],
        [board[0][5], board[1][4], board[2][3], board[3][2], board[4][1], board[5][0]],
        [board[0][6], board[1][5], board[2][4], board[3][3], board[4][2], board[5][1]],
        [board[1][6], board[2][5], board[3][4], board[4][3], board[5][2]],
        [board[2][6], board[3][5], board[4][4], board[5][3]],
    ]

    for diag in diagonals:
        fours_diagonals = find_sequences_four_cells(diag)
        sequences.extend(fours_diagonals)

    return sequences


def find_sequences_four_cells(cells: List[str]) -> List[List[str]]:
    sequences = []
    for n in range(0, len(cells) - 3):
        candidate = cells[n:n + 4]
        if len(candidate) == 4:
            sequences.append(candidate)

    return sequences


def show_board(board):
    print("  1   2   3   4   5   6   7")
    for row in board:
        print("| ", end="")
        for cell in row:
            symbol = cell if cell is not None else "_"
            print(symbol, end=" | ")
        print()


def choose_location(board, symbol, player):
    try:
        if player == 'AI':
            column = random.randint(1, 7)
        else:
            column = int(input("Choose which column: "))

        row = 5
        column -= 1
        if row < 0 or column < 0 or column > 6:
            return False

        cell = board[row][column]
        while cell is not None:
            row -= 1
            if row < 0:
                return False
            cell = board[row][column]
        board[row][column] = symbol
        return True
    except:
        print()
        print("ERROR: Invalid Input")
        return False

def get_leaders():
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'c4leader.json')

    if not os.path.exists(filename):
        return {}

    with open(filename, 'r', encoding='utf-8') as fin:
        return json.load(fin)

def record_win(winner_name):
    leaders = get_leaders()
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'c4leader.json')

    if winner_name in leaders:
        leaders[winner_name] += 1
    else:
        leaders[winner_name] = 1

    with open(filename, 'w', encoding='utf-8') as fout:
        json.dump(leaders, fout)

def log(msg):
    directory = os.path.dirname(__file__)
    filename = os.path.join(directory, 'c4.log')

    with open(filename, 'a', encoding='utf-8') as fout:
        fout.write(f'[{datetime.datetime.now().date().isoformat()}]')
        fout.write(msg)
        fout.write('\n')


if __name__ == "__main__":
    main()
