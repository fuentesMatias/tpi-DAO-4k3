class Factura:
    def __init__(self, id, cliente, reserva, fechaEmision, total):
        self._id = id
        self._cliente = cliente
        self._reserva = reserva
        self._fechaEmision = fechaEmision
        self._total = total

    def getId(self):
        return self._id

    def getCliente(self):
        return self._cliente

    def getReserva(self):
        return self._reserva

    def getFechaEmision(self):
        return self._fechaEmision

    def getTotal(self):
        return self._total

    def setId(self, id):
        self._id = id

    def setCliente(self, cliente):
        self._cliente = cliente

    def setReserva(self, res):
        self._reserva = res

    def setFechaEmision(self, fecha):
        self._fechaEmision = fecha

    def setTotal(self, cantidad):
        self._total = cantidad

    def __str__(self) -> str:
        return f"ID Factura: {str(self.getId())} | Cliente: {str(self.getCliente())} | Reserva: {str(self.getReserva())} | Fecha de emision: {self.getFechaEmision()} | Total: ${str(self.getTotal())}"
