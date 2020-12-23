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
        self._firstCoup = True
        self._openerCoup = ["C7","G7","C3","G3"]
        


    # ALPHA BETA TEST

    def heuristic(self, b):
        board_value = 0
        black, white = b.compute_score();
        if b.is_game_over():  # y'a moy d'optimiser ça en recuperant la profondeur ou pas
            if b.result() == "1-0":
                board_value += white
            elif b.result() == "0-1":
                board_value -= black
            else:
                board_value = 0
            return board_value

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
        elif self._mycolor == self._board._BLACK and self._firstCoup:
            print("First Move")
            move = self._board.str_to_move(choice(self._openerCoup))
            while(move not in moves):
                move = self._board.str_to_move(choice(self._openerCoup))
            self._firstCoup = False
        else:
            print("AlphaBeta")
            if self._mycolor == self._board._BLACK:
                move = self.minimaxAB(self._board, 3, False)
            else: 
                move = self.minimaxAB(self._board, 3, True)

            # move = choice(moves) 
        self._board.push(move)
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



