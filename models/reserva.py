class Reserva:
    def __init__(
        self, id, cliente, habitacion, fechaEntrada, fechaSalida, cantPersonas, estado
    ):
        self._id = id
        self._cliente = cliente
        self._habitacion = habitacion
        self._fechaEntrada = fechaEntrada
        self._fechaSalida = fechaSalida
        self._cantPersonas = cantPersonas
        self._estado = estado  


    def getEstado(self):
        return self._estado
    
    def getId(self):
        return self._id

    def getCliente(self):
        return self._cliente

    def getHabitacion(self):
        return self._habitacion

    def getFechaEntrada(self):
        return self._fechaEntrada

    def getFechaSalida(self):
        return self._fechaSalida

    def getCantPersonas(self):
        return self._cantPersonas

    def setId(self, id):
        self._id = id

    def setCliente(self, cliente):
        self._cliente = cliente

    def setHabitacion(self, hab):
        self._habitacion = hab

    def setFechaEntrada(self, fecha):
        self._fechaEntrada = fecha

    def setFechaSalida(self, fecha):
        self._fechaSalida = fecha

    def setCantPersonas(self, cantidad):
        self._cantPersonas = cantidad

    def setEstado(self, estado):
        self._estado = estado
    
    def __str__(self) -> str:
        return f"ID Reserva: {str(self.getId())} | Cliente: {str(self.getCliente())} | Habitacion: {str(self.getHabitacion())} | Fecha de entrada: {self.getFechaEntrada()} | Fecha de salida: {self.getFechaSalida()} | Cantidad de personas: {str(self.getCantPersonas())} | Estado: {self.getEstado()}"
