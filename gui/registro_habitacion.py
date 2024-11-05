import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import DbSingleton
from services.gestorHabitaciones import GestorHabitaciones

class RegistroHabitacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Habitación")
        self.gestorHabitacion = GestorHabitaciones()
        # Crear los widgets
        tk.Label(root, text="Número").grid(row=0, column=0, padx=5, pady=5)
        self.numero_entry = tk.Entry(root)
        self.numero_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Tipo").grid(row=1, column=0, padx=5, pady=5)
        self.tipo_selector = ttk.Combobox(root, values=["simple", "doble", "suite"])
        self.tipo_selector.grid(row=1, column=1, padx=5, pady=5)
        self.tipo_selector.state(['readonly'])

        tk.Label(root, text="Precio").grid(row=2, column=0, padx=5, pady=5)
        self.precio_entry = tk.Entry(root)
        self.precio_entry.grid(row=2, column=1, padx=5, pady=5)

        self.registrar_btn = tk.Button(root, text="Registrar", command=self.registrar_habitacion, state=tk.DISABLED)
        self.registrar_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Asociar validaciones
        self.numero_entry.bind("<KeyRelease>", self.validar_campos)
        self.tipo_selector.bind("<<ComboboxSelected>>", self.validar_campos)
        self.precio_entry.bind("<KeyRelease>", self.validar_campos)

    def validar_campos(self, event=None):
        """Habilita el botón solo si todos los campos son válidos."""
        numero = self.numero_entry.get().strip()
        tipo = self.tipo_selector.get()
        precio = self.precio_entry.get().strip()

        if numero.isdigit() and tipo and self.es_numero_valido(precio):
            self.registrar_btn.config(state=tk.NORMAL)
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def es_numero_valido(self, valor):
        """Verifica si el valor ingresado es un número flotante positivo."""
        try:
            return float(valor) > 0
        except ValueError:
            return False

    def registrar_habitacion(self):
        """Registra la habitación utilizando un gestor especializado."""
        numero = self.numero_entry.get()
        tipo = self.tipo_selector.get()
        precio = self.precio_entry.get()

        try:
            self.gestorHabitacion.registrarHabitacion(numero, tipo, precio)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la habitación: {e}")
            return
        messagebox.showinfo("Éxito", f"Habitación {numero} registrada con éxito")
        self.limpiar_campos()

    def limpiar_campos(self):
        """Limpia los campos después de registrar la habitación."""
        self.numero_entry.delete(0, tk.END)
        self.tipo_selector.set('')
        self.precio_entry.delete(0, tk.END)
        self.registrar_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroHabitacion(root)
    root.mainloop()
