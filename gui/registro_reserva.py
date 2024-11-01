import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from database.conexion import DbSingleton
from services.gestorCliente import GestorCliente
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorReserva import GestorReserva


class RegistroReserva:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Reserva")

        # Autocompletar para Cliente
        tk.Label(root, text="Cliente").grid(row=0, column=0)
        self.cliente_combobox = ttk.Combobox(root)
        self.cliente_combobox.grid(row=0, column=1)
        self.cliente_combobox['values'] = self.cargar_clientes()  # Cargar valores

        # Autocompletar para Habitación
        tk.Label(root, text="Habitación").grid(row=1, column=0)
        self.habitacion_combobox = ttk.Combobox(root)
        self.habitacion_combobox.grid(row=1, column=1)
        self.habitacion_combobox['values'] = self.cargar_habitaciones_disponibles()  # Cargar valores

        # Selección de Fecha de Entrada con calendario
        tk.Label(root, text="Fecha de Entrada").grid(row=2, column=0)
        self.fecha_entrada_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.fecha_entrada_entry.grid(row=2, column=1)

        # Selección de Fecha de Salida con calendario
        tk.Label(root, text="Fecha de Salida").grid(row=3, column=0)
        self.fecha_salida_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.fecha_salida_entry.grid(row=3, column=1)

        # Selección de Cantidad de Personas
        tk.Label(root, text="Cantidad de Personas").grid(row=4, column=0)
        self.personas_combobox = ttk.Combobox(root, values=[1, 2, 3, 4, 5], state="readonly")
        self.personas_combobox.grid(row=4, column=1)
        self.personas_combobox.current(0)  # Seleccionar por defecto 1

        # Botón para registrar
        tk.Button(root, text="Registrar", command=self.registrar_reserva).grid(
            row=5, column=0, columnspan=2
        )

    def cargar_clientes(self):
        # Lógica para cargar clientes desde gestorClientes
        gestorClientes = GestorCliente()
        clientes = gestorClientes.getClientes() 
        return [f"{cliente.getId()} - {cliente.getNombre()} {cliente.getApellido()}" for cliente in clientes]

    def cargar_habitaciones_disponibles(self):
        # Lógica para cargar habitaciones desde gestorHabitaciones
        gestorHabitaciones = GestorHabitaciones()
        habitaciones = gestorHabitaciones.getHabitacionesDisponibles()  
        return [f"{habitacion.getId()} - {habitacion.getTipo()}" for habitacion in habitaciones]

    def registrar_reserva(self):
        # Obtener solo el ID de cliente y habitación
        cliente_id = self.cliente_combobox.get().split(" - ")[0]
        habitacion_id = self.habitacion_combobox.get().split(" - ")[0]
        fecha_entrada = self.fecha_entrada_entry.get_date().strftime('%Y-%m-%d')
        fecha_salida = self.fecha_salida_entry.get_date().strftime('%Y-%m-%d')
        personas = self.personas_combobox.get()

        # Lógica para registrar reserva
        gestorReserva = GestorReserva()
        try:
            gestorReserva.registrarReserva(habitacion_id, cliente_id, fecha_entrada, fecha_salida, personas)
            tk.messagebox.showinfo("Reserva Registrada", "La reserva se ha registrado correctamente")
        except:
            tk.messagebox.showerror("Error", "No se pudo registrar la reserva")


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroReserva(root)
    root.mainloop()
