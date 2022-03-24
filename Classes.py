import sys
import tkinter as tk
from tkinter import ttk, RIGHT
import socket
from _thread import *
class Servidor():
    def __init__(self, ip,puerto):
        self.ip = ip
        self.puerto = puerto
        #Iniciar el servidor
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Colocar la ip y el puerto
        self.server.bind((ip,puerto))
        #Definir la cantidad de clientes que vamos a escuchar
        self.server.listen(50)

        self.client_list = []

    def listen(self):
        while True:
            coneccion, addr = self.server.accept()
            self.client_list.append(coneccion)
            print("Conectado: " + addr[0])

class Cliente():
    pass


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

        self.btn_start = ttk.Button(self,command=self.go_App, text="Iniciar")
        self.btn_start.grid(row=4,column=1)

        self.pack()

    def addText(self,text,row,col):
        text = ttk.Label(self, text=text)
        text.grid(row=row, column=col)

    def go_App(self):

        main = tk.Tk()
        App(main, self.ipText.get(),self.puertoText.get(),self.NombreText.get())
#Ventana App
class App(ttk.Frame):
    def __init__(self, main_window, ip, puerto, nombre):
        super().__init__(main_window)
        self.main = main_window
        self.main.title("TU_App_Mensajeria")
        self.Mensaje = tk.StringVar()
        self.nombre = nombre
        self.puerto = puerto
        self.ip = ip
        self.main = main_window

        self.cliente = Cliente

        self.text = ttk.Label(self, text=self.nombre)
        self.scrollbar = tk.Scrollbar(self)
        self.btn_atras = ttk.Button(self, command=self.go_Exit, text="EXIT")
        self.btn_enviar = ttk.Button(self, command=self.Enviar, text="Enviar")
        self.entry_mensaje = ttk.Entry(self)
        self.texto = tk.Text(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.texto.yview)

        self.text.pack(side=tk.TOP)
        self.scrollbar.pack(side=RIGHT,fill=tk.Y)
        self.btn_atras.pack(side=tk.BOTTOM, fill=tk.X)
        self.btn_enviar.pack(side=tk.BOTTOM, fill=tk.X)
        self.entry_mensaje.pack(side=tk.BOTTOM, fill=tk.X)
        self.texto.pack(side=tk.BOTTOM, fill=tk.X)

        self.pack()

    def go_Exit(self):
        self.main.destroy()

    def Enviar(self):
        pass

