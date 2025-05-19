
CREATE DATABASE MovingService;

USE MovingService;

CREATE TABLE movings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    team_size INT NOT NULL,
    truck_size ENUM('petit', 'moyen', 'grand') NOT NULL,
    status ENUM('préparation', 'en cours', 'terminé', 'annulé') DEFAULT 'préparation',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
