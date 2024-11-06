import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import DbSingleton
from services.gestorHabitaciones import GestorHabitaciones

class RegistroHabitacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Habitación")
        self.root.geometry("400x180")  # Fixed window size
        self.gestorHabitacion = GestorHabitaciones()

        # Center window on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 180) // 2
        root.geometry(f"400x180+{x}+{y}")

        # Create widgets
        tk.Label(root, text="Número").grid(row=0, column=0, padx=5, pady=5)
        self.numero_entry = tk.Entry(root)
        self.numero_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label for displaying error message next to room number input
        self.error_label = tk.Label(root, text="", fg="red")
        self.error_label.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Tipo").grid(row=1, column=0, padx=5, pady=5)
        self.tipo_selector = ttk.Combobox(root, values=["simple", "doble", "suite"], state='readonly')
        self.tipo_selector.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Precio").grid(row=2, column=0, padx=5, pady=5)
        self.precio_entry = tk.Entry(root)
        self.precio_entry.grid(row=2, column=1, padx=5, pady=5)

        self.registrar_btn = tk.Button(root, text="Registrar", command=self.registrar_habitacion, state=tk.DISABLED)
        self.registrar_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Bind validation events
        self.numero_entry.bind("<KeyRelease>", self.validar_numero)
        self.tipo_selector.bind("<<ComboboxSelected>>", self.validar_tipo)
        self.precio_entry.bind("<KeyRelease>", self.validar_precio)

    def validar_numero(self, event=None):
        """Validate the room number input."""
        numero = self.numero_entry.get().strip()
        
        if numero.isdigit():
            numero_int = int(numero)
            if numero_int > 0:
                if self.numero_ya_registrado(numero_int):
                    self.error_label.config(text="Número ya registrado")
                    self.registrar_btn.config(state=tk.DISABLED)
                else:
                    self.error_label.config(text="")  # Clear any previous error message
                    self.validar_formulario_completo()
            else:
                self.error_label.config(text="Número no válido")
                self.registrar_btn.config(state=tk.DISABLED)
        else:
            self.error_label.config(text="Número no válido")
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_tipo(self, event=None):
        """Validate that a room type has been selected."""
        tipo = self.tipo_selector.get()
        if tipo:
            self.validar_formulario_completo()
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_precio(self, event=None):
        """Validate that the price is a positive number."""
        precio = self.precio_entry.get().strip()
        if self.es_numero_valido(precio):
            self.validar_formulario_completo()
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_formulario_completo(self):
        """Enable the register button if all fields are valid."""
        numero = self.numero_entry.get().strip()
        tipo = self.tipo_selector.get()
        precio = self.precio_entry.get().strip()

        # Ensure all validations pass before enabling the button
        if numero.isdigit() and int(numero) > 0 and not self.numero_ya_registrado(int(numero)) \
                and tipo and self.es_numero_valido(precio):
            self.registrar_btn.config(state=tk.NORMAL)
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def numero_ya_registrado(self, numero):
        """Check if the room number is already registered."""
        habitaciones = self.gestorHabitacion.obtenerNumerosHabitaciones()
        return numero in map(int, habitaciones)

    def es_numero_valido(self, valor):
        """Verify if the entered value is a positive number."""
        try:
            return float(valor) > 0
        except ValueError:
            return False

    def registrar_habitacion(self):
        """Register the room using a specialized manager."""
        numero = int(self.numero_entry.get())
        tipo = self.tipo_selector.get()
        precio = self.precio_entry.get()

        try:
            self.gestorHabitacion.registrarHabitacion(numero, tipo, precio)
            messagebox.showinfo("Éxito", f"Habitación {numero} registrada con éxito")
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la habitación: {e}")

    def limpiar_campos(self):
        """Clear fields after registering the room."""
        self.numero_entry.delete(0, tk.END)
        self.tipo_selector.set('')
        self.precio_entry.delete(0, tk.END)
        self.error_label.config(text="")
        self.registrar_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroHabitacion(root)
    root.mainloop()
