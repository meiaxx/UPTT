CREATE DATABASE uptt;

USE uptt;

CREATE TABLE users (`id` INT(10) NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(255) NOT NULL , `apellido` VARCHAR(255) NOT NULL , `edad` INT(2) NOT NULL,fecha DATE,correo VARCHAR(255),direccion VARCHAR(255),numero VARCHAR(255),usuario VARCHAR(255),contraseña VARCHAR(255),tipocargo VARCHAR(255), imagen VARCHAR(2500),hora_entrada VARCHAR(255),hora_salida VARCHAR(255), PRIMARY KEY (`id`));

ALTER TABLE users ADD token VARCHAR(255) AFTER hora_salida;

CREATE TABLE tasks (`id` INT(10) NOT NULL AUTO_INCREMENT , `email` VARCHAR(255) NOT NULL , `title` VARCHAR(255) NOT NULL , `description` VARCHAR(255) NOT NULL,date_task VARCHAR(255), PRIMARY KEY (`id`));

CREATE TABLE users_attendance (
    user_id INT(10) NOT NULL,
    date DATE NOT NULL,
    status ENUM('presente', 'ausente'),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;
