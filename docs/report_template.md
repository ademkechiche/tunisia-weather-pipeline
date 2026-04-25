# Rapport Technique — Tunisia Weather Pipeline

## 1. Contexte et objectif
L'objectif de ce projet est de concevoir un pipeline Data Engineering end-to-end permettant de collecter, transformer, stocker et restituer des données météorologiques concernant plusieurs villes tunisiennes.

## 2. Sources de données
- Source 1 : API Open-Meteo pour la météo actuelle et les prévisions
- Source 2 : fichier CSV local contenant les métadonnées des villes (nom, région, latitude, longitude)

## 3. Architecture choisie
L'architecture retenue est simple et adaptée à un déploiement local :
- stockage brut en fichiers JSON
- stockage analytique en SQLite
- transformations avec Pandas
- orchestration avec APScheduler
- visualisation avec Streamlit

## 4. Transformations principales
1. Normalisation des timestamps
2. Calcul de la température moyenne journalière
3. Classification du niveau de confort thermique
4. Génération d'un niveau d'alerte météo
5. Enrichissement avec la région administrative

## 5. Orchestration
Deux types d'exécution sont utilisés :
- exécution planifiée de type batch
- exécution fréquente simulant un flux quasi temps réel

## 6. Qualité et robustesse
- logs structurés au format JSON
- retry sur la récupération API
- 5 tests unitaires
- Docker pour la reproductibilité

## 7. Difficultés rencontrées
- gestion des appels API et des erreurs réseau
- choix d'une architecture simple mais cohérente avec les contraintes de temps
- conception d'un tableau de bord clair et exploitable

## 8. Limites
- streaming simulé et non basé sur Kafka
- déploiement local au lieu d'une infrastructure cloud
- historique limité aux exécutions du pipeline

## 9. Perspectives d'amélioration
- ajout de Kafka pour un vrai streaming
- déploiement cloud public
- historisation avancée des snapshots
- alertes automatiques par email ou webhook
