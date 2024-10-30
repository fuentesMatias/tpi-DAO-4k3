-- Tabla de clientes
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    direccion TEXT,
    telefono TEXT,
    email TEXT UNIQUE
);

-- Tabla de habitaciones
CREATE TABLE IF NOT EXISTS habitaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT NOT NULL,
    tipo TEXT CHECK (tipo IN ('simple', 'doble', 'suite')) NOT NULL,
    estado TEXT CHECK (estado IN ('disponible', 'ocupada')) DEFAULT 'disponible',
    precio REAL NOT NULL
);

-- Tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_habitacion INTEGER NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    personas INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_habitacion) REFERENCES habitaciones(id)
);

-- Tabla de facturas
CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_reserva INTEGER NOT NULL,
    fecha_emision DATE NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_reserva) REFERENCES reservas(id)
);

-- Tabla de empleados
CREATE TABLE IF NOT EXISTS empleados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    cargo TEXT CHECK (cargo IN ('recepcionista', 'servicio de limpieza', 'gerente', 'mantenimiento')) NOT NULL,
    sueldo REAL NOT NULL
);
