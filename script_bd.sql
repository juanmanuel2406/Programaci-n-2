-- ============================================================
-- Script para crear la base de datos del Homebanking en MySQL
-- Ejecutar en DbVisualizer conectado al servidor MySQL
-- ============================================================

-- 1. Crear la base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS homebanking
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- 2. Seleccionar la base de datos
USE homebanking;

-- 3. Tabla: user
-- Almacena los usuarios registrados con su contraseña hasheada (bcrypt)
CREATE TABLE IF NOT EXISTS user (
    id           INT          NOT NULL AUTO_INCREMENT,
    username     VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Tabla: account
-- Almacena las cuentas bancarias de cada usuario por moneda
CREATE TABLE IF NOT EXISTS account (
    id         INT         NOT NULL AUTO_INCREMENT,
    user_id    INT         NOT NULL,
    currency   VARCHAR(3)  NOT NULL,
    balance    VARCHAR(50) NOT NULL DEFAULT '0',
    PRIMARY KEY (id),
    KEY fk_account_user (user_id),
    CONSTRAINT fk_account_user FOREIGN KEY (user_id) REFERENCES user (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- Fin del script
-- ============================================================
