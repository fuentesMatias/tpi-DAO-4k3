import tkinter as tk
from tkinter import messagebox
from database.conexion import DbSingleton
from services.gestorCliente import GestorCliente

class VentanaRegistrarCliente:
    def __init__(self, root):
        self.root = root
        self.root.title("Registro de Cliente")

        # Variables de control con validaciones
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.direccion_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.email_var = tk.StringVar()

        # Función para habilitar o deshabilitar el botón de registro
        self.nombre_var.trace_add("write", self.validate_form)
        self.apellido_var.trace_add("write", self.validate_form)
        self.direccion_var.trace_add("write", self.validate_form)
        self.telefono_var.trace_add("write", self.validate_form)
        self.email_var.trace_add("write", self.validate_form)

        tk.Label(root, text="Nombre").grid(row=0, column=0)
        self.nombre_entry = tk.Entry(root, textvariable=self.nombre_var)
        self.nombre_entry.grid(row=0, column=1)

        tk.Label(root, text="Apellido").grid(row=1, column=0)
        self.apellido_entry = tk.Entry(root, textvariable=self.apellido_var)
        self.apellido_entry.grid(row=1, column=1)

        tk.Label(root, text="Dirección").grid(row=2, column=0)
        self.direccion_entry = tk.Entry(root, textvariable=self.direccion_var)
        self.direccion_entry.grid(row=2, column=1)

        tk.Label(root, text="Teléfono").grid(row=3, column=0)
        self.telefono_entry = tk.Entry(root, textvariable=self.telefono_var)
        self.telefono_entry.grid(row=3, column=1)
        self.telefono_entry.bind("<KeyRelease>", self.validate_numeric)

        tk.Label(root, text="Email").grid(row=4, column=0)
        self.mail_entry = tk.Entry(root, textvariable=self.email_var)
        self.mail_entry.grid(row=4, column=1)

        self.register_button = tk.Button(root, text="Registrar", command=self.registrar_cliente, state=tk.DISABLED)
        self.register_button.grid(row=5, column=0, columnspan=2)

    def validate_numeric(self, event):
        # Permite solo números en el campo de teléfono y limita la longitud a 10 caracteres
        current_value = self.telefono_var.get()
        if not current_value.isdigit():
            self.telefono_var.set("".join(filter(str.isdigit, current_value)))
        elif len(current_value) > 10:
            self.telefono_var.set(current_value[:10])

    def validate_form(self, *args):
        # Verifica que todos los campos tengan la longitud correcta y que no estén vacíos
        is_valid = (
            2 <= len(self.nombre_var.get()) <= 30 and
            2 <= len(self.apellido_var.get()) <= 30 and
            5 <= len(self.direccion_var.get()) <= 50 and
            len(self.telefono_var.get()) == 10 and
            "@" in self.email_var.get() and "." in self.email_var.get()
        )
        self.register_button.config(state=tk.NORMAL if is_valid else tk.DISABLED)

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
            self.root.destroy()  # Cierra la ventana al registrar exitosamente
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar cliente: {e}")
            # La ventana permanece abierta y los datos ingresados quedan

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaRegistrarCliente(root)
    root.mainloop()
