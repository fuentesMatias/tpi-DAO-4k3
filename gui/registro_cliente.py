import tkinter as tk
from database.conexion import ConexionDB

class RegistroCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Cliente")

        tk.Label(root, text="Nombre").grid(row=0, column=0)
        self.nombre_entry = tk.Entry(root)
        self.nombre_entry.grid(row=0, column=1)

        tk.Label(root, text="Apellido").grid(row=1, column=0)
        self.apellido_entry = tk.Entry(root)
        self.apellido_entry.grid(row=1, column=1)

        tk.Button(root, text="Registrar", command=self.registrar_cliente).grid(row=2, column=0, columnspan=2)

    def registrar_cliente(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()

        db = ConexionDB()
        cursor = db.get_cursor()
        cursor.execute("INSERT INTO clientes (nombre, apellido) VALUES (?, ?)", (nombre, apellido))
        db.commit()

        print(f"Cliente {nombre} {apellido} registrado con éxito")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroCliente(root)
    root.mainloop()
