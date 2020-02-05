import copy
import random
import operator

EMPTY, BLACK, WHITE, OUTER = '.', 'B', 'W', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

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

def eval_board(board):
    #plus 1 for black, minus 1 for white
    score = 0
    for s in squares():
        if board[s] == BLACK:
            score += 1
        elif board[s] == WHITE:
            score -= 1
    return score

# def minimax(board, player, depth):
#     #maximizes worst case scenarios for black for input depth
#     moves = valid_moves(board, player)
#     #print("valid moves for", player, moves)
#
#     if depth == 0 or len(moves) == 0:
#         return (0, eval_board(board))
#     bestmove = moves[0]
#     copyboard = copy.copy(board)
#     if player == BLACK:
#         bestval = -64
#         for move in moves:
#             temp_board = make_move(copyboard, player, move)
#             val = minimax(temp_board, get_opponent(player), depth-1)[1]
#             if val > bestval:
#                 bestval = val
#                 bestmove = move
#     elif player == WHITE:
#         bestval = 64
#         for move in moves:
#             temp_board = make_move(copyboard, player, move)
#             val = minimax(temp_board, get_opponent(player), depth-1)[1]
#             if val < bestval:
#                 bestval = val
#                 bestmove = move
#     return (bestmove, bestval)

def alphabeta(board, player, alpha, beta, depth):
    moves = valid_moves(board, player)
    if depth == 0 or len(moves) == 0:
        return (0, eval_board(board))
    m = moves[0]

    if player == BLACK:
        val = -64
        for move in moves:
            if alpha > beta:
                break
            next_board = make_move(copy.copy(board), player, move)
            val = max(val, alphabeta(next_board, get_opponent(player), alpha, beta, depth-1)[1])
            if val > alpha:
                alpha = val
                m = move

        return m, alpha
    else:
        val = 64
        for move in moves:
            if alpha > beta:
                break
            next_board = make_move(copy.copy(board), player, move)
            val = min(val, alphabeta(next_board, get_opponent(player), alpha, beta, depth-1)[1])
            if val < beta:
                beta = val
                m = move

        return m, beta

#GAME LOOP
whitescore = 0
blackscore = 0
alpha_0 = -64
beta_0 = 64
dep = 3
for i in range(100):
    board = initial_board()
    player = BLACK
    while True:
        valmoves = valid_moves(board, player)
        if len(valmoves) == 0:
            print(print_board(board))
            print("GAME OVER")
            break
        elif player == BLACK:
            #print(print_board(board))
            cpu_move = alphabeta(board, player, alpha_0, beta_0, dep)[0]
            board = make_move(board, player, cpu_move)
            player = WHITE
        elif player == WHITE:
            randmove = random.choice(valmoves)
            board = make_move(board, player, randmove)
            player = BLACK
    if eval_board(board) < 0:
        whitescore += 1
    elif eval_board(board) > 0:
        blackscore += 1

print("white:", whitescore, "black:", blackscore)
