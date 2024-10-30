from models.persona import Persona


class Cliente(Persona):
    def __init__(self, id, nombre, apellido, direccion, telefono, email):
        super().__init__(id, nombre, apellido)
        self._direccion = direccion
        self._telefono = telefono
        self._email = email

    def getDireccion(self):
        return self._direccion

    def getTelefono(self):
        return self._telefono

    def getemail(self):
        return self._email

    def setDireccion(self, dir):
        self._direccion = dir

    def setTelefono(self, tel):
        self._telefono = tel

    def setemail(self, email):
        self._email = email

    def __str__(self) -> str:
        return (
            f"Cliente | "
            + super().__str__()
            + f" | Direccion: {self.getDireccion()} | Telefono: {self.getTelefono()} | email: {self.getemail()}"
        )
