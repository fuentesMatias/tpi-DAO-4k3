import tkinter as tk
from database.conexion import DbSingleton


class RegistroReserva:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Reserva")

        tk.Label(root, text="ID Cliente").grid(row=0, column=0)
        self.cliente_entry = tk.Entry(root)
        self.cliente_entry.grid(row=0, column=1)

        tk.Label(root, text="ID Habitación").grid(row=1, column=0)
        self.habitacion_entry = tk.Entry(root)
        self.habitacion_entry.grid(row=1, column=1)

        tk.Label(root, text="Fecha de Entrada (YYYY-MM-DD)").grid(row=2, column=0)
        self.fecha_entrada_entry = tk.Entry(root)
        self.fecha_entrada_entry.grid(row=2, column=1)

        tk.Label(root, text="Fecha de Salida (YYYY-MM-DD)").grid(row=3, column=0)
        self.fecha_salida_entry = tk.Entry(root)
        self.fecha_salida_entry.grid(row=3, column=1)

        tk.Label(root, text="Cantidad de Personas").grid(row=4, column=0)
        self.personas_entry = tk.Entry(root)
        self.personas_entry.grid(row=4, column=1)

        tk.Button(root, text="Registrar", command=self.registrar_reserva).grid(
            row=5, column=0, columnspan=2
        )

    def registrar_reserva(self):
        cliente = self.cliente_entry.get()
        habitacion = self.habitacion_entry.get()
        fecha_entrada = self.fecha_entrada_entry.get()
        fecha_salida = self.fecha_salida_entry.get()
        personas = self.personas_entry.get()

        db = DbSingleton()
        db.execute_query(
            "INSERT INTO reservas (id_cliente, id_habitacion, fecha_entrada, fecha_salida, personas) "
            "VALUES (%s, %s, %s, %s, %s)",
            (cliente, habitacion, fecha_entrada, fecha_salida, personas),
        )
        db.commit()
        print(f"Reserva registrada exitosamente para el cliente {cliente}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroReserva(root)
    root.mainloop()
