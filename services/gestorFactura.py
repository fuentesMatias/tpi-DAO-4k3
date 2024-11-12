from database.conexion import DbSingleton
from models.factura import Factura
from services.gestorCliente import GestorCliente
from services.gestorReserva import GestorReserva
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


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
        precioTotal = self.gestorReservas.calcularTotalReserva(reserva.getId())
        
        # obtener la fecha de emision
        fecha_emision = datetime.date.today()
        
        # guardar la factura en la base de datos
        query = "INSERT INTO facturas (id_cliente, id_reserva, fecha_emision, total) VALUES (?, ?, ?, ?)"
        #pasar todos los valores como string
        self._db.execute_query(query, (str(idCliente), str(idReserva), fecha_emision, str(precioTotal)))
        self._db.commit()
        
        
    def getFacturasByReserva(self, idReserva):
        query = "SELECT * FROM facturas WHERE id_reserva = ?"
        facturas_data = self._db.fetch_query(query, (idReserva,))
        facturas = [Factura(*data) for data in facturas_data]
        return facturas


    def imprimirFacturaPDF(self, factura):
        cliente = self.gestorClientes.getClienteById(factura.getCliente())
        reserva = self.gestorReservas.getReservaById(factura.getReserva())
        
        # Nombre del archivo PDF
        pdf_filename = f"Factura_{factura.getId()}.pdf"
        
        # Crear un documento PDF
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
        elements = []

        # Estilos para el texto
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        normal_style = styles["BodyText"]

        # Título de la factura
        elements.append(Paragraph(f"Factura #{factura.getId()}", title_style))
        elements.append(Spacer(1, 12))  # Espacio en blanco

        # Información del cliente
        elements.append(Paragraph(f"{cliente.__str__()}", normal_style))
        elements.append(Spacer(1, 12))

        # Información de la reserva
        elements.append(Paragraph(f"{reserva.__str__()}", normal_style))
        elements.append(Spacer(1, 12))

        # Fecha de emisión
        elements.append(Paragraph(f"Fecha de Emisión: {factura.getFechaEmision()}", normal_style))
        elements.append(Spacer(1, 12))

        # Total
        elements.append(Paragraph(f"Total: ${factura.getTotal()}", normal_style))
        elements.append(Spacer(1, 12))

        # Línea divisoria
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Detalles de la Factura", styles["Heading2"]))
        elements.append(Spacer(1, 12))

        # Tabla de resumen (puedes modificar y añadir más datos según necesites)
        data = [
            ["ID Factura", factura.getId()],
            ["Cliente", cliente.getNombre() + cliente.getApellido()],
            ["Reserva", factura.getReserva()],
            ["Fecha de Emisión", factura.getFechaEmision()],
            ["Total", f"${factura.getTotal()}"]
        ]
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(table)

        # Construir el PDF
        doc.build(elements)

        print(f"Factura PDF generada: {pdf_filename}")

    
    def getFacturaByClienteAndReserva(self, idCliente, idReserva):
        query = "SELECT * FROM facturas WHERE id_cliente = ? AND id_reserva = ?"
        factura_data = self._db.fetch_query(query, (idCliente, idReserva))
        factura = Factura(*factura_data[0])
        return factura