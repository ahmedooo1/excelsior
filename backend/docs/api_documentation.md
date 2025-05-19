# Documentation de l'API QuickServe

## Introduction

L'API QuickServe est une API RESTful qui permet de gérer les services à la demande pour les utilisateurs. Elle est basée sur une architecture microservices et utilise FastAPI comme framework principal.

Cette documentation décrit les différentes routes disponibles, les formats de données attendus et les réponses renvoyées par l'API.

## Architecture

L'API QuickServe est composée des microservices suivants :

1. **API Gateway** : Point d'entrée unique pour toutes les requêtes
2. **UserService** : Gestion des utilisateurs et authentification
3. **OrderService** : Gestion des commandes
4. **PaymentService** : Gestion des paiements
5. **NotificationService** : Gestion des notifications
6. **ProviderService** : Gestion des prestataires
7. **TransportService** : Gestion des services de transport
8. **MovingService** : Gestion des services de déménagement
9. **CleaningService** : Gestion des services de nettoyage
10. **RepairService** : Gestion des services de dépannage
11. **ChildAssistanceService** : Gestion des services de garde d'enfant

## Base URL

Toutes les requêtes doivent être adressées à l'URL de base suivante :

```
http://api.quickserve.com/api
```

## Authentification

L'API utilise l'authentification JWT (JSON Web Token). Pour accéder aux endpoints protégés, vous devez inclure un token d'accès dans l'en-tête de vos requêtes :

```
Authorization: Bearer <token>
```

Pour obtenir un token, utilisez l'endpoint `/token` avec vos identifiants.

## Endpoints

### Utilisateurs

#### Créer un utilisateur

```
POST /users/
```

**Corps de la requête :**
```json
{
  "email": "utilisateur@example.com",
  "password": "motdepasse123",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone_number": "0123456789"
}
```

**Réponse :**
```json
{
  "id": 1,
  "email": "utilisateur@example.com",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone_number": "0123456789",
  "created_at": "2025-04-05T10:00:00"
}
```

#### Obtenir tous les utilisateurs

```
GET /users/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "email": "utilisateur@example.com",
    "first_name": "Prénom",
    "last_name": "Nom",
    "phone_number": "0123456789",
    "created_at": "2025-04-05T10:00:00"
  }
]
```

#### Obtenir un utilisateur par ID

```
GET /users/{user_id}
```

**Réponse :**
```json
{
  "id": 1,
  "email": "utilisateur@example.com",
  "first_name": "Prénom",
  "last_name": "Nom",
  "phone_number": "0123456789",
  "created_at": "2025-04-05T10:00:00"
}
```

#### Obtenir un token d'authentification

```
POST /token
```

**Corps de la requête :**
```json
{
  "username": "utilisateur@example.com",
  "password": "motdepasse123"
}
```

**Réponse :**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Commandes

#### Créer une commande

```
POST /orders/
```

**Corps de la requête :**
```json
{
  "user_id": 1,
  "service_type": "transport",
  "status": "pending",
  "details": {
    "pickup_location": "123 Rue Principale",
    "dropoff_location": "456 Avenue Secondaire"
  }
}
```

**Réponse :**
```json
{
  "id": 1,
  "user_id": 1,
  "service_type": "transport",
  "status": "pending",
  "details": {
    "pickup_location": "123 Rue Principale",
    "dropoff_location": "456 Avenue Secondaire"
  },
  "created_at": "2025-04-05T10:30:00"
}
```

#### Obtenir toutes les commandes

```
GET /orders/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "service_type": "transport",
    "status": "pending",
    "details": {
      "pickup_location": "123 Rue Principale",
      "dropoff_location": "456 Avenue Secondaire"
    },
    "created_at": "2025-04-05T10:30:00"
  }
]
```

#### Obtenir une commande par ID

```
GET /orders/{order_id}
```

**Réponse :**
```json
{
  "id": 1,
  "user_id": 1,
  "service_type": "transport",
  "status": "pending",
  "details": {
    "pickup_location": "123 Rue Principale",
    "dropoff_location": "456 Avenue Secondaire"
  },
  "created_at": "2025-04-05T10:30:00"
}
```

#### Obtenir les commandes d'un utilisateur

```
GET /users/{user_id}/orders/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "service_type": "transport",
    "status": "pending",
    "details": {
      "pickup_location": "123 Rue Principale",
      "dropoff_location": "456 Avenue Secondaire"
    },
    "created_at": "2025-04-05T10:30:00"
  }
]
```

### Paiements

#### Créer un paiement

```
POST /payments/
```

**Corps de la requête :**
```json
{
  "order_id": 1,
  "amount": 150.50,
  "payment_method": "carte",
  "status": "en attente"
}
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "amount": 150.50,
  "payment_method": "carte",
  "status": "en attente",
  "created_at": "2025-04-05T11:00:00"
}
```

#### Obtenir tous les paiements

```
GET /payments/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "order_id": 1,
    "amount": 150.50,
    "payment_method": "carte",
    "status": "en attente",
    "created_at": "2025-04-05T11:00:00"
  }
]
```

#### Obtenir un paiement par ID

```
GET /payments/{payment_id}
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "amount": 150.50,
  "payment_method": "carte",
  "status": "en attente",
  "created_at": "2025-04-05T11:00:00"
}
```

#### Obtenir le paiement d'une commande

```
GET /orders/{order_id}/payment
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "amount": 150.50,
  "payment_method": "carte",
  "status": "en attente",
  "created_at": "2025-04-05T11:00:00"
}
```

### Notifications

#### Créer une notification

```
POST /notifications/
```

**Corps de la requête :**
```json
{
  "user_id": 1,
  "title": "Nouvelle commande",
  "content": "Votre commande a été confirmée",
  "notification_type": "order_confirmation"
}
```

**Réponse :**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Nouvelle commande",
  "content": "Votre commande a été confirmée",
  "notification_type": "order_confirmation",
  "read": false,
  "created_at": "2025-04-05T11:30:00"
}
```

#### Obtenir toutes les notifications

```
GET /notifications/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Nouvelle commande",
    "content": "Votre commande a été confirmée",
    "notification_type": "order_confirmation",
    "read": false,
    "created_at": "2025-04-05T11:30:00"
  }
]
```

#### Obtenir les notifications d'un utilisateur

```
GET /users/{user_id}/notifications/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "title": "Nouvelle commande",
    "content": "Votre commande a été confirmée",
    "notification_type": "order_confirmation",
    "read": false,
    "created_at": "2025-04-05T11:30:00"
  }
]
```

### Prestataires

#### Créer un prestataire

```
POST /providers/
```

**Corps de la requête :**
```json
{
  "name": "Entreprise Test",
  "email": "contact@entreprise-test.com",
  "phone_number": "0123456789",
  "service_types": ["transport", "moving"],
  "rating": 4.5,
  "is_available": true
}
```

**Réponse :**
```json
{
  "id": 1,
  "name": "Entreprise Test",
  "email": "contact@entreprise-test.com",
  "phone_number": "0123456789",
  "service_types": ["transport", "moving"],
  "rating": 4.5,
  "is_available": true,
  "created_at": "2025-04-05T12:00:00"
}
```

#### Obtenir tous les prestataires

```
GET /providers/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "name": "Entreprise Test",
    "email": "contact@entreprise-test.com",
    "phone_number": "0123456789",
    "service_types": ["transport", "moving"],
    "rating": 4.5,
    "is_available": true,
    "created_at": "2025-04-05T12:00:00"
  }
]
```

#### Obtenir les prestataires disponibles

```
GET /providers/available/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "name": "Entreprise Test",
    "email": "contact@entreprise-test.com",
    "phone_number": "0123456789",
    "service_types": ["transport", "moving"],
    "rating": 4.5,
    "is_available": true,
    "created_at": "2025-04-05T12:00:00"
  }
]
```

### Services de transport

#### Créer un service de transport

```
POST /transports/
```

**Corps de la requête :**
```json
{
  "order_id": 1,
  "vehicle_type": "voiture",
  "driver_name": "Jean Dupont",
  "driver_contact": "0612345678"
}
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "vehicle_type": "voiture",
  "driver_name": "Jean Dupont",
  "driver_contact": "0612345678",
  "status": "en route",
  "created_at": "2025-04-05T12:30:00"
}
```

#### Obtenir tous les services de transport

```
GET /transports/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "order_id": 1,
    "vehicle_type": "voiture",
    "driver_name": "Jean Dupont",
    "driver_contact": "0612345678",
    "status": "en route",
    "created_at": "2025-04-05T12:30:00"
  }
]
```

#### Obtenir le service de transport d'une commande

```
GET /orders/{order_id}/transport
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "vehicle_type": "voiture",
  "driver_name": "Jean Dupont",
  "driver_contact": "0612345678",
  "status": "en route",
  "created_at": "2025-04-05T12:30:00"
}
```

### Services de déménagement

#### Créer un service de déménagement

```
POST /movings/
```

**Corps de la requête :**
```json
{
  "order_id": 1,
  "team_size": 3,
  "truck_size": "grand"
}
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "team_size": 3,
  "truck_size": "grand",
  "status": "préparation",
  "created_at": "2025-04-05T13:00:00"
}
```

#### Obtenir tous les services de déménagement

```
GET /movings/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "order_id": 1,
    "team_size": 3,
    "truck_size": "grand",
    "status": "préparation",
    "created_at": "2025-04-05T13:00:00"
  }
]
```

#### Obtenir le service de déménagement d'une commande

```
GET /orders/{order_id}/moving
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "team_size": 3,
  "truck_size": "grand",
  "status": "préparation",
  "created_at": "2025-04-05T13:00:00"
}
```

### Services de nettoyage

#### Créer un service de nettoyage

```
POST /cleanings/
```

**Corps de la requête :**
```json
{
  "order_id": 1,
  "location_type": "maison",
  "cleaning_duration": 3
}
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "location_type": "maison",
  "cleaning_duration": 3,
  "status": "préparation",
  "created_at": "2025-04-05T13:30:00"
}
```

#### Obtenir tous les services de nettoyage

```
GET /cleanings/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "order_id": 1,
    "location_type": "maison",
    "cleaning_duration": 3,
    "status": "préparation",
    "created_at": "2025-04-05T13:30:00"
  }
]
```

#### Obtenir le service de nettoyage d'une commande

```
GET /orders/{order_id}/cleaning
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "location_type": "maison",
  "cleaning_duration": 3,
  "status": "préparation",
  "created_at": "2025-04-05T13:30:00"
}
```

### Services de dépannage

#### Créer un service de dépannage

```
POST /repairs/
```

**Corps de la requête :**
```json
{
  "order_id": 1,
  "issue_type": "batterie",
  "technician_name": "Michel Martin"
}
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "issue_type": "batterie",
  "technician_name": "Michel Martin",
  "status": "en route",
  "created_at": "2025-04-05T14:00:00"
}
```

#### Obtenir tous les services de dépannage

```
GET /repairs/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "order_id": 1,
    "issue_type": "batterie",
    "technician_name": "Michel Martin",
    "status": "en route",
    "created_at": "2025-04-05T14:00:00"
  }
]
```

#### Obtenir le service de dépannage d'une commande

```
GET /orders/{order_id}/repair
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "issue_type": "batterie",
  "technician_name": "Michel Martin",
  "status": "en route",
  "created_at": "2025-04-05T14:00:00"
}
```

### Services de garde d'enfant

#### Créer un service de garde d'enfant

```
POST /child-assistances/
```

**Corps de la requête :**
```json
{
  "order_id": 1,
  "guardian_name": "Sophie Dubois",
  "child_count": 2,
  "destination": "École primaire"
}
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "guardian_name": "Sophie Dubois",
  "child_count": 2,
  "destination": "École primaire",
  "status": "en cours",
  "created_at": "2025-04-05T14:30:00"
}
```

#### Obtenir tous les services de garde d'enfant

```
GET /child-assistances/
```

**Réponse :**
```json
[
  {
    "id": 1,
    "order_id": 1,
    "guardian_name": "Sophie Dubois",
    "child_count": 2,
    "destination": "École primaire",
    "status": "en cours",
    "created_at": "2025-04-05T14:30:00"
  }
]
```

#### Obtenir le service de garde d'enfant d'une commande

```
GET /orders/{order_id}/child-assistance
```

**Réponse :**
```json
{
  "id": 1,
  "order_id": 1,
  "guardian_name": "Sophie Dubois",
  "child_count": 2,
  "destination": "École primaire",
  "status": "en cours",
  "created_at": "2025-04-05T14:30:00"
}
```

## Codes d'erreur

L'API utilise les codes d'erreur HTTP standard :

- `200 OK` : La requête a réussi
- `201 Created` : La ressource a été créée avec succès
- `400 Bad Request` : La requête est invalide
- `401 Unauthorized` : L'authentification est requise
- `403 Forbidden` : L'accès est interdit
- `404 Not Found` : La ressource n'a pas été trouvée
- `500 Internal Server Error` : Une erreur interne est survenue

## Limites de taux

L'API impose des limites de taux pour éviter les abus. Les limites actuelles sont :

- 100 requêtes par minute par adresse IP
- 1000 requêtes par heure par utilisateur authentifié

## Versions

Cette documentation concerne la version 1.0.0 de l'API QuickServe.
