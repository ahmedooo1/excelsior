# Modèles de données PostgreSQL pour QuickServe

Ce document décrit les modèles de données implémentés pour chaque microservice du projet QuickServe, adaptés pour PostgreSQL.

## Adaptation pour PostgreSQL

Les scripts SQL originaux utilisaient la syntaxe MySQL/MariaDB. Pour PostgreSQL, les adaptations suivantes ont été effectuées :

1. Remplacement de `AUTO_INCREMENT` par des colonnes de type `SERIAL`
2. Remplacement des types `ENUM` par des colonnes `String` avec validation au niveau de l'application
3. Utilisation de `Float` pour les coordonnées géographiques au lieu de `DECIMAL`
4. Configuration des connexions à la base de données via SQLAlchemy

## Modèles par service

### 1. UserService

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'client' ou 'prestataire'
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 2. OrderService

```python
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    service_type = Column(String, nullable=False)  # 'transport', 'nettoyage', 'dépannage', 'garde enfant', 'déménagement'
    status = Column(String, default='en cours')  # 'en cours', 'terminé', 'annulé'
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 3. PaymentService

```python
class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_status = Column(String, default='en attente')  # 'en attente', 'validé', 'échoué'
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 4. NotificationService

```python
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 5. ProviderService

```python
class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    availability = Column(Boolean, default=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 6. TransportService

```python
class Transport(Base):
    __tablename__ = "transports"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    vehicle_type = Column(String, nullable=False)  # 'voiture', 'camion', 'moto'
    driver_name = Column(String, nullable=False)
    driver_contact = Column(String)
    status = Column(String, default='en route')  # 'en route', 'livré', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 7. MovingService

```python
class Moving(Base):
    __tablename__ = "movings"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    team_size = Column(Integer, nullable=False)
    truck_size = Column(String, nullable=False)  # 'petit', 'moyen', 'grand'
    status = Column(String, default='préparation')  # 'préparation', 'en cours', 'terminé', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 8. CleaningService

```python
class Cleaning(Base):
    __tablename__ = "cleanings"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    location_type = Column(String, nullable=False)  # 'maison', 'bureau', 'véhicule'
    cleaning_duration = Column(Integer, nullable=False)
    status = Column(String, default='préparation')  # 'préparation', 'en cours', 'terminé', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 9. RepairService

```python
class Repair(Base):
    __tablename__ = "repairs"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    issue_type = Column(String, nullable=False)  # 'batterie', 'pneu', 'moteur', 'autre'
    technician_name = Column(String)
    status = Column(String, default='en route')  # 'en route', 'en cours', 'terminé', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 10. ChildAssistanceService

```python
class ChildAssistance(Base):
    __tablename__ = "child_assistances"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    guardian_name = Column(String, nullable=False)
    child_count = Column(Integer, nullable=False)
    destination = Column(String, nullable=False)
    status = Column(String, default='en cours')  # 'en cours', 'terminé', 'annulé'
    created_at = Column(DateTime, default=datetime.utcnow)
```

## Configuration de la base de données

Chaque service utilise SQLAlchemy pour se connecter à sa propre base de données PostgreSQL :

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@service_db:5432/service_name")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Validation des données

La validation des données sera effectuée à l'aide de Pydantic pour s'assurer que les valeurs des champs respectent les contraintes définies, notamment pour les champs qui étaient de type ENUM dans les scripts SQL originaux.

## Migrations

Pour gérer l'évolution des schémas de base de données, Alembic sera utilisé pour créer et appliquer les migrations.
