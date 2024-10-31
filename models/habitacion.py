class Habitacion:
    def __init__(self, id, numero, tipo, estado, precioPorNoche):
        self._id = id
        self._numero = numero
        self._tipo = tipo
        self._estado = estado
        self._precioPorNoche = precioPorNoche


    def getId(self):
        return self._id
    
    def getNumero(self):
        return self._numero

    def getTipo(self):
        return self._tipo

    def getEstado(self):
        return self._estado

    def getPrecioPorNoche(self):
        return self._precioPorNoche

    def setNumero(self, nro):
        self._numero = nro

    def setTipo(self, tipo):
        self._tipo = tipo

    def setEstado(self, estado):
        self._estado = estado

    def setPrecioPorNoche(self, precio):
        self._precioPorNoche = precio

    def __str__(self) -> str:
        return f"ID: {self._id} | N° de Habitacion: {str(self.getNumero())} | Tipo: {self.getTipo()} | Estado: {self.getEstado()} | Precio por noche: ${str(self.getPrecioPorNoche())}"

    def reservar(self):
        self._estado = "ocupada"

    def disponibilizar(self):
        self._estado = "disponible"
