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
import sys

MAX = 10000000
MIN =-10000000

class myPlayer(PlayerInterface):
    ''' Example of a random player for the go. The only tricky part is to be able to handle
    the internal representation of moves given by legal_moves() and used by push() and 
    to translate them to the GO-move strings "A1", ..., "J8", "PASS". Easy!

    '''

    def __init__(self):
        self._board = Goban.Board()
        self._mycolor = None

        self._launchTime = 0
        self._time = 0
        self._maxTime = 300

        self._1Move = True
        self._2Move = True
        self._3Move = True
        self._4Move = True
        self._1openerMove = ["C7","C6","D7"]
        self._2openerMove = ["G7","G6","F7"]
        self._3openerMove = ["C3","C4","D3"]
        self._4openerMove = ["G3","G4","F3"]      
        # Liste des coins  
        self._corners = ["A1","J1","A9","J9"]
        self._cornersMove = [0,8,72,80]
        # Liste des positions des bordures
        self._outlines = ["A1","A2","A3","A4","A5","A6","A7","A8","A9","B1","C1","D1","E1","F1","G1","H1","J1","B9","C9","D9","E9","F9","H9","G9","J9","J2","J3","J4","J5","J6","J7","J8"]
        self._nbmoves = 0
        self._coeff = 3
        
    # Si le jeu est terminé, on met la valeur de l'heuristique ou gagnant
    def scoreIsOver(self):
        board_value = 0
        if self._board.is_game_over():
            if self._board.result() == "1-0":
                if self._mycolor == self._board._WHITE:
                    board_value = 500
                else:
                    board_value = -500
            elif self._board.result() == "0-1":
                if self._mycolor == self._board._BLACK:
                    board_value = 500
                else:
                    board_value = -500
            else:
                board_value = 0
            return board_value

    #Petite heuristique qui compte le nombre de pièce et de territoire
    def getBoardScore(self):
        black, white = self._board.compute_score()
        if self._mycolor == self._board._WHITE:
            return white
        elif self._mycolor == self._board._BLACK:
            return black

    # Permet de selectionner des moves qui ont des voisins parmis la liste des meilleurs possibilités renvoyées par AlphaBeta
    # On prend des positions qui ont des voisins de notre couleur afin qu'il est plus d'impact
    def choiceGo(self, moves):
        move = -1
        max = 0
        list = []
        for m in moves:
            nb_v = 0
            for v in self._board._get_neighbors(m):
                if self._mycolor == self._board._board[v]:
                    list.append(m)
        if len(list) > 0:
            move = random.choice(list)
        if move == -1:
            move = random.choice(moves)
        return move

    def MaxValue(self, alpha, beta, depth = 3):
        if self._board.is_game_over():
            return self.scoreIsOver()
        if depth == 0:
            return self.getBoardScore()
        moves = self._board.generate_legal_moves()
        random.shuffle(moves)
        for m in moves:
            self._time = time.time() - self._launchTime 
            if(self._maxTime - self._time <= 1):
                print("No more time")
                break
            mStr = self._board.move_to_str(m)
            # Si le move correspond a un coin on le passe
            if (mStr in self._corners and self._cornersMove != self._board.generate_legal_moves()):
                continue
            # On a décidé d'éviter de jouer les bords pendant les 10 premiers cours
            if(self._nbmoves < 10 and mStr in self._outlines):
                continue
            self._board.push(m)
            v = self.MinValue(alpha,beta, depth - 1)
            self._board.pop()
            if v > alpha:
                alpha = v
            if alpha >= beta:
                return beta
        return alpha
    
    def MinValue(self, alpha, beta, depth = 3):
        if self._board.is_game_over():
            return self.scoreIsOver()
        if depth == 0:
            return self.getBoardScore()
        moves = self._board.generate_legal_moves()
        random.shuffle(moves)
        for m in moves:
            self._time = time.time() - self._launchTime 
            if(self._maxTime - self._time <= 1):
                print("No more time")
                break
            mStr = self._board.move_to_str(m)
            # Si le move correspond a un coin on le passe
            if (mStr in self._corners and self._cornersMove != self._board.generate_legal_moves()):
                continue
            # On a décidé d'éviter de jouer les bords pendant les 10 premiers cours
            if(self._nbmoves < 10 and mStr in self._outlines):
                continue
            self._board.push(m)
            v = self.MaxValue(alpha,beta, depth - 1)
            self._board.pop()
            if v < beta:
                beta = v
            if alpha >= beta:
                return alpha
        return beta

    def AlphaBeta(self, depth = 3):
        alpha = MIN
        coup = []
        moves = self._board.generate_legal_moves()
        random.shuffle(moves)
        for m in moves:
            self._time = time.time() - self._launchTime 
            if(self._maxTime - self._time <= 1):
                print("No more time")
                break
            mStr = self._board.move_to_str(m)
            # Si le move correspond a un coin on le passe
            if (mStr in self._corners and self._cornersMove != self._board.generate_legal_moves()):
                continue
            # On a décidé d'éviter de jouer les bords pendant les 10 premiers cours
            if(self._nbmoves < 10 and mStr in self._outlines):
                continue
            self._board.push(m)
            v = self.MinValue(alpha, MAX, depth - 1)
            if v == alpha:
                coup.append(m)
            elif v > alpha or coup == None:
                alpha = v
                coup = [m]
            self._board.pop()
        return coup

    # ******************

    def getPlayerName(self):
        return "LaHonteDeLaPromo"

    def getPlayerMove(self):
        # Permet depuis combien de temps notre joueur joue
        self._time = time.time() - self._launchTime 
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return "PASS" 
        moves = self._board.legal_moves() # Dont use weak_legal_moves() here!
        # Si il reste peu de possibilités on augmente la depth pour avoir quelque chose de plus précis
        if len(moves) < 11:
            self._coeff = 6
        else:
            self.coeff = 3
        # Si 1 move on le donne direct
        if len(moves) == 1:
            print("Only one move possibility\n")
            move = moves[0]
        # Les 4 premiers moves sont imposés
        elif self._1Move:
            print("First Move")
            move = self._board.str_to_move(choice(self._1openerMove))
            while(move not in moves):
                move = self._board.str_to_move(choice(self._1openerMove))
            self._1Move = False
        elif self._2Move:
            print("Second Move")
            move = self._board.str_to_move(choice(self._2openerMove))
            while(move not in moves):
                move = self._board.str_to_move(choice(self._2openerMove))
            self._2Move = False
        elif self._3Move:
            print("Third Move")
            move = self._board.str_to_move(choice(self._3openerMove))
            while(move not in moves):
                move = self._board.str_to_move(choice(self._3openerMove))
            self._3Move = False
        elif self._4Move:
            print("Fourth Move")
            move = self._board.str_to_move(choice(self._4openerMove))
            while(move not in moves):
                move = self._board.str_to_move(choice(self._4openerMove))
            self._4Move = False
        # Check si on est a moins de 1 secondes des 3 minutes, si c'est le cas on joue en random pour pas dépasser 3minutes
        elif(self._maxTime - self._time <= 1):
            move = choice(moves) 
        else: 
            print(self._time)
            print("AlphaBeta Move")
            moves = self.AlphaBeta(self._coeff)
            if(len(moves)>0):
                move = self.choiceGo(moves)
            # Si pas de move -1 pas gérer dans le choiceGo()
            else:
                move = random.choice(moves)
        self._board.push(move)
        self._nbmoves += 1;

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
        # Initialisation du temps au moment de création de la partie
        self._launchTime = time.time()

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")



