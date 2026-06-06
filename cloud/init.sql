CREATE DATABASE IF NOT EXISTS sistema_monitoreo;
USE sistema_monitoreo;

-- Tabla para almacenar datos de sensores
CREATE TABLE IF NOT EXISTS sensores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50),
    valor FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Usuario seguro para conexiones externas (No root)
DROP USER IF EXISTS 'operador_cloud'@'%';
CREATE USER 'operador_cloud'@'%' IDENTIFIED BY 'proyecto123so';
GRANT ALL PRIVILEGES ON sistema_monitoreo.* TO 'operador_cloud'@'%';
FLUSH PRIVILEGES;

-- Insertar datos de pruebas
INSERT INTO sensores (tipo, valor) VALUES ('CPU_Temp', 42.5), ('RAM_Usage', 75.0);