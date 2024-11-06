import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from database.conexion import DbSingleton
from gui.registro_cliente import VentanaRegistrarCliente
from gui.registro_habitacion import RegistroHabitacion
from gui.registro_reserva import RegistroReserva
from gui.finalizar_estadia import FinalizarEstadia
from gui.iniciar_estadia import IniciarEstadia  # Importamos la nueva ventana
from gui.asignar_habitacion import VentanaAsignarEmpleadoAHabitacion
from services.gestorAsignacion import GestorAsignacion
from gui.generar_reportes import VentanaGenerarReportes


def abrir_ventana(ventana_clase, root):
    ventana = tk.Toplevel(root)
    instancia = ventana_clase(ventana)
    ventana.protocol(
        "WM_DELETE_WINDOW", ventana.destroy
    )  # Destruye completamente al cerrarse


def centrar_ventana(ventana, ancho=400, alto=350):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho - ancho) // 2
    y = (pantalla_alto - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def main():
    # Establecer la conexión con la base de datos
    db = DbSingleton()

    # Crear ventana principal
    root = tk.Tk()
    root.title("Sistema de Gestión de Hotel")
    root.geometry("1200x750")
    root.configure(background="#b3e5fc")

    centrar_ventana(root, 1200, 750)

    # Agregar ícono a la ventana
    root.iconphoto(False, tk.PhotoImage(file="./assets/hotel.png"))

    imagen_fondo = Image.open(
        "./assets/hotel_bg.jpg"
    )  # Reemplaza con tu imagen de fondo
    imagen_fondo = imagen_fondo.resize((1200, 750))  # Ajusta tamaño a la ventana
    bg_image = ImageTk.PhotoImage(imagen_fondo)

    # Configurar un Label para mostrar la imagen de fondo
    fondo_label = tk.Label(root, image=bg_image)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ocupa toda la ventana

    # Crear marco para contenido y widgets
    contenido_frame = tk.Frame(root, bg="#d6f0ff", padx=10, pady=5)
    contenido_frame.place(relx=0.5, rely=0.1, anchor="n")

    # Título de la ventana
    titulo_frame = tk.Frame(root, bg="#d6f0ff", padx=10, pady=5)  # Fondo más claro
    titulo_frame.pack(pady=(10, 20))
    titulo_label = tk.Label(
        titulo_frame,
        text="Bienvenido al Sistema de Gestión Hotelera",
        font=("Arial", 16, "bold"),
        bg="#d6f0ff",
        fg="#007acc",
    )
    titulo_label.pack()

    # Estilos personalizados para botones
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "RoundedButton.TButton",
        background="white",
        foreground="#4a4a4a",
        font=("Arial", 12, "bold"),
        padding=10,
        relief="flat",
    )
    style.map(
        "RoundedButton.TButton",
        background=[("active", "#e0e0e0")],
        relief=[("pressed", "sunken")],
    )

    # Crear los gestores para asignar a las ventanas

    # Botones principales
    ttk.Button(
        root,
        text="Registrar Cliente",
        style="RoundedButton.TButton",
        command=lambda: abrir_ventana(VentanaRegistrarCliente, root),
    ).pack(pady=10)
    ttk.Button(
        root,
        text="Registrar Habitación",
        style="RoundedButton.TButton",
        command=lambda: abrir_ventana(RegistroHabitacion, root),
    ).pack(pady=10)
    ttk.Button(
        root,
        text="Registrar Reserva",
        style="RoundedButton.TButton",
        command=lambda: abrir_ventana(RegistroReserva, root),
    ).pack(pady=10)
    ttk.Button(
        root,
        text="Finalizar Estadia",
        style="RoundedButton.TButton",
        command=lambda: abrir_ventana(FinalizarEstadia, root),
    ).pack(pady=10)
    ttk.Button(
        root,
        text="Iniciar Estadia",  # Nuevo botón
        style="RoundedButton.TButton",
        command=lambda: abrir_ventana(IniciarEstadia, root),
    ).pack(pady=10)  # Botón para iniciar estadía
    ttk.Button(
        root,
        text="Asignar Empleado a Habitación",
        style="RoundedButton.TButton",
        command=lambda: abrir_ventana(VentanaAsignarEmpleadoAHabitacion, root),
    ).pack(pady=10)
    ttk.Button(
        root,
        text="Reportes",
        style="RoundedButton.TButton",
        command=lambda: abrir_ventana(VentanaGenerarReportes, root),
    ).pack(pady=10)

    fondo_label.image = bg_image

    root.mainloop()


if __name__ == "__main__":
    main()
