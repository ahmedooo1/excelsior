# QuickServe - Plateforme de Services

## Description
QuickServe est une plateforme de mise en relation entre utilisateurs et prestataires de services.

## Architecture Microservices

### Services
- **User Service** (Port 8001) : Gestion des utilisateurs et authentification
- **Order Service** (Port 8002) : Gestion des commandes de services
- **Payment Service** (Port 8003) : Traitement des paiements
- **Notification Service** (Port 8004) : Système de notifications
- **Provider Service** (Port 8005) : Gestion des prestataires
- **Repair Service** (Port 8006) : Service de réparation

### Technologies
- FastAPI
- Python 3.12
- Pydantic pour la validation des données
- PostgreSQL (Base de données utilisée pour les services)


## Installation

1. Installer les dépendances :
```bash
pip install fastapi uvicorn pydantic
```

2. Lancer un service (exemple avec le User Service) :
```bash
cd user_service
uvicorn main:app --host 0.0.0.0 --port 8001
```

## Fonctionnalités

- Inscription/Connexion utilisateurs
- Gestion des commandes
- Système de paiement
- Notifications en temps réel
- Gestion des prestataires
- Service de réparation


## Structure du projet
```
QuickServe_api/
├── user_service/
│   ├── auth_service.py       # Gestion de l'authentification et des tokens JWT
│   ├── main.py               # Points d'entrée de l'API utilisateur
│   ├── models.py             # Modèles de données pour les utilisateurs
│   ├── repositories.py       # Gestion des données utilisateur
│   ├── dto.py                # Objets de transfert de données utilisateur
│   ├── requirements.txt      # Dépendances Python pour le service utilisateur
│   └── Dockerfile            # Configuration Docker pour le service utilisateur
├── notification_service/
│   ├── main.py               # Points d'entrée de l'API de notification
│   ├── models.py             # Modèles de données pour les notifications
│   ├── repositories.py       # Gestion des données de notification
│   ├── dto.py                # Objets de transfert de données pour les notifications
│   ├── requirements.txt      # Dépendances Python pour le service de notification
│   └── Dockerfile            # Configuration Docker pour le service de notification
├── order_service/
│   ├── main.py               # Points d'entrée de l'API de commande
│   ├── models.py             # Modèles de données pour les commandes
│   ├── repositories.py       # Gestion des données de commande
│   ├── dto.py                # Objets de transfert de données pour les commandes
│   ├── requirements.txt      # Dépendances Python pour le service de commande
│   └── Dockerfile            # Configuration Docker pour le service de commande
├── payment_service/
│   ├── main.py               # Points d'entrée de l'API de paiement
│   ├── models.py             # Modèles de données pour les paiements
│   ├── repositories.py       # Gestion des données de paiement
│   ├── dto.py                # Objets de transfert de données pour les paiements
│   ├── requirements.txt      # Dépendances Python pour le service de paiement
│   └── Dockerfile            # Configuration Docker pour le service de paiement
├── provider_service/
│   ├── main.py               # Points d'entrée de l'API des fournisseurs
│   ├── models.py             # Modèles de données pour les fournisseurs
│   ├── repositories.py       # Gestion des données des fournisseurs
│   ├── dto.py                # Objets de transfert de données pour les fournisseurs
│   ├── requirements.txt      # Dépendances Python pour le service des fournisseurs
│   └── Dockerfile            # Configuration Docker pour le service des fournisseurs
├── repair_service/
│   ├── main.py               # Points d'entrée de l'API de réparation
│   ├── models.py             # Modèles de données pour les réparations
│   ├── repositories.py       # Gestion des données de réparation
│   ├── dto.py                # Objets de transfert de données pour les réparations
│   ├── requirements.txt      # Dépendances Python pour le service de réparation
│   └── Dockerfile            # Configuration Docker pour le service de réparation
├── docker-compose.yml        # Orchestration des services avec Docker Compose
└── README.md                 # Documentation principale du projet
```

## Tests

1. **Tester avec Swagger** :
   - Accédez à [http://localhost:8001/docs](http://localhost:8001/docs).
   - Testez les endpoints interactifs.

2. **Tester avec `curl`** :
   Exemple de requête pour créer un utilisateur :
   ```bash
   curl -X 'POST' \
     'http://localhost:8001/api/auth/register' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/x-www-form-urlencoded' \
     -d 'email=email@example.com&name=John&password=yourpassword'
   ```

## Contribution

1. Forkez le dépôt.
2. Créez une branche pour vos modifications :
   ```bash
   git checkout -b feature/your-feature
   ```
3. Soumettez une pull request.

## Licence

Ce projet est sous licence MIT. Consultez le fichier `LICENSE` pour plus d'informations.