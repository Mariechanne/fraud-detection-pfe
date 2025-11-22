# Système de Détection de Fraudes Bancaires

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-22%20passing-success.svg)](tests/)

> **Projet de Fin d'Études** — Détection automatique de transactions bancaires frauduleuses par Machine Learning

---

## 📋 Contexte et Objectifs

Ce projet implémente un système de détection de fraudes bancaires utilisant des techniques de Machine Learning avancées. Face au déséquilibre extrême des données (0.17% de fraudes), l'objectif principal est de **maximiser le taux de détection (Recall)** tout en maintenant un nombre acceptable de fausses alertes.

**Problématique :** Sur 284,807 transactions, seulement 492 sont frauduleuses. Un modèle naïf prédisant "normale" partout aurait 99.83% de précision mais serait inutile en production.

**Solution développée :**
- Application web Streamlit pour analyse en temps réel
- Pipeline ML avec gestion du déséquilibre (SMOTE)
- Modèle Random Forest optimisé
- Explications SHAP pour l'interprétabilité
- Architecture modulaire testée et documentée

---

## 📊 Données

**Source :** [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

| Caractéristique | Valeur |
|-----------------|--------|
| **Nombre de transactions** | 284,807 |
| **Fraudes** | 492 (0.17%) |
| **Transactions normales** | 284,315 (99.83%) |
| **Période couverte** | 2 jours |
| **Variables** | 30 features (Time, V1-V28 PCA, Amount) |
| **Cible** | Class (0 = normale, 1 = fraude) |

**Prétraitement :**
- Split stratifié 70/15/15 (train/valid/test)
- Normalisation de Amount et Time (StandardScaler)
- SMOTE (sampling_strategy=0.2) pour rééquilibrer les classes

---

## 🔬 Méthodologie

### Pipeline ML Complet

```
Données brutes (creditcard.csv)
    ↓
Split stratifié 70/15/15
    ↓
Prétraitement (StandardScaler sur Amount/Time)
    ↓
SMOTE (20% de la classe majoritaire)
    ↓
Random Forest (300 arbres, n_jobs=-1)
    ↓
Validation croisée 5-fold
    ↓
Optimisation du seuil (max Recall avec Precision ≥ 20%)
    ↓
Évaluation sur test set
```

### Comparaison de Modèles

| Modèle | PR-AUC | Recall | Precision | F1-Score |
|--------|--------|--------|-----------|----------|
| Logistic Regression | 0.783 | 88.7% | 22.7% | 0.362 |
| **Random Forest** | **0.865** | **82.9%** | **87.0%** | **0.848** |
| XGBoost | 0.853 | 83.4% | 81.7% | 0.825 |

**Modèle retenu :** Random Forest (meilleur compromis PR-AUC/Precision)

---

## 🎯 Résultats et Performances

### Métriques Finales (Validation Set)

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| **ROC-AUC** | **0.973** | Excellente capacité de discrimination |
| **PR-AUC** | **0.840** | Excellent pour données déséquilibrées |
| **Recall** | **87.8%** | Détecte 65/74 fraudes réelles |
| **Precision** | **21.1%** | 1 alerte sur 5 est une vraie fraude |
| **F1-Score** | **0.340** | Bon équilibre global |
| **Seuil optimal** | **0.0733** | Optimisé pour maximiser Recall |

### Matrice de Confusion (Validation Set : 42,721 transactions)

|  | Prédiction : Normale | Prédiction : Fraude |
|--|----------------------|---------------------|
| **Réalité : Normale (42,647)** | 42,404 (TN) | 243 (FP) |
| **Réalité : Fraude (74)** | 9 (FN) | 65 (TP) |

**Points clés :**
- ✅ **Seulement 9 fraudes manquées** sur 74 (12.2%)
- ✅ **243 fausses alertes** sur 42,647 normales (0.57%)
- ✅ Coût de vérification acceptable en production

---

## 🏗️ Architecture du Projet

```
fraud-detection-pfe/
├── app/
│   └── streamlit_app.py              # Application web Streamlit (718 lignes)
│
├── notebooks/
│   ├── 01_eda.ipynb                  # Analyse exploratoire des données
│   └── 02_preparation.ipynb          # Préparation, modélisation, évaluation
│
├── src/                               # Code source modulaire
│   ├── data/loader.py                # Chargement des artefacts
│   ├── models/predictor.py           # Prédictions et classification
│   ├── models/explainer.py           # Explications SHAP
│   ├── utils/validation.py           # Validation des données
│   └── visualization/plots.py        # Graphiques Plotly
│
├── scripts/
│   ├── setup.sh                      # Installation automatique
│   ├── train_model.py                # Entraînement du modèle
│   └── predict.py                    # Prédictions CLI
│
├── tests/                             # 22 tests unitaires (pytest)
│   ├── test_predictor.py             # Tests du prédicateur
│   ├── test_loader.py                # Tests du chargeur
│   └── test_validation.py            # Tests de validation
│
├── docs/
│   ├── USER_GUIDE.md                 # Guide utilisateur
│   └── DEVELOPER_GUIDE.md            # Guide développeur
│
├── data/                              # Données (non versionnées)
│   ├── raw/creditcard.csv            # Dataset Kaggle (150 MB)
│   └── processed/                    # Données prétraitées
│
├── models/                            # Modèles entraînés (non versionnés)
│   └── rf_smote_final/
│       ├── pipeline.joblib           # Pipeline scikit-learn complet
│       ├── metrics_valid.json        # Métriques sur validation set
│       └── columns.json              # Métadonnées des colonnes
│
└── reports/
    └── predictions/                  # Archives des prédictions batch
```

---

## 🔧 Technologies Utilisées

| Catégorie | Technologies |
|-----------|-------------|
| **ML/Data Science** | scikit-learn, XGBoost, imbalanced-learn (SMOTE), SHAP |
| **Visualisation** | Plotly, Matplotlib, Seaborn |
| **Web Framework** | Streamlit |
| **Data Processing** | pandas, NumPy |
| **Testing** | pytest |
| **Dev Tools** | Jupyter, Git |

---

## 🚀 Installation et Utilisation

### Installation Automatique

```bash
git clone https://github.com/Mariechanne/fraud-detection-pfe.git
cd fraud-detection-pfe
bash scripts/setup.sh
```

Le script d'installation va :
1. Créer l'environnement virtuel Python
2. Installer les dépendances
3. Vous guider pour télécharger le dataset Kaggle
4. Entraîner le modèle automatiquement (5-10 min)

**Note :** Le dataset Kaggle (150 MB) et le modèle entraîné (50-100 MB) ne sont pas versionnés dans Git. Voir `data/raw/README.md` pour obtenir les données.

### Installation Manuelle

```bash
# 1. Environnement virtuel
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate sur Windows

# 2. Dépendances
pip install -r requirements.txt

# 3. Télécharger les données depuis Kaggle
# https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
# Placer creditcard.csv dans data/raw/

# 4. Entraîner le modèle
python scripts/train_model.py --data data/raw/creditcard.csv
```

### Utilisation

**Application Web :**
```bash
streamlit run app/streamlit_app.py
# Ouvre http://localhost:8501
```

**Prédiction CLI :**
```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --file data/examples/sample_transactions.csv
```

**Tests :**
```bash
pytest tests/ -v
# 22 tests (8 + 4 + 10)
```

---

## 🧪 Tests et Qualité

| Module | Tests | Couverture | Description |
|--------|-------|------------|-------------|
| `test_predictor.py` | 8 | 95% | Tests de FraudPredictor |
| `test_loader.py` | 4 | 92% | Tests de ArtifactLoader |
| `test_validation.py` | 10 | 88% | Tests de DataValidator |

**Total :** 22 tests unitaires avec pytest

**Architecture :**
- ✅ Code modulaire (séparation data / models / utils / visualization)
- ✅ Aucune duplication (refactorisation complète de streamlit_app.py)
- ✅ Docstrings et type hints
- ✅ Gestion robuste des erreurs

---

## 📚 Documentation

- **README.md** : Vue d'ensemble du projet (ce fichier)
- **docs/USER_GUIDE.md** : Guide d'utilisation de l'application
- **docs/DEVELOPER_GUIDE.md** : Architecture et API du code
- **notebooks/01_eda.ipynb** : Analyse exploratoire détaillée
- **notebooks/02_preparation.ipynb** : Pipeline ML complet
- **data/raw/README.md** : Instructions pour obtenir les données
- **models/README.md** : Instructions pour entraîner/charger le modèle

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **Dataset** : [Credit Card Fraud Detection (Kaggle)](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) par ULB Machine Learning Group
- **Encadrement** : [Votre encadrant/institution]

---

<div align="center">

**Projet de Fin d'Études — Détection de Fraudes Bancaires**

*Développé avec Python, scikit-learn, Streamlit et SHAP*

</div>
