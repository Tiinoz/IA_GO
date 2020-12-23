# -*- coding: utf-8 -*-

import time
import chess
from random import randint, choice


COLORS = [WHITE, BLACK] = [True, False] #From pychess

def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.generate_legal_moves()])

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

def allGameAtDepth(b, depth=3):
    #print("\n----------\n")
    #print(b)
    if depth > 0 and not b.is_game_over():
        for m in b.generate_legal_moves():
            b.push(m)
            allGameAtDepth(b, depth-1)
            b.pop()
    return

def getBoardScore(b):
    score = 0
    pieces = b.piece_map()
    for k in pieces :
        if pieces[k].symbol() == 'k' :
            score -= 200
        elif pieces[k].symbol() == 'K' :
            score += 200
        elif pieces[k].symbol() == 'q' :
            score -= 9
        elif pieces[k].symbol() == 'Q' :
            score += 9
        elif pieces[k].symbol() == 'r' :
            score -= 5
        elif pieces[k].symbol() == 'R' :
            score += 5
        elif pieces[k].symbol() == 'b' or pieces[k].symbol() == 'n' :
            score -= 3
        elif pieces[k].symbol() == 'B' or pieces[k].symbol() == 'N':
            score += 3
        elif pieces[k].symbol() == 'p' :
            score -= 1
        elif pieces[k].symbol() == 'P' :
            score += 1
    return score

def Maxmin(b, depth):
    if b.is_game_over():
        res = b.result()
        if res == '1-0':
            return (1000, None)
        elif res == '0-1':
            return (-1000, None)
        else:
            return (0,None)
    if depth == 0:
        return (getBoardScore(b), None)
    best = -1000
    move = []
    for m in b.generate_legal_moves():
        b.push(m)
        mini = Minmax(b, depth - 1)[0]
        b.pop()
        if mini > best:
            best = mini
            move = [m]
        elif mini == best:
            move.append(m)
    return (best, move)

def Minmax(b, depth):
    if b.is_game_over():
        res = b.result()
        if res == '1-0':
            return (1000, None)
        elif res == '0-1':
            return (-1000, None)
        else:
            return (0,None)
    if depth == 0:
        return (getBoardScore(b), None)
    worst = 1000
    move = []
    for m in b.generate_legal_moves():
        b.push(m)
        maxi = Maxmin(b, depth - 1)[0]
        b.pop()
        if maxi < worst:
            worst = maxi
            move = [m]
        elif maxi == worst:
            move.append(m)
    return (worst, move)

def Minimax(b, depth):
    move = None
    if b.turn == WHITE :
        move = Maxmin(b, depth)[1]
    else:
        move = Minmax(b, depth)[1]
    return choice(move)

def MaxValue(b, alpha, beta, depth, limitCPU=None):
    if limitCPU is not None and time.time() > limitCPU :
        raise TimeoutError
    if b.is_game_over():
        res = b.result()
        if res == '1-0':
            return (1000, None)
        elif res == '0-1':
            return (-1000, None)
        else:
            return (0,None)
    if depth == 0:
        return (getBoardScore(b), None)
    move = []
    for m in b.generate_legal_moves():
        b.push(m)
        try:
            mini = MinValue(b, alpha, beta, depth - 1, limitCPU)[0]
        except TimeoutError:
            b.pop()
            raise TimeoutError
        b.pop()
        if mini > alpha:
            alpha = mini
            move = [m]
        elif mini == alpha:
            move.append(m)
        if alpha >= beta :
            return (beta, move)
    return (alpha, move)

def MinValue(b, alpha, beta, depth, limitCPU):
    if limitCPU is not None and time.time() > limitCPU :
        raise TimeoutError
    if b.is_game_over():
        res = b.result()
        if res == '1-0':
            return (1000, None)
        elif res == '0-1':
            return (-1000, None)
        else:
            return (0,None)
    if depth == 0:
        return (getBoardScore(b), None)
    move = []
    for m in b.generate_legal_moves():
        b.push(m)
        try:
            maxi = MaxValue(b, alpha, beta, depth - 1, limitCPU)[0]
        except TimeoutError:
            b.pop()
            raise TimeoutError
        b.pop()
        if maxi < beta:
            beta = maxi
            move = [m]
        elif maxi == beta:
            move.append(m)
        if alpha >= beta :
            return (alpha, move)
    return (beta, move)

def AlphaBeta(b, depth, limiteCPU=None):
    alpha = -1000
    beta = 1000
    move = None
    if b.turn == WHITE :
        move = MaxValue(b, alpha, beta, depth, limiteCPU)[1]
    else:
        move = MinValue(b, alpha, beta, depth, limiteCPU)[1]
    return choice(move)

def IDAlphaBeta(b ,depth):
    maxCPU = time.time() + 10 # 10 sec de calcul
    thisDepth = depth
    res = None
    t = 0
    while True:
        try:
            t = time.time()
            res = AlphaBeta(b, thisDepth, maxCPU)
            t = time.time() - t
        except TimeoutError:
            return res
        thisDepth +=1;

def Minimax3VRandom(b):
    print(b)
    if not b.is_game_over():
        if b.turn == WHITE :
            print("\n->white")
            print("\n ------------- \n")
            b.push(Minimax(b, 3))
            Minimax3VRandom(b)
            b.pop()
        else:
            print("\n->black")
            print("\n ------------- \n")
            b.push(randomMove(b))
            Minimax3VRandom(b)
            b.pop()
    else:
        print("\nRésultat : ", b.result())
    return

def Minimax3VMinimax1(b):
    print(b)
    if not b.is_game_over():
        if b.turn == WHITE :
            print("\n-> white")
            print("\n ------------- \n")
            b.push(Minimax(b, 3))
            Minimax3VMinimax1(b)
            b.pop()
        else:
            print("\n-> black")        
            print("\n ------------- \n")
            b.push(Minimax(b, 1))
            Minimax3VMinimax1(b)
            b.pop()
    else:
        print("\nRésultat : ", b.result())
    return

def Minimax3VAlphaBeta3(b):
    print(b)
    if not b.is_game_over():
        if b.turn == WHITE :
            print("\n-> white")
            print("\n ------------- \n")
            b.push(Minimax(b, 3))
            Minimax3VAlphaBeta3(b)
            b.pop()
        else:
            print("\n-> black")        
            print("\n ------------- \n")
            b.push(IDAlphaBeta(b, 4))
            Minimax3VAlphaBeta3(b)
            b.pop()
    else:
        print("\nRésultat : ", b.result())
    return



board = chess.Board()
t1 = time.time()
#allGameAtDepth(board, 5) #5 -> tps < 1min
Minimax3VAlphaBeta3(board)

print("tps = ",time.time() - t1)
