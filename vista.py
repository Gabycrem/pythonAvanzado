import os

from numpy import size
import modelo

from tkinter import END, BooleanVar, Button
from tkinter.messagebox import *
from tkinter import Label
from tkinter import Entry
from tkinter import ttk
from tkinter import StringVar
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import DISABLED, NORMAL


class VistaPrincipal:
    def __init__(self, windows):
        self.master = windows
        self.master.title("Planilla del Club")

        BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
        ruta = os.path.join(BASE_DIR, "logo.jpg")
        # self.master.geometry("800x700")

        self.var_nombre = StringVar()
        self.var_apellido = StringVar()
        self.var_dni = StringVar()
        self.var_nacimiento = StringVar()
        self.var_categoria = StringVar()
        self.objeto = modelo.Abmc()
        self.selec = BooleanVar()

        self.selec = False

        self.espacio = Label(self.master)
        self.espacio.grid(row=0, columnspan=4)
        self.nombre_del_club = Label(self.master, text="CLUB UNIVERSITARIO")
        self.nombre_del_club.grid(columnspan=8, row=1, column=0)

        self.nombre_del_club2 = Label(self.master, text="DE RUGBY")
        self.nombre_del_club2.grid(columnspan=8, row=2, column=0)
        self.espacio = Label(self.master)
        self.espacio.grid(row=4, columnspan=4)

        self.logo = Image.open(ruta)
        self.resize_logo = self.logo.resize((100, 100))
        self.logo2 = ImageTk.PhotoImage(self.resize_logo)
        self.mi_logo = tk.Label(self.master, image=self.logo2)
        self.mi_logo.grid(row=0, column=6, rowspan=4, pady=10)

        self.nombre = Label(self.master, text="Nombre")
        self.nombre.grid(row=7, column=0, sticky="w", padx=10)

        self.apellido = Label(self.master, text="Apellido", anchor="n")
        self.apellido.grid(row=7, column=2, sticky="w", padx=10)

        self.dni = Label(self.master, text="DNI", anchor="n")
        self.dni.grid(row=8, column=0, sticky="w", padx=10)

        self.nacimiento = Label(
            self.master, text="Fecha de nacimiento", anchor="n")
        self.nacimiento.grid(row=8, column=2, sticky="w", padx=10)

        self.categoria = Label(self.master, text="Categoria", anchor="n")
        self.categoria.grid(row=9, column=0, sticky="w", padx=10)
        self.w_ancho = 25

        self.entry_nombre = Entry(
            self.master, textvariable=self.var_nombre, width=self.w_ancho
        )
        self.entry_nombre.grid(row=7, column=1)

        self.entry_apellido = Entry(
            self.master, textvariable=self.var_apellido, width=self.w_ancho
        )
        self.entry_apellido.grid(row=7, column=3)

        self.entry_dni = Entry(
            self.master, textvariable=self.var_dni, width=self.w_ancho
        )
        self.entry_dni.grid(row=8, column=1)

        self.entry_nacimiento = Entry(
            self.master, textvariable=self.var_nacimiento, width=self.w_ancho
        )
        self.entry_nacimiento.grid(row=8, column=3)

        self.entry_categoria = Entry(
            self.master, textvariable=self.var_categoria, width=self.w_ancho
        )
        self.entry_categoria.grid(row=9, column=1)

        self.espacio = Label(self.master)
        self.espacio.grid(row=10, columnspan=4)

        self.limpiar_campos()

        self.entry_dni.bind("<Key>", self.ingresoDni)
        self.entry_dni.bind(
            "<BackSpace>", lambda _: self.entry_dni.delete(END))
        self.entry_dni.bind(
            "<Tab>", lambda _: self.valDni())

        self.entry_nacimiento.bind("<Key>", self.ingresoFecha)
        self.entry_nacimiento.bind(
            "<BackSpace>", lambda _: self.entry_nacimiento.delete(END))
        self.entry_nacimiento.bind(
            "<Tab>", lambda _: self.valFecha())

        self.var_nombre.trace_add("write", self.val_form)
        self.var_apellido.trace_add("write", self.val_form)
        self.var_dni.trace_add("write", self.val_form)
        self.var_nacimiento.trace_add("write", self.val_form)
        self.var_categoria.trace_add("write", self.val_form)

        self.tree = ttk.Treeview(self.master)
        self.tree["columns"] = (
            "Nom",
            "Apell",
            "DNI",
            "Nac",
            "Cat",
        )

        self.tree.column("#0", width=50, minwidth=20, anchor="w")
        self.tree.column("Nom", width=200, minwidth=20, anchor="w")
        self.tree.column("Apell", width=200, minwidth=20, anchor="w")
        self.tree.column("DNI", width=100, minwidth=20, anchor="w")
        self.tree.column("Nac", width=150, minwidth=20, anchor="w")
        self.tree.column("Cat", width=80, minwidth=20, anchor="w")

        self.tree.heading("#0", text="ID")
        self.tree.heading("Nom", text="NOMBRE")
        self.tree.heading("Apell", text="APELLIDO")
        self.tree.heading("DNI", text="DNI")
        self.tree.heading("Nac", text="FECHA DE NACIMIENTO")
        self.tree.heading("Cat", text="CATEGORIA")

        self.tree.grid(column=0, row=11, columnspan=8, padx=10)

        self.objeto.actualizar_treeview(self.tree)

        self.bt_guardar = Button(
            self.master,
            text="Guardar",
            command=lambda: self.alta(),
            bg="#DCDCDC",
            width=20,
            state=DISABLED
        )
        self.bt_guardar.grid(row=10, column=-0, pady=5, padx=5, columnspan=1)

        self.bt_modificar = Button(
            self.master,
            text="Modificar",
            command=lambda: self.modif(),
            bg="#DCDCDC",
            width=20,
            state=DISABLED,
        )
        self.bt_modificar.grid(row=10, column=1, pady=5, padx=5, columnspan=1)

        self.bt_seleccionar = Button(
            self.master,
            text="Seleccionar",
            command=lambda: self.f_seleccionar(self.tree),
            bg="#DCDCDC",
            width=20,
        )
        self.bt_seleccionar.grid(
            row=10, column=3, pady=5, padx=5, columnspan=2)

        self.bt_borrar = Button(
            self.master,
            text="Borrar",
            command=lambda: self.baja(),
            bg="#DCDCDC",
            width=20,
            state=DISABLED,
        )
        self.bt_borrar.grid(row=10, column=5, pady=5, padx=5, columnspan=2)

        self.bt_salir = Button(
            self.master, text="Salir", command=self.master.quit, bg="#DCDCDC", width=15
        )
        self.bt_salir.grid(row=15, column=6, sticky="SE", padx=10, pady=10)

    def val_form(self, var, indx, mode):

        if (self.entry_nombre.get() and self.entry_apellido.get() and self.entry_dni.get() and self.entry_nacimiento.get() and self.entry_categoria.get()):
            if self.selec:
                self.bt_modificar["state"] = NORMAL
            else:
                self.bt_guardar["state"] = NORMAL
        else:
            self.bt_guardar["state"] = DISABLED
            self.bt_modificar["state"] = DISABLED

    def valFecha(self,):
        fecha = self.entry_nacimiento.get()
        if (len(fecha) < 10):
            self.objeto.f_error(
                "Ingresar fecha completa en formato: dd/mm/aaaa. Ingresando solo los números.")
            return "break"
        else:
            self.entry_categoria.focus()

    def valDni(self,):
        dni = self.entry_dni.get()

        if (len(dni) < 10):

            self.objeto.f_error(
                "DNI debe tener 8 números.")
            return "break"
        else:
            self.entry_nacimiento.focus()

    def ingresoFecha(self, event):
        if event.char.isdigit():
            texto = self.entry_nacimiento.get()
            car = 0
            for i in texto:
                car += 1
            if car <= 9:
                if car == 2:
                    self.entry_nacimiento.insert(2, "/")
                elif car == 5:
                    self.entry_nacimiento.insert(5, "/")
            else:
                return "break"

        else:
            return "break"

    def ingresoDni(self, event):
        if event.char.isdigit():
            texto = self.entry_dni.get()
            car = 0
            for i in texto:
                car += 1
            if car <= 9:
                if car == 2:
                    self.entry_dni.insert(2, ".")
                elif car == 6:
                    self.entry_dni.insert(6, ".")
            else:
                return "break"

        else:
            return "break"

    def completar_campos(
        self,
        campos,
    ):
        self.entry_nombre.insert(0, campos[0])
        self.entry_apellido.insert(0, campos[1])
        self.entry_dni.insert(0, campos[2])
        self.entry_nacimiento.insert(0, campos[3])
        self.entry_categoria.insert(0, campos[4])

    def limpiar_campos(self,):  # Vacia los campos de ingreso de datos
        self.entry_nombre.delete(0, END)
        self.entry_apellido.delete(0, END)
        self.entry_dni.delete(0, END)
        self.entry_nacimiento.delete(0, END)
        self.entry_categoria.delete(0, END)

    def f_seleccionar(self, tree):
        self.bt_guardar["state"] = DISABLED
        self.limpiar_campos()
        self.selec = True

        if tree.selection():
            valor = tree.selection()
            item = tree.item(valor)
            mi_id = item["text"]
            campos = item["values"]
            mi_id = int(mi_id)
            self.completar_campos(campos)
            self.bt_modificar["state"] = NORMAL
            self.bt_borrar["state"] = NORMAL
            return mi_id
        else:
            self.objeto.f_error("No hay ningún ítem seleccionado")

    def alta(self, ):
        self.objeto.f_guardar(
            self.tree,
            self.var_nombre,
            self.var_apellido,
            self.var_dni,
            self.var_nacimiento,
            self.var_categoria,
            self.bt_guardar,
        )
        if self.bt_guardar["state"] == DISABLED:
            self.limpiar_campos()
            self.entry_nombre.focus()

    def baja(self,):
        self.objeto.f_borrar(
            self.bt_borrar,
            self.tree,
        )
        if (self.bt_borrar["state"] == DISABLED):
            self.limpiar_campos()
            self.selec = False

    def modif(self, ):
        self.objeto.f_modificar(
            self.var_nombre,
            self.var_apellido,
            self.var_dni,
            self.var_nacimiento,
            self.var_categoria,
            self.tree,
            self.bt_guardar,
            self.bt_modificar,
            self.bt_borrar,
        )
        if (self.bt_modificar["state"] == DISABLED):
            self.limpiar_campos()
            self.selec = False
