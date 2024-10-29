from persona import Persona


class Cliente(Persona):
    def __init__(self, id, nombre, apellido, direccion, telefono, mail):
        super().__init__(id, nombre, apellido)
        self._direccion = direccion
        self._telefono = telefono
        self._mail = mail

    def getDireccion(self):
        return self._direccion

    def getTelefono(self):
        return self._telefono

    def getMail(self):
        return self._mail

    def setDireccion(self, dir):
        self._direccion = dir

    def setTelefono(self, tel):
        self._telefono = tel

    def setMail(self, mail):
        self._mail = mail

    def __str__(self) -> str:
        return (
            f"Cliente | "
            + super().__str__()
            + f" | Direccion: {self.getDireccion()} | Telefono: {self.getTelefono()} | Mail: {self.getMail()}"
        )
