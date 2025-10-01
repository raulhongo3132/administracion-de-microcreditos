# Plan de Negocios – Sistema de Administración de Microcréditos
## 1. Resumen Ejecutivo

Objetivo: Desarrollar una aplicación web para que los cobradores de microcréditos registren pagos, consulten saldos y generen reportes en tiempo real para el administrador principal.

Usuarios clave:
- Cobradores: capturan pagos y actualizan información.
- Administrador principal: consulta reportes y controla cartera de créditos.

Propuesta de Valor:
- Centralizar y digitalizar la información de los cobros.
- Reducir errores y fraudes en el manejo de dinero.
- Mejorar la rendición de cuentas y la transparencia.
- Mejorar la accesibilidad a los cobradores y administrador.

## 2. Análisis del Mercado

El mercado objetivo está conformado por prestamistas y administradores de microcréditos en centrales de abastos y mercados similares. Estos usuarios suelen operar de manera manual o con sistemas rudimentarios, lo que representa una oportunidad clara para la digitalización. No existe una oferta tecnológica especializada ampliamente adoptada, por lo que la competencia directa es limitada. La tendencia hacia la digitalización de procesos financieros informales y el crecimiento del sector microcrediticio apoyan la viabilidad del proyecto.


Problema actual:
 - Registros manuales en libretas o hojas de cálculo.
 - Dificultad para verificar pagos y saldos reales.
 - Reportes tardados y poco confiables.

Oportunidad:
- Digitalizar el proceso de cobranza.
- Facilitar control diario de ingresos y adeudos.
- Automatizar reportes para el administrador.

## 3. Modelo de Uso

No es un sistema abierto al público.

Clientes internos: personal de cobranza y administrador principal.

Beneficios esperados:

- Trazabilidad de cada pago.
- Control centralizado de cuentas.
- Reducción de tiempos en conciliación de dinero.

## 4. Propuesta de Solución

Funcionalidades clave:
- Registro de usuarios cobradores.
- Asignación de cartera de créditos a cada cobrador.
- Registro de pagos por cliente.
- Consulta de historial de pagos y adeudos.
- Reportes automáticos para el administrador (por cobrador, por periodo, por monto).
- Alertas de clientes morosos.
- Agregar clientes/creditos nuevos.
- Administrar moras.

## 5. Estrategia de Implementación

Front-End (HTML+CSS+JS):
- Dashboard para cobradores.
- Dashboard de control para administrador.
- Login

Back-End (Flask):

- API para registrar pagos, actualizar saldos y generar reportes.
- Roles de usuario: cobrador y administrador.

Base de Datos (Postgres):
- Tablas principales: usuarios, creditos, pagos, clientes, carteras.
- Vistas o queries para reportes de cobranza.

Control de versiones (GitHub):
- Ramas: main, develop, feature/*.
- Uso de Issues y Pull Requests.

## 6. Roles y Responsabilidades

Product Owner (PO): Define requerimientos de cobradores y administrador. - Rene Bermejo.

Project Manager (PM): Planifica actividades y hace seguimiento. - Raúl Valverde.

Front-End (FE): Diseña dashboards para cobradores y administrador. - Fernanda Iglesias / Gustavo Granados.

Back-End (BE): Implementa API de cobranza y reportes. - Rebeca Gómez.

DBA: Diseña tablas de clientes, créditos, pagos y genera vistas para reportes. - Alfredo Esquivel.

## 7. Plan de Trabajo (tentativo)
- 1-2	  Diseño BD + mockups dashboard	  DBA + FE
- 3-4	  API inicial (registro pagos, créditos)	  BE
- 5-6	  Desarrollo FE (formularios, dashboards)	  FE
- 7	  Integración FE+BE + pruebas de flujo	  FE + BE
- 8	  Reportes + documentación final	  DBA + PM



Organización y Gestión
La estructura operativa inicial contempla tres roles principales:
•	Cobrador: Usuario final que realiza la gestión diaria de créditos y pagos.
•	Administrador: Responsable de la configuración, reportes y supervisión general.
•	Superusuario: Encargado del mantenimiento, actualizaciones y mejora continua del sistema.
Se prevé un equipo de desarrollo ágil y soporte técnico remoto. La gestión será centralizada y escalable según la demanda.

Producto o Servicio
El sistema será una aplicación web responsive con las siguientes funcionalidades, organizadas por versión:
Función	MVP (Versión Inicial)	Versiones Futuras
Registro de créditos	Si	Mejoras en flujo
Pagos diarios	Si	Ninguna por el momento
Cálculo de moras	Si	Automatización avanzada
Alertas y reportes	Basicos	Dashboard interactivo
Gestión de tandas	No	Si
Administración financiera	No	Si (Personal/Laboral)
Soporte offline	No	Si
Estrategia de Marketing y Ventas
La comercialización se basará en un enfoque directo y personalizado:
•	Presentación del sistema a asociaciones de prestamistas y administradores de la central de abastos.
•	Demostraciones in situ y período de prueba gratuito para reducir barreras de adopción.
•	Estrategia de precios por suscripción mensual o anual, ajustada al volumen de créditos gestionados.
•	Uso de casos de éxito y testimonios para construir confianza y referencias.




Plan Operativo
Fase	Actividades Clave	Duración Estimada
1. Desarrollo MVP	Diseño, programación, pruebas internas	3-4 meses
2. Pruebas piloto	Implementación con grupo pequeño de usuarios	1 mes
3. Lanzamiento	Despliegue oficial, soporte inicial, marketing	Continuo
4. Mejoras	Desarrollo de nuevas funcionalidades	A partir del 6° mes

Plan Financiero
Se tiene pensado plantear un modelo de ingresos basado en suscripciones. Los costos iniciales estarán asociados al desarrollo, hosting y marketing. Se tiene planeado alcanzar el punto de equilibrio en el primer año, con crecimiento sostenido a partir del segundo año mediante la incorporación de nuevos clientes y funcionalidades premium.
Anexos
Se incluirán:
•	Cuestionario de necesidades.
•	Diagramas de flujo de procesos de crédito y pago.
•	Prototipos de interfaz de usuario.
•	Cronograma detallado de desarrollo y lanzamiento
