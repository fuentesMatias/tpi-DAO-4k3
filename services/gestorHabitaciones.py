from models.habitacion import Habitacion
from database.conexion import DbSingleton

class GestorHabitaciones():
    def __init__(self) -> None:
        self._habitaciones = []
        self.db = DbSingleton()

    def getHabitaciones(self):
        return self._habitaciones
    
    def registrarHabitacion(self, tipo, precioPorNoche):
        self.db.execute_query("INSERT INTO habitaciones(tipo, estado, precioPorNoche) VALUES (?,?)", (tipo, "disponible", precioPorNoche))

    def actualizarHabitacion(self, id, tipo, precioPorNoche):
        self.db.execute_query("UPDATE Habitaciones SET tipo = ?, precioPorNoche = ? WHERE id = ?", (tipo, precioPorNoche, id))

    def getHabitacion(self, id):
        habitacion_data = self._db.fetch_query(f"SELECT * FROM habitaciones WHERE id = {id}")
        if habitacion_data:
            data = habitacion_data[0]
            hab = Habitacion(*data)  
            return hab
        else:
            print(f"No se encontró ninguna habitacion con ID {id}")
            return None
