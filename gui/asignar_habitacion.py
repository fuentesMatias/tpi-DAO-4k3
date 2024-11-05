import tkinter as tk
from tkinter import ttk, messagebox
from services.gestorEmpleado import GestorEmpleado
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorAsignacion import GestorAsignacion
from datetime import date, datetime

class VentanaAsignarEmpleadoAHabitacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Asignar Empleado a Habitación")
        self.root.geometry("600x400")

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
        tk.Label(root, text="Seleccionar Empleado:").grid(row=0, column=0, padx=10, pady=10)
        self.empleado_var = tk.StringVar()
        self.empleado_combobox = ttk.Combobox(root, textvariable=self.empleado_var, width=50, state='readonly')
        self.empleado_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.empleado_combobox.bind("<<ComboboxSelected>>", self.cargar_habitaciones)

        tk.Label(root, text="Seleccionar Habitación:").grid(row=1, column=0, padx=10, pady=10)
        self.habitacion_var = tk.StringVar()
        self.habitacion_combobox = ttk.Combobox(root, textvariable=self.habitacion_var, width=50, state='readonly')
        self.habitacion_combobox.grid(row=1, column=1, padx=10, pady=10)

        # Etiqueta y entrada para la fecha de asignación
        tk.Label(root, text="Fecha (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
        self.fecha_entry = tk.Entry(root)
        self.fecha_entry.grid(row=2, column=1, padx=10, pady=10)

        self.gestorAsignacion.cargarAsignaciones()
        self.gestorAsignacion.getAsignaciones()

        # Botón para asignar
        ttk.Button(root, text="Asignar", command=self.asignar_empleado).grid(row=4, column=1, pady=15)

        # Cargar empleados en el combobox inicialmente
        self.actualizar_combobox(self.empleado_combobox, self.empleados)

    def cargar_habitaciones(self, event):
        """Carga las habitaciones disponibles en el combobox cuando se selecciona un empleado."""
        empleado_seleccionado = self.empleado_combobox.get()
        self.selected_empleado = next(
            (emp for emp in self.empleados if f"{emp.getNombre()} {emp.getApellido()}" == empleado_seleccionado),
            None,
        )

        if self.selected_empleado:
            # Solo cargar habitaciones si hay un empleado seleccionado
            self.actualizar_combobox(self.habitacion_combobox, self.habitaciones)

    def actualizar_combobox(self, combobox, lista):
        """Actualiza las opciones del combobox."""
        if isinstance(lista, list):
            # Si se trata de empleados, mostrar nombre y apellido
            if combobox == self.empleado_combobox:
                combobox["values"] = [f"{emp.getNombre()} {emp.getApellido()}" for emp in lista]
            # Si se trata de habitaciones, mostrar información relevante de las habitaciones
            elif combobox == self.habitacion_combobox:
                combobox["values"] = [h.getId() for h in lista]  # O cualquier otro atributo relevante
        else:
            combobox["values"] = []

    def asignar_empleado(self):
        # Obtener datos del formulario
        habitacion_seleccionada = self.habitacion_combobox.get().strip()
        empleado_seleccionado = self.empleado_combobox.get().strip()

        empleado_id = next(
            emp.getId() for emp in self.empleados if f"{emp.getNombre()} {emp.getApellido()}" == empleado_seleccionado
        )

        fecha_str = self.fecha_entry.get().strip()

        # Validación y conversión de fechas
        try:
            # Validar y convertir la fecha ingresada
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

            # Llamada al gestor para registrar la asignación
            self.gestorAsignacion.registrarAsignacion(
                int(habitacion_seleccionada),
                int(empleado_id),
                fecha,
            )
            messagebox.showinfo("Éxito", "Asignación registrada correctamente.")
            self.root.destroy()

        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo realizar la asignación: {str(e)}")

# Ejecución de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaAsignarEmpleadoAHabitacion(root)
    root.mainloop()
