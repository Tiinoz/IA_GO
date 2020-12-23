import random
import time
from math import inf
import chess


def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return random.choice([m for m in b.generate_legal_moves()])


def deroulementRandom(b):
    '''Déroulement d'une partie d'échecs au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues et sans gagnant. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement.'''
    print("----------")
    print(b)
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    b.push(randomMove(b))
    deroulementRandom(b)
    b.pop()


def heuristic(b):
    board_value = 0
    if b.is_game_over():  # y'a moy d'optimiser ça en recuperant la profondeur ou pas
        if b.result() == "1-0":
            board_value += 500
        if b.result() == "0-1":
            board_value -= 500
        # else:                 #j'ai commencé à réfléchir à un truc pour ponderer les égalitées en fonction du joueur à qui c'est le tour
        #     if b.turn() == 1:
        #         board_value = 500
        #     else:
        #         board_value = -500
        return board_value

    value = {'K': 200, 'Q': 9, 'B': 3, 'N': 3, 'R': 5, 'P': 1,
             'k': -200, 'q': -9, 'b': -3, 'n': -3, 'r': -5, 'p': -1
             }

    pieceMap = b.piece_map()
    for index in pieceMap:

        board_value += value[pieceMap[index].symbol()]

        if pieceMap[index].symbol() == 'P':
            board_value += 0.1 * (index // 8)
        elif pieceMap[index] == 'p':
            board_value -= 0.1 * (7 - index // 8)
    # BEAUCOUP TROP LENT DE CALCULER LA MOBILITE COMME CA
    # mobility = len([m for m in b.generate_legal_moves()])
    # b.push(chess.Move.null())
    # mobility -= len([m for m in b.generate_legal_moves()])
    # b.pop()

    return board_value  # + mobility


def minimax(b, depth, white):
    max_eval = -inf
    min_eval = inf
    best_move = []

    for i in b.generate_legal_moves():
        b.push(i)
        eval = minimax_rec(b, depth - 1, not white)
        if white and max_eval <= eval:
            if max_eval == eval:
                best_move.append(i)
            else:
                best_move = [i]
                max_eval = eval
        elif not white and min_eval >= eval:
            if min_eval == eval:
                best_move.append(i)
            else:
                best_move = [i]
                min_eval = eval
        b.pop()
    return random.choice(best_move)


def minimax_rec(b, depth, white):
    if depth == 0 or b.is_game_over():
        return heuristic(b)

    to_ret = None
    for i in b.generate_legal_moves():
        b.push(i)
        eval = minimax_rec(b, depth - 1, not white)
        if to_ret is None:
            to_ret = eval
        elif white:
            to_ret = max(to_ret, eval)
        else:
            to_ret = min(to_ret, eval)
        b.pop()
    return to_ret


def minimaxAB(b, depth, white):
    max_eval = -inf
    min_eval = inf
    alpha = -inf
    beta = inf
    best_move = []

    for i in b.generate_legal_moves():
        b.push(i)
        eval = minimax_recAB(b, depth - 1, not white, alpha, beta)
        eval -= 0.00000001 * (100 - depth)
        b.pop()
        if white and max_eval <= eval:
            if max_eval == eval:
                best_move.append(i)
            else:
                best_move = [i]
                max_eval = eval
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        elif not white and min_eval >= eval:
            if min_eval == eval:
                best_move.append(i)
            else:
                best_move = [i]
                min_eval = eval
            beta = min(beta, eval)
            if alpha >= beta:
                break
    return random.choice(best_move)


def minimax_recAB(b, depth, white, alpha, beta):
    if depth == 0 or b.is_game_over():
        return heuristic(b)

    to_ret = None
    for i in b.generate_legal_moves():
        b.push(i)
        eval = minimax_recAB(b, depth - 1, not white, alpha, beta)
        eval -= 0.00000001 * (100 - depth)  # valeur un peu magique pour faire varier le poids des
        b.pop()
        if to_ret is None:
            to_ret = eval
        if white:
            to_ret = max(to_ret, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        else:
            to_ret = min(to_ret, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break

    return to_ret


# -------------------------------------------------------------------TESTS
# -----------match minimax or minimaxAB or random or humain(pas de partie graphique ou interactive, selection des coups en uci)

board = chess.Board()
start_game = time.time()
print(board)
while not board.is_game_over():
    print("White to move:")
    start = time.time()
    # partie joueur humain
    # move = None
    # move = input("Votre tour: ")
    # while chess.Move.from_uci(move) not in board.generate_legal_moves():
    #     move = input("Votre tour: ")
    #
    # board.push(chess.Move.from_uci(move))
    # partie joueur humain
    board.push(minimaxAB(board, 3, True))
    elapsed_time = time.time() - start
    print(board)
    print("Move played in ", elapsed_time)
    print("-------------------------------")
    if board.is_game_over():
        break
    print("Black to move:")
    start = time.time()
    #black_move = minimaxAB(board, 3, False)
    black_move = randomMove(board)
    board.push(black_move)
    elapsed_time = time.time() - start
    print(board)
    print(black_move.uci(), " played in ", elapsed_time)
    print("-------------------------------")
print("Result: ", board.result())
print("Game duration: ", time.time() - start_game)
# -------------------------------------------------------------------TESTS
# -----------Tournois pour faire des stats de victoires (on fait n fois le même match"
# n = 10
# remaining_games = n
# white_win = 0
# black_win = 0
# tie = 0
#
# start_tournament = time.time()
# while remaining_games > 0:
#     remaining_games -= 1
#     board = chess.Board()
#     while not board.is_game_over():
#         board.push(minimaxAB(board, 2, True))
#         if board.is_game_over():
#             break
#         # board.push(randomMove(board))
#         board.push(minimaxAB(board, 1, False))
#     print(n - remaining_games, " games over")
#     if board.result() == "1-0":
#         white_win += 1
#     elif board.result() == "0-1":
#         black_win += 1
#     else:
#         tie += 1
# print("-------------------------------")
# print("OPEN Lecomte Tournament:")
# print(n, " parties jouées en ", time.time() - start_tournament)
# print("Résultats :")
# print("White :", white_win, "; Black :", black_win, "; Tie :", tie)
# board = chess.Board()

# ------------------------PUZZLE (nan juste deux mat en 2 coups pour tester l'efficacité des ia)

# for i in range(64):
#     board.remove_piece_at(i)
#
# board.set_piece_at(54, chess.Piece(chess.KING, chess.BLACK))
# board.set_piece_at(4, chess.Piece(chess.KING, chess.WHITE))
# board.set_piece_at(2, chess.Piece(chess.ROOK, chess.WHITE))
# board.set_piece_at(1, chess.Piece(chess.ROOK, chess.WHITE))
#
# print(board)
# while not board.is_game_over():
#     board.push(minimaxAB(board, 5, True))
#     print("Move white: ",)
#     print(board)
#     print("-------------------------------")
#     if board.is_game_over():
#         break
#     print("Move black: ",)
#     board.push(randomMove(board))
#     print(board)
#     print("-------------------------------")
#
# for i in range(64):
#     board.remove_piece_at(i)
#
# board.set_piece_at(62, chess.Piece(chess.KING, chess.BLACK))
# board.set_piece_at(14, chess.Piece(chess.KING, chess.WHITE))
# board.set_piece_at(58, chess.Piece(chess.ROOK, chess.BLACK))
# board.set_piece_at(59, chess.Piece(chess.ROOK, chess.BLACK))
#
# print(board)
# board.push(chess.Move.null())
# while not board.is_game_over():
#     print("Move black: ", )
#     board.push(minimaxAB(board, 5, False))
#     print(board)
#     print("-------------------------------")
#     if board.is_game_over():
#         break
#
#     board.push(randomMove(board))
#     print("Move white: ", )
#     print(board)
#     print("-------------------------------")
