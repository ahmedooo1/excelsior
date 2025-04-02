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
│   ├── main.py               # Points d'entrée de l'API
│   ├── models.py             # Modèles de données
│   ├── repositories.py       # Gestion des données en mémoire
│   ├── dto.py                # Objets de transfert de données
│   ├── requirements.txt      # Dépendances Python
│   └── Dockerfile            # Configuration Docker pour le service utilisateur
├── docker-compose.yml        # Orchestration des services avec Docker Compose
└── README.md                 # Documentation du projet
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


