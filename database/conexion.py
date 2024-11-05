import sqlite3
from sqlite3 import Error


class DbSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DbSingleton, cls).__new__(cls)
            try:
                cls._instance._initialize_connection()
                cls._instance._run_init_script()  # Ejecuta el script init.sql
            except Error as e:
                print(f"Error al conectar a SQLite: {e}")
                cls._instance = None
        return cls._instance

    def _initialize_connection(self):
        try:
            self.connection = sqlite3.connect("./database/hotel.db")
            self.cursor = self.connection.cursor()
            print("Conexión con DB establecida")
        except Error as e:
            print(f"Error al conectarse: {e}")

    def _run_init_script(self):
        """Ejecuta un script SQL para inicializar la base de datos."""
        try:
            with open("./database/init.sql", "r") as file:
                sql_script = file.read()
            self.cursor.executescript(sql_script)
            self.commit()  # Asegura que los cambios se guarden
            print("Script init.sql ejecutado correctamente")
        except FileNotFoundError:
            print("El archivo init.sql no fue encontrado")
        except Error as e:
            print(f"Error al ejecutar el script init.sql: {e}")

    def execute_query(self, query, params=()):
        try:
            self.test_connection()
            self.cursor.execute(query, params)
        except Error as e:
            raise e
            print(f"Error al intentar ejecutar la consulta: {e}")

    def fetch_query(self, query, parameters=()):
        try:
            self.test_connection()
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error al intentar obtener datos: {e}")
            raise e

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Conexión a la BD cerrada")

    def test_connection(self):
        if not self.connection:
            self._initialize_connection()

    def commit(self):
        if self.connection:
            self.connection.commit()
