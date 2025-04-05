# Configuration Docker pour le projet QuickServe

Ce document décrit la configuration Docker mise en place pour le projet QuickServe, qui utilise une architecture microservices avec FastAPI et PostgreSQL.

## Structure du projet

```
quickserve_api/
├── docker-compose.yml           # Configuration Docker Compose
├── api_gateway/                 # Passerelle API
│   ├── Dockerfile               # Configuration Docker pour la passerelle
│   ├── requirements.txt         # Dépendances Python
│   └── app/                     # Code source de la passerelle
│       ├── main.py              # Point d'entrée de l'application
│       └── api/                 # Routes API
│           └── endpoints/       # Endpoints spécifiques
├── services/                    # Dossier contenant tous les microservices
│   ├── user_service/            # Service de gestion des utilisateurs
│   │   ├── Dockerfile           # Configuration Docker pour le service
│   │   ├── requirements.txt     # Dépendances Python
│   │   └── app/                 # Code source du service
│   │       ├── main.py          # Point d'entrée de l'application
│   │       ├── models.py        # Modèles de données (SQLAlchemy)
│   │       ├── database.py      # Configuration de la base de données
│   │       └── api/             # Routes API
│   │           └── endpoints/   # Endpoints spécifiques
│   ├── order_service/           # Service de gestion des commandes
│   │   └── ...                  # Structure similaire aux autres services
│   └── ...                      # Autres services
```

## Composants Docker

### Docker Compose

Le fichier `docker-compose.yml` définit tous les services nécessaires pour le projet QuickServe :

- **API Gateway** : Point d'entrée unique pour les clients
- **Microservices** : 10 services distincts (UserService, OrderService, etc.)
- **Bases de données PostgreSQL** : Une base de données dédiée pour chaque microservice
- **Redis** : Pour le cache et les opérations nécessitant une faible latence

### Dockerfiles

Chaque service possède son propre Dockerfile qui définit l'environnement d'exécution :

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${SERVICE_PORT}", "--reload"]
```

### Volumes

Des volumes Docker sont utilisés pour :

- Persister les données des bases de données PostgreSQL
- Persister les données Redis
- Monter les répertoires de code source pour le développement

### Réseaux

Docker Compose crée automatiquement un réseau pour permettre la communication entre les services.

## Utilisation

### Démarrage des services

```bash
docker-compose up -d
```

### Arrêt des services

```bash
docker-compose down
```

### Reconstruction des images

```bash
docker-compose build
```

### Accès aux logs

```bash
docker-compose logs -f [service]
```

## Environnement de développement

En mode développement, les répertoires de code source sont montés dans les conteneurs, ce qui permet de modifier le code sans avoir à reconstruire les images.

## Environnement de production

Pour la production, il est recommandé de :

1. Désactiver le mode `--reload` d'Uvicorn
2. Utiliser des secrets pour les mots de passe et les clés d'API
3. Configurer des limites de ressources pour chaque conteneur
4. Mettre en place un système de monitoring
