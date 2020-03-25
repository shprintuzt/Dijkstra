# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 22:28:24 2019

@author: T-GOTOH
"""
import numpy as np

class Grid():
    def __init__(self, row, col, width, height, mergin, fix=False):#, n_num):
        self.row = row
        self.col = col
        self.n = row * col # number of nodes
        n = self.n
        self.flug = [ False for _ in range(n) ]
        self.flug_e = [ [ 0 for _ in range(n) ] for _ in range(n) ]
        self.dist = [ -1 for _ in range(n) ]
        self.path = [ [] for _ in range(n) ]
        self.dist[0] = 0
        
        self.width = width
        self.height = height
        self.mergin = mergin
        
        x = [ i*width+width//2 for i in range(col) ]
        y = [ i*height+mergin+height//2 for i in range(row) ]
        self.L = [ [j, i] for i in y for j in x ] # location (coordination) of nodes
        
        self.E = [[0 for _ in range(self.n)] for _ in range(self.n)] # edges
        
        i_j = [(i, j) for i in range(self.n) for j in range(self.n)]
        for i, j in i_j:
            if (i % col != col-1 and j == i+1) or (i // col != row-1 and j == i+col): # grid
                dist = np.random.randint(1, 21)
                self.E[i][j], self.E[j][i] = dist, dist
        if fix == True:
            E1 = [[0 for _ in range(self.n)] for _ in range(self.n)]
            E1[0][1], E1[0][7], E1[1][2], E1[1][8], E1[2][3], E1[2][9] = 6, 9, 10, 15, 1, 15
            E1[3][4], E1[3][10], E1[4][5], E1[4][11], E1[5][6], E1[5][12], E1[6][13] = 13, 2, 9, 20, 20, 2, 1
            E1[7][8], E1[7][14], E1[8][9], E1[8][15], E1[9][10], E1[9][16] = 10, 20, 20, 11, 9, 10
            E1[10][11], E1[10][17], E1[11][12], E1[11][18], E1[12][13], E1[12][19], E1[13][20] = 9, 10, 13, 4, 5, 12, 2
            E1[14][15], E1[14][21], E1[15][16], E1[15][22], E1[16][17], E1[16][23] = 9, 17, 8, 6, 2, 10
            E1[17][18], E1[17][24], E1[18][19], E1[18][25], E1[19][20], E1[19][26], E1[20][27] = 18, 11, 10, 12, 5, 15, 14
            E1[21][22], E1[21][28], E1[22][23], E1[22][29], E1[23][24], E1[23][30] = 6, 15, 4, 5, 18, 13
            E1[24][25], E1[24][31], E1[25][26], E1[25][32], E1[26][27], E1[26][33], E1[27][34] = 9, 20, 7, 8, 4, 5, 3
            E1[28][29], E1[28][35], E1[29][30], E1[29][36], E1[30][31], E1[30][37] = 12, 9, 4, 11, 20, 5
            E1[31][32], E1[31][38], E1[32][33], E1[32][39], E1[33][34], E1[33][40], E1[34][41] = 18, 9, 16, 6, 20, 2, 14
            E1[35][36], E1[36][37], E1[37][38], E1[38][39], E1[39][40], E1[40][41] = 20, 9, 6, 11, 13, 9
            for i in range(self.n):
                for j in range(self.n):
                    if i < j:
                        self.E[i][j] = E1[i][j]
                    else:
                        self.E[i][j] = E1[j][i]

    def next_phase(self):
        n = self.n
        cands = [(m, self.dist[m]) for m in range(n) if self.dist[m] != -1 and self.flug[m] == False]
        cand = sorted(cands, key=lambda x: x[1])[0][0]
        print(cand)
        nei = [(j, self.E[cand][j]) for j in range(n) if self.E[cand][j] > 0]
        for ne, d in nei:
            if self.dist[ne] == -1:
                self.dist[ne] = self.dist[cand]+d
                self.path[ne] = self.path[cand]+[cand]
            elif self.dist[cand]+d < self.dist[ne]:
                self.dist[ne] = self.dist[cand]+d
                self.path[ne] = self.path[cand]+[cand]
        
        self.flug[cand] = True
        if cand != 0:
            self.flug_e[cand][self.path[cand][-1]] = 1
            self.flug_e[self.path[cand][-1]][cand] = 2
