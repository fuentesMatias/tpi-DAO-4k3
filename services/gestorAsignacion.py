from database.conexion import DbSingleton
from datetime import date
from models.asignacion import Asignacion
from services.gestorEmpleado import GestorEmpleado
from services.gestorHabitaciones import GestorHabitaciones
from datetime import datetime


class GestorAsignacion:
    def __init__(self):
        self._db = DbSingleton()
        self.gestorHabitaciones = GestorHabitaciones()
        self.gestorEmpleados = GestorEmpleado()
        self._habitaciones = self.gestorHabitaciones.getHabitaciones()
        self._empleados = self.gestorEmpleados.getEmpleados()
        self._asignaciones = []

    def getAsignaciones(self):
        return self._asignaciones

    def getHabitaciones(self):
        return self._habitaciones

    def cargarAsignaciones(self):
        try:
            query = "SELECT * FROM asignaciones"
            asignaciones_data = self._db.fetch_query(query)
            asignaciones = []

            print(f"asignaciones: {asignaciones_data}")
            for data in asignaciones_data:
                id, idEmpleado, idHabitacion, fecha = data
                empleado = self.gestorEmpleados.getEmpleadoById(idEmpleado)
                habitacion = self.gestorHabitaciones.getHabitacion(idHabitacion)
                asignacion = Asignacion(id, empleado, habitacion, fecha)
                asignaciones.append(asignacion)

            self._asignaciones = asignaciones
        except:
            print("No se pudieron cargar las asignaciones")
            return

    def registrarAsignacion(self, idHabitacion, idEmpleado, fecha):
        # validar que el id de la habitacion y el id del empleado existan con try except
        try:
            habitacion = self.gestorHabitaciones.getHabitacion(idHabitacion)
            print(habitacion)
            empleado = self.gestorEmpleados.getEmpleadoById(idEmpleado)
        except:
            print("No se pudo asignar la habitacion al empleado")
            return

        # ESTE IF ES EL QUE NO ANDA
        # validar que la habitacion no este asignada
        if not any(
            hab.getId() == idHabitacion for hab in self.getHabitacionesParaAsignar()
        ):
            print(f"La habitacion {idHabitacion} ya esta asignada")
            raise Exception("La habitacion ya se encuentra asignada")

        # validar que el empleado no tenga mas de 5 asignaciones
        asignacionesDelEmpleado = self.getAsignacionesActivasByEmpleado(idEmpleado)

        if len(asignacionesDelEmpleado) > 5:
            print(f"El empleado debe tener menos de 5 asignaciones activas")
            raise Exception("El empleado debe tener menos de 5 asignaciones activas")

        # guardar la asignacion
        query = "INSERT INTO asignaciones (id_empleado, id_habitacion, fecha) VALUES (?, ?, ?)"
        self._db.execute_query(query, (idEmpleado, idHabitacion, fecha))
        self._db.commit()

    def getAsignacionesActivasByEmpleado(self, idEmpleado):
        # validar que el id del empleado exista
        try:
            empleado = self.gestorEmpleados.getEmpleadoById(idEmpleado)
        except:
            print(
                f"No se pudo obtener la informacion de las asignaciones para el empleado {str(idEmpleado)}"
            )
            return
        # buscar las asignaciones para el empleado por el id
        asignaciones = self.getAsignaciones()
        asignacionesDelEmpleado = [
            asign for asign in asignaciones if asign.getEmpleado().getId() == idEmpleado
        ]
        asignacionesActivas = [
            asign for asign in asignacionesDelEmpleado if asign.estaActiva()
        ]

        return asignacionesActivas

    def getHabitacionesParaAsignar(self):
        habitaciones = self.getHabitaciones()
        asignaciones = self.getAsignaciones()
        # Obtener las asignaciones entre las fechas establecidas
        for asign in asignaciones:
            if asign.estaActiva():
                # Si la asignacion está activa, eliminar la habitacion
                habitaciones = [
                    hab
                    for hab in habitaciones
                    if hab.getId() != asign.getHabitacion().getId()
                ]
        print(f"Asignaciones: {asignaciones} \nHabitaciones: {habitaciones}")
        return habitaciones
