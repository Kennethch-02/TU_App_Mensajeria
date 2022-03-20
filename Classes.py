import tkinter as tk
from tkinter import ttk

#Ventana Menu
class Menu(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("TU_App_Mensajeria")
        self.main = main_window
        self.addText("Menu",0,1)
        self.addText("IP",1,0)
        self.addText("Puerto",2,0)
        self.addText("Nombre",3, 0)

        self.ipText = ttk.Entry(self)
        self.ipText.grid(row=1, column=1)

        self.NombreText = ttk.Entry(self)
        self.NombreText.grid(row=3, column=1)

        self.puertoText = ttk.Spinbox(self,from_=8888,to=15000)
        self.puertoText.grid(row=2, column=1)

        self.btn_start = ttk.Button(self,command= self.Start, text="Iniciar")
        self.btn_start.grid(row=4,column=1)

        self.pack()

    def addText(self,text,row,col):
        text = ttk.Label(self, text=text)
        text.grid(row=row, column=col)

    def Start (self):
        print("Iniciando...")

#Ventana App
class App(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("TU_App_Mensajeria")
        self.main = main_window
        self.text = ttk.Label(self, text="Inicio")
        self.text.grid(row=0, column=1)
        self.pack()

class Servidor():
    pass

class Cliente():
    pass