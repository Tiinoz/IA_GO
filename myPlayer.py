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
import copy

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

    def minimaxAB(self, b, white):
        bestValue = 0
        bestMove = None
        print("before J")

        for i in b.generate_legal_moves():
            boardCopy = copy.deepcopy(b)
            boardCopy.push(i)
            cpt = 0
            print("before J")
            for j in range (0, 10):
                self.weakDeroulementRandom(boardCopy, self._mycolor, cpt)
            print("after J")
            cpt = cpt / 2
            if bestValue < cpt:
                bestValue = cpt
                bestMove = i
            boardCopy.pop()       
        return bestMove



        # ******************
    def weakRandomMove(self,b):
        '''Renvoie un mouvement au hasard sur la liste des mouvements possibles mais attention, dans ce cas
        weak_legal_moves() peut renvoyer des coups qui entrainent des super ko. Si on prend un coup au hasard
        il y a donc un risque qu'il ne soit pas légal. Du coup, il faudra surveiller si push() nous renvoie
        bien True et sinon, défaire immédiatement le coup par un pop() et essayer un autre coup.'''
        return choice(b.weak_legal_moves())


    def weakDeroulementRandom(self, b, color, heuristic):
        '''Déroulement d'une partie de go au hasard des coups possibles. Cela va donner presque exclusivement
        des parties très longues. Cela illustre cependant comment on peut jouer avec la librairie
        très simplement en utilisant les coups weak_legal_moves().
        
        Ce petit exemple montre comment utiliser weak_legal_moves() plutot que legal_moves(). Vous y gagnerez en efficacité.'''

        # print("----------")
        # b.prettyPrint()
        
        if b.is_game_over():
            print("Resultat : ", b.result())
            black, white = b.compute_score()
            if color == b._BLACK:
                heuristic += black
            else:
                heuristic += white
            return

        while True:
            # push peut nous renvoyer faux si le coup demandé n'est pas valide à cause d'un superKo. Dans ce cas il faut
            # faire un pop() avant de retenter un nouveau coup 
            valid = b.push(self.weakRandomMove(b))
            if valid:
                break
            b.pop()
        self.weakDeroulementRandom(b,color,heuristic)
        b.pop()

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
            # value = 0
            # for i in range (0,10000):
            #     testCopy = copy.deepcopy(self._board)
            #     self.weakDeroulementRandom(testCopy, self._mycolor, value)
            # value = value / 10000
            # print(value)
            if self._mycolor == self._board._BLACK:
                move = self.minimaxAB(self._board, False)
            else: 
                move = self.minimaxAB(self._board, True)
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



