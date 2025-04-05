****Architecture Choisie et Justification****
=============================================

****

****

![](Pictures/10000001000019C600001491F23B1028.png){width="17cm"
height="13.564cm"}****

****

****

****

****

****

L\'architecture retenue pour le projet ****QuickServe**** repose sur une
structure ****microservices**** déployée sur le cloud ****Azure****.
Cette approche garantit une scalabilité, une modularité, et une
maintenance simplifiée.

****Justification des choix architecturaux****
----------------------------------------------

Les choix ont été guidés par les critères suivants :

-   ****Scalabilité et résilience**** : Les services doivent être
    capables de supporter un grand volume d\'utilisateurs simultanés.
-   ****Sécurité des données**** : Protéger les transactions et les
    informations sensibles des utilisateurs.
-   ****Flexibilité**** : Faciliter les mises à jour et l\'ajout de
    nouvelles fonctionnalités.
-   ****Compatibilité**** avec l'écosystème Azure.

  --------------------------- ---------------------------------------------------------------------------------------
  Critère                     Explication
  Scalabilité et résilience   Supporter un grand volume d\'utilisateurs simultanés avec un scaling dynamique.
  Sécurité des données        Protéger les transactions financières et les informations sensibles des utilisateurs.
  Flexibilité                 Faciliter les mises à jour et ajouter de nouvelles fonctionnalités rapidement.
  Compatibilité Azure         Exploiter l'écosystème d'Azure pour une intégration fluide et un coût optimisé.
  --------------------------- ---------------------------------------------------------------------------------------

#### 

****Composants clés de l'architecture****
-----------------------------------------

****

1.  ****API Gateway : Azure API Management****

    -   ****Rôle**** : Centralise et sécurise les requêtes vers les
        microservices.
    -   ****Pourquoi ?**** : Azure API Management offre des
        fonctionnalités avancées comme la gestion des clés API, le
        throttling, et la sécurité via OAuth2.

1.  ****Microservices : FastAPI****

2.  ****Rôle**** : Chaque microservice (OrderService, PaymentService,
    etc.) est isolé et gère une fonctionnalité spécifique.

3.  ****Pourquoi ?**** : FastAPI a été choisi pour sa rapidité, sa
    légèreté et sa capacité à gérer un grand nombre de requêtes avec une
    faible latence.

    -   ****Justification du changement de technologie**** :
        Initialement, Symfony était choisi pour sa robustesse et son
        adaptabilité aux architectures RESTful. Cependant, après
        évaluation, FastAPI a été retenu pour ses performances
        supérieures en termes de temps de réponse et sa gestion efficace
        des requêtes HTTP asynchrones. De plus, FastAPI est écrit en
        Python, ce qui facilite l\'intégration avec d\'autres services
        Python et les outils de data science ou d\'analyse que nous
        pourrions ajouter à l\'avenir.

    ****

1.  ****Bus d'événements : Azure Event Grid****

    -   ****Rôle**** : Gère la communication asynchrone entre
        microservices.
    -   ****Pourquoi ?**** : Il garantit une faible latence et une
        livraison fiable des messages.

1.  ****Bases de données : PostgreSQL et Redis****

    -   ****Rôle**** :

        -   PostgreSQL pour les données transactionnelles (Commandes,
            Paiements).
        -   Redis pour le cache des notifications et des sessions.

    -   ****Pourquoi ?**** : PostgreSQL est performant pour les requêtes
        complexes et Redis optimise les performances.

1.  ****Orchestrateur : Azure Kubernetes Service (AKS)****

    -   ****Rôle**** : Gère le déploiement et le scaling automatique des
        conteneurs Docker.
    -   ****Pourquoi ?**** : AKS s'intègre parfaitement avec Azure et
        garantit une haute disponibilité.

1.  ****CI/CD : GitHub Actions****

    -   ****Rôle**** : Automatise les tests, les déploiements, et les
        mises à jour des services.
    -   ****Pourquoi ?**** : GitHub Actions est simple à configurer et
        intégré à notre flux de travail.

  ------------------ ---------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------
  Composant          Rôle                                                                   Pourquoi ce choix ?
  API Gateway        Centralise et sécurise les requêtes vers les microservices.            Azure API Management offre des fonctionnalités avancées comme la gestion des clés API, le throttling, et OAuth2.
  Microservices      Chaque service gère une fonctionnalité spécifique (ex. : commandes).   FastAPI est extrêmement rapide, léger, et idéal pour des architectures RESTful performantes
  Bus d'événements   Gère la communication asynchrone entre services.                       Azure Event Grid garantit une faible latence et une livraison fiable des messages.
  Bases de données   PostgreSQL pour les données critiques et Redis pour le cache.          PostgreSQL est performant pour les requêtes complexes, Redis optimise les performances des services fréquents.
  Orchestrateur      Gestion des conteneurs et scaling automatique.                         Azure Kubernetes Service (AKS) permet un déploiement fluide avec haute disponibilité.
  CI/CD              Automatise les tests et les déploiements des services.                 GitHub Actions est simple, rapide à configurer et parfaitement intégré avec notre workflow.
  ------------------ ---------------------------------------------------------------------- ------------------------------------------------------------------------------------------------------------------

#### 

### ****Changements depuis le livrable 1****

****

-   ****Adoption de FastAPI pour les microservices**** afin d\'améliorer
    la réactivité de l\'API et de supporter une charge plus élevée avec
    une latence minimale. FastAPI permet une gestion optimale des
    requêtes HTTP avec des performances élevées et une gestion facile
    des fonctionnalités asynchrones.

-   ****Adoption de Redis pour le cache**** afin de réduire la latence
    des services fréquemment sollicités (Notifications, Tracking en
    temps réel).

-   ****Précision sur l'utilisation d'Azure Event Grid**** pour les
    communications interservices.

-   ****Ajout d'un service de monitoring via Azure Monitor**** pour
    surveiller les performances et détecter les anomalies.

****

****

****

****Compromis et impacts****
----------------------------

-   ****Coût élevé**** : L'utilisation d'Azure et de composants avancés
    (AKS, Event Grid) peut augmenter les coûts opérationnels.

    -   ****Atténuation**** : Optimisation des ressources avec des
        mécanismes de scaling automatique.

-   ****Complexité technique**** : L\'architecture microservices et les
    outils comme Kubernetes nécessitent une expertise technique.

    -   ****Atténuation**** : Formation initiale de l'équipe et
        utilisation de services managés pour simplifier la gestion.

-   ****Latence entre microservices**** : La communication via Event
    Grid peut ajouter une légère latence.

    -   ****Atténuation**** : Optimisation des messages pour réduire les
        délais.

****

****

  ------------------------ ----------------------------------------- ------------------------------------------------------------------------------------------------------------
  Compromis                Impact                                    Atténuation
  Coût élevé               Augmentation des coûts opérationnels.     Optimisation des ressources via le scaling automatique sur AKS.
  Complexité technique     Courbe d\'apprentissage pour l\'équipe.   Formation initiale sur Kubernetes et Azure, utilisation de services managés.
  Latence entre services   Légère latence due à Event Grid.          Optimisation des messages pour réduire les délais, choix de l'asynchrone uniquement pour certains services
  ------------------------ ----------------------------------------- ------------------------------------------------------------------------------------------------------------
