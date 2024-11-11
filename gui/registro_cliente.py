import tkinter as tk
from tkinter import ttk, messagebox
from database.conexion import DbSingleton
from services.gestorCliente import GestorCliente


class VentanaRegistrarCliente:

    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Cliente")
        # centrar
        pantalla_ancho = root.winfo_screenwidth()
        pantalla_alto = root.winfo_screenheight()
        x = (pantalla_ancho - 800) // 2
        y = (pantalla_alto - 550) // 2
        root.geometry(f"800x550+{x}+{y}")
        self.root.configure(bg="#d6f0ff")  # Color de fondo
        root.resizable(False, False)

        container = tk.Frame(root, bg="#d6f0ff")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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

        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()

        self.nombre_var.trace_add("write", self.validate_form)
        self.apellido_var.trace_add("write", self.validate_form)
        self.direccion_var.trace_add("write", self.validate_form)
        self.telefono_var.trace_add("write", self.validate_form)
        self.email_var.trace_add("write", self.validate_form)

        # Creación de etiquetas, campos de entrada y etiquetas de estado
        tk.Label(
            container, text="Nombre", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, pady=10, sticky="w")
        self.nombre_entry = tk.Entry(
            container, textvariable=self.nombre_var, font=("Arial", 14)
        )
        self.nombre_entry.grid(row=0, column=1, pady=5)
        self.nombre_entry.bind(
            "<KeyRelease>", lambda event: self.validate_max_length(event, 30)
        )
        self.nombre_entry.bind("<KeyRelease>", self.validate_alpha)
        self.nombre_status = tk.Label(container, text="", fg="red", bg="#d6f0ff")
        self.nombre_status.grid(row=0, column=2, padx=(10, 0), pady=(0, 5))

        tk.Label(
            container, text="Apellido", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=1, column=0, pady=10, sticky="w")
        self.apellido_entry = tk.Entry(
            container, textvariable=self.apellido_var, font=("Arial", 14)
        )
        self.apellido_entry.grid(row=1, column=1, pady=5)
        self.apellido_entry.bind(
            "<KeyRelease>", lambda event: self.validate_max_length(event, 30)
        )
        self.apellido_entry.bind("<KeyRelease>", self.validate_alpha)
        self.apellido_status = tk.Label(container, text="", fg="red", bg="#d6f0ff")
        self.apellido_status.grid(row=1, column=2, padx=(10, 0), pady=(0, 5))

        tk.Label(
            container, text="Dirección", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=2, column=0, pady=10, sticky="w")
        self.direccion_entry = tk.Entry(
            container, textvariable=self.direccion_var, font=("Arial", 14)
        )
        self.direccion_entry.grid(row=2, column=1, pady=5)
        self.direccion_entry.bind(
            "<KeyRelease>", lambda event: self.validate_max_length(event, 30)
        )
        self.direccion_status = tk.Label(container, text="", fg="red", bg="#d6f0ff")
        self.direccion_status.grid(row=2, column=2, padx=(10, 0), pady=(0, 5))

        tk.Label(
            container, text="Teléfono", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=3, column=0, pady=10, sticky="w")
        self.telefono_entry = tk.Entry(
            container, textvariable=self.telefono_var, font=("Arial", 14)
        )
        self.telefono_entry.grid(row=3, column=1, pady=5)
        self.telefono_entry.bind("<KeyRelease>", self.validate_numeric)
        self.telefono_status = tk.Label(container, text="", fg="red", bg="#d6f0ff")
        self.telefono_status.grid(row=3, column=2, padx=(10, 0), pady=(0, 5))

        tk.Label(
            container, text="Email", bg="#d6f0ff", font=("Arial", 14, "bold")
        ).grid(row=4, column=0, pady=10, sticky="w")
        self.mail_entry = tk.Entry(
            container, textvariable=self.email_var, font=("Arial", 14)
        )
        self.mail_entry.grid(row=4, column=1, pady=5)
        self.email_status = tk.Label(container, text="", fg="red", bg="#d6f0ff")
        self.email_status.grid(row=4, column=2, padx=(10, 0), pady=(0, 5))

        self.register_button = ttk.Button(
            container,
            text="Registrar",
            command=self.registrar_cliente,
            state=tk.DISABLED,
            style="RoundedButton.TButton",
        )

        self.register_button.grid(row=5, column=0, columnspan=2, pady=20)

    def validate_alpha(self, event):
        current_value = event.widget.get()
        if not current_value.isalpha():
            event.widget.delete(0, tk.END)
            valid_value = "".join(
                filter(lambda c: c.isalpha() or c.isspace(), current_value)
            )[:30]
            event.widget.insert(0, valid_value)

    def validate_numeric(self, event):
        current_value = self.telefono_var.get()
        if not current_value.isdigit():
            self.telefono_var.set("".join(filter(str.isdigit, current_value)))
        elif len(current_value) > 10:
            self.telefono_var.set(current_value[:10])

    def validate_address(self, address):
        # Filtra los caracteres alfabéticos de la dirección
        chars = [char for char in address if char.isalpha()]
        numbers = [char for char in address if char.isdigit()]
        # Verifica que haya al menos 3 letras y menos de 6 números
        return len(chars) >= 3 and len(numbers) <= 6
    
    def validate_mail(self, email):
        chars = [char for char in email if char.isalpha()]
        return "@" in email and "." in email and len(chars) >= 4 and chars[0] != "@" and chars[-1] != "."

    def validate_form(self, *args):
        # Limpiamos todos los mensajes de error al iniciar la validación
        for status_label_name in [
            "nombre_status",
            "apellido_status",
            "direccion_status",
            "telefono_status",
            "email_status",
        ]:
            status_label = getattr(self, status_label_name)
            status_label.config(text="", bg="#d6f0ff")

        # Validamos cada campo uno a la vez, si encuentra un error, lo muestra y se detiene
        if not self.check_field(
        self.nombre_var,
        "nombre_status",
        lambda v: 2 <= len(v.strip()) <= 30,
        "Nombre inválido",
        ):
            return

        if not self.check_field(
            self.apellido_var,
            "apellido_status",
            lambda v: 2 <= len(v.strip()) <= 30,
            "Apellido inválido",
        ):
            return

        if not self.check_field(
            self.direccion_var,
            "direccion_status",
            lambda v: 5 <= len(v.strip()) <= 30 and self.validate_address(v),
            "Dirección inválida",
        ):
            return

        if not self.check_field(
            self.telefono_var,
            "telefono_status",
            lambda v: len(v) == 10,
            "Teléfono inválido",
        ):
            return

        if not self.check_field(
            self.email_var,
            "email_status",
            lambda v: self.validate_mail(v),
            "Email inválido",
        ):
            return

        # Habilitar el botón si todo está validado
        self.register_button.config(state=tk.NORMAL)

    def validate_max_length(self, event, max_length=30):
        current_value = event.widget.get()
        if len(current_value) > max_length:
            event.widget.delete(max_length, tk.END)

    def check_field(self, var, status_label_name, condition, error_message):
        status_label = getattr(self, status_label_name)
        value = var.get()
        if condition(value):
            status_label.config(
                text="✔️", fg="green", font=("Arial", 12, "bold"), bg="#d6f0ff"
            )
            return True
        else:
            # Configuramos el mensaje de error con estilo uniforme
            status_label.config(
                text=error_message,
                fg="red",
                font=("Arial", 12, "bold"),
                bg="#ffe6e6",  # Fondo rojo claro para indicar error
            )
            self.register_button.config(
                state=tk.DISABLED
            )  # Deshabilitar botón en caso de error
            return False

    def registrar_cliente(self):
        nombre = self.nombre_var.get()
        apellido = self.apellido_var.get()
        direccion = self.direccion_var.get()
        telefono = self.telefono_var.get()
        email = self.email_var.get()

        try:
            gestorCliente = GestorCliente()
            gestorCliente.registrarCliente(nombre, apellido, direccion, telefono, email)
            messagebox.showinfo(
                "Éxito", f"Cliente {nombre} {apellido} registrado con éxito"
            )
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar cliente: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaRegistrarCliente(root)
    root.mainloop()
