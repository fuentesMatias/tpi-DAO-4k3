import tkinter as tk
from tkinter import messagebox
from services.gestorPdf import GestorPDF
from tkcalendar import DateEntry

class VentanaGenerarReportes:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Reservas")
        self.root.geometry("600x350")
        self.gestorPdf = GestorPDF()

        # Botones principales en la ventana principal
        tk.Button(root, text="Listar Reservas en Periodo", command=self.open_reservas_window).pack(pady=10)
        tk.Button(root, text="Reporte de Ingresos", command=self.gestorPdf.generarPdfIngresos).pack(pady=10)
        tk.Button(root, text="Reporte de Ocupación Promedio", command=self.gestorPdf.generarPdfPromedioOcupacion).pack(pady=10)

    def open_reservas_window(self):
            reservas_window = tk.Toplevel(self.root)
            reservas_window.title("Listar Reservas")

            # Selección de fecha usando DateEntry para el campo 'Desde'
            tk.Label(reservas_window, text="Desde:").pack(pady=5)
            desde_entry = DateEntry(reservas_window, width=12, background='darkblue', foreground='white', borderwidth=2)
            desde_entry.pack(pady=5)

            # Selección de fecha usando DateEntry para el campo 'Hasta'
            tk.Label(reservas_window, text="Hasta:").pack(pady=5)
            hasta_entry = DateEntry(reservas_window, width=12, background='darkblue', foreground='white', borderwidth=2)
            hasta_entry.pack(pady=5)

            def listar_reservas():
                # Obtiene las fechas seleccionadas en el calendario
                desde = desde_entry.get_date()
                hasta = hasta_entry.get_date()

                # Aquí deberías hacer la lógica para listar reservas
                messagebox.showinfo("Reservas", f"Listando reservas desde {desde} hasta {hasta}")

                # Llamada al método para generar el PDF con el rango de fechas seleccionado
                self.gestorPdf.generarPdfReservas(desde, hasta)  # Pasa las fechas al método para generar el PDF

            # Botón para ejecutar la función listar_reservas
            tk.Button(reservas_window, text="Listar", command=listar_reservas).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaGenerarReportes(root)
    root.mainloop()
