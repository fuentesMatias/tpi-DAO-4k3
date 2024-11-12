import tkinter as tk
from tkinter import ttk
import sqlite3
from services.gestorCliente import GestorCliente
from services.gestorReserva import GestorReserva
from services.gestorFactura import gestorFactura
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorEmpleado import GestorEmpleado
from services.gestorAsignacion import GestorAsignacion

class VentanaConsultaEntidades:
    def __init__(self, root):
        self.root = root
        self.root.title("Consultar Entidades del Sistema")
        self.root.geometry("900x500")
        self.root.configure(bg="#d6f0ff")

        # Centrar ventana
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        x = (pantalla_ancho - 900) // 2
        y = (pantalla_alto - 500) // 2
        self.root.geometry(f"900x500+{x}+{y}")
        root.resizable(False, False)

        # Selector de entidades
        tk.Label(
            root, text="Seleccione la entidad a consultar:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.entidades = ["Clientes", "Habitaciones", "Reservas", "Facturas", "Empleados", "Asignaciones"]
        self.selector_entidad = ttk.Combobox(root, values=self.entidades, state="readonly", font=("Arial", 12))
        self.selector_entidad.pack(pady=5)
        self.selector_entidad.bind("<<ComboboxSelected>>", self.mostrar_datos)

        # Contenedor de la tabla de datos
        self.frame_tabla = tk.Frame(root)
        self.frame_tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Tabla con scroll
        self.tree = ttk.Treeview(self.frame_tabla, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

    def mostrar_datos(self, event):
        entidad = self.selector_entidad.get().lower()

        # Limpiar la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Configurar columnas según la entidad seleccionada
        columnas, datos = self.consultar_datos(entidad)

        # Ajustar las columnas y encabezados de la tabla
        self.tree["columns"] = columnas
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')  # Ajustar el ancho de las columnas

            # Mostrar datos en la tabla
        for fila in datos:
            self.tree.insert("", "end", values=fila)

    def consultar_datos(self, entidad):
        # si la entidad es cliente se consulta al gestor de clientes las columnas y los datos
        
        if entidad == "clientes":
            gestor = GestorCliente()
            columnas = ["ID", "Nombre", "Apellido", "direccion", "Teléfono", "Email"]
            objetos = gestor.getClientes()
            # obtener los datos de los clientes en una lista usando objeto.getDato()
            datos = [[cliente.getId(), cliente.getNombre(), cliente.getApellido(), cliente.getDireccion(), cliente.getTelefono(), cliente.getemail()] for cliente in objetos]
            
        elif entidad == "habitaciones":
            gestor = GestorHabitaciones()
            columnas = ["ID","Numero","Tipo","Precio","Estado"]
            objetos = gestor.getHabitaciones()
            # pasar los objetos a una lista de tuplas
            datos = [[habitacion.getId(), habitacion.getNumero(), habitacion.getTipo(), habitacion.getPrecioPorNoche(), habitacion.getEstado()] for habitacion in objetos]

        elif entidad == "reservas":
            gestor = GestorReserva()
            gestorCliente = GestorCliente()
            columnas = ["ID", "Cliente", "Habitación", "Fecha Entrada", "Fecha Salida","Personas", "Estado"]
            objetos = gestor.getReservas()
            datos = [[reserva.getId(), f"{gestorCliente.getClienteById(reserva.getCliente()).getNombre()} {gestorCliente.getClienteById(reserva.getCliente()).getApellido()}", reserva.getHabitacion(), reserva.getFechaEntrada(), reserva.getFechaSalida(),reserva.getCantPersonas(), reserva.getEstado()] for reserva in objetos]

        elif entidad == "facturas":
            gestor = gestorFactura()
            gestorCliente = GestorCliente()
            columnas = ["ID","cliente", "ID Reserva", "Emision", "Total"]
            objetos = gestor.getFacturas()
            datos = [[factura.getId(),f"{gestorCliente.getClienteById(factura.getCliente()).getNombre()} {gestorCliente.getClienteById(factura.getCliente()).getApellido()}", factura.getReserva(), factura.getFechaEmision(), factura.getTotal()] for factura in objetos]
            
        elif entidad == "empleados":
            gestor = GestorEmpleado()
            columnas = ["ID", "Nombre", "Apellido", "Cargo", "sueldo"]
            objetos = gestor.getEmpleados()
            datos = [[empleado.getId(), empleado.getNombre(), empleado.getApellido(), empleado.getCargo(),empleado.getSueldo()] for empleado in objetos]
            
        elif entidad == "asignaciones":
            gestor = GestorAsignacion()
            gestorEmpleado = GestorEmpleado()
            columnas = ["ID", "Habitación", "Empleado", "Fecha"]
            objetos = gestor.getAsignaciones()
            datos = [[asignacion.getId(), asignacion.getHabitacion(), f"{gestorEmpleado.getEmpleadoById(asignacion.getEmpleado()).getNombre()} {gestorEmpleado.getEmpleadoById(asignacion.getEmpleado()).getApellido()}", asignacion.getFecha()] for asignacion in objetos]
            
        return columnas, datos

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaConsultaEntidades(root)
    root.mainloop()
