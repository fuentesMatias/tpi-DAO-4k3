import tkinter as tk
from database.crear_db import crear_tablas
from gui.registro_cliente import RegistroCliente
from gui.registro_habitacion import RegistroHabitacion
from gui.registro_reserva import RegistroReserva

def main():
    # Crear la base de datos y las tablas si no existen
    crear_tablas()

    root = tk.Tk()
    root.title("Sistema de Gestión de Hotel")

    tk.Button(root, text="Registrar Cliente", command=lambda: RegistroCliente(tk.Toplevel(root))).pack()
    tk.Button(root, text="Registrar Habitación", command=lambda: RegistroHabitacion(tk.Toplevel(root))).pack()
    tk.Button(root, text="Registrar Reserva", command=lambda: RegistroReserva(tk.Toplevel(root))).pack()

    root.mainloop()

if __name__ == "__main__":
    main()
