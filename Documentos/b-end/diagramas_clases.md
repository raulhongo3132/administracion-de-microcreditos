+---------------------------+      +--------------------------+    +--------------------------+
|        Usuario            |      |        Cartera           |    |      Notificacion        |
|                           |      |                          |    |                          |
+---------------------------+      +--------------------------+    +--------------------------+
| -usuario_id Int	        |      | -cartera_id Int          |    | -notificacion_id Int     |
| -nombre varchar(50)       |      | -nombre varchar(50)      |    | -usuario_id   Int        |
| -email varchar(100)       |      | -cobrador_id Int         |    | -tipo varchar(100)       |
| -telefono int             |      |                          |    | -mensaje varchar(100)    |                                                                                    |                                 |    | -vista
| -password_hash (100)      |      | -descripcion varchar(100)|    +--------------------------+
| -rol varchar (100)        |      +--------------------------+    | +marcarVista()           |  
| -status varchar (100)     |      | +anadirCliente()         |    | +enviar()                |
+---------------------------+      | +quitarCliente()         |    | +alertaMora()            |
| +login()                  |      |                          |    +--------------------------+
|  +autenticarContrasena()  |      +--------------------------+
| +cambiarContrasena()      |
| +logout()                 |
+---------------------------+


+-------------------------------+     +--------------------------+   +-----------------------------+
|          Cliente              |     |         Credito          |   |             Pago            |
|                               |     |                          |   |                             |
+-------------------------------+     +--------------------------+   +-----------------------------+
| -cliente_id Int               |     | -credito_id Int          |   | -pago_id Int                |
| -nombre varchar(100)          |     | -cliente_id Int          |   | -prestamo_id Int            |
| -identificacion varchar(100)  |     | -montoPrincipal Decimal  |   | -fecha_pago  DateTime	   |
| -direccion varchar (100)      |     | -saldoActual Decimal     |   | -retraso                    |
| -telefono varchar (100)       |     | -tasaInteres Decimal     |   | -monto    decimal           |
| -email varchar (100)          |     | -fechaOtorgamiento Date  |   | -cobrador_id  Int           |
| -fecha_registro DateTime      |     | -plazoMeses Int          |   +-----------------------------+
+-------------------------------+     | -estado varchar(50)      |   | + agregarPago()             |
|                               |     | -cartera_id Int          |   | + consultar_pago()          |    
| +obtenerPrestamos()           |     +--------------------------+   | + calcularDiasRetraso()     |
+-------------------------------+     | +aplicarPago()           |   | + modificar_pago()          |
                                      | +calcularIntereses()     |   |                             |
                                      | +comprobarMora()         |   +-----------------------------+
                                      +--------------------------+
+-------------------------------+                                       
|          Cobrador             |
|                               |     +--------------------------+   +-----------------------------+
+-------------------------------+     |       Prestamo           |   |            Cuota            |
| -id_cobrador Int              |     |                          |   |                             |
+-------------------------------+     |                          |   +-----------------------------+
| +IngresoPagosDiarios()        |     |                          |   | -cuota_id Int               |
| +ReportarPagos()              |     +--------------------------+   | -credito_id  Int            |
| +ConsultarPrestamos()         |     | -prestamo_id Int         |   | -cuota_numero               |
+-------------------------------+     | -cliente varchar (100)   |   | -fecha_vencimiento  DateTime|
                                      | -monto  int              |   | -monto_cuota Decimal        |
+-------------------------------+     | -retorno_base            |   | -pagado  bool               |
|        Administrador          |     |	-plazo                   |   | -fecha_pago DateTime        |
|                               |     | -dias_mora               |   +-----------------------------+
+-------------------------------+     | -retorno_actual          |   | +marcarPago(pago_id)        |
| +AutorizarPrestamos()         |     | -fecha_entrega           |   | +estadoMora()               |
| +ConsultarPagos()             |     | -fecha_fin               |   +-----------------------------+
| +ConsultarReportes()          |     | -estado                  |   
| +DeterminarMora()             |     | -saldo_actual            |   +------------------------------+
| +ConsultarResumenGeneral()    |     +--------------------------+   |          Reportes            |
+-------------------------------+     | +calcularPagoDiario()    |   |                              |
                                      | +agregarMora()           |   +------------------------------+
                                      | +agregarPrestamo()       |   | +generarReporteParaCobrador()|
                                      | +consultarPrestamos()    |   | +genertReporteMora()         |
                                      | +modificarPrestamo()     |   +------------------------------+
                                      | +cerrarPrestamo()        |
                                      +--------------------------+
