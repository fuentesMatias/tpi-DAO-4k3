import tkinter as tk
from tkinter import messagebox
from database.conexion import DbSingleton
from services.gestorCliente import GestorCliente

class VentanaRegistrarCliente:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Cliente")
        # centrar
        pantalla_ancho = root.winfo_screenwidth()
        pantalla_alto = root.winfo_screenheight()
        x = (pantalla_ancho - 400) // 2
        y = (pantalla_alto - 350) // 2
        root.geometry(f"400x350+{x}+{y}")
        root.resizable(False, False)

        container = tk.Frame(root)
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

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
        tk.Label(container, text="Nombre").grid(row=0, column=0, pady=5)
        self.nombre_entry = tk.Entry(container, textvariable=self.nombre_var)
        self.nombre_entry.grid(row=0, column=1, pady=5)
        self.nombre_entry.bind("<KeyRelease>", self.validate_alpha)
        self.nombre_status = tk.Label(container, text="", fg="red")
        self.nombre_status.grid(row=0, column=2)

        tk.Label(container, text="Apellido").grid(row=1, column=0, pady=5)
        self.apellido_entry = tk.Entry(container, textvariable=self.apellido_var)
        self.apellido_entry.grid(row=1, column=1, pady=5)
        self.apellido_entry.bind("<KeyRelease>", self.validate_alpha)
        self.apellido_status = tk.Label(container, text="", fg="red")
        self.apellido_status.grid(row=1, column=2)

        tk.Label(container, text="Dirección").grid(row=2, column=0, pady=5)
        self.direccion_entry = tk.Entry(container, textvariable=self.direccion_var)
        self.direccion_entry.grid(row=2, column=1, pady=5)
        self.direccion_status = tk.Label(container, text="", fg="red")
        self.direccion_status.grid(row=2, column=2)

        tk.Label(container, text="Teléfono").grid(row=3, column=0, pady=5)
        self.telefono_entry = tk.Entry(container, textvariable=self.telefono_var)
        self.telefono_entry.grid(row=3, column=1, pady=5)
        self.telefono_entry.bind("<KeyRelease>", self.validate_numeric)
        self.telefono_status = tk.Label(container, text="", fg="red")
        self.telefono_status.grid(row=3, column=2)

        tk.Label(container, text="Email").grid(row=4, column=0, pady=5)
        self.mail_entry = tk.Entry(container, textvariable=self.email_var)
        self.mail_entry.grid(row=4, column=1, pady=5)
        self.email_status = tk.Label(container, text="", fg="red")
        self.email_status.grid(row=4, column=2)

        self.register_button = tk.Button(container, text="Registrar", command=self.registrar_cliente, state=tk.DISABLED)
        self.register_button.grid(row=5, column=0, columnspan=2, pady=20)

    def validate_alpha(self, event):
        current_value = event.widget.get()
        if not current_value.isalpha():
            event.widget.delete(0, tk.END)
            event.widget.insert(0, ''.join(filter(str.isalpha, current_value)))

    def validate_numeric(self, event):
        current_value = self.telefono_var.get()
        if not current_value.isdigit():
            self.telefono_var.set("".join(filter(str.isdigit, current_value)))
        elif len(current_value) > 10:
            self.telefono_var.set(current_value[:10])

    def validate_form(self, *args):
        self.check_field(self.nombre_var, "nombre_status", lambda v: 2 <= len(v) <= 30, "Nombre inválido")
        self.check_field(self.apellido_var, "apellido_status", lambda v: 2 <= len(v) <= 30, "Apellido inválido")
        self.check_field(self.direccion_var, "direccion_status", lambda v: 5 <= len(v) <= 30, "Dirección inválida")
        self.check_field(self.telefono_var, "telefono_status", lambda v: len(v) == 10, "Teléfono inválido")
        self.check_field(self.email_var, "email_status", lambda v: "@" in v and "." in v, "Email inválido")

        is_valid = (
            2 <= len(self.nombre_var.get()) <= 30 and
            2 <= len(self.apellido_var.get()) <= 30 and
            5 <= len(self.direccion_var.get()) <= 30 and
            len(self.telefono_var.get()) == 10 and
            "@" in self.email_var.get() and "." in self.email_var.get()
        )
        self.register_button.config(state=tk.NORMAL if is_valid else tk.DISABLED)

    def check_field(self, var, status_label_name, condition, error_message):
        status_label = getattr(self, status_label_name)
        value = var.get()
        if condition(value):
            status_label.config(text="✔️", fg="green")
        else:
            status_label.config(text=error_message, fg="red")

    def registrar_cliente(self):
        nombre = self.nombre_var.get()
        apellido = self.apellido_var.get()
        direccion = self.direccion_var.get()
        telefono = self.telefono_var.get()
        email = self.email_var.get()

        try:
            gestorCliente = GestorCliente()
            gestorCliente.registrarCliente(nombre, apellido, direccion, telefono, email)
            messagebox.showinfo("Éxito", f"Cliente {nombre} {apellido} registrado con éxito")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar cliente: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaRegistrarCliente(root)
    root.mainloop()
