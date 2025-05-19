
CREATE DATABASE CleaningService;

USE CleaningService;

CREATE TABLE cleanings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    location_type ENUM('maison', 'bureau', 'véhicule') NOT NULL,
    cleaning_duration INT NOT NULL,
    status ENUM('préparation', 'en cours', 'terminé', 'annulé') DEFAULT 'préparation',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
