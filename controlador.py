from tkinter import Tk
import vista

"""-------------
Controlador
--------------"""


class Controlador:
    def __init__(self, root_w):
        self.root = root_w
        self.objeto_vista = vista.VistaPrincipal(self.root)


if __name__ == "__main__":
    root = Tk()
    mi_App = Controlador(root)

    root.mainloop()
