from database.conexion import DbSingleton
from services.gestorCliente import GestorCliente
from services.gestorReserva import GestorReserva
import datetime



class gestorFactura:
    def __init__(self):
        self._db = DbSingleton()
        self.gestorReservas = GestorReserva()
        self.gestorClientes = GestorCliente()
        
    def getFacturas(self):
        pass
    
    
    def registrarFactura(self,idCliente,idReserva):
        # validar que el id del cliente y el id de la reserva existan con try except
        try:
            cliente = self.gestorClientes.getClienteById(idCliente)
            reserva = self.gestorReservas.getReservaById(idReserva)
        except:
            print("No se pudo registrar la factura")
            return
        
        # calcular el total
        precioTotal = GestorReserva.calcularTotalReserva(reserva.getId())
        
        # obtener la fecha de emision
        fecha_emision = datetime.date.today()
        
        # guardar la factura en la base de datos
        query = "INSERT INTO facturas (id_cliente, id_reserva, fecha_emision, total) VALUES (?, ?, ?, ?)"
        #pasar todos los valores como string
        self._db.execute_query(query, (str(idCliente), str(idReserva), fecha_emision, str(precioTotal)))
        self._db.commit()