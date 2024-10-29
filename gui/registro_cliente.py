import tkinter as tk
from database.conexion import DbSingleton


class VentanaRegistrarCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Cliente")

        tk.Label(root, text="Nombre").grid(row=0, column=0)
        self.nombre_entry = tk.Entry(root)
        self.nombre_entry.grid(row=0, column=1)

        tk.Label(root, text="Apellido").grid(row=1, column=0)
        self.apellido_entry = tk.Entry(root)
        self.apellido_entry.grid(row=1, column=1)

        tk.Label(root, text="Dirección").grid(row=2, column=0)
        self.direccion_entry = tk.Entry(root)
        self.direccion_entry.grid(row=2, column=1)

        tk.Label(root, text="Teléfono").grid(row=3, column=0)
        self.telefono_entry = tk.Entry(root)
        self.telefono_entry.grid(row=3, column=1)

        tk.Label(root, text="Email").grid(row=4, column=0)
        self.mail_entry = tk.Entry(root)
        self.mail_entry.grid(row=4, column=1)

        tk.Button(root, text="Registrar", command=self.registrar_cliente).grid(
            row=5, column=0, columnspan=2
        )

    def registrar_cliente(self):
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        direccion = self.direccion_entry.get()
        telefono = self.telefono_entry.get()
        email = self.mail_entry.get()

        db = DbSingleton()
        db.execute_query(
            """
            INSERT INTO clientes (nombre, apellido, direccion, telefono, email)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, apellido, direccion, telefono, email),
        )
        db.commit()

        print(f"Cliente {nombre} {apellido} registrado con éxito")


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaRegistrarCliente(root)
    root.mainloop()
