# 🕵️‍♀️ Système de Détection de Fraudes Bancaires

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Projet de Fin d'Études** - Détection automatique de transactions bancaires frauduleuses par Machine Learning

Application web interactive développée avec **Streamlit** permettant de détecter les fraudes bancaires en temps réel avec une précision exceptionnelle (PR-AUC: 0.86, ROC-AUC: 0.97).

---

## 📸 Aperçu

- ✅ **Application Streamlit** professionnelle et interactive
- 🤖 **Modèle Random Forest** optimisé avec SMOTE
- 📊 **Explications SHAP** pour l'interprétabilité
- 🧪 **22 tests unitaires** pour la fiabilité
- 📝 **Documentation complète** (utilisateur + développeur)
- 🛠️ **Scripts CLI** pour entraînement et prédiction

---

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le projet
git clone https://github.com/Mariechanne/fraud-detection-pfe.git
cd fraud-detection-pfe

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer l'Application

```bash
streamlit run app/streamlit_app.py
```

L'application s'ouvrira automatiquement à `http://localhost:8501`

---

## 📊 Performances du Modèle

| Métrique | Score | Interprétation |
|----------|-------|----------------|
| **PR-AUC** | 0.86 | ⭐⭐⭐⭐⭐ Excellent pour données déséquilibrées |
| **ROC-AUC** | 0.97 | ⭐⭐⭐⭐⭐ Excellente capacité de discrimination |
| **Recall** | 86% | Détecte 86% des fraudes réelles |
| **Precision** | 20% | 1 alerte sur 5 est une vraie fraude |
| **Seuil optimal** | 0.0733 | Équilibre Recall/Precision |

**Dataset** : [Kaggle Credit Card Fraud](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) - 284,807 transactions (0.17% fraudes)

---

## 🏗️ Architecture du Projet

```
fraud-detection-pfe/
├── 📱 app/
│   └── streamlit_app.py          # Application web Streamlit
│
├── 📓 notebooks/
│   ├── 01_eda.ipynb              # Analyse exploratoire
│   └── 02_preparation.ipynb      # Préparation et modélisation
│
├── 🔧 scripts/
│   ├── train_model.py            # Entraînement du modèle
│   ├── predict.py                # Prédictions CLI
│   └── env_check.py              # Vérification environnement
│
├── 📦 src/
│   ├── data/                     # Chargement artefacts
│   ├── models/                   # Prédiction et SHAP
│   ├── utils/                    # Validation données
│   └── visualization/            # Graphiques Plotly
│
├── 🧪 tests/
│   ├── test_predictor.py         # Tests prédictions
│   ├── test_loader.py            # Tests chargement
│   └── test_validation.py        # Tests validation
│
├── 📚 docs/
│   ├── USER_GUIDE.md             # Guide utilisateur
│   └── DEVELOPER_GUIDE.md        # Guide développeur
│
└── 📊 reports/
    └── predictions/              # Archives prédictions
```

---

## 🎯 Fonctionnalités

### 1. 🔍 Analyse de Transaction Unique

- Formulaire intuitif (Amount, Time, V1-V28)
- Prédiction en temps réel
- Score de risque (FAIBLE, MODÉRÉ, ÉLEVÉ, CRITIQUE)
- Top 5 facteurs influents (SHAP)
- Graphiques interactifs

### 2. 📁 Analyse par Lot (CSV)

- Upload de fichiers jusqu'à 100k transactions
- Traitement par batch avec barre de progression
- 4 onglets de visualisation
- Export CSV avec résultats
- Archivage automatique

### 3. ⚙️ Configuration Avancée

- Seuil de décision ajustable (0-50%)
- Métriques du modèle en temps réel
- Archivage activable/désactivable

---

## 🛠️ Scripts en Ligne de Commande

### Entraîner un Nouveau Modèle

```bash
python scripts/train_model.py \
  --data data/raw/creditcard.csv \
  --output models/my_model \
  --smote-strategy 0.2
```

### Prédire sur de Nouvelles Données

**Fichier CSV :**
```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --input data/test.csv \
  --output results/predictions.csv
```

**Transaction unique :**
```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --amount 250.50 \
  --time 3600
```

---

## 🧪 Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Avec couverture de code
pytest tests/ --cov=src --cov-report=html

# Tests spécifiques
pytest tests/test_predictor.py -v
```

**Couverture** : 22 tests unitaires sur les modules critiques

---

## 🧠 Méthodologie ML

### Pipeline Complet

```
Données brutes (CSV)
    ↓
Split 70/15/15 (Train/Valid/Test)
    ↓
Preprocessing (StandardScaler sur Amount & Time)
    ↓
SMOTE (Rééquilibrage à 20%)
    ↓
Random Forest (100 arbres, max_depth=20)
    ↓
Optimisation du seuil (Recall ≥ 85%)
    ↓
Modèle final + Explications SHAP
```

### Technologies Utilisées

**Core ML:**
- `scikit-learn` - Pipeline et modèles
- `xgboost` - Alternative Random Forest
- `imbalanced-learn` - SMOTE pour déséquilibre

**Interprétabilité:**
- `shap` - Explications des prédictions

**Visualisation:**
- `plotly` - Graphiques interactifs
- `matplotlib`, `seaborn` - Analyses EDA

**Déploiement:**
- `streamlit` - Application web

---

## 📚 Documentation

- 📖 **[Guide Utilisateur](docs/USER_GUIDE.md)** - Installation, utilisation de l'app et des scripts
- 👨‍💻 **[Guide Développeur](docs/DEVELOPER_GUIDE.md)** - Architecture, API, tests, déploiement
- 📝 **[Scripts README](scripts/README)** - Documentation technique détaillée

---

## 🎓 Contexte Académique

**Établissement** : ESLSCA Paris
**Type** : Projet de Fin d'Études (PFE)
**Auteur** : Marie Chandeste Melvina J. H. Medetadji Migan
**Année** : 2025

---

## 📈 Résultats Clés

✅ **Détecte 86% des fraudes** avec un seuil optimisé
✅ **Application web professionnelle** déployable
✅ **Code modulaire et testé** (22 tests unitaires)
✅ **Documentation complète** pour utilisateurs et développeurs
✅ **Explications SHAP** pour chaque prédiction
✅ **Scripts CLI** pour automatisation

---

## 🚀 Déploiement

### Option 1: Streamlit Cloud

1. Pusher sur GitHub
2. Connecter à [Streamlit Cloud](https://streamlit.io/cloud)
3. Sélectionner `app/streamlit_app.py`
4. Déployer !

### Option 2: Docker

```bash
# Build
docker build -t fraud-detector .

# Run
docker run -p 8501:8501 fraud-detector
```

### Option 3: Serveur Local

```bash
streamlit run app/streamlit_app.py --server.port 8501
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **Kaggle** pour le dataset Credit Card Fraud Detection
- **ESLSCA Paris** pour l'encadrement académique
- La communauté **Streamlit** pour les ressources
- Les auteurs de **SHAP** pour l'interprétabilité

---

## 📧 Contact

**Marie Chandeste Melvina J. H. Medetadji Migan**
📧 Email: melvinamedetadji@gmail.com
🔗 GitHub: [@Mariechanne](https://github.com/Mariechanne)

---

<div align="center">

**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !**

Made with ❤️ for fraud detection

</div>
