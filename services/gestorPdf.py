from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from services.gestorReserva import GestorReserva
from services.gestorCliente import GestorCliente
from services.gestorHabitaciones import GestorHabitaciones
from services.gestorFactura import gestorFactura
from datetime import datetime
import os

class GestorPDF:
    def __init__(self):
        self.doc = None
        self.gestorReservas = GestorReserva()
        self.gestorClientes = GestorCliente()
        self.gestorHabitaciones = GestorHabitaciones()
        self.gestorReservas = GestorReserva()
        self.gestorFactura = gestorFactura()

    def generarPdfReservas(self, fechaInicio, fechaFin):
        # Configuración del documento y estilo
        self.doc = SimpleDocTemplate("reporte_reservas.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Insertar logo en el encabezado
        logo_path = os.path.abspath("./assets/hotel.png")  # Reemplaza con la ruta de tu logo
        logo = Image(logo_path, 1.5 * inch, 1.5 * inch)  # Ajusta el tamaño según el diseño
        elements.append(logo)

        # Título y descripción del reporte
        title = f"Reporte de Reservas desde {fechaInicio.strftime('%d/%m/%Y').lstrip('0')} hasta {fechaFin.strftime('%d/%m/%Y').lstrip('0')}"
        elements.append(Spacer(1, 0.2 * inch))
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 0.3 * inch))

        # Obtiene las reservas filtradas
        lista_reservas_filtradas = self.gestorReservas.getReservasByFecha(fechaInicio, fechaFin)

        # Encabezado de la tabla
        data = [["Cliente", "Habitación", "Fecha de Entrada", "Fecha de Salida", "Cantidad de Personas"]]

        # Agregar reservas filtradas a la tabla
        for reserva in lista_reservas_filtradas:
            cliente = self.gestorClientes.getClienteById(reserva.getCliente())
            habitacion = self.gestorHabitaciones.getHabitacion(reserva.getHabitacion())
            data.append([
                f"{cliente.getNombre()} {cliente.getApellido()}",
                habitacion.getNumero(),
                datetime.strptime(reserva.getFechaEntrada(), "%Y-%m-%d").strftime("%d/%m/%Y"),
                datetime.strptime(reserva.getFechaSalida(), "%Y-%m-%d").strftime("%d/%m/%Y"),
                reserva.getCantPersonas()
            ])

        # Configuración de estilo para la tabla
        col_widths = [2 * inch, 1 * inch, 1.2 * inch, 1.2 * inch, 1.8 * inch]
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Tamaño de fuente de los títulos
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),  # Padding inferior en encabezados
            ('TOPPADDING', (0, 0), (-1, 0), 8),  # Padding superior en encabezados
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
        ]))

        # Agregar tabla al documento
        elements.append(t)
        elements.append(Spacer(1, 0.3 * inch))

        # Agregar pie de página
        footer_text = f"Reporte generado automáticamente el {datetime.now().strftime('%d/%m/%Y')}"
        elements.append(Paragraph(footer_text, styles['Normal']))

        # Construir el documento PDF
        self.doc.build(elements)
        print("PDF generado con éxito")

        
    def generarPdfIngresos(self):
        # Configuración del documento y estilo
        self.doc = SimpleDocTemplate("reporte_ingresos.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Agregar logo (Asegúrate de tener el archivo 'hotel_logo.png' en la ruta correcta)
        logo_path = os.path.abspath("./assets/hotel.png") 
        elements.append(Image(logo_path, width=2*inch, height=1*inch))  # Ajusta el tamaño del logo según lo necesario
        elements.append(Spacer(1, 0.2 * inch))  # Espaciado entre logo y título

        # Título y descripción del reporte
        title = f"Reporte de INGRESOS POR HABITACIONES"
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 0.3 * inch))  # Espaciado entre el título y la tabla

        # Encabezado de la tabla
        data = [["Habitación", "Tipo", "Ingresos"]]

        # Agregar datos de ingresos por habitación
        habitaciones = self.gestorHabitaciones.getHabitaciones()
        for habitacion in habitaciones:
            total = 0
            reservas = self.gestorReservas.getReservasByHabitacion(habitacion.getId())
            for reserva in reservas:
                facturas = self.gestorFactura.getFacturasByReserva(reserva.getId())
                for factura in facturas:
                    total += factura.getTotal()
            data.append([habitacion.getNumero(), habitacion.getTipo(), f"${total:,.2f}"])  # Formato de ingresos con separador de miles

        # Estilo de la tabla
        col_widths = [2 * inch, 2 * inch, 2 * inch]
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Fondo azul claro en el encabezado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Texto negro en el encabezado
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación central
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado en la parte inferior del encabezado
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Fondo blanco en las celdas
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de borde finas
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Borde alrededor de la tabla
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas internas de la rejilla
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Alineación a la derecha para los ingresos
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente para la tabla
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])  # Fondo alternado en las filas
        ]))

        # Agregar tabla al documento
        elements.append(t)
        elements.append(Spacer(1, 0.3 * inch))
        
        footer_text = f"Reporte generado automáticamente el {datetime.now().strftime('%d/%m/%Y')}"
        elements.append(Paragraph(footer_text, styles['Normal']))

        # Construir el documento PDF
        self.doc.build(elements)
        print("PDF generado con éxito")
        
        
    def generarPdfPromedioOcupacion(self):
        # fecha actual, aca iria un set.
        self.fecha = datetime.now().strftime('%d/%m/%Y')
        
        # Configuración del documento y estilo
        self.doc = SimpleDocTemplate("reporte_promedio_ocupacion.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Agregar logo (Asegúrate de tener el archivo 'hotel_logo.png' en la ruta correcta)
        logo_path = os.path.abspath("./assets/hotel.png") 
        elements.append(Image(logo_path, width=2*inch, height=1*inch))  # Ajusta el tamaño del logo según lo necesario
        elements.append(Spacer(1, 0.2 * inch))  # Espaciado entre logo y título

        # Título y descripción del reporte
        title = f"Reporte de OCUPACIÓN PROMEDIO por tipo de habitación en la fecha {self.fecha}"
        elements.append(Paragraph(title, styles['Title']))
        elements.append(Spacer(1, 0.3 * inch))  # Espaciado entre el título y la tabla

        # Encabezado de la tabla
        data = [["Tipo", "Ocupación Promedio"]]

        # Promedio de ocupación por tipo de habitación
        promedioHabitacionesSimples = self.gestorReservas.porcentajeOcupacion("simple")
        promedioHabitacionesDobles = self.gestorReservas.porcentajeOcupacion("doble")
        promedioHabitacionesSuites = self.gestorReservas.porcentajeOcupacion("suite")
        
        def formatear(value):
            if isinstance(value, str):
                return value  # Si es un string, no hacemos el formateo
            else:
                return f"{value:.2f}%"  # Si no es un string, formateamos a 2 decimales
            
        data.append(["Simple", formatear(promedioHabitacionesSimples)])
        data.append(["Doble", formatear(promedioHabitacionesDobles)])
        data.append(["Suite", formatear(promedioHabitacionesSuites)])


        # Estilo de la tabla
        col_widths = [2.5 * inch, 3.5 * inch]
        t = Table(data, colWidths=col_widths)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Fondo azul claro en el encabezado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Texto negro en el encabezado
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alineación central
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente en negrita para el encabezado
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado en la parte inferior del encabezado
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Fondo blanco en las celdas
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Líneas de borde finas
            ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Borde alrededor de la tabla
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Líneas internas de la rejilla
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente para la tabla
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])  # Fondo alternado en las filas
        ]))

        # Agregar tabla al documento
        elements.append(t)
        elements.append(Spacer(1, 0.3 * inch))
        
        # Pie de página
        footer_text = f"Reporte generado automáticamente el {datetime.now().strftime('%d/%m/%Y')}"
        elements.append(Paragraph(footer_text, styles['Normal']))

        # Construir el documento PDF
        self.doc.build(elements)
        print("PDF generado con éxito")
        
    
        

        
        

    
