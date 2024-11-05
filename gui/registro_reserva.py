import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
# from database.conexion import DbSingleton
from services.gestorCliente import GestorCliente
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorReserva import GestorReserva

class RegistroReserva:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Reserva")

        # Attributes to hold selected client and room
        self.cliente_seleccionado = None
        self.habitacion_seleccionada = None

        # Autocompletar para Cliente
        tk.Label(root, text="Cliente").grid(row=0, column=0)
        self.cliente_combobox = ttk.Combobox(root)
        self.cliente_combobox.grid(row=0, column=1)
        self.cliente_combobox['values'] = self.cargar_clientes()  # Cargar valores

        # Bind event to save selected client
        self.cliente_combobox.bind("<<ComboboxSelected>>", self.seleccionar_cliente)

        # Selección de Fecha de Entrada con calendario
        tk.Label(root, text="Fecha de Entrada").grid(row=1, column=0)
        self.fecha_entrada_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.fecha_entrada_entry.grid(row=1, column=1)

        # Selección de Fecha de Salida con calendario
        tk.Label(root, text="Fecha de Salida").grid(row=2, column=0)
        self.fecha_salida_entry = DateEntry(root, date_pattern='yyyy-mm-dd')
        self.fecha_salida_entry.grid(row=2, column=1)

        # Botón para cargar habitaciones disponibles
        tk.Button(root, text="Buscar Habitaciones Disponibles", command=self.cargar_habitaciones_disponibles).grid(row=3, column=0, columnspan=2)

        # Autocompletar para Habitación
        tk.Label(root, text="Habitación").grid(row=4, column=0)
        self.habitacion_combobox = ttk.Combobox(root)
        self.habitacion_combobox.grid(row=4, column=1)

        # Bind event to save selected room
        self.habitacion_combobox.bind("<<ComboboxSelected>>", self.seleccionar_habitacion)

        # Selección de Cantidad de Personas
        tk.Label(root, text="Cantidad de Personas").grid(row=5, column=0)
        self.personas_combobox = ttk.Combobox(root, values=[1, 2, 3, 4, 5], state="readonly")
        self.personas_combobox.grid(row=5, column=1)
        self.personas_combobox.current(0)  # Seleccionar por defecto 1

        # Botón para registrar
        self.registrar_button = tk.Button(root, text="Registrar", command=self.registrar_reserva)
        self.registrar_button.grid(row=6, column=0, columnspan=2)
        self.registrar_button.config(state=tk.DISABLED)  # Deshabilitar inicialmente

        # Bind events to check if all fields are filled
        self.fecha_entrada_entry.bind("<<DateEntrySelected>>", self.check_fields)
        self.fecha_salida_entry.bind("<<DateEntrySelected>>", self.check_fields)
        self.personas_combobox.bind("<<ComboboxSelected>>", self.check_fields)

    def cargar_clientes(self):
        # Lógica para cargar clientes desde gestorClientes
        gestorClientes = GestorCliente()
        clientes = gestorClientes.getClientes() 
        return [f"{cliente.getId()} - {cliente.getNombre()} {cliente.getApellido()}" for cliente in clientes]

    def seleccionar_cliente(self, event):
        # Store the selected client object
        cliente_text = self.cliente_combobox.get()
        cliente_id = cliente_text.split(" - ")[0]  # Get the ID
        gestorClientes = GestorCliente()
        self.cliente_seleccionado = gestorClientes.getClienteById(cliente_id)

        # Check fields to enable register button
        self.check_fields()

    def cargar_habitaciones_disponibles(self):
        # Obtener fechas
        fecha_entrada = self.fecha_entrada_entry.get_date().strftime('%Y-%m-%d')
        fecha_salida = self.fecha_salida_entry.get_date().strftime('%Y-%m-%d')

        # Validar fechas
        if fecha_entrada >= fecha_salida:
            tk.messagebox.showerror("Error", "La fecha de entrada debe ser anterior a la de salida.")
            return

        # Lógica para cargar habitaciones disponibles desde gestorHabitaciones
        gestorReserva = GestorReserva()
        habitaciones_disponibles = gestorReserva.getHabitacionesDisponibles(fecha_entrada, fecha_salida)

        if habitaciones_disponibles:
            self.habitacion_combobox['values'] = [f"{habitacion.getId()} - Nro: {habitacion.getNumero()} - {habitacion.getTipo()}" for habitacion in habitaciones_disponibles]
        else:
            self.habitacion_combobox['values'] = []  # Limpiar la lista si no hay habitaciones
            tk.messagebox.showinfo("Sin Disponibilidad", "No hay habitaciones disponibles para las fechas seleccionadas.")

        # Re-evaluar los campos para habilitar el botón
        self.check_fields()

    def seleccionar_habitacion(self, event):
        # Store the selected room object
        habitacion_text = self.habitacion_combobox.get()
        habitacion_id = habitacion_text.split(" - ")[0]  # Get the ID
        gestorHabitaciones = GestorHabitaciones()
        self.habitacion_seleccionada = gestorHabitaciones.getHabitacion(habitacion_id)

        # Check fields to enable register button
        self.check_fields()

    def check_fields(self, event=None):
        # Verificar si todos los campos están completos
        fecha_entrada_valida = self.fecha_entrada_entry.get() != ""
        fecha_salida_valida = self.fecha_salida_entry.get() != ""
        personas_seleccionadas = self.personas_combobox.get().strip() != ""

        # Habilitar el botón solo si todos los campos están llenos
        if all([self.cliente_seleccionado, self.habitacion_seleccionada, fecha_entrada_valida, fecha_salida_valida, personas_seleccionadas]):
            self.registrar_button.config(state=tk.NORMAL)
        else:
            self.registrar_button.config(state=tk.DISABLED)

    def registrar_reserva(self):
        # Obtener los IDs directamente de los objetos almacenados
        cliente_id = self.cliente_seleccionado.getId() if self.cliente_seleccionado else None
        habitacion_id = self.habitacion_seleccionada.getId() if self.habitacion_seleccionada else None
        fecha_entrada = self.fecha_entrada_entry.get_date().strftime('%Y-%m-%d')
        fecha_salida = self.fecha_salida_entry.get_date().strftime('%Y-%m-%d')
        personas = self.personas_combobox.get()

        # Mostrar por terminal los datos que se van a registrar
        print(f"Cliente ID: {cliente_id}")
        print(f"Habitacion ID: {habitacion_id}")
        print(f"Fecha de entrada: {fecha_entrada}")
        print(f"Fecha de salida: {fecha_salida}")
        print(f"Cantidad de personas: {personas}")
        
        # Lógica para registrar reserva
        gestorReserva = GestorReserva()
        try:
            gestorReserva.registrarReserva(habitacion_id, cliente_id, fecha_entrada, fecha_salida, personas)
            tk.messagebox.showinfo("Reserva Registrada", "La reserva se ha registrado correctamente")
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo registrar la reserva: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroReserva(root)
    root.mainloop()
