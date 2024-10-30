import tkinter as tk
from tkinter import ttk, messagebox
from services.gestorCliente import GestorCliente
from services.GestorReserva import GestorReserva
from database.conexion import DbSingleton
import datetime

class FinalizarEstadia:
    def __init__(self, root):
        self.root = root
        self.root.title("Finalizar Estadia")
        self.root.geometry("500x350")

        # Conexión a la BD y gestor de clientes
        self.db = DbSingleton()
        self.gestor_cliente = GestorCliente()
        self.gestorReservas = GestorReserva()
        self.clientes = self.gestor_cliente.getClientes()  # Traer todos los clientes al abrir

        # Variables
        self.selected_cliente_id = None

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

        ttk.Button(root, text="Emitir Factura", command=self.emitir_factura).grid(row=2, column=1, pady=10)

        # Cargar clientes en el combobox inicialmente
        self.actualizar_combobox([f"{c.getNombre()} {c.getApellido()}" for c in self.clientes])

    def filtrar_clientes(self, event):
        """Filtra los clientes a medida que se escribe en el combobox."""
        filtro = self.cliente_var.get().lower()
        clientes_filtrados = [
            f"{c.getNombre()} {c.getApellido()}" for c in self.clientes
            if filtro in c.getNombre().lower()
        ]
        self.actualizar_combobox(clientes_filtrados)

    def actualizar_combobox(self, lista):
        """Actualiza las opciones del combobox."""
        self.cliente_combobox["values"] = lista

    def cargar_reservas(self, event):
        """Carga las reservas del cliente seleccionado."""
        cliente_nombre = self.cliente_combobox.get()
        cliente = next(
            (c for c in self.clientes if f"{c.getNombre()} {c.getApellido()}" == cliente_nombre), None
        )

        if cliente:
            self.selected_cliente_id = cliente.getId()
            reservas = self.gestorReservas.getReservasByClienteId(self.selected_cliente_id)
            self.mostrar_reservas(reservas)

    def mostrar_reservas(self, reservas):
        """Muestra las reservas en el Treeview."""
        for row in self.reservas_tree.get_children():
            self.reservas_tree.delete(row)

        for reserva in reservas:
            self.reservas_tree.insert(
                "", "end", values=(
                    reserva.getId(),
                    reserva.getHabitacion().getNumero(),
                    reserva.getFechaEntrada(),
                    reserva.getFechaSalida()
                )
            )

    def emitir_factura(self):
        """Genera la factura para la reserva seleccionada."""
        selected_item = self.reservas_tree.focus()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione una reserva.")
            return

        reserva = self.reservas_tree.item(selected_item, "values")
        reserva_id = reserva[0]

        try:
            fecha_emision = datetime.date.today()
            total = self.gestor_cliente.calcularTotalReserva(reserva_id)

            self.db.execute_query(
                "INSERT INTO facturas (id_cliente, id_reserva, fecha_emision, total) VALUES (?, ?, ?, ?)",
                (self.selected_cliente_id, reserva_id, fecha_emision, total)
            )
            self.db.commit()

            messagebox.showinfo("Éxito", "Factura emitida correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo emitir la factura: {e}")

# Ejecución de la ventana
if __name__ == "__main__":
    root = tk.Tk()
    app = FinalizarEstadia(root)
    root.mainloop()
