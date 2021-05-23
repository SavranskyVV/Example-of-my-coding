import tkinter as tk
from tkinter import Label, Button
import numpy as np
import config as cfg

class ResultsTable(tk.Toplevel):
    
    def __init__(self, parent, Result):
        tk.Toplevel.__init__(self, parent)
        self.title("Результат работы программы")
        self.frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.frame)
        self.frame.grid(row=0, column=0, sticky = 'nw')
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.canvas.grid(row=0,column=0,sticky='news')
        self.frame2 = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window = self.frame2, anchor='nw')
        self.frame2._entry = {}
        self.frame2._entry[0,0] = Label(self.frame2, text="Номер маршрута"
                                        ).grid(row = 0, column = 0)
        self.frame2._entry[0,1] = Label(self.frame2, text="Маршрут"
                                        ).grid(row = 0, column = 1)
        self.frame2._entry[0,2] = Label(self.frame2, text="Время на маршруте, сек"
                                        ).grid(row = 0, column = 2)
        self.frame2._entry[0,3] = Label(self.frame2, text="Собрано артикулов"
                                        ).grid(row = 0, column = 3)
        self.frame2._entry[0,4] = Label(self.frame2, text="Вес артикулов, кг"
                                        ).grid(row = 0, column = 4)
        for i in range(len(Result)):
            for j in range(5):
                L = Label(self.frame2, text = str(Result[i][j]))
                L.grid(row=i+1, column=j, stick="nsew")
                self.frame2._entry[i+1,j] = L
        self.submit = Button(self, text="Завершить работу", command=self.close)
        self.canvas.config(width=900, height = 200)
        self.submit.grid(row = len(Result)+3, column = 0)

    def close(self):
        self.destroy()

class MatrixOutput(tk.Toplevel):
    
    def __init__(self, parent, matrix, name):
        tk.Toplevel.__init__(self, parent)
        self.title(name)
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side = 'left', fill = tk.BOTH, expand = True)
        
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side = 'right', fill = tk.BOTH, expand = True)
        
        self.frame2 = tk.Frame(self.canvas)
        
        self.canvas_frame = self.canvas.create_window((0,0),
                                                     window = self.frame2,
                                                     anchor = 'nw')

        self.hsb = tk.Scrollbar(self.canvas, orient = "horizontal",
                               command = self.canvas.xview)
        self.hsb.pack(side = 'bottom', fill = tk.X)
        self.canvas.config(xscrollcommand=self.hsb.set)
        self.geometry('400x400+200+200')
        self.frame2.bind('<Configure>', self.OnFrameConfigure)
  
        self.vsb = tk.Scrollbar(self.canvas, orient = "vertical", 
                                command = self.canvas.yview)
        self.vsb.pack(side = 'right', fill = tk.Y)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.frame2._entry = {}
        self.frame2.rows = cfg.CountOfColumbs+2
        self.frame2.columns = cfg.CountOfColumbs+2
        for column in range(1, self.frame2.columns):
            index = (0, column)
            L = tk.Label(self.frame2, text = str(cfg.Names[column-1]))
            L.grid(row=0, column=column, stick="nsew")
            self.frame2._entry[index] = L
        for row in range(1, self.frame2.rows):
            index = (row, 0)
            L = tk.Label(self.frame2, text = str(cfg.Names[row-1]))
            L.grid(row=row, column=0, stick="nsew")
            self.frame2._entry[index] = L
        for row in range(1, self.frame2.rows):
            for column in range(1, self.frame2.columns):
                index = (row, column)
                L = tk.Label(self.frame2, text = str('{:.2f}'.format(matrix[row-1,column-1])))
                L.grid(row=row, column=column, stick="nsew")
                self.frame2._entry[index] = L
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.submit = tk.Button(self, text="Закрыть", command=self.close)
        self.submit.pack(side = 'bottom')

    def OnFrameConfigure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def close(self):
        self.destroy()


