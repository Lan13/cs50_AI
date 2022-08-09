"""
Tic Tac Toe Player
"""

import copy
import math
from os import access

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    X_count = 0
    O_count = 0
    for row in board:
        for cell in row:
            X_count += 1 if cell == X else 0
            O_count += 1 if cell == O else 0
    return X if X_count <= O_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_list = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_list.append((i, j))
    return actions_list


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_new = copy.deepcopy(board)
    i, j = action
    if board_new[i][j] != EMPTY:
        raise Exception("invalid action")
    board_new[i][j] = player(board)
    return board_new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    X_winState = [X, X, X]
    O_winState = [O, O, O]
    for i in range(3):
        row = board[i]
        col = [board[0][i], board[1][i], board[2][i]]
        if row == X_winState or col == X_winState:
            return X
        elif row == O_winState or col == O_winState:
            return O
    diag0 = [board[0][0], board[1][1], board[2][2]]
    diag1 = [board[0][2], board[1][1], board[2][0]]
    if diag0 == X_winState or diag1 == X_winState:
        return X
    elif diag0 == O_winState or diag1 == O_winState:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    current_winner = winner(board)
    if current_winner == X:
        return 1
    elif current_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    current_player = player(board)
    actions_list = actions(board)
    optimal = None
    current_max = -1e10
    current_min = 1e10
    for action in actions_list:
        if current_player == X:
            value_min = min_value(result(board, action))
            if current_max < value_min:
                current_max = value_min
                optimal = action
        else:
            value_max = max_value(result(board, action))
            if current_min > value_max:
                current_min = value_max
                optimal = action
    return optimal


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -1e10
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = 1e10
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
