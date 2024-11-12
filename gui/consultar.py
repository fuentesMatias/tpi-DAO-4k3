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
        
        self.imprimir_boton = None  # Agregar una variable para el botón

        # Centrar ventana
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        x = (pantalla_ancho - 900) // 2
        y = (pantalla_alto - 500) // 2
        self.root.geometry(f"900x500+{x}+{y}")
        root.resizable(False, False)

        # Selector de entidades
        tk.Label(
            root,
            text="Seleccione la consulta a realizar:",
            bg="#d6f0ff",
            font=("Arial", 14, "bold"),
        ).pack(pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            rowheight=40,# Ajusta este valor según la altura deseada
            font=("Arial", 15)
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            foreground="#4a4a4a",
            background="#d0e0ff",
            rowheight=25,
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#b0c4de")],
            foreground=[("active", "#000000")],
        )

        self.entidades = [
            "Clientes",
            "Habitaciones",
            "Reservas",
            "Facturas",
            "Empleados",
            "Asignaciones",
        ]
        self.selector_entidad = ttk.Combobox(
            root, values=self.entidades, state="readonly", font=("Arial", 12)
        )
        self.selector_entidad.pack(pady=5)
        self.selector_entidad.bind("<<ComboboxSelected>>", self.mostrar_datos)

        # Contenedor de la tabla de datos
        self.frame_tabla = tk.Frame(root)
        self.frame_tabla.pack(expand=True, fill="both", padx=10, pady=10)

        # Tabla con scroll
        self.tree = ttk.Treeview(self.frame_tabla, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.frame_tabla, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

    def mostrar_datos(self, event):
            entidad = self.selector_entidad.get().lower()

            # Eliminar cualquier botón de "Imprimir" existente
            if self.imprimir_boton:
                self.imprimir_boton.place_forget()
                self.imprimir_boton = None

            # Limpiar la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Configurar columnas según la entidad seleccionada
            columnas, datos = self.consultar_datos(entidad)

            # Ajustar las columnas y encabezados de la tabla
            self.tree["columns"] = columnas + (["Acciones"] if entidad == "facturas" else [])
            for col in self.tree["columns"]:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100, anchor="center")

            # Mostrar datos en la tabla
            for fila in datos:
                if entidad == "facturas":
                    self.agregar_fila_con_boton(fila)
                else:
                    self.tree.insert("", "end", values=fila)

    def agregar_fila_con_boton(self, fila):
            # Almacena el id de la factura en la etiqueta del Treeview
            item_id = self.tree.insert("", "end", values=fila, tags=(fila[0],))

            # Crear un botón "Imprimir"
            self.imprimir_boton = tk.Button(
                self.tree,
                text="Imprimir",
                command=lambda: self.imprimir_factura(fila[0]),
                bg="lightblue",
                fg="black",
                height=1,
                width=7
            )
            # Agregar el botón al Treeview
            self.tree.item(item_id, tags=("btn",))
            self.tree.bind("<ButtonRelease-1>", lambda e: self.mostrar_botones(e, self.imprimir_boton))

    def mostrar_botones(self, event, btn):
        selected_item = self.tree.focus()
        if not selected_item:
            btn.place_forget()
            return

        item_tags = self.tree.item(selected_item, "tags")
        if "btn" in item_tags:
            bbox = self.tree.bbox(selected_item, column="#{}".format(len(self.tree["columns"])))
            if bbox:
                # Calcular la posición centrada del botón dentro de la columna "Acciones"
                boton_ancho = btn.winfo_reqwidth()
                boton_alto = btn.winfo_reqheight()
                x_centrado = bbox[0] + (bbox[2] - boton_ancho) // 2  # Centrar horizontalmente dentro de la columna
                y_centrado = bbox[1] + (bbox[3] - boton_alto) // 2  # Centrar verticalmente en la celda
                btn.place(x=x_centrado, y=y_centrado)


    def imprimir_factura(self, event):
        # Obtiene el item seleccionado
        selected_item = self.tree.focus()
        if selected_item:
            # Recupera el ID de la factura del item seleccionado
            id_factura = self.tree.item(selected_item, "values")[0]
            
            print(f"Imprimiendo factura con ID: {id_factura}")
            gestor = gestorFactura()
            gestor.imprimirFacturaPDF(gestor.getFacturaById(id_factura))

    def consultar_datos(self, entidad):
        if entidad == "clientes":
            gestor = GestorCliente()
            columnas = ["ID", "Nombre", "Apellido", "direccion", "Teléfono", "Email"]
            objetos = gestor.getClientes()
            datos = [
                [
                    cliente.getId(),
                    cliente.getNombre(),
                    cliente.getApellido(),
                    cliente.getDireccion(),
                    cliente.getTelefono(),
                    cliente.getemail(),
                ]
                for cliente in objetos
            ]
        elif entidad == "habitaciones":
            gestor = GestorHabitaciones()
            columnas = ["ID", "Numero", "Tipo", "Precio", "Estado"]
            objetos = gestor.getHabitaciones()
            datos = [
                [
                    habitacion.getId(),
                    habitacion.getNumero(),
                    habitacion.getTipo(),
                    f"${habitacion.getPrecioPorNoche()}",
                    habitacion.getEstado(),
                ]
                for habitacion in objetos
            ]
        elif entidad == "reservas":
            gestor = GestorReserva()
            gestorCliente = GestorCliente()
            columnas = [
                "ID",
                "Cliente",
                "Habitación",
                "Fecha Entrada",
                "Fecha Salida",
                "Personas",
                "Estado",
            ]
            objetos = gestor.getReservas()
            datos = [
                [
                    reserva.getId(),
                    f"{gestorCliente.getClienteById(reserva.getCliente()).getNombre()} {gestorCliente.getClienteById(reserva.getCliente()).getApellido()}",
                    reserva.getHabitacion(),
                    reserva.getFechaEntrada(),
                    reserva.getFechaSalida(),
                    reserva.getCantPersonas(),
                    reserva.getEstado(),
                ]
                for reserva in objetos
            ]
        elif entidad == "facturas":
            gestor = gestorFactura()
            gestorCliente = GestorCliente()
            columnas = ["ID", "cliente", "ID Reserva", "Emision", "Total"]
            objetos = gestor.getFacturas()
            datos = [
                [
                    factura.getId(),
                    f"{gestorCliente.getClienteById(factura.getCliente()).getNombre()} {gestorCliente.getClienteById(factura.getCliente()).getApellido()}",
                    factura.getReserva(),
                    factura.getFechaEmision(),
                    f"${factura.getTotal()}",
                ]
                for factura in objetos
            ]
        elif entidad == "empleados":
            gestor = GestorEmpleado()
            columnas = ["ID", "Nombre", "Apellido", "Cargo", "sueldo"]
            objetos = gestor.getEmpleados()
            datos = [
                [
                    empleado.getId(),
                    empleado.getNombre(),
                    empleado.getApellido(),
                    empleado.getCargo(),
                    empleado.getSueldo(),
                ]
                for empleado in objetos
            ]
        elif entidad == "asignaciones":
            gestor = GestorAsignacion()
            gestorEmpleado = GestorEmpleado()
            columnas = ["ID", "Habitación", "Empleado", "Fecha"]
            objetos = gestor.getAsignaciones()
            datos = [
                [
                    asignacion.getId(),
                    asignacion.getHabitacion().getNumero(),
                    f"{asignacion.getEmpleado().getNombre()} {asignacion.getEmpleado().getApellido()}",
                    asignacion.getFecha(),
                ]
                for asignacion in objetos
            ]

        return columnas, datos


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaConsultaEntidades(root)
    root.mainloop()
