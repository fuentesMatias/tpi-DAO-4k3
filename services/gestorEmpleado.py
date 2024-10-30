from database.conexion import DbSingleton
from models.empleado import Empleado
class GestorEmpleado:
    def __init__(self):
        self.db = DbSingleton()
        
    def getEmpleados(self):
        empleado_data = self.db.query("SELECT * FROM empleados")
        empleado = Empleado(empleado_data[0], empleado_data[1], empleado_data[2], empleado_data[3], empleado_data[4])
        return empleado
    
    def getEmpleado(self, id):
        return self.db.query("SELECT * FROM empleados WHERE id = %s", (id,))
    
    def addEmpleado(self, nombre, apellido, email, telefono):
        self.db.query("INSERT INTO empleados (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)", (nombre, apellido, email, telefono))
        
    def updateEmpleado(self, id, nombre, apellido, email, telefono):
        self.db.query("UPDATE empleados SET nombre = %s, apellido = %s, email = %s, telefono = %s WHERE id = %s", (nombre, apellido, email, telefono, id))
        
    def deleteEmpleado(self, id):
        self.db.query("DELETE FROM empleados WHERE id = %s", (id,))
    