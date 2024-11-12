import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from services.gestorEmpleado import GestorEmpleado
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorAsignacion import GestorAsignacion
from datetime import datetime, date


class VentanaAsignarEmpleadoAHabitacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Asignar Empleado a Habitación")
        self.root.geometry("1000x650")
        self.root.configure(bg="#d6f0ff")
        # centrar ventana en pantalla
        pantalla_ancho = root.winfo_screenwidth()
        pantalla_alto = root.winfo_screenheight()
        x = (pantalla_ancho - 1000) // 2
        y = (pantalla_alto - 650) // 2
        root.geometry(f"1000x650+{x}+{y}")

        # Frame principal centrado
        self.main_frame = tk.Frame(root, bg="#d6f0ff")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

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

        input_font = ("Arial", 12)
        input_style = {
            "background": "#ffffff",
            "foreground": "#333333",
            "font": input_font,
        }

        # Instancias de los gestores
        self.gestorAsignacion = GestorAsignacion()
        self.gestorEmpleados = GestorEmpleado()
        self.gestorHabitaciones = GestorHabitaciones()

        # Obtener datos iniciales
        self.empleados = self.gestorEmpleados.getEmpleados()
        self.habitaciones = self.gestorHabitaciones.getHabitaciones()

        # Variables
        self.selected_empleado = None
        self.selected_habitacion = None

        # Widgets
        tk.Label(
            self.main_frame,
            text="Fecha de Asignación:",
            bg="#d6f0ff",
            font=("Arial", 14, "bold"),
        ).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.fecha_entry = DateEntry(
            self.main_frame, date_pattern="yyyy-MM-dd", width=47, mindate=date.today()
        )
        self.fecha_entry.grid(row=0, column=1, padx=10, pady=10)
        self.fecha_entry.bind(
            "<<DateEntrySelected>>", self.cargar_habitaciones_disponibles
        )

        tk.Label(
            self.main_frame,
            text="Seleccionar Empleado:",
            bg="#d6f0ff",
            font=("Arial", 14, "bold"),
        ).grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.empleado_var = tk.StringVar()
        self.empleado_combobox = ttk.Combobox(
            self.main_frame,
            textvariable=self.empleado_var,
            width=50,
            state="readonly",
            **input_style,
        )
        self.empleado_combobox.grid(row=1, column=1, padx=10, pady=10)
        self.empleado_combobox.bind(
            "<<ComboboxSelected>>", self.cargar_habitaciones_disponibles
        )

        tk.Label(
            self.main_frame,
            text="Seleccionar Habitación:",
            bg="#d6f0ff",
            font=("Arial", 14, "bold"),
        ).grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.habitacion_var = tk.StringVar()
        self.habitacion_combobox = ttk.Combobox(
            self.main_frame,
            textvariable=self.habitacion_var,
            width=50,
            state="readonly",
            **input_style,
        )
        self.habitacion_combobox.grid(row=2, column=1, padx=10, pady=10)

        # Botón para asignar
        ttk.Button(
            self.main_frame,
            text="Asignar",
            style="RoundedButton.TButton",
            command=self.asignar_empleado,
        ).grid(row=3, column=1, pady=20)

        # Cargar empleados en el combobox inicialmente
        self.actualizar_combobox(self.empleado_combobox, self.empleados)

    def cargar_habitaciones_disponibles(self, event=None):
        """Carga las habitaciones disponibles en el combobox según la fecha seleccionada."""
        fecha_seleccionada_str = self.fecha_entry.get()
        try:
            fecha_seleccionada = datetime.strptime(
                fecha_seleccionada_str, "%Y-%m-%d"
            ).date()
            habitaciones_disponibles = self.gestorAsignacion.getHabitacionesParaAsignar(
                fecha_seleccionada
            )
            self.actualizar_combobox(self.habitacion_combobox, habitaciones_disponibles)
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto.")

    def actualizar_combobox(self, combobox, lista):
        """Actualiza las opciones del combobox."""
        if isinstance(lista, list):
            if combobox == self.empleado_combobox:
                combobox["values"] = [
                    f"{emp.getNombre()} {emp.getApellido()}" for emp in lista
                ]
            elif combobox == self.habitacion_combobox:
                combobox["values"] = [h.getId() for h in lista]
        else:
            combobox["values"] = []

    def asignar_empleado(self):
        habitacion_seleccionada = self.habitacion_combobox.get().strip()
        empleado_seleccionado = self.empleado_combobox.get().strip()
        empleado_id = next(
            emp.getId()
            for emp in self.empleados
            if f"{emp.getNombre()} {emp.getApellido()}" == empleado_seleccionado
        )
        fecha_str = self.fecha_entry.get()
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            self.gestorAsignacion.registrarAsignacion(
                int(habitacion_seleccionada), int(empleado_id), fecha
            )
            messagebox.showinfo("Éxito", "Asignación registrada correctamente.")
            self.root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la asignación")


# Ejecución de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaAsignarEmpleadoAHabitacion(root)
    root.mainloop()
