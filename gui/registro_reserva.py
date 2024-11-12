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
        self.root.geometry("800x500")
        self.root.configure(bg="#d6f0ff")

        # Centrar ventana
        pantalla_ancho = root.winfo_screenwidth()
        pantalla_alto = root.winfo_screenheight()
        x = (pantalla_ancho - 800) // 2
        y = (pantalla_alto - 500) // 2
        root.geometry(f"800x500+{x}+{y}")

        # Estilo de botón
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "RoundedButton.TButton",
            background="#ffffff",
            foreground="#4a4a4a",
            font=("Arial", 12, "bold"),
            padding=14,
            relief="flat",
        )
        style.map(
            "RoundedButton.TButton",
            background=[("active", "#e0e0e0")],
            relief=[("pressed", "sunken")],
        )

        # Fuentes y estilo de input
        input_font = ("Arial", 12)
        input_style = {
            "background": "#ffffff",
            "foreground": "#000000",
            "font": input_font,
        }

        # Crear Frame centrado
        frame = tk.Frame(root, bg="#d6f0ff")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Widgets
        # Fecha de Entrada
        tk.Label(
            frame, text="Fecha de Entrada:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.fecha_entrada_entry = DateEntry(
            frame, date_pattern="yyyy-mm-dd", mindate=date.today(), **input_style
        )
        self.fecha_entrada_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Fecha de Salida
        tk.Label(
            frame, text="Fecha de Salida:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.fecha_salida_entry = DateEntry(
            frame,
            date_pattern="yyyy-mm-dd",
            mindate=date.today() + timedelta(days=1),
            **input_style,
        )
        self.fecha_salida_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Botón para cargar habitaciones disponibles
        self.buscar_btn = ttk.Button(
            frame,
            text="Buscar Habitaciones Disponibles",
            command=self.cargar_habitaciones_disponibles,
            style="RoundedButton.TButton",
        )
        self.buscar_btn.grid(row=2, column=0, columnspan=2, pady=20)

        # Autocompletar para Habitación
        tk.Label(
            frame, text="Habitación:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.habitacion_combobox = ttk.Combobox(frame, **input_style)
        self.habitacion_combobox.grid(row=3, column=1, padx=10, pady=10)

        # Autocompletar para Cliente
        tk.Label(frame, text="Cliente:", bg="#d6f0ff", font=("Arial", 14, "bold")).grid(
            row=4, column=0, padx=10, pady=10, sticky="w"
        )

        self.cliente_combobox = ttk.Combobox(frame, **input_style)
        self.cliente_combobox.grid(row=4, column=1, padx=10, pady=10)
        self.cliente_combobox["values"] = self.cargar_clientes()

        # Cantidad de Personas
        tk.Label(
            frame,
            text="Cantidad de Personas:",
            bg="#d6f0ff",
            font=("Arial", 14, "bold"),
        ).grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.personas_combobox = ttk.Combobox(
            frame, values=[1, 2, 3], state="readonly", **input_style
        )
        self.personas_combobox.grid(row=5, column=1, padx=10, pady=10)
        self.personas_label_status = tk.Label(frame, text="", bg="#d6f0ff", fg="red")
        self.personas_label_status.grid(row=5, column=2, padx=10, pady=10)
        self.personas_combobox.current(0)

        # Botón para registrar
        self.registrar_button = ttk.Button(
            frame,
            text="Registrar",
            command=self.registrar_reserva,
            style="RoundedButton.TButton",
            state=tk.DISABLED,
        )
        self.registrar_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Eventos de validación
        self.fecha_entrada_entry.bind("<<DateEntrySelected>>", self.check_fields)
        self.fecha_salida_entry.bind("<<DateEntrySelected>>", self.check_fields)
        self.personas_combobox.bind("<<ComboboxSelected>>", self.check_fields)

    def cargar_clientes(self):
        gestorClientes = GestorCliente()
        clientes = gestorClientes.getClientes()
        return [
            f"{cliente.getId()} - {cliente.getNombre()} {cliente.getApellido()}"
            for cliente in clientes
        ]

    def validar_cantidad_personas(self, idHabitacion, cantidadPersonas):
        habitacionElegida = GestorHabitaciones().getHabitacion(idHabitacion)
        tipoHabitacion = habitacionElegida.getTipo()
        if (
            (tipoHabitacion == "simple" and cantidadPersonas != 1)
            or (tipoHabitacion == "doble" and cantidadPersonas > 2)
            or (tipoHabitacion == "triple" and cantidadPersonas < 3)
        ):
            self.personas_label_status.config(
                text="Cantidad de personas incorrecta para la habitacion.",
                fg="red",
                font=("Arial", 8, "bold"),
                bg="#ffe6e6",
            )
            return False
        else:
            self.personas_label_status.config(
                text="",
                fg="red",
                font=("Arial", 8, "bold"),
                bg="#ffe6e6",
            ) 
            return True

    def cargar_habitaciones_disponibles(self):
        fecha_entrada = self.fecha_entrada_entry.get_date().strftime("%Y-%m-%d")
        fecha_salida = self.fecha_salida_entry.get_date().strftime("%Y-%m-%d")

        gestorReserva = GestorReserva()
        habitaciones_disponibles = gestorReserva.getHabitacionesDisponibles(
            fecha_entrada, fecha_salida
        )

        if habitaciones_disponibles:
            self.habitacion_combobox["values"] = [
                f"{hab.getId()} - Nro: {hab.getNumero()} - {hab.getTipo()}"
                for hab in habitaciones_disponibles
            ]
        else:
            self.habitacion_combobox["values"] = []
            messagebox.showinfo(
                "Sin Disponibilidad", "No hay habitaciones disponibles."
            )

    def registrar_reserva(self):
        gestorReserva = GestorReserva()
        idHabitacion = self.habitacion_combobox.get().split(" - ")[0]
        idCliente = self.cliente_combobox.get().split(" - ")[0]
        # capturar excepciones del metodo registrarReserva de gestorReserva
        try:
            gestorReserva.registrarReserva(
                idHabitacion,
                idCliente,
                self.fecha_entrada_entry.get_date().strftime("%Y-%m-%d"),
                self.fecha_salida_entry.get_date().strftime("%Y-%m-%d"),
                self.personas_combobox.get(),
            )
            messagebox.showinfo("Registro Exitoso", "Reserva registrada con éxito.")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Registro Fallido", str(e))
        self.root.destroy()

    def check_fields(self, event=None):
        # Validar si todos los campos están completos
        if (
            self.fecha_entrada_entry.get()
            and self.fecha_salida_entry.get()
            and self.habitacion_combobox.get()
            and self.cliente_combobox.get()
            and self.personas_combobox.get()
            and self.validar_cantidad_personas(
                int(self.habitacion_combobox.get().split(" - ")[0]),
                int(self.personas_combobox.get()),)
        ):
            self.registrar_button.config(state=tk.NORMAL)
        else:
            self.registrar_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroReserva(root)
    root.mainloop()
