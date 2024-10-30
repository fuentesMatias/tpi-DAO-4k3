from database.conexion import DbSingleton
from models.cliente import Cliente

class GestorCliente():
    def __init__(self):
        self._db = DbSingleton()
    
    def getClienteById(self, id):
        cliente_data = self._db.fetch_query(f"SELECT * FROM clientes WHERE id = {id}")
        if cliente_data:
            data = cliente_data[0]  # Extrae la primera fila
            cliente = Cliente(*data)  # Crea un objeto Cliente con la data
            return cliente
        else:
            print(f"No se encontró ningún cliente con ID {id}")
            return None
    
    def registrarCliente(self, nombre, apellido, direccion, telefono, email):
        query = "INSERT INTO clientes (nombre, apellido, direccion, telefono, email) VALUES (?, ?, ?, ?, ?)"
        self._db.execute_query(query, (nombre, apellido, direccion, telefono, email))

        