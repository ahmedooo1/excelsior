# QuickServe API

QuickServe API est un service RESTful basé sur FastAPI pour la gestion des utilisateurs et l'authentification avec JWT.

## Fonctionnalités

- **Gestion des utilisateurs** : Créer, lire, mettre à jour et supprimer des utilisateurs.
- **Authentification JWT** : Authentification sécurisée avec des tokens JWT.
- **Endpoints protégés** : Accès restreint aux utilisateurs connectés.
- **Swagger UI** : Documentation interactive disponible à `/docs`.

## Prérequis

- **Python** : Version 3.9 ou supérieure.
- **Docker** : Pour exécuter le projet dans des conteneurs.
- **PostgreSQL** : Base de données utilisée pour les services.

## Installation

1. Clonez le dépôt :
   ```bash
   git clone <repository-url>
   cd QuickServe_api
   ```

2. Installez les dépendances Python :
   ```bash
   pip install -r user_service/requirements.txt
   ```

3. Configurez les variables d'environnement :
   - Créez un fichier `.env` dans le dossier `user_service` avec les variables suivantes :
     ```
     SECRET_KEY=your-secret-key
     DATABASE_URL=postgresql://user:password@localhost:5432/userdb
     ```

4. Lancez les services avec Docker Compose :
   ```bash
   docker-compose up --build
   ```

## Utilisation

### Accéder à l'API

- **Swagger UI** : [http://localhost:8001/docs](http://localhost:8001/docs)
- **Requête d'exemple** :
  ```bash
  curl -X 'POST' \
    'http://localhost:8001/api/auth/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'username=email@example.com&password=yourpassword'
  ```

### Endpoints principaux

#### Authentification

- **POST /api/auth/register** : Inscription d'un utilisateur.
- **POST /api/auth/login** : Connexion et obtention d'un token JWT.

#### Gestion des utilisateurs

- **GET /api/users** : Liste des utilisateurs (protégé).
- **GET /api/users/{user_id}** : Détails d'un utilisateur (protégé).
- **PUT /api/users/{user_id}** : Mise à jour d'un utilisateur (protégé).
- **DELETE /api/users/{user_id}** : Suppression d'un utilisateur (protégé).

#### Endpoint de santé

- **GET /health** : Vérifie si le service est opérationnel.

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


