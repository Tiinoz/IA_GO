# -*- coding: utf-8 -*-
''' This is the file you have to modify for the tournament. Your default AI player must be called by this module, in the
myPlayer class.

Right now, this class contains the copy of the randomPlayer. But you have to change this!
'''

import time
import Goban 
from random import choice
from playerInterface import *
from math import inf
import random

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

    # ALPHA BETA TEST

    def heuristic(self, b):
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

        # value = {'K': 200, 'Q': 9, 'B': 3, 'N': 3, 'R': 5, 'P': 1,
        #         'k': -200, 'q': -9, 'b': -3, 'n': -3, 'r': -5, 'p': -1
        #         }

        # pieceMap = b.piece_map()
        # for index in pieceMap:

        #     board_value += value[pieceMap[index].symbol()]

        #     if pieceMap[index].symbol() == 'P':
        #         board_value += 0.1 * (index // 8)
        #     elif pieceMap[index] == 'p':
        #         board_value -= 0.1 * (7 - index // 8)
        # BEAUCOUP TROP LENT DE CALCULER LA MOBILITE COMME CA
        # mobility = len([m for m in b.generate_legal_moves()])
        # b.push(chess.Move.null())
        # mobility -= len([m for m in b.generate_legal_moves()])
        # b.pop()

        return board_value  # + mobility
    
    def minimax_recAB(self, b, depth, white, alpha, beta):
        if depth == 0 or b.is_game_over():
            return self.heuristic(b)

        to_ret = None
        for i in b.generate_legal_moves():
            b.push(i)
            eval = self.minimax_recAB(b, depth - 1, not white, alpha, beta)
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

    def minimaxAB(self, b, depth, white):
        max_eval = -inf
        min_eval = inf
        alpha = -inf
        beta = inf
        best_move = []

        for i in b.generate_legal_moves():
            b.push(i)
            eval = self.minimax_recAB(b, depth - 1, not white, alpha, beta)
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

    # ******************
    def getPlayerName(self):
        if self._mycolor == self._board._BLACK:
            return "Lucas trop nul au GO"
        else:
            return "EnzoBG le pro du GO"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
        if len(moves) == 1:
            print("Only one move possibility\n")
            move = moves[0]
            self._board.push(move)
        else:
            print("BOARD TEST")
            print(self._board)
            if self._mycolor == self._board._BLACK:
                move = self.minimaxAB(self._board, 3, False)
            else: 
                move = self.minimaxAB(self._board, 3, True)

            # move = choice(moves) 
            self._board.push(move)
        self._nbmoves +=1
        # New here: allows to consider internal representations of moves
        print("I am playing ", self._board.move_to_str(move))
        print("My current board :")
        self._board.prettyPrint()
        # move is an internal representation. To communicate with the interface I need to change if to a string
        return Goban.Board.flat_to_name(move) 

    def playOpponentMove(self, move):
        print("Opponent played ", move) # New here
        # the board needs an internal represetation to push the move.  Not a string
        self._board.push(Goban.Board.name_to_flat(move)) 

    def newGame(self, color):
        self._mycolor = color
        self._opponent = Goban.Board.flip(color)

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



