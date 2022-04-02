import sys
import tkinter as tk
from tkinter import ttk, RIGHT
import socket
from threading import Thread

class Servidor():
    #Constructor
    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto

        #Lista de clientes
        self.client_list = set()

        #Socket
        self.server = socket.socket()

    #Iniciar el servidor
    def start(self):
        #Establecemos que el servidor sea reutilizable
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        #Conectamos el cliente
        self.server.bind((self.ip,self.puerto))

        #Establecemos la cantidad maxima de clientes
        self.server.listen(50)

        #Se mantiene escuchando por nuevas conecciones
        while True:
            # Verificamos que alguien se conecte
            client_socket, client_address = self.server.accept() # Funcion de espera

            # Agregamos el nuevo cliente
            self.client_list.add(client_socket)

            # Iniciamos un nuevo Thread para escuchar este cliente
            t = Thread(target=self.listen, args=(client_socket,))
            t.daemon = True
            t.start()

        self.close()

    # Funcion que escucha a cada cliente
    def listen(self,cs):
        while True:
            try:
                # Mantendernos escuchando un mensaje
                msg = cs.recv(1024).decode()

            except Exception as e:
                #Si el cliente se desconecta
                self.client_list.remove(cs)

           # Reparte el mensaje recibido en los clientes
            for client_socket in self.client_list:
                #Envia el mensaje
                client_socket.send(msg.encode())

    # Cerrar el servidor
    def close(self):
        # Cerramos los clientes
        for cs in self.client_list:
            cs.close()
        #Cerramos el servidor
        self.server.close()


class Cliente():
    # Clase Constructor
    def __init__(self, ip, puerto, nombre):
        self.puerto = puerto
        self.ip = ip
        self.client = socket.socket()
        self.nombre = nombre
        self.message = ""

    # Conectamos el cliente
    def connect(self):
        # Conectamos
        self.client.connect((self.ip, self.puerto))

        # Iniciamos un Thread
        t = Thread(target=self.listen)
        t.daemon = True
        t.start()

    # Escuchamos cualquier mensaje
    def listen(self):
        while True:
            self.message = self.client.recv(1024).decode()


    # Enviamos un mensaje
    def send_message(self, m):
        msg = self.nombre + ": " + m

        # Codificar el mensaje
        msg = msg.encode()

        self.client.send(msg)

    # Cerramos el cliente
    def close(self):
        self.client.close()


# Ventana Menu
class Menu(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("TU_App_Mensajeria")
        self.main = main_window
        self.addText("Menu", 0, 1)
        self.addText("IP", 1, 0)
        self.addText("Puerto", 2, 0)
        self.addText("Nombre", 3, 0)

        self.ipText = ttk.Entry(self)
        self.ipText.grid(row=1, column=1)

        self.NombreText = ttk.Entry(self)
        self.NombreText.grid(row=3, column=1)

        self.puertoText = ttk.Spinbox(self, from_=8888, to=15000)
        self.puertoText.grid(row=2, column=1)

        self.btn_s_start = ttk.Button(self, command=self.init_server, text="Iniciar Servidor")
        self.btn_s_start.grid(row=4, column=1)

        self.btn_start = ttk.Button(self, command=self.go_App, text="Iniciar Cliente")
        self.btn_start.configure(state=tk.DISABLED)
        self.btn_start.grid(row=5, column=1)



        self.pack()

    def addText(self, text, row, col):
        text = ttk.Label(self, text=text)
        text.grid(row=row, column=col)

    def init_server(self):
        self.server = Servidor(self.ipText.get(), int(self.puertoText.get()))

        t = Thread(target=self.server.start)
        t.daemon = True
        t.start()

        self.btn_s_start.configure(state=tk.DISABLED)
        self.btn_start.configure(state=tk.ACTIVE)
        self.ipText.configure(state=tk.DISABLED)
        self.puertoText.configure(state=tk.DISABLED)

    def go_App(self):
        main = tk.Tk()
        App(main, "127.0.0.1", int(self.puertoText.get()), self.NombreText.get())

# Ventana App
class App(ttk.Frame):
    def __init__(self, main_window, ip, puerto, nombre):
        super().__init__(main_window)
        self.main = main_window
        self.main.title("TU_App_Mensajeria")
        self.Mensaje = ""
        self.nombre = nombre
        self.puerto = puerto
        self.ip = ip
        self.main = main_window

        self.text = ttk.Label(self, text=self.nombre)
        self.scrollbar = tk.Scrollbar(self)
        self.btn_atras = ttk.Button(self, command=self.go_Exit, text="EXIT")
        self.btn_enviar = ttk.Button(self, command=self.Enviar, text="Enviar")
        self.entry_mensaje = ttk.Entry(self)
        self.texto = tk.Text(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.texto.yview)

        self.text.pack(side=tk.TOP)
        self.scrollbar.pack(side=RIGHT, fill=tk.Y)
        self.btn_atras.pack(side=tk.BOTTOM, fill=tk.X)
        self.btn_enviar.pack(side=tk.BOTTOM, fill=tk.X)
        self.entry_mensaje.pack(side=tk.BOTTOM, fill=tk.X)
        self.texto.pack(side=tk.BOTTOM, fill=tk.X)

        self.pack()

        self.cliente = Cliente(self.ip, self.puerto, self.nombre)
        self.cliente.connect()

        self.pos = 1.0

        self.Update()

    def Enviar(self):
        m = self.entry_mensaje.get()
        self.cliente.send_message(m)

    def Update(self):
        if (self.cliente.message != ""):
            self.cliente.message += "\n"
            self.texto.insert(self.pos, self.cliente.message)
            self.cliente.message = ""
            self.pos += 1

        self.after(100, self.Update)

    def go_Exit(self):
        self.cliente.close()
        self.main.destroy()


