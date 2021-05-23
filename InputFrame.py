# Импорт Tkinter для создания окон, config для записи глобальных
# переменных и Function для вызова вычисляющей функции
import tkinter as tk
from tkinter import Label, Entry, Button
import config as cfg
import Function

# Первое окно, root widget, программа запущена пока оно открыто, 
# содержит Entry для ввода значений, Label над Entry содержат
# описание вводимых значений, Button записывает значения
# в глобальные переменные и открывает следующее окно
class FirstInputFrame(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Построение маршрутов при ограничении на время")
        self.label1 = Label(self, text = "Скорость работника, м/с")
        self.label2 = Label(self, text = "Скорость транспортера, м/с")
        self.label3 = Label(self, text = "Время выемки товара, сек")
        self.label4 = Label(self, text = "Время установки тары на " 
                            "транспортер, сек")
        self.label5 = Label(self, text = "Контрольный срок, сек")
        self.label6 = Label(self, text = "Допустимое отклонение от " 
                            "контрольного срока, сек")
        self.label7 = Label(self, text = "Число обслуживаемых колонок ячеек")
        self.label8 = Label(self, text = "Коэффициент непрямолинейности движения, %")
        self.Entry1 = Entry(self, width=10)
        self.Entry2 = Entry(self, width=10)
        self.Entry3 = Entry(self, width=10)
        self.Entry4 = Entry(self, width=10)
        self.Entry5 = Entry(self, width=10)
        self.Entry6 = Entry(self, width=10)
        self.Entry7 = Entry(self, width=10)
        self.Entry8 = Entry(self, width=10)
        self.Button1 = Button(self, text = "Продолжить ввод")
        self.var = tk.IntVar()
        self.Check = tk.Checkbutton(self, text = "Учесть непрямолинейность движения", variable=self.var)
        self.label1.pack()
        self.Entry1.pack()
        self.label2.pack()
        self.Entry2.pack()
        self.label3.pack()
        self.Entry3.pack()
        self.label4.pack()
        self.Entry4.pack()
        self.label5.pack()
        self.Entry5.pack()
        self.label6.pack()
        self.Entry6.pack()
        self.label7.pack()
        self.Entry7.pack()
        self.Check.pack()
        self.label8.pack()
        self.Entry8.pack()
        self.Button1['command'] = self.Calculate
        self.Button1.pack()

    # Присвоение глобальным переменным, значения Entry 
    # и вызов FirstTableInput.
    def Calculate(self):
        cfg.WorkerSpeed = float(self.Entry1.get())
        cfg.BeltSpeed = float(self.Entry2.get())
        cfg.TimeToCollect = float(self.Entry3.get())
        cfg.TimeToUnload = float(self.Entry4.get())
        cfg.MaxTime = float(self.Entry5.get())
        cfg.DeviationOfTime = float(self.Entry6.get())
        cfg.CountOfColumbs = int(self.Entry7.get())
        if self.var.get():
            cfg.Alpha = float(self.Entry8.get())/100
        else:
            cfg.Alpha = 0.0
        Launch = FirstTableInput(cfg.app, 5, cfg.CountOfColumbs + 1)
        # Обнуление остальных глобальных переменных 
        # в случае повторного использования программы
        cfg.Names = ["Транспортер"]
        cfg.Length = [0.0]
        cfg.Articles = [0]
        cfg.DistanceMatrix = []
        cfg.Weight = [0]
        cfg.Result = []

# Второе окно для ввода следующих параметров: Координаты КЯ (str),
# число артикулов в КЯ (int), Расстояние по транспортеру
# до границы цеха (double)
class FirstTableInput(tk.Toplevel):
    
    def __init__(self, parent, rows, columns):

        tk.Toplevel.__init__(self, parent)
        self.title("Ввод параметров колонок ячеек и их артикулов")
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

        self.geometry('700x150+200+200')
        self.frame2.bind('<Configure>', self.OnFrameConfigure)

        self.frame2._entry = {}
        self.frame2.rows = rows+1
        self.frame2.columns = columns
        self.frame2._entry[1,0] = Label(self.frame2,
                                       text="Координаты КЯ").grid(row = 1,
                                                                 column = 0)
        self.frame2._entry[2,0] = Label(self.frame2,
                                       text="Число артикулов в КЯ").grid(
                                           row = 2, column = 0)
        self.frame2._entry[3,0] = Label(self.frame2,
                                       text="Расстояние до " 
                                       "границы цеха, м").grid(row = 3,
                                                           column = 0)
        self.frame2._entry[4,0] = Label(self.frame2,
                                       text="Вес артикула, кг").grid(row = 4,
                                                                 column = 0)
        for column in range(1, self.frame2.columns):
            index = (0, column)
            L = tk.Label(self.frame2, text = int(column))
            L.grid(row=0, column=column, stick="nsew")
            self.frame2._entry[index] = L
        for row in range(1, self.frame2.rows - 1):
            for column in range(1, self.frame2.columns):
                index = (row, column)
                e = tk.Entry(self.frame2)
                e.grid(row=row, column=column, stick="nsew")
                self.frame2._entry[index] = e
        self.submit = tk.Button(self, text="Далее", command=self.get)
        self.submit.pack(side = 'bottom')

    def OnFrameConfigure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Запись введенных значений в глобальные переменные и вызов
    # третьего окна. Данное окно закрывается
    def get(self):
        for column in range(1, self.frame2.columns):
            cfg.Names.append(self.frame2._entry[1, column].get())
            Value = int(self.frame2._entry[2, column].get())
            cfg.Articles.append(Value)
            # Расстояние по транспортеру не учитывается для пустых КЯ
            if Value is not 0:
                cfg.Length.append(float(self.frame2._entry[3, column].get()))
            else:
                cfg.Length.append(0.0)
            cfg.Weight.append(float(self.frame2._entry[4, column].get()))
        STI = SecondTableInput(cfg.app)
        self.destroy()

# Третье окно для ввода расстояний между каждой парой КЯ
class SecondTableInput(tk.Toplevel):
    
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Ввод матрицы расстояний между КЯ")
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
        self.geometry('600x300+200+200')
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
                e = tk.Entry(self.frame2)
                e.grid(row=row, column=column, stick="nsew")
                self.frame2._entry[index] = e
        self.frame2.update_idletasks()
        self.canvas.config(width=600, height = 200)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.submit = tk.Button(self, text="Рассчитать", command=self.get)
        self.submit.pack(side = 'bottom')

    def OnFrameConfigure(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # Запись в глобальную переменную. Вызов функции для рассчета итога
    def get(self):
        for row in range(1, self.frame2.rows):
            CurrentRow = []
            for column in range(1, self.frame2.columns):
                CurrentRow.append(float(self.frame2._entry[row,
                                                          column].get()))
            cfg.DistanceMatrix.append(CurrentRow)
        Function.calculate()
        self.destroy()