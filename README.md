# QuickServe API

API de services à la demande basée sur une architecture microservices avec FastAPI et PostgreSQL.

## Description
QuickServe est une plateforme de mise en relation entre utilisateurs et prestataires de services.

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

## Technologies utilisées

- **FastAPI** : Framework API Python rapide et moderne
- **PostgreSQL** : Base de données relationnelle
- **Docker** : Conteneurisation des services
- **Redis** : Cache pour améliorer les performances
- **Pydantic** : Validation des données

## Prérequis

- Docker et Docker Compose
- Python 3.10+
- Git

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/ahmedooo1/quickserve_api.git
cd quickserve_api
```

2. Lancer les services avec Docker Compose :
```bash
docker-compose up -d
```

3. Vérifier que tous les services sont en cours d'exécution :
```bash
docker-compose ps
```

## Utilisation

L'API est accessible à l'adresse suivante : http://localhost:8080/docs/

Pour vérifier l'état de santé de tous les services :
```
GET /health
```

Consultez la documentation complète de l'API dans le fichier [docs/api_documentation.md](docs/api_documentation.md).

## Structure du projet

```
quickserve_api/
├── api_gateway/               # Passerelle API
├── services/                  # Microservices
│   ├── user_service/          # Service utilisateur
│   ├── order_service/         # Service commande
│   ├── payment_service/       # Service paiement
│   ├── notification_service/  # Service notification
│   ├── provider_service/      # Service prestataire
│   ├── transport_service/     # Service transport
│   ├── moving_service/        # Service déménagement
│   ├── cleaning_service/      # Service nettoyage
│   ├── repair_service/        # Service dépannage
│   └── child_assistance_service/ # Service garde d'enfant
├── docs/                      # Documentation
├── docker-compose.yml         # Configuration Docker Compose
└── README.md                  # Ce fichier
```

## Tests

Chaque microservice dispose de ses propres tests unitaires. Pour exécuter les tests :

```bash
# Pour l'API Gateway
cd api_gateway
pytest

# Pour un service spécifique (exemple avec le service utilisateur)
cd services/user_service
pytest
```

Vous pouvez également tester l'API avec Swagger :
- Accédez à [http://localhost:8080/docs](http://localhost:8080/docs).
- Testez les endpoints interactifs.

## Contribution

1. Forkez le dépôt.
2. Créez une branche pour vos modifications :
   ```bash
   git checkout -b feature/your-feature
   ```
3. Soumettez une pull request.

## Licence

Ce projet est sous licence MIT.
