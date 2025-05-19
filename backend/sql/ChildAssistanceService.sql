
CREATE DATABASE ChildAssistanceService;

USE ChildAssistanceService;

CREATE TABLE child_assistances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    guardian_name VARCHAR(100) NOT NULL,
    child_count INT NOT NULL,
    destination VARCHAR(255) NOT NULL,
    status ENUM('en cours', 'terminé', 'annulé') DEFAULT 'en cours',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
