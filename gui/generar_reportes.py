import tkinter as tk
from tkinter import ttk, messagebox
from services.gestorPdf import GestorPDF
from tkcalendar import DateEntry


class VentanaGenerarReportes:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Reservas")
        self.root.geometry("700x400")
        self.root.configure(bg="#d6f0ff")
        # centrar
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        x = (pantalla_ancho - 700) // 2
        y = (pantalla_alto - 400) // 2
        self.root.geometry(f"700x400+{x}+{y}")
        self.root.configure(bg="#d6f0ff")  # Color de fondo
        root.resizable(False, False)
        self.gestorPdf = GestorPDF()

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

        # Botones principales en la ventana principal
        ttk.Button(
            root,
            text="Listar Reservas en Periodo",
            command=self.open_reservas_window,
            style="RoundedButton.TButton",
        ).pack(pady=10)
        ttk.Button(
            root,
            text="Reporte de Ingresos",
            command=self.gestorPdf.generarPdfIngresos,
            style="RoundedButton.TButton",
        ).pack(pady=10)
        ttk.Button(
            root,
            text="Reporte de Ocupación Promedio",
            command=self.gestorPdf.generarPdfPromedioOcupacion,
            style="RoundedButton.TButton",
        ).pack(pady=10)

    def open_reservas_window(self):
        reservas_window = tk.Toplevel(self.root)
        reservas_window.title("Listar Reservas")
        
        # Ajustar el tamaño de la ventana
        reservas_window.geometry("500x300")

        # Centrar la ventana secundaria
        pantalla_ancho = self.root.winfo_screenwidth()
        pantalla_alto = self.root.winfo_screenheight()
        x = (pantalla_ancho - 500) // 2
        y = (pantalla_alto - 300) // 2
        reservas_window.geometry(f"500x300+{x}+{y}")
        
        reservas_window.configure(bg="#d6f0ff")  # Color de fondo

        # Selección de fecha usando DateEntry para el campo 'Desde'
        tk.Label(
            reservas_window, text="Desde:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).pack(pady=5)
        desde_entry = DateEntry(
            reservas_window,
            width=12,
            font=("Arial", 12),
            background="#ffffff",
            foreground="000000",
            borderwidth=2,
        )
        desde_entry.pack(pady=5)

        # Selección de fecha usando DateEntry para el campo 'Hasta'
        tk.Label(
            reservas_window, text="Hasta:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).pack(pady=5)
        hasta_entry = DateEntry(
            reservas_window,
            width=12,
            font=("Arial", 12),
            background="#ffffff",
            foreground="000000",
            borderwidth=2,
        )
        hasta_entry.pack(pady=5)

        def listar_reservas():
            # Obtiene las fechas seleccionadas en el calendario
            desde = desde_entry.get_date()
            hasta = hasta_entry.get_date()

            # Aquí deberías hacer la lógica para listar reservas
            messagebox.showinfo(
                "Reservas", f"Listando reservas desde {desde} hasta {hasta}."
            )

            # Llamada al método para generar el PDF con el rango de fechas seleccionado
            self.gestorPdf.generarPdfReservas(desde, hasta)
            self.root.destroy()

        # Botón para ejecutar la función listar_reservas
        ttk.Button(
            reservas_window,
            text="Listar",
            command=listar_reservas,
            style="RoundedButton.TButton",
        ).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaGenerarReportes(root)
    root.mainloop()
