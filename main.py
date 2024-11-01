import tkinter as tk
from tkinter import ttk
from database.conexion import DbSingleton
from gui.registro_cliente import VentanaRegistrarCliente
from gui.registro_habitacion import RegistroHabitacion
from gui.registro_reserva import RegistroReserva
from gui.finalizar_estadia import FinalizarEstadia
from services.gestorCliente import GestorCliente
from services.gestorHabitaciones import GestorHabitaciones

def abrir_ventana(ventana_clase, root):
    ventana = tk.Toplevel(root)
    instancia = ventana_clase(ventana)
    ventana.protocol("WM_DELETE_WINDOW", ventana.destroy)  # Destruye completamente al cerrarse

def main():
    # Establecer la conexión con la base de datos
    db = DbSingleton()

    # Crear ventana principal
    root = tk.Tk()
    root.title("Sistema de Gestión de Hotel")
    root.geometry("400x350")
    root.configure(background="#b3e5fc")

    # Estilos personalizados para botones
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("RoundedButton.TButton",
                    background="white",
                    foreground="#4a4a4a",
                    font=("Arial", 12, "bold"),
                    padding=10,
                    relief="flat")
    style.map("RoundedButton.TButton",
              background=[("active", "#e0e0e0")],
              relief=[("pressed", "sunken")])

    # Botones principales
    ttk.Button(root, text="Registrar Cliente", style="RoundedButton.TButton",
               command=lambda: abrir_ventana(VentanaRegistrarCliente, root)).pack(pady=10)
    ttk.Button(root, text="Registrar Habitación", style="RoundedButton.TButton",
               command=lambda: abrir_ventana(RegistroHabitacion, root)).pack(pady=10)
    ttk.Button(root, text="Registrar Reserva", style="RoundedButton.TButton",
               command=lambda: abrir_ventana(RegistroReserva, root)).pack(pady=10)
    ttk.Button(root, text="Finalizar Estadia", style="RoundedButton.TButton",
               command=lambda: abrir_ventana(FinalizarEstadia, root)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
