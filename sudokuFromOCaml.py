#!/usr/bin/env python
"""
pythonisation de https://ocaml.org/exercises
nom de l'exxercise = sudoku
"""
import os,sys,subprocess
from sys import exit,argv
from os import popen,system
sys.path.append("/mnt/diskc/1/dauriac/lib")
def w(x):sys.stdout.writelines(x)
import numpy as np

import jc2 as jc
levelFill = 0
levelTry = 0
def printG(grille):
    for i in range(81):
        print(grille[i],end=" "if i%3==2 else "")
        if i%9==8:
            print()
        if i%27 ==26:
            print()

def next(kpos):
        return (kpos+1)
# k=x*9+y    x=k//9 y=k%9

def fill(b,kpos):
    """
    tente de remplir les entrées non décidées apres kpos
    """
    global levelFill,levelTry    
    levelFill += 1
    print(f"fill({levelFill}): entering {kpos=} ")
    if kpos>80:
        levelFill -= 1
        print("fill: ok tout est rempli") 
        return b
    if b[kpos]>=1: # il y a une valeur legale on analyse l'entrée d'après
        fill(b,next(kpos))
        print(f"fill({levelFill}): retour de fill")
    else:
        # l'entrée n'est pas décidée
        atester = available(b,kpos)
        if atester==[]:
            levelFill -= 1
            print(f"fill({levelFill}): leaving1")
            return None
        else:
            try_values(b,kpos,atester)
            print(f"fill({levelFill}): retour de tryValues")
    levelFill -= 1
    return b
    print(f"fill({levelFill}): leaving2")

def try_values(b,kpos,l):    
    global levelFill,levelTry
    levelTry += 1
    print(f"try_values({levelTry}): entering with  with {l=} {kpos=}")
    levelTry += 1
    if l == []:
        print("try_values: NONNONNONONNON")
        levelTry -= 1
        return
    bux = b[:]
    bux[kpos] = l.pop()
    print(f"try_values({levelTry}): tente {bux[kpos]} en {kpos}")
    res = fill(bux,kpos)
    levelTry -= 1
    print(f"try_values({levelTry}): leaving {len(l)=}")
    return  res if res is not None else try_values(b, pos, rest)

def voisins(kpos):
    """
    retouurne la liste des sites de meme sous-ensemble en pos=(x,y)
    """
    x = kpos//9
    y = kpos%9
    return [x*9+i for i in range(9)] + [i*9+y for i in range(9)] + [((x//3)*3+i)*9 + ((y//3)*3+j) for i in range(3) for j in range(3)]

def available(grille,kpos):
    """
    retourne la liste des valeurs possibles sur la case pos (vide si deja affecte
    """
    global ans,L
    if grille[kpos]!=0:
        return [] # since pos has already a value
    L = voisins(kpos)
    dejaLa =  list(set(map(lambda x:grille[x],L)))
    dejaLa.remove(0)
    ans= list(set(range(1,10)).difference(set(dejaLa)))
    # print(f"available: {kpos=} {ans=}")
    return ans

def go(example):
    global grille
    for i in range(9*9):
        grille[i]= int(example[i])
    printG(grille)
    fill(grille,0)
    printG(grille)
    print("fin")

# ############################################################# #
#                   EN AVANT SIMONE                             #
# ############################################################# #
grille = np.zeros(9*9,dtype=int)
example1 = "030007240640020509700009000000053608900201007405970000000700005506030021098100034"
example2 = "950300401000500002040080007009000050006408200070000300700060020800007000605004093"
example3 = "300024007000030600970651002600090080250000079080070005500743018008010000700560004"
example4 = "508004000600070009000030060015700000920080041000001970060010000700020008000900302"
example5 = "900417005003086000000900040270000403430000098601000057050001000000790500700528006"
exsimple = "958372461367541982241689537489723156136458279572196348713965824894237615625804093"
go(example1)