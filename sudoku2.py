#!/usr/bin/env python
import os,sys,subprocess
from sys import exit,argv
from os import popen,system
sys.path.append("/mnt/diskc/1/dauriac/lib")
def w(x):sys.stdout.writelines(x)
from collections import defaultdict

import jc2 as jc
import re

Lfun = lambda k:k//9
Cfun = lambda k:k%9
Sfun = lambda k:((k//9)//3)*3 + (k%9)//3

class sudoku:
    """
    A partir des trois fonctions qui determinent les 3 types de sous-ensembles
    on construit les sous-ensembles eux-memes, ainsi que la liste qui explicite
    pour chaque case tous les sites appartenant a un des 3 types de sous-ensemble.
    """
    nCallmethod1 = 0
    nCallmethod1Single = 0
    nCallmethod2 = 0
    nCallmethod2Single = 0
    
    def __init__(self):
        self.T = [list(range(1,10))]*81
        # T contient la liste des possibilites  
        ssEnsl = [[],[],[],[],[],[],[],[],[]]
        ssEnsc = [[],[],[],[],[],[],[],[],[]]
        ssEnss = [[],[],[],[],[],[],[],[],[]]
        self.coMember = [[] for _ in range(81)]
        for k in range(81):
            l = Lfun(k)
            c = Cfun(k)
            s = Sfun(k)
            # print(f"{k,l,c,s=}")
            ssEnsl[l].append(k)
            ssEnsc[c].append(k)
            ssEnss[s].append(k)
        for k in range(81):
            l = Lfun(k)
            c = Cfun(k)
            s = Sfun(k)
            self.coMember[k]+=list(set(ssEnsl[l]+ssEnsc[c]+ssEnss[s]))
            self.coMember[k].remove(k)
        self.ssEns = ssEnsl + ssEnsc + ssEnss

    def set(self,inp):
        """
        'x' pour case inconnue,
        de # a fin de ligne = commentaire
        fin de ligne ignorees
        il doit rester 81 digits
        """
        inp = inp.replace(' ','')
        inp = inp.replace('x','0')
        inp = re.sub(r'#.*$', '', inp, flags=re.MULTILINE)
        inp = inp.replace('\n','')
        # print(inp)
        if not bool(re.fullmatch(r'\d{81}', inp)):
            print(f"{inp} non valide")
            return;
        for i,c in enumerate(inp):
            if c!='0':
                self.T[i] = [int(c)]

    def method1(self):
        self.nCallmethod1 += 1
        acc = 0
        # print(f"Entering method1 {self.nCallmethod1=}")
        while True :
            ans = self.method1Single()
            acc += ans
            print(f"method1 : {ans=}")
            if not ans:
                break
        return acc
        
    def method1Single(self):
        """ pour chaque case teste les valeurs possibles """
        self.nCallmethod1Single += 1
        # print(f"Entering method1Single {self.nCallmethod1Single=}")
        nbChgt = 0
        encore = False
        for k in range(81):
            if len(self.T[k])==1:
                continue
            aux = list(set(map(lambda x:self.T[x][0] if len(self.T[x])==1 else 0,self.coMember[k])))
            if aux.count(0)!=0:
                aux.remove(0)
            if len(aux)==8:
                v = set(range(1,10,1)).symmetric_difference(aux).pop()
                # print(f"OK pour {v=} en {k=}")
                self.T[k] = [v]
                nbChgt += 1
        # print(f"Leaving method1Single {nbChgt=}")
        return nbChgt
    
    def method2(self):
        self.nCallmethod2 += 1
        acc = 0
        # print(f"Entering method2 {self.nCallmethod2=}")
        while True :
            ans = self.method2Single()
            acc += ans
            # print(f"method2 : {ans=}")
            if not ans:
                break
        return acc
    
    def method2Single(self):
        """ pour chaque sous-ensemble teste les valeurs possibles """
        # print(f"Entering method2Single {self.nCallmethod2Single=}")
        nbChgt = 0
        for k,ss in enumerate(self.ssEns):
            # print(f"{k=} {ss=}")
            aux = list(map(lambda k: self.T[k][0] if len(self.T[k])==1 else 0,ss))
            bux = list(set(aux))
            if bux.count(0)!=0:
                bux.remove(0)
            if len(bux)==8 :
                s = set(range(1,10,1)).symmetric_difference(bux)
                if len(s)!=1:
                    exit(1)
                v = s.pop()
                # print(f"method2Single ok {k=} {aux=} {bux=} {v=}")
                # on doit mettre v
                for i in range(9):
                    if aux[i]==0: # ie une plage
                        # print(f"{v} en  {ss[i]}")
                        self.T[ss[i]]=[v]
                        nbChgt += 1
        # print(f"leaving method2Single")
        return nbChgt

    def methodSingle(self):
        """ pour chaque case teste les valeurs possibles """
        self.nCallmethod1Single += 1
        # print(f"Entering method1Single {self.nCallmethod1Single=}")
        Chgt = []
        encore = False
        for k in range(81):
            if len(self.T[k])==1:
                continue
            aux = list(set(map(lambda x:self.T[x][0] if len(self.T[x])==1 else 0,self.coMember[k])))
            if aux.count(0)!=0:
                aux.remove(0)
            possible = list(set(range(1,10,1)).symmetric_difference(set(aux)))
            self.T[k] = possible
            Chgt.append(k)
        return Chgt

    def out(self):
        aux = list(map(lambda v:chr(v[0]+ord('0')) if len(v)==1 else chr(len(v)+ord('a')-2),my.T))
        for k,v in enumerate(aux):
            print("%c"%v,end=" " if k%3==2 else "")
            if k%9==8:
                print('')
            if k==26 or k==53:
                print("")
        print('')

    def score(self):
        """
        retourne le nombre de cas a possible
        """
        v = 1
        for k in range(81):
            v *= len(self.T[k])
        return v

    def check(self):
        """
        all the entry with more than one possibilities are disregarded
        return the validity of the data
        """
        for k,ss in enumerate(self.ssEns): # for all subsets
            aux = list(map(lambda k: self.T[k][0] if len(self.T[k])==1 else 0,ss))
            aux = list(filter(lambda k:k!=0,aux))
            if len(aux) != len(list(set(aux))):
                return False
        return True

if __name__ == "__main__":
    # facile :
    example1 = "830007240640020509700009000000053608900201007405970000000700005506030021098100034"
    # diabolique :
    example2 = "950300401000500002040080007009000050006408200070000300700060020800007000605004093"
    # facile :
    example3 = "300024007000030600970651002600090080250000079080070005500743018008010000700560004"
    # difficile :
    example4 = "508004000600070009000030060015700000920080041000001970060010000700020008000900302"
    # demoniaque :
    example5 = "900417005003086000000900040270000403430000098601000057050001000000790500700528006"
    examples = [example1,example2,example3,example4,example5]
    while False:
        k = input("numero de l'example ? ")
        my = sudoku()
        my.set(examples[int(k)])
        for cpt in range(10):
            my.methodSingle()
            my.out()
            score = my.score()
            print(f"{cpt=} {score=}\n---------------------------------------------\n")
            if score==1:
                break
        print("#########################################################")



