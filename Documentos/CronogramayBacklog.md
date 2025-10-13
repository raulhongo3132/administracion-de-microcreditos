CRONOGRAMA

Análisis y diseño: 2 semanas

Desarrollo del backend: 4 semanas

Desarrollo frontend: 3 semanas

Integración y pruebas: 2 semanas

Implementación: 1 semana


BACKLOG DE HISTORIAS DE USUARIO

US-1.1 - Prioridad: Alta
Historia de Usuario: Como cobrador o administrador, quiero iniciar sesión con un usuario y contraseña para acceder de forma segura al sistema.

Criterios de Aceptación:
1.Los campos de usuario y contraseña son obligatorios.
2.El sistema muestra un mensaje de error claro si las credenciales son incorrectas.
3.Al autenticarse correctamente, el usuario es redirigido al dashboard.


US-1.2 - Prioridad: Media
Historia de Usuario: Como administrador, quiero poder cerrar mi sesión para garantizar que nadie más acceda a mi cuenta.

Criterios de Aceptación:
Existe un botón de "Cerrar sesión".
Al hacer clic, la sesión se invalida y se redirige al usuario a la pantalla de login.

US-2.1 - Prioridad: Alta
Historia de Usuario: Como cobrador, quiero registrar un nuevo crédito para tener un control inicial del préstamo.

Criterios de Aceptación:
1.Debo poder ingresar: nombre del cliente, monto, retorno de inversión (o interés), plazo (fecha inicio y fin), pago diario esperado.
2.El sistema debe calcular automáticamente el pago diario esperado si se ingresa el monto y el plazo.
3.Se debe poder subir una imagen de la identificación del cliente y/o la ubicación de su local.
4.Al guardar, el crédito debe aparecer en la lista de "Activos".

US-2.2 - Prioridad: Alta
Historia de Usuario: Como cobrador, quiero ver una lista de todos mis créditos activos para tener una visión general de mi cartera.

Criterios de Aceptación:
1.La lista muestra: Nombre del cliente, monto total, pago diario esperado, fecha de fin, deuda pendiente.
2.Se debe poder hacer clic en un cliente para ver sus detalles.
3.La lista se debe poder ordenar y buscar por nombre.

US-2.3 - Prioridad: Alta
Historia de Usuario: Como cobrador, quiero ver el detalle completo de un cliente y su crédito para conocer su historial y estado actual.

Criterios de Aceptación:
1.Se debe poder ver los detalles muestra de toda la información de la US-2.1.
2.Muestra un historial de todos los pagos realizados (fecha, monto).
3.Muestra el avance del pago.
4.Muestra si tiene mora pendiente.
5.Permite editar información básica como número de teléfono.

US-3.1 - Prioridad: Crítica
Historia de Usuario: Como cobrador, quiero registrar el pago diario de un crédito para actualizar el estado de la deuda.

Criterios de Aceptación:
1.Desde la lista o el detalle de un crédito, se debe poder ingresar el monto pagado del día de hoy.
2.Si el deudor no paga, se debe poder registrar un 0.
3.El sistema debe actualizar automáticamente la deuda pendiente y el avance del pago.

US-3.2 - Prioridad: Alta
Historia de Usuario: Como cobrador, quiero que el sistema calcule y muestre el total recaudado al final del día para hacer mi cierre diario.

Criterios de Aceptación:
1.Debe existir una pantalla o sección de Resumen Diario.
2.Se debe mostrar la suma total de todos los pagos registrados en el día.
3.Se debe mostrar la cantidad de créditos cobrados y no cobrados ese día.

US-4.1 - Prioridad: Alta
Historia de Usuario: Como cobrador, quiero que el sistema me alerte con una bandera o color en la lista de créditos cuando un pago esté atrasado para identificar rápidamente moras.

Criterios de Aceptación:
1.El sistema debe comparar la fecha actual con la fecha de pago esperada de cada cuota.
2.Los créditos de pagos atrasados se deben destacar con un color rojo.

US-4.2 - Prioridad: Alta
Historia de Usuario: Como cobrador, quiero poder calcular y aplicar una mora manualmente a un crédito para agregar días extra de pago según el acuerdo con el cliente.

Criterios de Aceptación:
1.Se debe tener un botón de calcular mora desde los detalles de un crédito en mora.
2.Se debe poder ingresar los días de retraso o el monto de la mora manualmente.
3.El sistema debe agregar una mora como una nueva cuota o incrementar la deuda total.

US-5.1 - Prioridad: Media
Historia de Usuario: Como cobrador, quiero ver un panel de control (dashboard) al iniciar sesión para tener una visión centralizada de mi operación.

Criterios de Aceptación:
1.El dashboard debe mostrar: total recaudado hoy, total de créditos activos y total de créditos en mora.
2.Se debe mostrar una gráfica simple del progreso de la cobranza del mes.

US-5.2 - Prioridad: Media
Historia de Usuario: Como administrador, quiero generar un reporte mensual de toda la gestión de cobranza para análisis y toma de decisiones.

Criterios de Aceptación:
1.El reporte muestra: Total prestado, Total recaudado, Total de moras aplicadas y lista de créditos cerrados en el mes.
2.Se debe poder exportar el reporte a PDF o Excel.