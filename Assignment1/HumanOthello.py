import copy
import random
import time

EMPTY, BLACK, WHITE, OUTER = '.', 'B', 'W', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

WEIGHTS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 4, -3, 2, 2, 2, 2, -3, 4, 0,
               0, -3, -4, -1, -1, -1, -1, -4, -3, 0,
               0, 2, -1, 1, 0, 0, 1, -1, 2, 0,
               0, 2, -1, 0, 1, 1, 0, -1, 2, 0,
               0, 2, -1, 0, 1, 1, 0, -1, 2, 0,
               0, 2, -1, 1, 0, 0, 1, -1, 2, 0,
               0, -3, -4, -1, -1, -1, -1, -4, -3, 0,
               0, 4, -3, 2, 2, 2, 2, -3, 4, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def squares():
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY

    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

def get_opponent(player):
    return BLACK if player == WHITE else WHITE

def valid_moves(board, player):
    validmoves = []
    playercoords = [i for i, x in enumerate(board) if x == player]

    for piece in playercoords:
        pos = piece
        for dir in DIRECTIONS:
            pos += dir
            while board[pos] == get_opponent(player):
                if board[pos+dir] == EMPTY and pos+dir not in validmoves:
                    validmoves.append(pos+dir)
                pos+=dir
            pos = piece
    return validmoves

def flip_pieces(board, player, move):
    tiles_to_flip = []
    for dir in DIRECTIONS:
        pos = move
        pos += dir
        line_to_flip = []
        while board[pos] == get_opponent(player):
            line_to_flip.append(pos)
            if board[pos + dir] == player:
                for tile in line_to_flip:
                    tiles_to_flip.append(tile)
            pos += dir

    for tile in tiles_to_flip:
        board[tile] = player

    return board

def make_move(board, player, validmove):
    board[validmove] = player
    board = flip_pieces(board, player, validmove)
    return board

def eval_board(board, player):
    eval = 0
    opp = get_opponent(player)

    for s in squares():
        if board[s] == player:
            eval += WEIGHTS[s]
        elif board[s] == opp:
            eval -= WEIGHTS[s]
    return eval

def board_score(board, player):
    score = 0
    opp = get_opponent(player)
    for s in squares():
        if board[s] == player:
            score += 1
        elif board[s] == opp:
            score -= 1
    return score

def alphabeta(board, player, alpha, beta, depth, algo, AI):
    moves = valid_moves(board, player)
    if depth == 0 or len(moves) == 0:
        return (0, eval_board(board, AI))
    m = moves[0]

    if algo == "maxi":#maximizing
        val = -64
        for move in moves:
            next_board = make_move(copy.copy(board), player, move)
            val = max(val, alphabeta(next_board, get_opponent(player), alpha, beta, depth-1, "mini", AI)[1])
            if val > alpha:
                alpha = val
                m = move
            if alpha >= beta:
                break
        return m, val
    else:#minimizing
        val = 64
        for move in moves:
            next_board = make_move(copy.copy(board), player, move)
            val = min(val, alphabeta(next_board, get_opponent(player), alpha, beta, depth-1, "maxi", AI)[1])
            if val < beta:
                beta = val
                m = move
            if alpha >= beta:
                break
        return m, val

#initial parameters
invcount = 0
alpha_0 = -64
beta_0 = 64
player = BLACK
dep = int(input("Max time per move of depths:\n1: 0.002s\n2: 0.013s\n3: 0.14s\n4: 0.76s\n5: 6.7s\nChoose depth:\n"))

#color selection
human = input("Play as B or W?\n")
while not (human == BLACK or human == WHITE):
    human = input("Invalid entry. Enter B or W")

AI = get_opponent(human)
board = initial_board()

#GAME LOOP
while True:
    valmoves = valid_moves(board, player)
    if invcount == 2:
        print(print_board(board))
        print("GAME OVER")
        break
    if len(valmoves) == 0:
        invcount += 1
    elif player == human:
        print("Valid moves: ", valmoves, "\n")
        coord = input("Make a move: \n")
        while(int(coord) not in valmoves):
            coord = input("Invalid move, try again: \n")
        move = int(coord)
        board = make_move(board, human, move)
        print("Move made:", move)
        invcount = 0
    elif player == AI:
        move = alphabeta(board, AI, alpha_0, beta_0, dep, "maxi", AI)[0]
        board = make_move(board, AI, move)
        print("AI move made:", move)
        invcount = 0
    print(print_board(board))
    player = get_opponent(player)

winner = WHITE if board_score(board, WHITE) > 0 else BLACK
print(print_board(board))
print("You played as", human + ", AI played as " + AI)

if board_score(board, human) == 0:
    print("tie")
else:
    print(winner + " wins!")
