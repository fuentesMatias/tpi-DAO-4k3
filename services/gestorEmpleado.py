from database.conexion import DbSingleton
from models.empleado import Empleado
class GestorEmpleado:
    def __init__(self):
        self.db = DbSingleton()
        
    def getEmpleados(self):
        empleados_data = self.db.fetch_query("SELECT * FROM empleados")
        empleado = [Empleado(*data) for data in empleados_data]
        return empleado
    
    def getEmpleadoById(self, id):
        empleado_data = self.db.fetch_query(f"SELECT * FROM empleados WHERE id = {id}")
        if empleado_data:
            data = empleado_data[0]  # Extrae la primera fila
            empleado = Empleado(*data)  # Crea un objeto Empleado con la data
            return empleado
        else:
            print(f"No se encontró ningún empleado con ID {id}")
            return None
    
    def addEmpleado(self, nombre, apellido, email, telefono):
        self.db.fetch_query("INSERT INTO empleados (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)", (nombre, apellido, email, telefono))
        
    def updateEmpleado(self, id, nombre, apellido, email, telefono):
        self.db.fetch_query("UPDATE empleados SET nombre = %s, apellido = %s, email = %s, telefono = %s WHERE id = %s", (nombre, apellido, email, telefono, id))
        
    def deleteEmpleado(self, id):
        self.db.fetch_query("DELETE FROM empleados WHERE id = %s", (id,))
    