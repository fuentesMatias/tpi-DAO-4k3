from abc import ABC

class Persona(ABC):
    def __init__(self, id, nombre, apellido):
        self._id = id
        self._nombre = nombre
        self._apellido = apellido

    def getId(self):
        return self._id

    def getNombre(self):
        return self._nombre

    def getApellido(self):
        return self._apellido

    def setId(self, id):
        self._id = id

    def setNombre(self, nombre):
        self._nombre = nombre

    def setApellido(self, apellido):
        self._apellido = apellido

    def __str__(self) -> str:
        return f"ID: {self.getId()} | Nombre: {self.getNombre()} | Apellido: {self.getApellido()}"
