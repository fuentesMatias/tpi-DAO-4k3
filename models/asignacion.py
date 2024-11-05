from datetime import date

class Asignacion:
    def __init__(self, id, empleado, habitacion, fecha):
        self._id = id
        self._empleado = empleado
        self._habitacion = habitacion
        self._fecha = fecha

    def getId(self):
        return self._id

    def getEmpleado(self):
        return self._empleado

    def getHabitacion(self):
        return self._habitacion

    def getFecha(self):
        return self._fecha

    def setId(self, id):
        self._id = id

    def setEmpleado(self, empleado):
        self._empleado = empleado

    def setHabitacion(self, hab):
        self._habitacion = hab

    def setFecha(self, fecha):
        self._fecha = fecha

    def estaActiva(self):
        return self.getFecha() == date.today()

    def __str__(self) -> str:
        return f"ID Asignacion: {str(self.getId())} | Empleado: {str(self.getEmpleado())} | Habitacion: {str(self.getHabitacion())} | Fecha: {self.getFecha()} | Activa: {"SI" if self.estaActiva() else "NO"}"
