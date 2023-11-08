import re
from peewee import *
from tkinter import DISABLED, END
from tkinter.font import NORMAL
from tkinter.messagebox import *

try:
    db = SqliteDatabase("mi_base.db")

    class BaseModel(Model):
        class Meta:
            database = db

    class Socios(BaseModel):
        nombre = CharField()
        apellido = CharField()
        dni = IntegerField(unique=True)
        nacimiento = DateField()
        categoria = CharField()

    db.connect()
    db.create_tables([Socios])
except:
    pass


class Abmc:

    def f_avisos(un_string):
        showinfo("AVISO", un_string)

    def avisos(funcion):
        def mis_avisos(*args, **kwargs):
            funcion(*args, **kwargs)
            if funcion.__name__ == "f_guardar":
                Abmc.f_avisos("Socio guardado")
            if funcion.__name__ == "f_modificar":
                Abmc.f_avisos("Socio Modificado")
            if funcion.__name__ == "f_borrar":
                Abmc.f_avisos("Socio Eliminado")
        return mis_avisos

    def actualizar_treeview(self, tree):
        records = tree.get_children()
        for element in records:
            tree.delete(element)

        for fila in Socios.select():
            tree.insert(
                "",
                END,
                text=fila.id,
                values=(fila.nombre, fila.apellido, fila.dni,
                        fila.nacimiento, fila.categoria),
            )

    def f_error(self, un_string):
        showerror("ERROR", un_string)

    def seleccionado(self, tree):
        valor = tree.selection()
        item = tree.item(valor)
        mi_idd = item["text"]
        return mi_idd

    def actualizar_bd(self, nombre, apellido, dni, nacimiento, categoria, tree):
        actualizar = Socios.update(
            nombre=nombre.get(), apellido=apellido.get(), dni=dni.get(), nacimiento=nacimiento.get(), categoria=categoria.get()
        ).where(Socios.id == self.seleccionado(tree))
        actualizar.execute()
        self.actualizar_treeview(tree)

    @avisos
    def f_borrar(
        self,
        bt_borrar,
        tree,
    ):
        if tree.selection():
            bt_borrar["state"] = DISABLED
            mi_id = self.seleccionado(tree)
            borrar = Socios.get(Socios.id == mi_id)
            borrar.delete_instance()
            self.actualizar_treeview(tree)
        else:
            self.f_error("No hay ningún ítem seleccionado")

    @avisos
    def f_guardar(
        self,
        tree,
        nombre,
        apellido,
        dni,
        nacimiento,
        categoria,
        bt_guardar,
    ):
        cadena1 = nombre.get()
        cadena2 = apellido.get()
        patron = "^[A-Za-záéíóú]*$"
        if re.match(patron, cadena1):
            if re.match(patron, cadena2):
                socio = Socios()
                socio.nombre = nombre.get()
                socio.apellido = apellido.get()
                socio.dni = dni.get()
                socio.nacimiento = nacimiento.get()
                socio.categoria = categoria.get()

                try:
                    socio.save()
                    bt_guardar["state"] = DISABLED
                except IntegrityError:
                    self.f_error("El DNI ingresado ya existe")

                self.actualizar_treeview(tree)
            else:
                self.f_error("Campos ingresados en 'Apellido' incorrectos")
        else:
            self.f_error("Campos ingresados en 'Nombre' incorrectos")

    @avisos
    def f_modificar(
        self,
        nombre,
        apellido,
        dni,
        nacimiento,
        categoria,
        tree,
        bt_guardar,
        bt_modificar,
        bt_borrar,
    ):

        bt_modificar["state"] = DISABLED
        bt_borrar["state"] = DISABLED
        bt_guardar["state"] = NORMAL
        self.actualizar_bd(
            nombre,
            apellido,
            dni,
            nacimiento,
            categoria,
            tree,
        )
