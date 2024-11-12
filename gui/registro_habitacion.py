import tkinter as tk
from tkinter import ttk, messagebox
from services.gestorHabitaciones import GestorHabitaciones

class RegistroHabitacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Habitación")
        self.root.geometry("700x480")
        self.root.configure(bg="#d6f0ff")  # Color de fondo
        self.gestorHabitacion = GestorHabitaciones()

        # Centrar la ventana en la pantalla
        pantalla_ancho = root.winfo_screenwidth()
        pantalla_alto = root.winfo_screenheight()
        x = (pantalla_ancho - 700) // 2
        y = (pantalla_alto - 480) // 2
        root.geometry(f"700x480+{x}+{y}")

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

        # Fuentes y estilo de input
        input_font = ("Arial", 14)
        input_style = {
            "background": "#ffffff",
            "foreground": "#000000",
            "font": input_font,
        }

        # Crear Frame centrado
        frame = tk.Frame(root, bg="#d6f0ff")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Widgets
        tk.Label(
            frame, text="Número de Habitación:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.numero_entry = tk.Entry(
            frame, validate="key",
            validatecommand=(root.register(self.validar_entrada_numerica), "%P"),
            **input_style
        )
        self.numero_entry.grid(row=0, column=1, padx=10, pady=10)

        # Etiqueta para mensajes de error
        self.error_label = tk.Label(frame, text="", fg="red", bg="#d6f0ff", font=("Arial", 12))
        self.error_label.grid(row=0, column=2, padx=5, pady=5)

        tk.Label(
            frame, text="Tipo de Habitación:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.tipo_selector = ttk.Combobox(
            frame, values=["simple", "doble", "suite"], state='readonly', font=("Arial", 12)
        )
        self.tipo_selector.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(
            frame, text="Precio:", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        
        self.precio_entry = tk.Entry(
            frame, validate="key",
            validatecommand=(root.register(self.validar_entrada_numerica), "%P"),
            **input_style
        )
        self.precio_entry.grid(row=2, column=1, padx=10, pady=10)

        # Botón para registrar
        self.registrar_btn = ttk.Button(
            frame, text="Registrar", command=self.registrar_habitacion,
            style="RoundedButton.TButton", state=tk.DISABLED
        )
        self.registrar_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # Eventos de validación
        self.numero_entry.bind("<KeyRelease>", self.validar_numero)
        self.tipo_selector.bind("<<ComboboxSelected>>", self.validar_tipo)
        self.precio_entry.bind("<KeyRelease>", self.validar_precio)

    def validar_entrada_numerica(self, valor):
        """Permite solo números en las entradas de texto."""
        return valor.isdigit() or valor == ""

    def validar_numero(self, event=None):
        numero = self.numero_entry.get().strip()
        if numero.isdigit() and int(numero) > 0:
            if self.numero_ya_registrado(int(numero)):
                self.error_label.config(text="Número ya registrado")
                self.registrar_btn.config(state=tk.DISABLED)
            else:
                self.error_label.config(text="")
                self.validar_formulario_completo()
        else:
            self.error_label.config(text="Número no válido")
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_tipo(self, event=None):
        tipo = self.tipo_selector.get()
        if tipo:
            self.validar_formulario_completo()
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_precio(self, event=None):
        precio = self.precio_entry.get().strip()
        if self.es_numero_valido(precio):
            self.validar_formulario_completo()
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def validar_formulario_completo(self):
        numero = self.numero_entry.get().strip()
        tipo = self.tipo_selector.get()
        precio = self.precio_entry.get().strip()
        if numero and tipo and self.es_numero_valido(precio) and not self.numero_ya_registrado(int(numero)):
            self.registrar_btn.config(state=tk.NORMAL)
        else:
            self.registrar_btn.config(state=tk.DISABLED)

    def numero_ya_registrado(self, numero):
        habitaciones = self.gestorHabitacion.obtenerNumerosHabitaciones()
        return numero in map(int, habitaciones)

    def es_numero_valido(self, valor):
        try:
            return float(valor) > 0
        except ValueError:
            return False

    def registrar_habitacion(self):
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
        self.numero_entry.delete(0, tk.END)
        self.tipo_selector.set('')
        self.precio_entry.delete(0, tk.END)
        self.error_label.config(text="")
        self.registrar_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroHabitacion(root)
    root.mainloop()
