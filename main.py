# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 00:34:05 2019

@author: T-GOTOH
"""

import tkinter as tk
from viewer import My_Canvas
#import time

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        params = (6, 7, True)
        #params = (2, 3, False)
        self.canvas = My_Canvas(self, row=params[0], col=params[1], fix=params[2], width=1100, height=600, bg="#000000")
        self.canvas.pack(side="bottom")
        
        self.button_frame = tk.Frame(self.master)
        
        self.button_frame.next_state = tk.Button(self)
        self.button_frame.next_state["text"] = "Next"
        self.button_frame.next_state["command"] = self.canvas.next_phase
        self.button_frame.next_state.pack(side="left")
        
        self.button_frame.start_f = tk.Button(self)
        self.button_frame.start_f["text"] = "Reset"
        self.button_frame.start_f["command"] = self.canvas.reset
        self.button_frame.start_f.pack(side="left")
        
        self.button_frame.start_f = tk.Button(self)
        self.button_frame.start_f["text"] = "Start"
        self.button_frame.start_f["command"] = self.canvas.start_sim
        self.button_frame.start_f.pack(side="left")
        
        self.button_frame.stop_f = tk.Button(self)
        self.button_frame.stop_f["text"] = "Stop"
        self.button_frame.stop_f["command"] = self.canvas.stop_sim
        self.button_frame.stop_f.pack(side="left")
        
        self.button_frame.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.button_frame.quit.pack(side="left")

        self.button_frame.pack(side="top")

root = tk.Tk()
app = Application(master=root)
app.mainloop()