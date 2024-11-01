from database.conexion import DbSingleton
from datetime import date
from models.reserva import Reserva
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorCliente import GestorCliente
from datetime import datetime



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
        # Crear objetos Reserva con los datos obtenidos
        reservas = [Reserva(*data) for data in reservas_data]
        return reservas
    
    def getReservaById(self, id_reserva):
        query = "SELECT * FROM reservas WHERE id = ?"
        reserva_data = self._db.fetch_query(query, (id_reserva,))
        if reserva_data:
            data = reserva_data[0]
            reserva = Reserva(*data)
            return reserva
        else:
            print(f"No se encontró ninguna reserva con ID {id_reserva}")
            return None
    
    
    def calcularTotalReserva(self, id_reserva):
        # Buscar la reserva y la habitación asociada
        reserva = self.getReservaById(id_reserva)
        habitacion = self.gestorHabitaciones.getHabitacion(reserva.getHabitacion())
        
        # Convertir las fechas de entrada y salida a objetos datetime si son cadenas
        fecha_entrada = reserva.getFechaEntrada()
        fecha_salida = reserva.getFechaSalida()
        
        if isinstance(fecha_entrada, str):
            fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d").date()  # Ajusta el formato según tu caso
        if isinstance(fecha_salida, str):
            fecha_salida = datetime.strptime(fecha_salida, "%Y-%m-%d").date()  # Ajusta el formato según tu caso

        # Calcular el total multiplicando los días de estancia por el precio por noche
        dias = (fecha_salida - fecha_entrada).days
        total = dias * habitacion.getPrecioPorNoche()
        return total
