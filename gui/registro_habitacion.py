import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import DbSingleton
from services.gestorHabitaciones import GestorHabitaciones

class RegistroHabitacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Habitación")
        self.root.geometry("400x180")  # Tamaño fijo de la ventana
        self.gestorHabitacion = GestorHabitaciones()

        # Centrar la ventana en la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 400) // 2
        y = (screen_height - 180) // 2
        root.geometry(f"400x180+{x}+{y}")

        # Crear widgets
        tk.Label(root, text="Número").grid(row=0, column=0, padx=5, pady=5)
        self.numero_entry = tk.Entry(root, validate="key", validatecommand=(root.register(self.validar_entrada_numerica), "%P"))
        self.numero_entry.grid(row=0, column=1, padx=5, pady=5)

        # Etiqueta para mostrar mensajes de error junto al número
        self.error_label = tk.Label(root, text="", fg="red")
        self.error_label.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Tipo").grid(row=1, column=0, padx=5, pady=5)
        self.tipo_selector = ttk.Combobox(root, values=["simple", "doble", "suite"], state='readonly')
        self.tipo_selector.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Precio").grid(row=2, column=0, padx=5, pady=5)
        self.precio_entry = tk.Entry(root, validate="key", validatecommand=(root.register(self.validar_entrada_numerica), "%P"))
        self.precio_entry.grid(row=2, column=1, padx=5, pady=5)

        self.registrar_btn = tk.Button(root, text="Registrar", command=self.registrar_habitacion, state=tk.DISABLED)
        self.registrar_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Vincular eventos de validación
        self.numero_entry.bind("<KeyRelease>", self.validar_numero)
        self.tipo_selector.bind("<<ComboboxSelected>>", self.validar_tipo)
        self.precio_entry.bind("<KeyRelease>", self.validar_precio)

    def validar_entrada_numerica(self, valor):
        """Permite solo números en las entradas de texto."""
        if valor == "" or valor.isdigit():  # Permite valores vacíos o números
            return True
        else:
            return False

    def validar_numero(self, event=None):
        """Valida la entrada del número de habitación."""
        numero = self.numero_entry.get().strip()
        
        if numero.isdigit():
            numero_int = int(numero)
            if numero_int > 0:
                if self.numero_ya_registrado(numero_int):
                    self.error_label.config(text="Número ya registrado")
                    self.registrar_btn.config(state=tk.DISABLED)
                else:
                    self.error_label.config(text="")  # Limpiar mensaje de error previo
                    self.validar_formulario_completo()
            else:
                self.error_label.config(text="Número no válido")
                self.registrar_btn.config(state=tk.DISABLED)
        else:
            self.error_label.config(text="Número no válido")
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_tipo(self, event=None):
        """Valida que se haya seleccionado un tipo de habitación."""
        tipo = self.tipo_selector.get()
        if tipo:
            self.validar_formulario_completo()
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_precio(self, event=None):
        """Valida que el precio sea un número positivo."""
        precio = self.precio_entry.get().strip()
        if self.es_numero_valido(precio):
            self.validar_formulario_completo()
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_formulario_completo(self):
        """Habilita el botón de registro si todos los campos son válidos."""
        numero = self.numero_entry.get().strip()
        tipo = self.tipo_selector.get()
        precio = self.precio_entry.get().strip()

        # Asegurar que todas las validaciones pasen antes de habilitar el botón
        if numero.isdigit() and int(numero) > 0 and not self.numero_ya_registrado(int(numero)) \
                and tipo and self.es_numero_valido(precio):
            self.registrar_btn.config(state=tk.NORMAL)
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def numero_ya_registrado(self, numero):
        """Verifica si el número de habitación ya está registrado."""
        habitaciones = self.gestorHabitacion.obtenerNumerosHabitaciones()
        return numero in map(int, habitaciones)

    def es_numero_valido(self, valor):
        """Verifica si el valor ingresado es un número positivo."""
        try:
            return float(valor) > 0
        except ValueError:
            return False

    def registrar_habitacion(self):
        """Registra la habitación usando el gestor especializado."""
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
        """Limpia los campos después de registrar la habitación."""
        self.numero_entry.delete(0, tk.END)
        self.tipo_selector.set('')
        self.precio_entry.delete(0, tk.END)
        self.error_label.config(text="")
        self.registrar_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroHabitacion(root)
    root.mainloop()
