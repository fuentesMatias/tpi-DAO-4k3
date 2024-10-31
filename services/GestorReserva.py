from database.conexion import DbSingleton
from datetime import date
from models.reserva import Reserva
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorCliente import GestorCliente



class GestorReserva:
    def __init__(self):
        self._db = DbSingleton()
        self.gestorHabitaciones = GestorHabitaciones()
        self.gestorClientes = GestorCliente()
        

    def getReservas(self):
        return self._reservas

    def getClientes(self):
        return self._clientes

    def getHabitaciones(self):
        return self._habitaciones

    def agregarReserva(self, res):
        self._reservas.append(res)
        

    def registrarReserva(self, idHabitacion, idCliente, fechaEntrada, fechaSalida, cantPersonas):
        # validar que el id de la habitacion y el id del cliente existan con try except
        try:
            habitacion = self.gestorHabitaciones.getHabitacion(idHabitacion)
            print(habitacion)
            cliente = self.gestorClientes.getClienteById(idCliente)
        except:
            print("No se pudo registrar la reserva")
            return
        
        # validar que la habitacion este disponible
        if habitacion.getEstado() != "disponible":
            print("La habitacion no esta disponible")
            print(habitacion.getEstado())
            return
        
        # validar que la fecha de entrada sea menor a la fecha de salida
        if fechaEntrada >= fechaSalida:
            print("La fecha de entrada debe ser menor a la fecha de salida")
            # retornar una excepcion
            raise Exception("La fecha de entrada debe ser menor a la fecha de salida")

        
        # guardar la reserva en la base de datos
        query = "INSERT INTO reservas (id_habitacion, id_cliente, fecha_entrada, fecha_salida, personas) VALUES (?, ?, ?, ?, ?)"
        self._db.execute_query(query, (idHabitacion, idCliente, fechaEntrada, fechaSalida, cantPersonas))
        self._db.commit()
        
    
    def getReservasByClienteId(self, id_cliente):
        query = "SELECT * FROM reservas WHERE id_cliente = ?"
        reservas_data = self._db.fetch_query(query, (id_cliente,))
        return reservas_data