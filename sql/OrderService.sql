
CREATE DATABASE OrderService;

USE OrderService;

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Reference managed via API
    service_type ENUM('transport', 'nettoyage', 'dépannage', 'garde enfant', 'déménagement') NOT NULL,
    status ENUM('en cours', 'terminé', 'annulé') DEFAULT 'en cours',
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
