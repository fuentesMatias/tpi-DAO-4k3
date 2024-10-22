class Habitacion:
    def __init__(self, numero, tipo, estado, precio):
        self.numero = numero
        self.tipo = tipo
        self.estado = estado
        self.precio = precio

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
