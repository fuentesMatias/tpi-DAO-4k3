class Hotel:
    def __init__(self) -> None:
        self._empleados = []
        self._habitaciones = []
        self._clientes = []
        self._reservas = []
        self._facturas = []

    def agregarEmpleado(self, empleado):
        self._empleados.append(empleado)

    def agregarHabitacion(self, hab):
        self._habitaciones.append(hab)

    def agregarCliente(self, cliente):
        self._clientes.append(cliente)

    def agregarReserva(self, res):
        self._reservas.append(res)

    def agregarFactura(self, fact):
        self._facturas.append(fact)
