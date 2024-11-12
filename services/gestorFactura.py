from database.conexion import DbSingleton
from models.factura import Factura
from services.gestorCliente import GestorCliente
from services.gestorReserva import GestorReserva
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


class gestorFactura:
    def __init__(self):
        self._db = DbSingleton()
        self.gestorReservas = GestorReserva()
        self.gestorClientes = GestorCliente()
        self.facturas = []

    def getFacturas(self):
        facturas_data = self._db.fetch_query("SELECT * FROM facturas")
        facturas = [Factura(*data) for data in facturas_data]
        return facturas

    def registrarFactura(self, idCliente, idReserva):
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

        lastId = self.getIdFacturaMasReciente()

        factura = Factura(lastId, idCliente, idReserva, fecha_emision, precioTotal)

        self.facturas.append(factura)

        self.imprimirFacturaPDF(factura)

        # guardar la factura en la base de datos
        query = "INSERT INTO facturas (id_cliente, id_reserva, fecha_emision, total) VALUES (?, ?, ?, ?)"
        # pasar todos los valores como string
        self._db.execute_query(
            query, (str(idCliente), str(idReserva), fecha_emision, str(precioTotal))
        )
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
        header_style = ParagraphStyle(
            "HeaderStyle",
            fontSize=14,
            leading=16,
            spaceAfter=12,
            alignment=1,  # Centramos el texto
        )

        # Logo (Asegúrate de tener un archivo "logo.png" en tu directorio de trabajo)
        try:
            logo = Image("./assets/hotel.png", width=1 * inch, height=1 * inch)
            logo.hAlign = "LEFT"
            elements.append(logo)
        except Exception as e:
            print("Error al cargar el logo:", e)

        # Título de la factura
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(f"Factura #{factura.getId()}", title_style))
        elements.append(Spacer(1, 12))  # Espacio en blanco

        # Información del cliente
        cliente_info = f"""
        <b>Cliente:</b> {cliente.getNombre()} {cliente.getApellido()}<br/>
        <b>Email:</b> {cliente.getemail()}<br/>
        <b>Teléfono:</b> {cliente.getTelefono()}<br/>
        """
        elements.append(Paragraph(cliente_info, normal_style))
        elements.append(Spacer(1, 12))

        # Información de la reserva
        reserva_info = f"""
        <b>Reserva ID:</b> {reserva.getId()}<br/>
        <b>Fecha de Reserva:</b> {reserva.getFechaEntrada()}<br/>
        <b>Habitación:</b> {reserva.getHabitacion()}<br/>
        """
        elements.append(Paragraph(reserva_info, normal_style))
        elements.append(Spacer(1, 12))

        # Fecha de emisión
        elements.append(
            Paragraph(f"<b>Fecha de Emisión:</b> {factura.getFechaEmision()}", normal_style)
        )
        elements.append(Spacer(1, 12))

        # Línea divisoria
        elements.append(Paragraph("Detalles de la Factura", styles["Heading2"]))
        elements.append(Spacer(1, 12))

        # Tabla de resumen
        data = [
            ["Descripción", "Valor"],
            ["ID Factura", factura.getId()],
            ["Cliente", f"{cliente.getNombre()} {cliente.getApellido()}"],
            ["ID Reserva", factura.getReserva()],
            ["Fecha de Emisión", factura.getFechaEmision()],
            # ["Total", f"${factura.getTotal()}"]
        ]

        table = Table(data, colWidths=[3 * inch, 3 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elements.append(table)
        elements.append(Spacer(1, 24))

        # Total destacado
        total_style = ParagraphStyle(
            "TotalStyle",
            fontSize=14,
            leading=16,
            spaceAfter=12,
            textColor=colors.green,
            alignment=1,  # Alineado a la derecha
        )
        elements.append(Paragraph(f"Total:  ${factura.getTotal()}", total_style))

        # Construir el PDF
        doc.build(elements)
        print(f"Factura PDF generada: {pdf_filename}")

    def getFacturaByClienteAndReserva(self, idCliente, idReserva):
        query = "SELECT * FROM facturas WHERE id_cliente = ? AND id_reserva = ?"
        factura_data = self._db.fetch_query(query, (idCliente, idReserva))
        factura = Factura(*factura_data[0])
        return factura

    def getIdFacturaMasReciente(self):
        query = "SELECT MAX(id) FROM facturas"
        factura_data = self._db.fetch_query(query)

        # Verificamos si hay resultados y devolvemos el id de la factura más reciente
        if factura_data and factura_data[0][0] is None:
            return 1
        else:
            print(f"Id de la factura mas reciente: {factura_data[0][0]}")
            return factura_data[0][0]
