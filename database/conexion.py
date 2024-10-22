import sqlite3
from sqlite3 import Error

class ConexionDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.conn = sqlite3.connect("hotel.db")
                print("Conexión exitosa a SQLite")
            except Error as e:
                print(f"Error al conectar a SQLite: {e}")
                cls._instance = None
        return cls._instance

    def get_cursor(self):
        return self.conn.cursor()

    def commit(self):
        self.conn.commit()
