# 4K3_DAO_TP_Grupo12
# Sistema de Gestión de Hotel

## Descripción

Este proyecto tiene como objetivo desarrollar un **Sistema de Gestión de Hotel** que permita gestionar de manera eficiente las habitaciones, reservas, clientes, facturación, empleados y otros servicios dentro de un hotel. El sistema ofrecerá funcionalidades para el registro, consulta y administración de datos, además de incluir reportes para la toma de decisiones.

---

## Funcionalidades

### Clases

- **Habitación**: 
  - Atributos:
    - Número
    - Tipo (simple, doble, suite)
    - Estado (disponible/ocupada)
    - Precio por noche

- **Cliente**: 
  - Atributos:
    - ID
    - Nombre
    - Apellido
    - Dirección
    - Teléfono
    - Email

- **Reserva**: 
  - Atributos:
    - ID
    - Cliente
    - Habitación
    - Fecha de entrada
    - Fecha de salida
    - Cantidad de personas

- **Factura**: 
  - Atributos:
    - ID
    - Cliente
    - Reserva
    - Fecha de emisión
    - Total

- **Empleado**: 
  - Atributos:
    - ID
    - Nombre
    - Apellido
    - Cargo (recepcionista, servicio de limpieza, etc.)
    - Sueldo

### Operaciones

1. **Registro de Habitaciones**: Permitir el registro de nuevas habitaciones en el sistema.
2. **Registro de Clientes**: Permitir el registro de nuevos clientes.
3. **Registro de Reservas**: Permitir reservar habitaciones y asignarlas a clientes.
4. **Registro de Facturas**: Generar facturas automáticamente al finalizar la estadía del cliente.
5. **Asignación de Empleados a Habitaciones**: Asignar empleados para el servicio de limpieza de las habitaciones.
6. **Consulta de Disponibilidad de Habitaciones**: Consultar la disponibilidad de habitaciones en una fecha específica.
7. **Reportes**:
   - Listar todas las reservas realizadas en un periodo de tiempo.
   - Generar un reporte de ingresos por habitaciones y servicios extras.
   - Reporte de ocupación promedio por tipo de habitación.

### Dificultad Extra

- **Validaciones**:
  - Verificar que las fechas de reserva no se superpongan para la misma habitación.
  - Verificar que los empleados asignados a habitaciones no tengan más de 5 asignaciones diarias.

- **Implementar reportes**:
  - Generar un gráfico de barras mostrando la ocupación promedio por tipo de habitación.
  - Generar un gráfico de líneas mostrando los ingresos mensuales.

### Operaciones Adicionales

1. **Gestión de Servicios Extras**: Implementar un módulo para manejar servicios adicionales como spa, restaurante, lavandería, etc. Los clientes podrán contratar estos servicios durante su estancia.
2. **Mantenimiento de Habitaciones**: Crear un sistema para programar y registrar tareas de mantenimiento de las habitaciones, con la posibilidad de bloquear habitaciones durante el mantenimiento.
3. **Gestión de Eventos**: Añadir un módulo para gestionar eventos (conferencias, bodas, etc.) que se lleven a cabo en el hotel, con la posibilidad de reservar salones y habitaciones específicas para el evento.
4. **Programas de Fidelización**: Implementar un sistema de puntos para clientes frecuentes, donde puedan acumular puntos y canjearlos por descuentos en futuras reservas.

### Reportes Adicionales

- **Reporte de Servicios Extras Contratados**: Generar un reporte que liste los servicios extras contratados por los clientes durante su estancia, con un gráfico de barras que muestre los servicios más solicitados.
- **Informe de Mantenimiento de Habitaciones**: Crear un reporte que muestre todas las tareas de mantenimiento realizadas, incluyendo las habitaciones afectadas y el tiempo que estuvieron fuera de servicio.
- **Estadísticas de Programas de Fidelización**: Generar un reporte sobre el uso de los programas de fidelización, mostrando cuántos puntos han sido canjeados y cuántos clientes han participado.

---

## Instalación

Instrucciones para instalar y ejecutar el proyecto.

```bash
# Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>

# Cambiar al directorio del proyecto
cd <NOMBRE_DEL_DIRECTORIO>

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el sistema
python main.py