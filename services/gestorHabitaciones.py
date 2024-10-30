from models.habitacion import Habitacion
from database.conexion import DbSingleton

class GestorHabitaciones():
    def __init__(self) -> None:
        self._habitaciones = []
        self.db = DbSingleton()

    def getHabitaciones(self):
        return self._habitaciones
    
    def registrarHabitacion(self,numero, tipo, precioPorNoche):
        self.db.execute_query("INSERT INTO Habitaciones (numero, tipo, precioPorNoche) VALUES (?, ?, ?)", (numero, tipo, precioPorNoche))
        self.db.commit()

    def actualizarHabitacion(self, id, tipo, precioPorNoche):
        self.db.execute_query("UPDATE Habitaciones SET tipo = ?, precioPorNoche = ? WHERE id = ?", (tipo, precioPorNoche, id))
        self.db.commit()

    def getHabitacion(self, id):
        habitacion_data = self._db.fetch_query(f"SELECT * FROM habitaciones WHERE id = {id}")
        if habitacion_data:
            data = habitacion_data[0]
            hab = Habitacion(*data)  
            return hab
        else:
            print(f"No se encontró ninguna habitacion con ID {id}")
            return None
