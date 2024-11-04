class Asignacion:
    def __init__(self, id, empleado, habitacion, fechaInicio, fechaFin=None):
        self._id = id
        self._empleado = empleado
        self._habitacion = habitacion
        self._fechaInicio = fechaInicio
        self._fechaFin = fechaFin

    def getId(self):
        return self._id

    def getEmpleado(self):
        return self._empleado

    def getHabitacion(self):
        return self._habitacion

    def getFechaInicio(self):
        return self._fechaInicio

    def getFechaFin(self):
        return self._fechaFin

    def setId(self, id):
        self._id = id

    def setEmpleado(self, empleado):
        self._empleado = empleado

    def setHabitacion(self, hab):
        self._habitacion = hab

    def setFechaInicio(self, fecha):
        self._fechaInicio = fecha

    def setFechaFin(self, fecha):
        self._fechaFin = fecha

    def estaActiva(self):
        return self.getFechaFin() is None

    def __str__(self) -> str:
        return f"ID Asignacion: {str(self.getId())} | Empleado: {str(self.getEmpleado())} | Habitacion: {str(self.getHabitacion())} | Fecha de Inicio: {self.getFechaInicio()} | Fecha de fin: {self.getFechaFin()}"
