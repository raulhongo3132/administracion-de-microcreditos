-- =======================================
-- CREACIÓN DE LA BASE DE DATOS
-- =======================================
CREATE DATABASE sistema_creditos;

-- Conectarse a la BD (solo para psql CLI)
-- \c sistema_creditos;

-- =======================================
-- TABLA USUARIO
-- =======================================
CREATE TABLE usuario (
    idusuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(20) CHECK (rol IN ('admin','gestor','cliente')) NOT NULL
);

-- =======================================
-- TABLA CLIENTE
-- =======================================
CREATE TABLE cliente (
    idcliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    documentos TEXT,
    idusuario INT,
    CONSTRAINT fk_cliente_usuario FOREIGN KEY (idusuario) REFERENCES usuario(idusuario)
);

-- =======================================
-- TABLA CREDITO
-- =======================================
CREATE TABLE credito (
    idcredito SERIAL PRIMARY KEY,
    idcliente INT NOT NULL,
    monto NUMERIC(10,2) NOT NULL,
    interes NUMERIC(5,2) NOT NULL,
    fechainicio DATE NOT NULL,
    fechafin DATE NOT NULL,
    plazo INT NOT NULL,
    pagodiario NUMERIC(10,2),
    deudapendiente NUMERIC(10,2),
    estado VARCHAR(20) CHECK (estado IN ('activo','pagado','atrasado','cancelado')) DEFAULT 'activo',
    CONSTRAINT fk_credito_cliente FOREIGN KEY (idcliente) REFERENCES cliente(idcliente)
);

-- =======================================
-- TABLA PAGO
-- =======================================
CREATE TABLE pago (
    idpago SERIAL PRIMARY KEY,
    idcredito INT NOT NULL,
    fechapago DATE NOT NULL,
    montopagado NUMERIC(10,2) NOT NULL,
    estado VARCHAR(20) CHECK (estado IN ('validado','pendiente')) DEFAULT 'pendiente',
    CONSTRAINT fk_pago_credito FOREIGN KEY (idcredito) REFERENCES credito(idcredito)
);

-- =======================================
-- TABLA MORA
-- =======================================
CREATE TABLE mora (
    idmora SERIAL PRIMARY KEY,
    idcredito INT NOT NULL,
    diasretraso INT NOT NULL,
    montoextra NUMERIC(10,2),
    fechacalculo DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_mora_credito FOREIGN KEY (idcredito) REFERENCES credito(idcredito)
);

-- =======================================
-- TABLA ALERTA
-- =======================================
CREATE TABLE alerta (
    idalerta SERIAL PRIMARY KEY,
    idcredito INT NOT NULL,
    tipo VARCHAR(50),
    mensaje TEXT,
    fechaalerta DATE DEFAULT CURRENT_DATE,
    CONSTRAINT fk_alerta_credito FOREIGN KEY (idcredito) REFERENCES credito(idcredito)
);

-- =======================================
-- TABLA REPORTE
-- =======================================
CREATE TABLE reporte (
    idreporte SERIAL PRIMARY KEY,
    fechagenerado DATE DEFAULT CURRENT_DATE,
    tipo VARCHAR(50),
    totalrecaudado NUMERIC(12,2) DEFAULT 0
);
