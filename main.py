import tkinter as tk
from tkinter import ttk
from database.crear_db import crear_tablas
from gui.registro_cliente import VentanaRegistrarCliente
from gui.registro_habitacion import RegistroHabitacion
from gui.registro_reserva import RegistroReserva
from services.gestorCliente import GestorCliente
import sqlite3
from database.conexion import DbSingleton

def main():
    # Establecer la conexion con la bd creando el objeto conexion
    db = DbSingleton()
    

    root = tk.Tk()
    root.title("Sistema de Gestión de Hotel")
    root.geometry("400x300")
    root.configure(background="#b3e5fc")  # Fondo celeste claro

    # Estilos para los botones
    style = ttk.Style()
    style.theme_use("clam")  # Usa el tema 'clam' que permite mejor personalización
    style.configure("RoundedButton.TButton",
                    background="white",
                    foreground="#4a4a4a",
                    font=("Arial", 12, "bold"),
                    padding=10,
                    relief="flat")
    style.map("RoundedButton.TButton",
              background=[("active", "#e0e0e0")],  # Color al hacer hover
              relief=[("pressed", "sunken")])

    # Crear botones con el nuevo estilo
    ttk.Button(root, text="Registrar Cliente", style="RoundedButton.TButton",
               command=lambda: VentanaRegistrarCliente(tk.Toplevel(root))).pack(pady=10)
    ttk.Button(root, text="Registrar Habitación", style="RoundedButton.TButton",
               command=lambda: RegistroHabitacion(tk.Toplevel(root))).pack(pady=10)
    ttk.Button(root, text="Registrar Reserva", style="RoundedButton.TButton",
               command=lambda: RegistroReserva(tk.Toplevel(root))).pack(pady=10)
    
    
    gestorCliente = GestorCliente()
    gestorCliente.registrarCliente("Juan", "Perez", "Direccion", "12345678", "email")
    cliente = gestorCliente.getClienteById(1)
    print(cliente)
    
    
    
    root.mainloop()

if __name__ == "__main__":
    main()
