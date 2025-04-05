# Configuration de la connexion PostgreSQL pour QuickServe

Ce document décrit la configuration de la connexion à PostgreSQL pour les microservices du projet QuickServe.

## Structure des fichiers de configuration

Pour chaque microservice, nous allons créer un fichier `.env` qui contiendra les variables d'environnement nécessaires à la connexion à la base de données PostgreSQL. Ces fichiers seront utilisés par Docker Compose pour injecter les variables d'environnement dans les conteneurs.

## Variables d'environnement

Les variables d'environnement suivantes seront définies pour chaque service :

- `DATABASE_URL`: URL de connexion à la base de données PostgreSQL
- `POSTGRES_USER`: Nom d'utilisateur PostgreSQL
- `POSTGRES_PASSWORD`: Mot de passe PostgreSQL
- `POSTGRES_DB`: Nom de la base de données PostgreSQL
- `POSTGRES_HOST`: Hôte PostgreSQL (nom du service dans Docker Compose)
- `POSTGRES_PORT`: Port PostgreSQL (par défaut 5432)

## Exemple de fichier .env

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=user_service
POSTGRES_HOST=user_db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@user_db:5432/user_service
```

## Mise à jour du docker-compose.yml

Le fichier docker-compose.yml sera mis à jour pour inclure les services PostgreSQL pour chaque microservice et pour charger les variables d'environnement à partir des fichiers .env.

## Initialisation des bases de données

Des scripts d'initialisation seront créés pour chaque base de données PostgreSQL afin de créer les tables nécessaires au démarrage des conteneurs.
