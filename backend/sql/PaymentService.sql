
CREATE DATABASE PaymentService;

USE PaymentService;

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    amount DECIMAL(10,2) NOT NULL,
    payment_status ENUM('en attente', 'validé', 'échoué') DEFAULT 'en attente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
