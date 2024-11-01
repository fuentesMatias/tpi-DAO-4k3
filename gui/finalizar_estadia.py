import tkinter as tk
from tkinter import ttk, messagebox
from services.gestorCliente import GestorCliente
from services.gestorReserva import GestorReserva
from services.gestorFactura import gestorFactura
from database.conexion import DbSingleton
import datetime

class FinalizarEstadia:
    def __init__(self, root):
        self.root = root
        self.root.title("Finalizar Estadia")
        self.root.geometry("1000x350")

        # Conexión a la BD y gestor de clientes
        self.db = DbSingleton()
        self.gestor_cliente = GestorCliente()
        self.gestor_reservas = GestorReserva()
        self.gestor_factura = gestorFactura()
        self.clientes = self.gestor_cliente.getClientes()  # Traer todos los clientes al abrir

        # Variables
        self.selected_cliente = None
        self.selected_reserva = None

        # Widgets
        tk.Label(root, text="Buscar Cliente:").grid(row=0, column=0, padx=10, pady=10)

        # Desplegable para búsqueda dinámica
        self.cliente_var = tk.StringVar()
        self.cliente_combobox = ttk.Combobox(
            root, textvariable=self.cliente_var, width=70
        )
        self.cliente_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.cliente_combobox.bind("<KeyRelease>", self.filtrar_clientes)
        self.cliente_combobox.bind("<<ComboboxSelected>>", self.cargar_reservas)

        # Treeview para mostrar reservas
        self.reservas_tree = ttk.Treeview(
            root, columns=("ID", "Habitación", "Fecha Entrada", "Fecha Salida"), show="headings"
        )
        self.reservas_tree.heading("ID", text="ID Reserva")
        self.reservas_tree.heading("Habitación", text="Habitación")
        self.reservas_tree.heading("Fecha Entrada", text="Fecha Entrada")
        self.reservas_tree.heading("Fecha Salida", text="Fecha Salida")
        self.reservas_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.reservas_tree.bind("<<TreeviewSelect>>", self.seleccionar_reserva)

        ttk.Button(root, text="Emitir Factura", command=self.emitir_factura).grid(row=2, column=1, pady=10)

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
            reservas = self.gestor_reservas.getReservasByClienteId(self.selected_cliente.getId())
            self.mostrar_reservas(reservas)

    def mostrar_reservas(self, reservas):
        """Muestra las reservas en el Treeview y almacena los objetos completos."""
        # Limpiar Treeview y lista de reservas seleccionadas
        for row in self.reservas_tree.get_children():
            self.reservas_tree.delete(row)

        # Insertar reservas en el Treeview con ID temporal para acceder al objeto
        self.reserva_objs = {}  # Diccionario para almacenar objetos de reserva por ID temporal
        for i, reserva in enumerate(reservas):
            self.reservas_tree.insert(
                "", "end", iid=i, values=(
                    reserva.getId(),
                    reserva.getHabitacion(),
                    reserva.getFechaEntrada(),
                    reserva.getFechaSalida()
                )
            )
            self.reserva_objs[i] = reserva  # Almacena el objeto `Reserva` completo

    def seleccionar_reserva(self, event):
        """Selecciona una reserva completa al hacer clic en el Treeview."""
        selected_item = self.reservas_tree.focus()
        if selected_item:
            self.selected_reserva = self.reserva_objs[int(selected_item)]  # Obtener el objeto `Reserva` completo

    def emitir_factura(self):
        """Genera la factura para la reserva seleccionada."""
        if not self.selected_reserva or not self.selected_cliente:
            messagebox.showwarning("Advertencia", "Seleccione un cliente y una reserva.")
            return
        
        try:
            self.gestor_factura.registrarFactura(
                self.selected_cliente.getId(),
                self.selected_reserva.getId(),
            )
            messagebox.showinfo("Éxito", "Factura emitida correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo emitir la factura: {e}")

# Ejecución de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = FinalizarEstadia(root)
    root.mainloop()
