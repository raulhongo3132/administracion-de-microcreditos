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

Front-End (FE): Diseña dashboards para cobradores y administrador. - Fernanda Iglesias / Gustavo .

Back-End (BE): Implementa API de cobranza y reportes. - Rebeca Gómez.

DBA: Diseña tablas de clientes, créditos, pagos y genera vistas para reportes. - Alfredo .

## 7. Plan de Trabajo (tentativo)
- 1-2	  Diseño BD + mockups dashboard	  DBA + FE
- 3-4	  API inicial (registro pagos, créditos)	  BE
- 5-6	  Desarrollo FE (formularios, dashboards)	  FE
- 7	  Integración FE+BE + pruebas de flujo	  FE + BE
- 8	  Reportes + documentación final	  DBA + PM

## -- Notas --
- Para el PO, DBA y BE: [Link al google sheets del cliente](https://docs.google.com/spreadsheets/d/1zv5CVmtzXvHYGdaY3UP40fK2whJVYFIGNw84OHz_w0c/edit?usp=sharing).
- Guía de instalación y configuración del proyecto [Link](https://github.com/raulhongo3132/administracion-de-microcreditos/blob/main/primeros_pasos.md).
