import copy
import random

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
    #returns a list of valid coordinates for input player
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
    #flips_pieces of valid input move
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
    #plus 1 for player, -1 for opponent
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
            if alpha > beta:
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
            if alpha > beta:
                break
        return m, val

#GAME LOOP
invcount = 0
whitescore = 0
blackscore = 0
tie = 0
alpha_0 = -64
beta_0 = 64
dep = 3
player = BLACK
for i in range(20):
    board = initial_board()
    while True:
        valmoves = valid_moves(board, player)
        if invcount == 2:
            print(print_board(board))
            print("GAME OVER")
            invcount = 0
            break
        if len(valmoves) == 0:
            invcount += 1
        elif player == BLACK:
            move = alphabeta(board, player, alpha_0, beta_0, dep, "maxi", player)[0]
            #move = random.choice(valmoves)
            board = make_move(board, player, move)
            invcount = 0
        elif player == WHITE:
            #move = alphabeta(board, player, alpha_0, beta_0, dep, "maxi", player)[0]
            move = random.choice(valmoves)
            board = make_move(board, player, move)
            invcount = 0
        player = get_opponent(player)
    if board_score(board, WHITE) > 0:
        whitescore += 1
    elif board_score(board, BLACK) > 0:
        blackscore += 1
    else:
        tie += 1

    print("white:", whitescore, "black:", blackscore, "tie:", tie)
