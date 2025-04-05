
CREATE DATABASE TransportService;

USE TransportService;

CREATE TABLE transports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    vehicle_type ENUM('voiture', 'camion', 'moto') NOT NULL,
    driver_name VARCHAR(100) NOT NULL,
    driver_contact VARCHAR(15),
    status ENUM('en route', 'livré', 'annulé') DEFAULT 'en route',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
