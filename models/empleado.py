from persona import Persona


class Empleado(Persona):
    def __init__(self, id, nombre, apellido, cargo, sueldo):
        super().__init__(id, nombre, apellido)
        self._cargo = cargo
        self._sueldo = sueldo

    def getCargo(self):
        return self._cargo

    def getSueldo(self):
        return self._sueldo

    def setCargo(self, cargo):
        self._cargo = cargo

    def setSueldo(self, sueldo):
        self._sueldo = sueldo

    def __str__(self) -> str:
        return (
            f"Empleado | "
            + super().__str__()
            + f" | Cargo: {self.getCargo()} | Sueldo: ${str(self.getSueldo())}"
        )
