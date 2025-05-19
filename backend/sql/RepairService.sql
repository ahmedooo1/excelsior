
CREATE DATABASE RepairService;

USE RepairService;

CREATE TABLE repairs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    issue_type ENUM('batterie', 'pneu', 'moteur', 'autre') NOT NULL,
    technician_name VARCHAR(100),
    status ENUM('en route', 'en cours', 'terminé', 'annulé') DEFAULT 'en route',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
