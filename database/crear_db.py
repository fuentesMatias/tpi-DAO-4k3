from database.conexion import DbSingleton

def crear_tablas():
    db = DbSingleton()

    # Crear tablas si no existen
    db.execute_query("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL
        )
    """)

    db.execute_query("""
        CREATE TABLE IF NOT EXISTS habitaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            tipo TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)

    db.execute_query("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER,
            id_habitacion INTEGER,
            fecha_entrada TEXT,
            fecha_salida TEXT,
            personas INTEGER,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id),
            FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id)
        )
    """)

    db.commit()
    print("Tablas creadas correctamente")

if __name__ == "__main__":
    crear_tablas()
