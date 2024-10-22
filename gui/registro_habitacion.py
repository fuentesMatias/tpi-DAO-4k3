import tkinter as tk
from database.conexion import ConexionDB

class RegistroHabitacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Habitación")

        tk.Label(root, text="Número").grid(row=0, column=0)
        self.numero_entry = tk.Entry(root)
        self.numero_entry.grid(row=0, column=1)

        tk.Label(root, text="Tipo").grid(row=1, column=0)
        self.tipo_entry = tk.Entry(root)
        self.tipo_entry.grid(row=1, column=1)

        tk.Label(root, text="Precio").grid(row=2, column=0)
        self.precio_entry = tk.Entry(root)
        self.precio_entry.grid(row=2, column=1)

        tk.Button(root, text="Registrar", command=self.registrar_habitacion).grid(row=3, column=0, columnspan=2)

    def registrar_habitacion(self):
        numero = self.numero_entry.get()
        tipo = self.tipo_entry.get()
        precio = self.precio_entry.get()

        db = ConexionDB()
        cursor = db.get_cursor()
        cursor.execute("INSERT INTO habitaciones (numero, tipo, precio) VALUES (?, ?, ?)", (numero, tipo, precio))
        db.commit()

        print(f"Habitación {numero} registrada con éxito")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroHabitacion(root)
    root.mainloop()
