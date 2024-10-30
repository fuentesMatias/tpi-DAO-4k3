from database.conexion import DbSingleton
from datetime import date
from models.reserva import Reserva


class GestorReserva:
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

    def agregarReserva(self, res):
        self._reservas.append(res)

    def registrarReserva(
        self, idHabitacion, idCliente, fechaEntrada, fechaSalida, cantPersonas
    ):
        hab = list(filter(lambda x: x.id == idHabitacion, self.getHabitaciones()))
        cliente = list(filter(lambda x: x.id == idCliente, self.getClientes()))
        hab.ocupar()
        ultimoId = self._db.fetch_query(
            "SELECT * from reservas ORDER BY id desc LIMIT 1"
        )[0]
        reserva = Reserva(
            ultimoId, cliente, hab, fechaEntrada, fechaSalida, cantPersonas
        )
        self.agregarReserva(reserva)
        self._db.execute_query(
            "INSERT INTO reservas(id_cliente, id_habitacion, fecha_entrada, fecha_salida, personas) VALUES (?, ?, ?, ?, ?)",
            (idCliente, idHabitacion, fechaEntrada, fechaSalida, cantPersonas),
        )
    
    def getReservasByClienteId(self, id_cliente):
        query = "SELECT * FROM reservas WHERE id_cliente = ?"
        reservas_data = self._db.fetch_query(query, (id_cliente,))
        return reservas_data