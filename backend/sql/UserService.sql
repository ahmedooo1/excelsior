
CREATE DATABASE UserService;

USE UserService;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('client', 'prestataire') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
