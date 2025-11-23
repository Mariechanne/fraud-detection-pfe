# Résumé Exécutif - Projet de Fin d'Études
## Système de Détection de Fraudes Bancaires par Machine Learning

---

**Étudiante :** Marie Chandeste Melvina J. H. Medetadji Migan
**Formation :** Licence Professionnelle - Data Science pour la Gestion des Entreprises
**Établissement :** ESLSCA Paris – Campus Rabat
**Encadrant :** M. DOUMI KARIM
**Année académique :** 2024-2025
**Date de soutenance :** 29 novembre 2024

---

## 1. Contexte et Problématique

### Enjeu métier
Les fraudes bancaires représentent un coût mondial de **31,3 milliards de dollars** (source: Nilson Report 2023). La détection manuelle est inefficace face au volume de transactions (millions/jour).

### Défi technique
Le dataset présente un **déséquilibre extrême** :
- **284,807 transactions** dont seulement **492 fraudes (0.17%)**
- Un modèle naïf prédisant "normale" partout aurait 99.83% de précision mais serait **inutile en production**
- **Objectif : Maximiser le Recall** (taux de détection) tout en limitant les fausses alertes

### Solution développée
Application web interactive permettant d'analyser des transactions bancaires en temps réel et d'expliquer les décisions du modèle via SHAP (interprétabilité IA).

---

## 2. Méthodologie Scientifique

### Pipeline ML Complet

```
Dataset Kaggle (284,807 transactions)
         ↓
Split stratifié 70/15/15 (train/valid/test)
         ↓
Prétraitement (StandardScaler sur Amount/Time)
         ↓
SMOTE (Synthetic Minority Oversampling) - 20% de la classe majoritaire
         ↓
Comparaison de 3 modèles (Logistic Regression, Random Forest, XGBoost)
         ↓
Validation croisée 5-fold
         ↓
Optimisation du seuil (max Recall avec Precision ≥ 20%)
         ↓
Évaluation finale sur test set
```

### Technologies utilisées
- **ML/Data Science :** scikit-learn, XGBoost, imbalanced-learn (SMOTE), SHAP
- **Visualisation :** Plotly, Matplotlib, Seaborn
- **Web Framework :** Streamlit 1.38+
- **Data Processing :** pandas, NumPy
- **Testing :** pytest (22 tests unitaires, 88-95% de couverture)

---

## 3. Résultats et Performances

### Performances du modèle final (Random Forest)

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| **ROC-AUC** | **0.973** | ⭐⭐⭐⭐⭐ Excellente capacité de discrimination |
| **PR-AUC** | **0.840** | ⭐⭐⭐⭐⭐ Excellent pour données déséquilibrées |
| **Recall** | **87.8%** | **Détecte 65/74 fraudes** (9 manquées seulement) |
| **Precision** | **21.1%** | 1 alerte sur 5 est une vraie fraude (acceptable) |
| **Seuil optimal** | **0.0733** | Optimisé pour maximiser la détection |

### Matrice de Confusion (Validation Set : 42,721 transactions)

|  | Prédiction : Normale | Prédiction : Fraude |
|--|----------------------|---------------------|
| **Réalité : Normale (42,647)** | 42,404 ✅ | 243 ⚠️ |
| **Réalité : Fraude (74)** | 9 ❌ | 65 ✅ |

**Impact métier :**
- ✅ Seulement **9 fraudes manquées** sur 74 (12.2%) → Risque financier limité
- ✅ **243 fausses alertes** sur 42,647 normales (0.57%) → Charge de vérification acceptable
- ✅ **Économies estimées :** Si montant moyen fraude = 500€, détection de 65 fraudes = **32,500€ protégés**

### Comparaison des modèles testés

| Modèle | PR-AUC | Recall | Precision | Choix |
|--------|--------|--------|-----------|-------|
| Logistic Regression | 0.783 | 88.7% | 22.7% | ❌ PR-AUC inférieur |
| **Random Forest** | **0.865** | **82.9%** | **87.0%** | ✅ **Meilleur compromis** |
| XGBoost | 0.853 | 83.4% | 81.7% | ❌ Moins bon que RF |

---

## 4. Livrables et Fonctionnalités

### Application Web (Streamlit)

**3 modules principaux :**

1. **Analyse de transaction unique**
   - Formulaire interactif (Time, Amount, V1-V28)
   - Prédiction en temps réel avec probabilité
   - Classification par niveau de risque (FAIBLE, MODÉRÉ, ÉLEVÉ, CRITIQUE)
   - Top 5 facteurs influents (SHAP)

2. **Analyse par lot (CSV)**
   - Upload de fichiers CSV jusqu'à 100,000 transactions
   - Traitement par batch de 5,000 lignes
   - Archivage automatique dans `reports/predictions/`
   - Export des résultats

3. **Visualisations avancées**
   - Histogramme des probabilités de fraude
   - Répartition par niveau de risque (camembert)
   - Tableaux interactifs avec highlighting des fraudes

**Configuration avancée :**
- Slider de seuil ajustable (0.00 - 0.50)
- Affichage des métriques du modèle
- Mode debug pour développeurs

### Architecture du Code

```
fraud-detection-pfe/
├── app/streamlit_app.py        (721 lignes) - Interface web
├── src/                        (705 lignes) - Code modulaire
│   ├── data/loader.py          - Chargement des artefacts
│   ├── models/predictor.py     - Prédictions ML
│   ├── models/explainer.py     - Explications SHAP
│   ├── utils/validation.py     - Validation des données
│   └── visualization/plots.py  - Graphiques Plotly
├── tests/                      (340 lignes, 22 tests)
│   ├── test_predictor.py       (8 tests, 95% couverture)
│   ├── test_loader.py          (4 tests, 92% couverture)
│   └── test_validation.py      (10 tests, 88% couverture)
├── notebooks/                  (2 notebooks Jupyter)
│   ├── 01_eda.ipynb            - Analyse exploratoire
│   └── 02_preparation.ipynb    - Modélisation complète
└── docs/                       (Documentation complète)
    ├── USER_GUIDE.md           (276 lignes)
    ├── DEVELOPER_GUIDE.md      (423 lignes)
    └── images/                 (8 screenshots professionnels)
```

### Documentation

- ✅ **README principal** : 464 lignes avec badges, captures d'écran, instructions d'installation
- ✅ **Guide utilisateur** : Installation rapide, utilisation de l'app, FAQ
- ✅ **Guide développeur** : Architecture, tests, déploiement (Docker, Streamlit Cloud)
- ✅ **Notebooks Jupyter** : EDA complet + modélisation documentée (1.3 MB)
- ✅ **8 captures d'écran professionnelles** (720 KB) démontrant toutes les fonctionnalités

---

## 5. Qualité et Bonnes Pratiques

### Tests et Reproductibilité

✅ **Tests unitaires :** 22 tests pytest avec couverture 88-95%
✅ **Installation automatisée :** Script `setup.sh` (10-15 minutes)
✅ **Versions lockées :** `requirements.lock.txt` avec 52 dépendances exactes
✅ **Git propre :** 31 commits bien nommés (feat, fix, docs, refactor)
✅ **Code modulaire :** Séparation des responsabilités (data/models/utils/viz)
✅ **Docstrings :** 100% des fonctions documentées avec type hints

### Sécurité et Production-Ready

✅ **Validation robuste :** Type checking, size limits, sanitization
✅ **Gestion des erreurs :** Fallbacks gracieux, logs détaillés
✅ **Performance :** Traitement par batch pour CSV volumineux
✅ **Déployable sur :** Streamlit Cloud, Docker, serveur local

---

## 6. Conclusion et Perspectives

### Réussites

1. **Performances exceptionnelles** malgré le déséquilibre extrême (0.17% fraudes)
2. **Application fonctionnelle** prête pour démonstration
3. **Code de qualité professionnelle** (tests, doc, architecture)
4. **Interprétabilité** via SHAP pour expliquer les décisions

### Limitations identifiées

- Dataset synthétique (PCA appliquée) → Transfert à données réelles nécessite adaptation
- Seuil fixe → En production, devrait s'adapter dynamiquement au coût métier
- Pas de détection de concept drift → Monitoring du modèle à ajouter

### Améliorations futures

1. **Modèle :** Tester des architectures Deep Learning (AutoEncoders pour anomalies)
2. **Features :** Ajouter des variables comportementales (historique client, géolocalisation)
3. **Déploiement :** API REST + interface mobile + intégration système bancaire
4. **Monitoring :** Alertes en temps réel, dashboard de supervision

---

## 7. Liens et Ressources

- **Code source :** https://github.com/Mariechanne/fraud-detection-pfe
- **Dataset :** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Démonstration vidéo :** [À créer avant soutenance]
- **Présentation PowerPoint :** [En préparation pour le 29/11]

---

## 8. Contact

**Marie Chandeste Melvina J. H. Medetadji Migan**
📧 melvinamedetadji@gmail.com
🔗 GitHub: https://github.com/Mariechanne
🔗 Kaggle: https://www.kaggle.com/melvinamedetadji

**Encadrant :** M. DOUMI KARIM / M. KHALID BENABBESS
**Établissement :** ESLSCA Paris – Campus Rabat

---

<div align="center">

**Ce projet démontre une maîtrise complète du cycle de vie d'un projet Data Science :**
*De l'analyse exploratoire au déploiement d'une application web fonctionnelle*

📊 **Data Science** • 🤖 **Machine Learning** • 💻 **Web Development** • 🧪 **Software Engineering**

</div>
