import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date, timedelta
from services.gestorCliente import GestorCliente
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorReserva import GestorReserva

class RegistroReserva:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Reserva")
        # centrar
        pantalla_ancho = root.winfo_screenwidth()
        pantalla_alto = root.winfo_screenheight()
        x = (pantalla_ancho - 350) // 2
        y = (pantalla_alto - 200) // 2
        root.geometry(f"500x250+{x}+{y}")
        

        # Attributes to hold selected client and room
        self.cliente_seleccionado = None
        self.habitacion_seleccionada = None

        # Initial date values
        self.hoy = date.today()
        self.manana = self.hoy + timedelta(days=1)

        # Selección de Fecha de Entrada con calendario
        tk.Label(root, text="Fecha de Entrada").grid(row=0, column=0)
        self.fecha_entrada_entry = DateEntry(root, date_pattern='yyyy-mm-dd', mindate=self.hoy)
        self.fecha_entrada_entry.set_date(self.hoy)  # Set default date to today
        self.fecha_entrada_entry.grid(row=0, column=1)

        # Selección de Fecha de Salida con calendario
        tk.Label(root, text="Fecha de Salida").grid(row=1, column=0)
        self.fecha_salida_entry = DateEntry(root, date_pattern='yyyy-mm-dd', mindate=self.manana)
        self.fecha_salida_entry.set_date(self.manana)  # Set default date to tomorrow
        self.fecha_salida_entry.grid(row=1, column=1)

        # Bind event to update mindate for salida when entrada changes
        self.fecha_entrada_entry.bind("<<DateEntrySelected>>", self.actualizar_fecha_salida_min)

        # Botón para cargar habitaciones disponibles
        tk.Button(root, text="Buscar Habitaciones Disponibles", command=self.cargar_habitaciones_disponibles).grid(row=2, column=0, columnspan=2)

        # Autocompletar para Habitación
        tk.Label(root, text="Habitación").grid(row=3, column=0)
        self.habitacion_combobox = ttk.Combobox(root)
        self.habitacion_combobox.grid(row=3, column=1)
        self.habitacion_combobox.bind("<<ComboboxSelected>>", self.seleccionar_habitacion)

        # Autocompletar para Cliente
        tk.Label(root, text="Cliente").grid(row=4, column=0)
        self.cliente_combobox = ttk.Combobox(root)
        self.cliente_combobox.grid(row=4, column=1)
        self.cliente_combobox['values'] = self.cargar_clientes()  # Cargar valores
        self.cliente_combobox.bind("<<ComboboxSelected>>", self.seleccionar_cliente)

        # Selección de Cantidad de Personas
        tk.Label(root, text="Cantidad de Personas").grid(row=5, column=0)
        self.personas_combobox = ttk.Combobox(root, values=[1, 2, 3], state="readonly")
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

    def actualizar_fecha_salida_min(self, event):
        # Set salida min date to one day after entrada
        nueva_fecha_salida_min = self.fecha_entrada_entry.get_date() + timedelta(days=1)
        self.fecha_salida_entry.config(mindate=nueva_fecha_salida_min)
        if self.fecha_salida_entry.get_date() < nueva_fecha_salida_min:
            self.fecha_salida_entry.set_date(nueva_fecha_salida_min)  # Update to valid date

    def cargar_clientes(self):
        gestorClientes = GestorCliente()
        clientes = gestorClientes.getClientes()
        return [f"{cliente.getId()} - {cliente.getNombre()} {cliente.getApellido()}" for cliente in clientes]

    def seleccionar_cliente(self, event):
        cliente_text = self.cliente_combobox.get()
        cliente_id = cliente_text.split(" - ")[0]
        gestorClientes = GestorCliente()
        self.cliente_seleccionado = gestorClientes.getClienteById(cliente_id)
        self.check_fields()

    def cargar_habitaciones_disponibles(self):
        fecha_entrada = self.fecha_entrada_entry.get_date().strftime('%Y-%m-%d')
        fecha_salida = self.fecha_salida_entry.get_date().strftime('%Y-%m-%d')

        if fecha_entrada >= fecha_salida:
            messagebox.showerror("Error", "La fecha de entrada debe ser anterior a la de salida.")
            return

        gestorReserva = GestorReserva()
        habitaciones_disponibles = gestorReserva.getHabitacionesDisponibles(fecha_entrada, fecha_salida)

        if habitaciones_disponibles:
            self.habitacion_combobox['values'] = [
                f"{habitacion.getId()} - Nro: {habitacion.getNumero()} - {habitacion.getTipo()}" for habitacion in habitaciones_disponibles
            ]
        else:
            self.habitacion_combobox['values'] = []
            messagebox.showinfo("Sin Disponibilidad", "No hay habitaciones disponibles para las fechas seleccionadas.")

        self.check_fields()

    def seleccionar_habitacion(self, event):
        habitacion_text = self.habitacion_combobox.get()
        habitacion_id = habitacion_text.split(" - ")[0]
        gestorHabitaciones = GestorHabitaciones()
        self.habitacion_seleccionada = gestorHabitaciones.getHabitacion(habitacion_id)

        tipo_habitacion = self.habitacion_seleccionada.getTipo()
        if tipo_habitacion == "Simple":
            self.personas_combobox['values'] = [1]
        elif tipo_habitacion == "Doble":
            self.personas_combobox['values'] = [1, 2]
        elif tipo_habitacion == "Suite":
            self.personas_combobox['values'] = [1, 2, 3]
        self.personas_combobox.current(0)

        self.check_fields()

    def check_fields(self, event=None):
        fecha_entrada_valida = self.fecha_entrada_entry.get() != ""
        fecha_salida_valida = self.fecha_salida_entry.get() != ""
        personas_seleccionadas = self.personas_combobox.get().strip() != ""

        if all([self.cliente_seleccionado, self.habitacion_seleccionada, fecha_entrada_valida, fecha_salida_valida, personas_seleccionadas]):
            self.registrar_button.config(state=tk.NORMAL)
        else:
            self.registrar_button.config(state=tk.DISABLED)

    def registrar_reserva(self):
        cliente_id = self.cliente_seleccionado.getId() if self.cliente_seleccionado else None
        habitacion_id = self.habitacion_seleccionada.getId() if self.habitacion_seleccionada else None
        fecha_entrada = self.fecha_entrada_entry.get_date().strftime('%Y-%m-%d')
        fecha_salida = self.fecha_salida_entry.get_date().strftime('%Y-%m-%d')
        personas = self.personas_combobox.get()

        print(f"Cliente ID: {cliente_id}")
        print(f"Habitacion ID: {habitacion_id}")
        print(f"Fecha de entrada: {fecha_entrada}")
        print(f"Fecha de salida: {fecha_salida}")
        print(f"Cantidad de personas: {personas}")

        gestorReserva = GestorReserva()
        try:
            gestorReserva.registrarReserva(habitacion_id, cliente_id, fecha_entrada, fecha_salida, personas)
            messagebox.showinfo("Reserva Registrada", "La reserva se ha registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la reserva: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroReserva(root)
    root.mainloop()
