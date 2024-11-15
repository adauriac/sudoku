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
            print(f"{k,l,c,s=}")
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
        print(inp)
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

    def out(self):
        aux = list(map(lambda v:chr(v[0]+ord('0')) if len(v)==1 else 'x',my.T))
        for k,v in enumerate(aux):
            print("%c"%v,end=" " if k%3==2 else "")
            if k%9==8:
                print('')
            if k==26 or k==53:
                print("")
            
if __name__ == "__main__":
    my = sudoku()
    ex = """
    x718x6xx2
    x36x1xx8x
    8xx7x96xx
    7x5x4xxxx
    xxx2x5xxx
    xxxx9x4x8
    xx89x4xx1
    x9xx6x84x
    5xx3x829x
    """
    ex2 = """
    x71 8x6 xx2 
    x36 x12 x8x 
    8x2 7x9 6xx 

    7x5 x43 xx9 
    xxx 285 xxx 
    xx3 x97 4x8 
    
    xx8 9x4 xx1 
    x97 561 843 
    514 378 296 
    """
    my.set(ex2)
    my.out()
    exit(123)
    while True:
        k1 = my.method1()
        k2 = my.method2()
        if k1==0 and k2==0:
            break
    my.out()
