import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import DbSingleton
from services.gestorReserva import GestorReserva
from services.gestorCliente import GestorCliente


class IniciarEstadia:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Iniciar Estadia")
        self.ventana.geometry("1100x400")
        
        # centrar la ventana al abrir
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho - 1100) // 2
        y = (pantalla_alto - 400) // 2
        ventana.geometry(f"1100x400+{x}+{y}")
        
        
        
        self.db = DbSingleton()  # Base de datos
        self.gestor_cliente = GestorCliente()
        self.gestor_reservas = GestorReserva()
        self.clientes = self.gestor_cliente.getClientes()  # Traer todos los clientes al abrir

        # Variables
        self.selected_cliente = None
        self.selected_reserva = None

        # Widgets
        tk.Label(self.ventana, text="Buscar Cliente:").grid(row=0, column=0, padx=10, pady=10)

        # Desplegable para búsqueda dinámica
        self.cliente_var = tk.StringVar()
        self.cliente_combobox = ttk.Combobox(
            self.ventana, textvariable=self.cliente_var, width=70
        )
        self.cliente_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.cliente_combobox.bind("<KeyRelease>", self.filtrar_clientes)
        self.cliente_combobox.bind("<<ComboboxSelected>>", self.cargar_reservas)

        # Treeview para mostrar reservas
        self.reservas_tree = ttk.Treeview(
            self.ventana, columns=("ID", "Cliente", "Fecha Inicio", "Fecha Fin", "Estado"), show="headings"
        )

        self.reservas_tree.heading("ID", text="ID Reserva")
        self.reservas_tree.heading("Cliente", text="Cliente")
        self.reservas_tree.heading("Fecha Inicio", text="Fecha Inicio")
        self.reservas_tree.heading("Fecha Fin", text="Fecha Fin")
        self.reservas_tree.heading("Estado", text="Estado")  # Nueva columna

        self.reservas_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.reservas_tree.bind("<<TreeviewSelect>>", self.seleccionar_reserva)

        # Botón para iniciar la estadía
        ttk.Button(self.ventana, text="Iniciar Estadia", command=self.iniciar_estadia).grid(row=2, column=1, pady=20)

        # Cargar clientes en el combobox inicialmente
        self.actualizar_combobox([f"{c.getNombre()} {c.getApellido()}" for c in self.clientes])

    def filtrar_clientes(self, event):
        """Filtra los clientes a medida que se escribe en el combobox."""
        filtro = self.cliente_var.get().lower()
        clientes_filtrados = [
            f"{c.getNombre()} {c.getApellido()}" for c in self.clientes
            if filtro in c.getNombre().lower() or filtro in c.getApellido().lower()
        ]
        self.actualizar_combobox(clientes_filtrados)

    def actualizar_combobox(self, lista):
        """Actualiza las opciones del combobox."""
        self.cliente_combobox["values"] = lista

    def cargar_reservas(self, event):
        """Carga las reservas del cliente seleccionado."""
        cliente_nombre = self.cliente_combobox.get()
        self.selected_cliente = next(
            (c for c in self.clientes if f"{c.getNombre()} {c.getApellido()}" == cliente_nombre), None
        )

        if self.selected_cliente:
            reservas = self.gestor_reservas.getReservasPendientesByIdCliente(self.selected_cliente.getId())
            self.mostrar_reservas(reservas)

    def mostrar_reservas(self, reservas):
        """Muestra las reservas en el Treeview y almacena los objetos completos."""
        # Limpiar Treeview y lista de reservas seleccionadas
        for row in self.reservas_tree.get_children():
            self.reservas_tree.delete(row)

        # Insertar reservas en el Treeview con ID temporal para acceder al objeto
        for reserva in reservas:
            self.reservas_tree.insert(
                "", "end", values=(
                    reserva.getId(),
                    f"{self.selected_cliente.getNombre()} {self.selected_cliente.getApellido()}",
                    reserva.getFechaEntrada(),
                    reserva.getFechaSalida(),
                    reserva.getEstado()  # Agregar estado aquí
                )
            )


    def seleccionar_reserva(self, event):
        """Selecciona una reserva completa al hacer clic en el Treeview."""
        selected_item = self.reservas_tree.focus()
        if selected_item:
            # buscar la reserva seleccionada por ID
            reserva_id = self.reservas_tree.item(selected_item)["values"][0]
            self.selected_reserva = self.gestor_reservas.getReservaById(reserva_id)
        else:
            self.selected_reserva = None

    def iniciar_estadia(self):
        """Inicia la estadía para la reserva seleccionada."""
        if not self.selected_reserva:
            messagebox.showwarning("Advertencia", "Seleccione una reserva.")
            return

        try:
            # Llamar al método para iniciar la estadía
            self.gestor_reservas.iniciar_estadia(self.selected_reserva.getId())
            messagebox.showinfo("Éxito", "Estadía iniciada correctamente.")
            self.ventana.destroy()  # Cerrar la ventana después de iniciar la estadía
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la estadía: {e}")


# Ejecución de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = IniciarEstadia(root)
    root.mainloop()
