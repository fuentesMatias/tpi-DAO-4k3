from database.conexion import DbSingleton

class GestorReserva():
    def __init__(self):
        self._reservas = []
        self._clientes = []
        self._habitaciones = []
        self._db = DbSingleton()

    def getReservas(self):
        return self._reservas

    def getClientes(self):
        return self._clientes

    def getHabitaciones(self):
        return self._habitaciones