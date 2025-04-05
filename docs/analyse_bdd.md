# Analyse des schémas de base de données QuickServe

## Vue d'ensemble
Le projet QuickServe utilise une architecture microservices avec 10 services distincts, chacun ayant sa propre base de données. Les bases de données sont conçues pour être indépendantes, avec des références gérées au niveau de l'API plutôt que par des contraintes de clé étrangère directes.

## Choix technologiques
- **PostgreSQL** pour les données relationnelles
- **Redis** pour le cache et les opérations nécessitant une faible latence

## Structure des bases de données par service

### 1. UserService
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('client', 'prestataire') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les utilisateurs (clients et prestataires)
- Stocke les informations d'authentification

### 2. OrderService
```sql
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Reference managed via API
    service_type ENUM('transport', 'nettoyage', 'dépannage', 'garde enfant', 'déménagement') NOT NULL,
    status ENUM('en cours', 'terminé', 'annulé') DEFAULT 'en cours',
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les commandes passées par les utilisateurs
- Référence l'utilisateur qui a passé la commande
- Stocke les coordonnées géographiques du lieu de service

### 3. PaymentService
```sql
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    amount DECIMAL(10,2) NOT NULL,
    payment_status ENUM('en attente', 'validé', 'échoué') DEFAULT 'en attente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les transactions financières liées aux commandes
- Référence la commande associée au paiement

### 4. NotificationService
```sql
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Reference managed via API
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les notifications envoyées aux utilisateurs
- Référence l'utilisateur concerné par la notification

### 5. ProviderService
```sql
CREATE TABLE providers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les informations des prestataires de services
- Stocke la disponibilité et la position géographique des prestataires

### 6. TransportService
```sql
CREATE TABLE transports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    vehicle_type ENUM('voiture', 'camion', 'moto') NOT NULL,
    driver_name VARCHAR(100) NOT NULL,
    driver_contact VARCHAR(15),
    status ENUM('en route', 'livré', 'annulé') DEFAULT 'en route',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les services de transport
- Référence la commande associée au transport

### 7. MovingService
```sql
CREATE TABLE movings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    team_size INT NOT NULL,
    truck_size ENUM('petit', 'moyen', 'grand') NOT NULL,
    status ENUM('préparation', 'en cours', 'terminé', 'annulé') DEFAULT 'préparation',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les services de déménagement
- Référence la commande associée au déménagement

### 8. CleaningService
```sql
CREATE TABLE cleanings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    location_type ENUM('maison', 'bureau', 'véhicule') NOT NULL,
    cleaning_duration INT NOT NULL,
    status ENUM('préparation', 'en cours', 'terminé', 'annulé') DEFAULT 'préparation',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les services de nettoyage
- Référence la commande associée au nettoyage

### 9. RepairService
```sql
CREATE TABLE repairs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    issue_type ENUM('batterie', 'pneu', 'moteur', 'autre') NOT NULL,
    technician_name VARCHAR(100),
    status ENUM('en route', 'en cours', 'terminé', 'annulé') DEFAULT 'en route',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les services de réparation
- Référence la commande associée à la réparation

### 10. ChildAssistanceService
```sql
CREATE TABLE child_assistances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL, -- Reference managed via API
    guardian_name VARCHAR(100) NOT NULL,
    child_count INT NOT NULL,
    destination VARCHAR(255) NOT NULL,
    status ENUM('en cours', 'terminé', 'annulé') DEFAULT 'en cours',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
- Gère les services d'assistance pour enfants
- Référence la commande associée à l'assistance

## Relations entre les tables

Les relations entre les tables sont gérées au niveau de l'API plutôt que par des contraintes de clé étrangère directes. Voici les principales relations :

1. **users** (UserService) → **orders** (OrderService) : Un utilisateur peut passer plusieurs commandes
2. **orders** (OrderService) → **payments** (PaymentService) : Une commande peut avoir un paiement associé
3. **orders** (OrderService) → **transports/movings/cleanings/repairs/child_assistances** : Une commande est associée à un service spécifique selon son type
4. **users** (UserService) → **notifications** (NotificationService) : Un utilisateur peut recevoir plusieurs notifications

## Adaptation pour PostgreSQL

Les scripts SQL fournis utilisent la syntaxe MySQL/MariaDB (AUTO_INCREMENT, ENUM). Pour PostgreSQL, il faudra adapter :

1. Remplacer `AUTO_INCREMENT` par `SERIAL`
2. Remplacer les `ENUM` par des types personnalisés ou des contraintes CHECK
3. Adapter les commandes `CREATE DATABASE` et `USE` pour PostgreSQL

## Considérations pour l'implémentation

1. **Gestion des références** : Implémenter la logique de vérification des références au niveau de l'API
2. **Transactions distribuées** : Gérer les transactions qui impliquent plusieurs services
3. **Cohérence des données** : Mettre en place des mécanismes pour assurer la cohérence entre les différentes bases de données
4. **Migrations** : Prévoir un système de migrations pour gérer l'évolution des schémas
