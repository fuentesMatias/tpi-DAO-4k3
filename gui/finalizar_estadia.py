import tkinter as tk
from tkinter import ttk, messagebox
from services.gestorCliente import GestorCliente
from services.gestorReserva import GestorReserva
from services.gestorFactura import gestorFactura
from database.conexion import DbSingleton


class FinalizarEstadia:
    def __init__(self, root):
        self.root = root
        self.root.title("Finalizar Estadia")
        self.root.geometry("1100x600")

        # Centrar ventana
        pantalla_ancho = root.winfo_screenwidth()
        pantalla_alto = root.winfo_screenheight()
        x = (pantalla_ancho - 1100) // 2
        y = (pantalla_alto - 600) // 2
        root.geometry(f"1100x600+{x}+{y}")
        root.configure(bg="#d6f0ff")  # Fondo de la ventana
        root.resizable(False, False)

        # Estilo de botón y de input
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

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),  # Fuente: Arial, Tamaño: 12, Negrita
            foreground="#4a4a4a",  # Color del texto
            background="#d0e0ff",  # Color de fondo del encabezado
            rowheight=25,  # Altura de los encabezados
        )
        style.map(
            "Treeview.Heading",
            background=[
                ("active", "#b0c4de")
            ],  # Color al interactuar con el encabezado
            foreground=[("active", "#000000")],  # Color de texto al interactuar
        )

        # Fuentes y estilo de input
        input_font = ("Arial", 14)
        input_style = {
            "background": "#ffffff",
            "foreground": "#000000",
            "font": input_font,
        }

        # Conexión a la BD y gestores
        self.db = DbSingleton()
        self.gestor_cliente = GestorCliente()
        self.gestor_reservas = GestorReserva()
        self.gestor_factura = gestorFactura()
        self.clientes = self.gestor_cliente.getClientes()

        # Variables
        self.selected_cliente = None
        self.selected_reserva = None

        # Contenedor principal
        container = tk.Frame(root, bg="#d6f0ff")
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Etiqueta y Combobox para buscar clientes
        tk.Label(
            container, text="Buscar Cliente:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.cliente_var = tk.StringVar()
        self.cliente_combobox = ttk.Combobox(
            container, textvariable=self.cliente_var, width=50, font=input_font
        )
        self.cliente_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.cliente_combobox.bind("<KeyRelease>", self.filtrar_clientes)
        self.cliente_combobox.bind("<<ComboboxSelected>>", self.cargar_reservas)

        # Treeview para mostrar reservas
        self.reservas_tree = ttk.Treeview(
            container,
            columns=("ID", "Habitación", "Fecha Entrada", "Fecha Salida", "Estado"),
            show="headings",
        )
        self.reservas_tree.heading("ID", text="ID Reserva")
        self.reservas_tree.heading("Habitación", text="Habitación")
        self.reservas_tree.heading("Fecha Entrada", text="Fecha Entrada")
        self.reservas_tree.heading("Fecha Salida", text="Fecha Salida")
        self.reservas_tree.heading("Estado", text="Estado")
        self.reservas_tree.grid(
            row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew"
        )

        # Configuración del Treeview con estilo
        self.reservas_tree.tag_configure("oddrow", background="#E8E8E8")
        self.reservas_tree.tag_configure("evenrow", background="#FFFFFF")

        # Botón para finalizar estadía
        self.finalizar_button = ttk.Button(
            container,
            text="Finalizar estadía y Emitir factura",
            command=self.emitir_factura,
            style="RoundedButton.TButton",
        )
        self.finalizar_button.grid(row=2, column=1, pady=20, padx=10)

        # Expansión de filas y columnas
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Cargar clientes en el combobox inicialmente
        self.actualizar_combobox(
            [f"{c.getNombre()} {c.getApellido()}" for c in self.clientes]
        )

    def filtrar_clientes(self, event):
        """Filtra los clientes a medida que se escribe en el combobox."""
        filtro = self.cliente_var.get().lower()
        clientes_filtrados = [
            f"{c.getNombre()} {c.getApellido()}"
            for c in self.clientes
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
            (
                c
                for c in self.clientes
                if f"{c.getNombre()} {c.getApellido()}" == cliente_nombre
            ),
            None,
        )

        if self.selected_cliente:
            reservas = self.gestor_reservas.getReservasFinalizablesByClienteId(
                self.selected_cliente.getId()
            )
            self.mostrar_reservas(reservas)

    def mostrar_reservas(self, reservas):
        """Muestra las reservas en el Treeview y almacena los objetos completos."""
        # Limpiar Treeview
        for row in self.reservas_tree.get_children():
            self.reservas_tree.delete(row)

        for i, reserva in enumerate(reservas):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.reservas_tree.insert(
                "",
                "end",
                iid=i,
                values=(
                    reserva.getId(),
                    reserva.getHabitacion(),
                    reserva.getFechaEntrada(),
                    reserva.getFechaSalida(),
                    reserva.getEstado(),
                ),
                tags=(tag,),
            )

    def emitir_factura(self):
        """Finaliza la estadía y emite la factura."""
        selected_item = self.reservas_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar una reserva")
            return

        reserva_id = self.reservas_tree.item(selected_item)["values"][0]

        try:
            self.gestor_factura.finalizarEstadia(reserva_id)
            messagebox.showinfo(
                "Éxito", "Estadía finalizada y factura emitida con éxito"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error al finalizar estadía: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FinalizarEstadia(root)
    root.mainloop()
