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
        try:
            query = "SELECT * FROM reservas"
            reservas_data = self._db.fetch_query(query)
            reservas = [Reserva(*data) for data in reservas_data]
            return reservas
        except:
            print("No se pudieron obtener las reservas")
            return

    def getClientes(self):
        return self._clientes

    def getHabitaciones(self):
        return self._habitaciones

    def agregarReserva(self, res):
        self._reservas.append(res)

    def registrarReserva(
        self, idHabitacion, idCliente, fechaEntrada, fechaSalida, cantPersonas
    ):
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
            raise ValueError("La habitación no está disponible")

        # validar que la fecha de entrada sea menor a la fecha de salida
        if fechaEntrada >= fechaSalida:
            print("La fecha de entrada debe ser menor a la fecha de salida")
            # retornar una excepcion
            raise Exception("La fecha de entrada debe ser menor a la fecha de salida")

        # guardar la reserva en la base de datos
        query = "INSERT INTO reservas (id_habitacion, id_cliente, fecha_entrada, fecha_salida, personas, estado) VALUES (?, ?, ?, ?, ?, ?)"
        self._db.execute_query(
            query,
            (
                idHabitacion,
                idCliente,
                fechaEntrada,
                fechaSalida,
                cantPersonas,
                "pendiente",
            ),
        )
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
            return []

    def calcularTotalReserva(self, id_reserva):
        # Buscar la reserva y la habitación asociada
        reserva = self.getReservaById(id_reserva)
        habitacion = self.gestorHabitaciones.getHabitacion(reserva.getHabitacion())

        # Convertir las fechas de entrada y salida a objetos datetime si son cadenas
        fecha_entrada = reserva.getFechaEntrada()
        fecha_salida = reserva.getFechaSalida()

        if isinstance(fecha_entrada, str):
            fecha_entrada = datetime.strptime(
                fecha_entrada, "%Y-%m-%d"
            ).date()  # Ajusta el formato según tu caso
        if isinstance(fecha_salida, str):
            fecha_salida = datetime.strptime(
                fecha_salida, "%Y-%m-%d"
            ).date()  # Ajusta el formato según tu caso

        # Calcular el total multiplicando los días de estancia por el precio por noche
        dias = (fecha_salida - fecha_entrada).days
        total = dias * habitacion.getPrecioPorNoche()
        return total

    def getHabitacionesDisponibles(self, fecha_entrada, fecha_salida):
        # Obtener todas las habitaciones
        habitaciones = self.gestorHabitaciones.getHabitaciones()
        # Obtener las reservas que se solapan con las fechas de entrada y salida
        reservas = self.getReservas()
        for reserva in reservas:
            if (
                fecha_entrada <= reserva.getFechaSalida()
                and fecha_salida >= reserva.getFechaEntrada()
                and reserva.getEstado() != 'finalizada' 
            ):
                # Si las fechas se solapan, la habitación no está disponible, eliminar de la lista de habitaciones comparandos los ids
                habitaciones = [
                    hab
                    for hab in habitaciones
                    if hab.getId() != reserva.getHabitacion()
                ]
        print(f"Reservas: f{reservas} \nHabitaciones: {habitaciones}")
        return habitaciones

    def getReservasByFecha(self, fechaInicio, fechaFin):
        reservas = self.getReservas()
        reservas_filtradas = [
            reserva
            for reserva in reservas
            if fechaInicio
            <= datetime.strptime(reserva.getFechaEntrada(), "%Y-%m-%d").date()
            <= fechaFin
            and fechaInicio
            <= datetime.strptime(reserva.getFechaSalida(), "%Y-%m-%d").date()
            <= fechaFin
        ]

        return reservas_filtradas

    def getReservasByHabitacion(self, id_habitacion):
        query = "SELECT * FROM reservas WHERE id_habitacion = ?"
        reservas_data = self._db.fetch_query(query, (id_habitacion,))
        reservas = [Reserva(*data) for data in reservas_data]
        return reservas

    def getReservasFuturas(self):
        # Obtener la fecha actual
        fechaActual = datetime.now().date()
        reservas = self.getReservas()
        # Determinar que reservas se encuentran en curso
        reservas_futuras = [
            reserva
            for reserva in reservas
            if datetime.strptime(reserva.getFechaEntrada(), "%Y-%m-%d").date()
            <= fechaActual
            <= datetime.strptime(reserva.getFechaSalida(), "%Y-%m-%d").date()
        ]

        return reservas_futuras

    def porcentajeOcupacion(self, tipo):
        habitaciones = self.gestorHabitaciones.getHabitacionByTipo(tipo)
        reservasFuturas = self.getReservasFuturas()
        # habitacionesOcupadas = [hab for hab in habitaciones if hab.getEstado() == "ocupada"]
        # cuento reservas por tipo de habitacion
        habitacionesOcupadas = [
            reserva
            for reserva in reservasFuturas
            if reserva.getHabitacion() in [hab.getId() for hab in habitaciones]
        ]
        if len(habitaciones) == 0:
            return "No hay habitaciones de ese tipo"
        return len(habitacionesOcupadas) / len(habitaciones) * 100

    def getReservasPendientesByIdCliente(self, id_cliente):
        query = (
            "SELECT * FROM reservas r WHERE r.id_cliente = ? AND r.estado = 'pendiente'"
        )
        reservas_data = self._db.fetch_query(query, (id_cliente,))
        print(f"reservas query: {reservas_data}")
        reservas = [Reserva(*data) for data in reservas_data]
        return reservas

    def iniciar_estadia(self, id_reserva):
        # buscar la habitacion de la reserva y validar que la habitacion este disponible, luego pasarla a ocupada y cambiar el estado de la reserva a iniciada
        reserva = self.getReservaById(id_reserva)
        habitacion = self.gestorHabitaciones.getHabitacion(reserva.getHabitacion())
        if habitacion.getEstado() != "disponible":
            raise ValueError("La habitación no está disponible")

        query = "UPDATE habitaciones SET estado = 'ocupada' WHERE id = ?"
        self._db.execute_query(query, (habitacion.getId(),))
        query = "UPDATE reservas SET estado = 'iniciada' WHERE id = ?"
        self._db.execute_query(query, (id_reserva,))
        self._db.commit()

    def getReservasFinalizablesByClienteId(self, id_cliente):
        query = "SELECT * FROM reservas WHERE id_cliente = ? AND estado = 'iniciada'"
        reservas_data = self._db.fetch_query(query, (id_cliente,))
        reservas = [Reserva(*data) for data in reservas_data]
        return reservas

    def finalizarReserva(self, id_reserva):
        # buscar la habitacion de la reserva y validar que la habitacion este ocupada, luego pasarla a disponible y cambiar el estado de la reserva a finalizada
        reserva = self.getReservaById(id_reserva)
        habitacion = self.gestorHabitaciones.getHabitacion(reserva.getHabitacion())
        print(habitacion)
        if habitacion.getEstado() != "ocupada":
            raise ValueError("La habitación no está ocupada")

        query = "UPDATE habitaciones SET estado = 'disponible' WHERE id = ?"
        self._db.execute_query(query, (habitacion.getId(),))
        query = "UPDATE reservas SET estado = 'finalizada' WHERE id = ?"
        self._db.execute_query(query, (id_reserva,))
        self._db.commit()
