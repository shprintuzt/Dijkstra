# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 22:48:39 2019

@author: T-GOTOH
"""

from models import Grid
import tkinter as tk

class My_Canvas(tk.Canvas):
    def __init__(self, master, row, col, fix, **kargs):
        super().__init__(master, **kargs)
        self.flag_flush = False
        self.params = (row, col, 900//col, 500//row, 50, 20)
        params = self.params
        self.g = Grid(params[0], params[1], params[2], params[3], params[4], fix=fix)
        self.n_size = params[5]
        self.id = []
        self.drawing()
        
    def reset(self):
        params = self.params
        self.g = Grid(params[0], params[1], params[2], params[3], params[4])
        self.drawing()
        self.flag_flush = False

    def next_phase(self):
        print("Transit to a next state.")
        self.g.next_phase()
        self.drawing()
    
    def start_sim(self):
        if self.flag_flush == False:
            self.flag_flush = True
            print("Start!")
            self.after(0, self.simulation)
    
    def simulation(self):
        if self.flag_flush == True:
            self.g.next_phase()
            self.drawing()
            self.after(100, self.simulation)
    
    def stop_sim(self):
        if self.flag_flush == True:
            print("Stop!")
            self.flag_flush = False
            
    def drawing(self):
        self.delete("all")
        
        g = self.g
        n = g.n
        i_j = [(i, j) for i in range(n) for j in range(n)]
        
        for _ in range(len(self.id)):
            self.delete(self.id[0])
            del self.id[0]
        
        # weight of each edge
        self.id = [ self.create_text((g.L[i][0]+g.L[j][0])/2, g.L[i][1]-20,
                                     fill="white",
                                     font="system 25 bold",
                                     text="{0}".format(g.E[i][j])) for i, j in i_j if g.E[i][j] > 0 and i-j in {1, -1} ]
        self.id += [ self.create_text(g.L[i][0]-20, (g.L[i][1]+g.L[j][1])/2,
                                      fill="white",
                                      font="system 25 bold",
                                      text="{0}".format(g.E[i][j])) for i, j in i_j if g.E[i][j] > 0 and i-j in {g.col, -g.col} and i < j ]
        try:
            # distance table
            cand = sorted([(i, d) for i, d in enumerate(g.dist) if d != -1 and g.flug[i] == False], key=lambda x:x[1])[0][0]
            # even id with false flug
            self.id += [self.create_text(900, 30+(i//2)*25,
                                          fill="#AAAAAA",
                                          font="system 20 bold",
                                          text="{0}".format(i+1)) for i in range(n) if i%2 == 0 and i != cand and g.flug[i] == False]
            # even id with true flug
            self.id += [self.create_text(900, 30+(i//2)*25,
                                          fill="#0000FF",
                                          font="system 20 bold",
                                          text="{0}".format(i+1)) for i in range(n) if i%2 == 0 and i != cand and g.flug[i] == True]
            # distance of even id with false flug
            self.id += [self.create_text(950, 30+(i//2)*25,
                                          fill="#AAAAAA",
                                          font="system 20 bold",
                                          text="{0}".format(d)) for i, d in enumerate(g.dist) if i%2 == 0 and d != -1 and g.flug[i] == False]
            # distance of even id with true flug
            self.id += [self.create_text(950, 30+(i//2)*25,
                                          fill="#0000FF",
                                          font="system 20 bold",
                                          text="{0}".format(d)) for i, d in enumerate(g.dist) if i%2 == 0 and d != -1 and g.flug[i] == True]
            # odd id with false flug
            self.id += [self.create_text(1000, 30+(i//2)*25,
                                          fill="#AAAAAA",
                                          font="system 20 bold",
                                          text="{0}".format(i+1)) for i in range(n) if i%2 == 1 and i != cand and g.flug[i] == False]
            # odd id with true flug
            self.id += [self.create_text(1000, 30+(i//2)*25,
                                          fill="#0000FF",
                                          font="system 20 bold",
                                          text="{0}".format(i+1)) for i in range(n) if i%2 == 1 and i != cand and g.flug[i] == True]
            # distance of even id with false flug
            self.id += [self.create_text(1050, 30+(i//2)*25,
                                          fill="#AAAAAA",
                                          font="system 20 bold",
                                          text="{0}".format(d)) for i, d in enumerate(g.dist) if i%2 == 1 and d != -1 and g.flug[i] == False]
            # distance of even id with true flug
            self.id += [self.create_text(1050, 30+(i//2)*25,
                                          fill="#0000FF",
                                          font="system 20 bold",
                                          text="{0}".format(d)) for i, d in enumerate(g.dist) if i%2 == 1 and d != -1 and g.flug[i] == True]
            # id of min distance
            self.id += [self.create_text(900+(cand%2)*100, 30+(cand//2)*25,
                                            fill="#00FF00",
                                            font="system 20 bold",
                                            text="{0}".format(cand+1))]
            def create_bold_line(x1, y1, x2, y2, fill=None, boldness=1, hori=True):
                if hori == True:
                    for t in range(1-boldness, boldness):
                        self.create_line(x1, y1+t, x2, y2+t, fill=fill)
                else:
                    for t in range(1-boldness, boldness):
                        self.create_line(x1+t, y1, x2+t, y2, fill=fill)
                    
            create_bold_line(875, 16, 875, 20+((n+1)//2)*25, fill="#AAAAAA", boldness=2, hori=False)
            create_bold_line(925, 16, 925, 20+((n+1)//2)*25, fill="#AAAAAA", boldness=1, hori=False)
            create_bold_line(975, 16, 975, 20+((n+1)//2)*25, fill="#AAAAAA", boldness=2, hori=False)
            create_bold_line(1025, 16, 1025, 20+((n+1)//2)*25, fill="#AAAAAA", boldness=1, hori=False)
            create_bold_line(1075, 16, 1075, 20+((n+1)//2)*25, fill="#AAAAAA", boldness=2, hori=False)
            for i in range((n+1)//2+1):
                create_bold_line(875, 17+i*25, 1075, 17+i*25, fill="#AAAAAA", boldness=2, hori=True)
        except:
            pass
        
        #draw edges from i to j
        for i, j in i_j:
            if g.E[i][j] > 0:
                if g.flug_e[i][j] == 0:
                    self.create_line(g.L[i][0], g.L[i][1], g.L[j][0], g.L[j][1], fill="#AAAAAA")
                elif g.flug_e[i][j] == 1:
                    if i-j in {1, -1}:
                        for t in range(-4, 5):
                            self.create_line(g.L[i][0], g.L[i][1]+t, g.L[j][0], g.L[j][1], fill="#00AA00")
                    elif i-j in {g.col, -g.col}:
                        for t in range(-4, 5):
                            self.create_line(g.L[i][0]+t, g.L[i][1], g.L[j][0], g.L[j][1], fill="#00AA00")
        
        for i in range(n):
            # draw nodes
            if g.flug[i] == False:
                self.create_rectangle(g.L[i][0]-self.n_size / 2, g.L[i][1]-self.n_size / 2,
                                      g.L[i][0]+self.n_size / 2, g.L[i][1]+self.n_size / 2,
                                      fill="#AAAAAA") # (x1, y1, x2, y2) x1 and y1 are upper-left, and x2 and y2 are lower-right
            else:
                self.create_rectangle(g.L[i][0]-self.n_size / 2, g.L[i][1]-self.n_size / 2,
                                      g.L[i][0]+self.n_size / 2, g.L[i][1]+self.n_size / 2,
                                      fill="#00FF00") # (x1, y1, x2, y2) x1 and y1 are upper-left, and x2 and y2 are lower-right
        
        if all(g.flug) == True:
            print("#hops of shortest path: {}".format(len(g.path[n-1])))
            for i in range(len(g.path[n-1])-1):
                for t in range(-6, 7):
                    if g.path[n-1][i]-g.path[n-1][i+1] in {-1, 1}:
                        self.create_line(g.L[g.path[n-1][i]][0], g.L[g.path[n-1][i]][1],
                                         g.L[g.path[n-1][i+1]][0], g.L[g.path[n-1][i+1]][1]+t, fill="#FF0000")
                    elif g.path[n-1][i]-g.path[n-1][i+1] in {-g.col, g.col}:
                        self.create_line(g.L[g.path[n-1][i]][0], g.L[g.path[n-1][i]][1],
                                         g.L[g.path[n-1][i+1]][0]+t, g.L[g.path[n-1][i+1]][1], fill="#FF0000")
            for t in range(-6, 7):
                if n-1-g.path[n-1][-1] in {-1, 1}:
                    self.create_line(g.L[g.path[n-1][-1]][0], g.L[g.path[n-1][-1]][1],
                                     g.L[n-1][0], g.L[n-1][1]+t, fill="#FF0000")
                elif n-1-g.path[n-1][-1] in {-g.col, g.col}:
                    self.create_line(g.L[g.path[n-1][-1]][0], g.L[g.path[n-1][-1]][1],
                                     g.L[n-1][0]+t, g.L[n-1][1], fill="#FF0000")


BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
green = (0, 125, 0)
YELLOW = (255, 255, 0)
yellow = (125, 125, 0)
color_list = [[(0, 255, 0), (0, 125, 0)],#[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],[(125, 125, 125), (125, 125, 125)],
              [(255, 0, 0), (125, 0, 0)],
              [(0, 0, 255), (0, 0, 125)],
              [(255, 255, 0), (125, 125, 0)],
              [(255, 0, 255), (125, 0, 125)],
              [(0, 255, 255), (0, 125, 125)],
              [(255, 125, 0), (125, 60, 0)],
              [(125, 255, 0), (60, 125, 0)],
              [(255, 0, 125), (125, 0, 60)],
              [(125, 0, 255), (60, 0, 125)],
              [(0, 125, 255), (0, 60, 125)],
              [(0, 255, 125), (0, 125, 60)]]
