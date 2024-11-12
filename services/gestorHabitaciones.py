from models.habitacion import Habitacion
from database.conexion import DbSingleton


class GestorHabitaciones:
    def __init__(self) -> None:
        self._db = DbSingleton()

    def obtenerNumerosHabitaciones(self):
        habitaciones_data = self._db.fetch_query("SELECT numero FROM habitaciones")
        numeros = [data[0] for data in habitaciones_data]
        return numeros

    def getHabitaciones(self):
        self._habitaciones = []
        habitaciones_data = self._db.fetch_query("SELECT * FROM habitaciones")
        for data in habitaciones_data:
            hab = Habitacion(*data)
            self._habitaciones.append(hab)
        return self._habitaciones

    def registrarHabitacion(self, numero, tipo, precioPorNoche):
        try:
            self._db.execute_query(
                "INSERT INTO Habitaciones (numero, tipo, estado, precio) VALUES (?, ?, ?, ?)",
                (numero, tipo, "disponible", precioPorNoche),
            )
        except Exception as e:
            print(f"No se pudo registrar la habitación: {e}")
            raise e
        self._db.commit()

    def actualizarHabitacion(self, id, tipo, precioPorNoche):
        self._db.execute_query(
            "UPDATE Habitaciones SET tipo = ?, precioPorNoche = ? WHERE id = ?",
            (tipo, precioPorNoche, id),
        )
        self._db.commit()

    def getHabitacion(self, id):
        habitacion_data = self._db.fetch_query(
            f"SELECT * FROM habitaciones WHERE id = {id}"
        )
        if habitacion_data:
            data = habitacion_data[0]
            hab = Habitacion(*data)
            return hab
        else:
            print(f"No se encontró ninguna habitacion con ID {id}")
            return None

    def eliminarHabitacion(self, id):
        self._db.execute_query("DELETE FROM habitaciones WHERE id = ?", (id))

    # get habitaciones disponibles
    def getHabitacionesDisponibles(self):
        habitaciones_data = self._db.fetch_query(
            "SELECT * FROM habitaciones WHERE estado = 'disponible'"
        )
        habitacionesDispobibles = [Habitacion(*data) for data in habitaciones_data]
        return habitacionesDispobibles

    def getHabitacionByTipo(self, tipo):
        habitaciones_data = self._db.fetch_query(
            f"SELECT * FROM habitaciones WHERE tipo = '{tipo}'"
        )
        habitaciones = [Habitacion(*data) for data in habitaciones_data]
        return habitaciones
    
    def getHabitacionByTipoAndOcupada(self, tipo):
        habitaciones_data = self._db.fetch_query(
            f"SELECT * FROM habitaciones WHERE tipo = '{tipo}' AND estado = 'ocupada'"
        )
        habitaciones = [Habitacion(*data) for data in habitaciones_data]
        return habitaciones
    