from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from services.gestorReserva import GestorReserva
from services.gestorCliente import GestorCliente
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorFactura import gestorFactura

class GestorPDF:
    def __init__(self):
        self.doc = None
        self.gestorReservas = GestorReserva()
        self.gestorClientes = GestorCliente()
        self.gestorHabitaciones = GestorHabitaciones()
        self.gestorReservas = GestorReserva()
        self.gestorFactura = gestorFactura()

    def generar_pdf_reservas(self, fechaInicio, fechaFin):
        # Configuración del documento y estilo
        self.doc = SimpleDocTemplate("reporte_reservas.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Título y descripción del reporte
        title = f"Reporte de Reservas desde {fechaInicio} hasta {fechaFin}"
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 0.2 * inch))
        lista_reservas_filtradas = self.gestorReservas.getReservasByFecha(fechaInicio, fechaFin)

        # Encabezado de la tabla
        data = [["Cliente", "Habitación", "Fecha de Entrada", "Fecha de Salida", "Cantidad de Personas"]]

        # Agregar reservas filtradas a la tabla
        for reserva in lista_reservas_filtradas:
            data.append([
                self.gestorClientes.getClienteById(reserva.getCliente()).getNombre(),
                self.gestorHabitaciones.getHabitacion(reserva.getHabitacion()).getNumero(),
                reserva.getFechaEntrada(),
                reserva.getFechaSalida(),
                reserva.getCantPersonas()
            ])
        # Estilo de la tabla
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Agregar tabla al documento
        elements.append(t)
        self.doc.build(elements)
        print("PDF generado con éxito")
        
    def generar_pdf_ingresos(self):
        # Configuración del documento y estilo
        self.doc = SimpleDocTemplate("reporte_ingresos.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        # Título y descripción del reporte
        title = f"Reporte de INGRESOS POR HABITACIONES"
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 0.2 * inch))
        # Encabezado de la tabla
        data = [["Habitación", "Tipo", "Ingresos"]]
        # Agregar reservas filtradas a la tabla
        habitaciones = self.gestorHabitaciones.getHabitaciones()
        # por cada habitacion traigo sus reservas usando el gestor de reservas y por cada reserva traigo todas sus facturas y sumo el total
        for habitacion in habitaciones:
            total = 0
            reservas = self.gestorReservas.getReservasByHabitacion(habitacion.getId())
            for reserva in reservas:
                facturas = self.gestorFactura.getFacturasByReserva(reserva.getId())
                for factura in facturas:
                    total += factura.getTotal()
            data.append([habitacion.getNumero(), habitacion.getTipo(), total])
        
        t = Table(data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Agregar tabla al documento
        elements.append(t)
        self.doc.build(elements)
        print("PDF generado con éxito")
        
        

        
        

    
