# 🕵️‍♀️ Système de Détection de Fraudes Bancaires

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-22%20passing-success.svg)](tests/)

> **Projet de Fin d'Études** — Détection automatique de transactions bancaires frauduleuses par Machine Learning

Application web interactive développée avec **Streamlit** permettant de détecter les fraudes bancaires en temps réel avec une précision exceptionnelle (**PR-AUC: 0.84**, **ROC-AUC: 0.97**).

---

## 📸 Aperçu

- ✅ **Application Streamlit** professionnelle et interactive
- 🤖 **Modèle Random Forest** optimisé avec SMOTE (300 arbres)
- 📊 **Explications SHAP** pour l'interprétabilité
- 🧪 **22 tests unitaires** pour la fiabilité
- 📝 **Documentation complète** (guides utilisateur et développeur)
- 🛠️ **Architecture modulaire** avec code propre et testé
- 🎯 **Validation croisée 5-fold** et optimisation du seuil

---

## 🖼️ Captures d'Écran

### Interface Principale

> **💡 Astuce** : Consultez [docs/SCREENSHOTS.md](docs/SCREENSHOTS.md) pour savoir comment prendre ces captures.

<!-- Décommentez et ajoutez vos images ci-dessous -->

<!--
### Vue d'ensemble de l'application
![Vue d'ensemble](docs/images/app-overview.png)

### Analyse de Transaction Unique
![Formulaire](docs/images/single-transaction-form.png)

### Résultat de l'Analyse avec SHAP
![Résultat](docs/images/single-transaction-result.png)
![Explications SHAP](docs/images/shap-explanation.png)

### Analyse par Lot (CSV)
![Analyse batch](docs/images/batch-analysis.png)
![Résultats batch](docs/images/batch-results-tabs.png)
-->

**📌 Note** : Les captures d'écran seront ajoutées après avoir lancé l'application. Voir le guide dans `docs/SCREENSHOTS.md`.

---

## 📊 Performances du Modèle

| Métrique | Score | Interprétation |
|----------|-------|----------------|
| **ROC-AUC** | **0.973** | ⭐⭐⭐⭐⭐ Excellente capacité de discrimination |
| **PR-AUC** | **0.840** | ⭐⭐⭐⭐⭐ Excellent pour données déséquilibrées (0.17% fraudes) |
| **Recall** | **87.8%** | Détecte 65/74 fraudes réelles (seulement 9 manquées) |
| **Precision** | **21.1%** | 1 alerte sur 5 est une vraie fraude (65 vraies / 308 alertes) |
| **Seuil optimal** | **0.0733** | Optimisé pour maximiser le Recall (Precision ≥ 20%) |
| **F1-Score** | **0.340** | Bon équilibre global |

**Dataset** : [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) — 284,807 transactions (0.17% fraudes)

**Méthodologie** : Split stratifié 70/15/15 → Preprocessing (StandardScaler) → SMOTE (20%) → Random Forest (300 trees) → Validation croisée 5-fold → Optimisation du seuil

---

## 🚀 Installation Complète

> **🚨 IMPORTANT** : Ce projet nécessite des données (150 MB) et un modèle entraîné (50-100 MB) qui ne sont **pas inclus dans Git**.

### Méthode 1 : Installation Automatique (Recommandé)

```bash
# 1. Cloner le projet
git clone https://github.com/Mariechanne/fraud-detection-pfe.git
cd fraud-detection-pfe

# 2. Lancer le script d'installation
bash scripts/setup.sh
```

Le script va :
1. ✅ Vérifier Python 3.11+
2. ✅ Créer l'environnement virtuel
3. ✅ Installer les dépendances (`requirements.txt`)
4. ⏸️ Vous demander de télécharger le dataset Kaggle
5. ✅ Entraîner le modèle automatiquement (5-10 min)
6. ✅ Lancer les tests

**Temps estimé** : 10-15 minutes (selon votre connexion et CPU)

---

### Méthode 2 : Installation Manuelle (Étape par Étape)

#### Étape 1 : Cloner et Préparer l'Environnement

```bash
# Cloner le projet
git clone https://github.com/Mariechanne/fraud-detection-pfe.git
cd fraud-detection-pfe

# Créer un environnement virtuel Python
python3 -m venv .venv

# Activer l'environnement
source .venv/bin/activate  # Linux/macOS
# OU
.venv\Scripts\activate     # Windows
```

#### Étape 2 : Installer les Dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Vérification :**

```bash
python scripts/env_check.py
# Devrait afficher : ✅ Toutes les dépendances sont installées
```

#### Étape 3 : Télécharger les Données

Le dataset Kaggle n'est **pas inclus dans Git** (150 MB, licence Kaggle).

**Option A — Téléchargement Manuel (Recommandé) :**

1. Créez un compte gratuit sur [Kaggle](https://www.kaggle.com)
2. Téléchargez le dataset : **https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud**
3. Décompressez et placez `creditcard.csv` dans `data/raw/`

```bash
# Vérifier
ls -lh data/raw/creditcard.csv
# Devrait afficher : creditcard.csv (~150 MB)
```

**Option B — Kaggle API (Avancé) :**

```bash
# Installer la CLI Kaggle
pip install kaggle

# Configurer vos credentials (~/.kaggle/kaggle.json)
# Voir : https://www.kaggle.com/docs/api

# Télécharger automatiquement
kaggle datasets download -d mlg-ulb/creditcardfraud -p data/raw/ --unzip
```

#### Étape 4 : Préparer les Données et Entraîner le Modèle

**Option A — Via Jupyter Notebook (Recommandé pour comprendre) :**

```bash
jupyter notebook notebooks/02_preparation.ipynb
# Exécutez toutes les cellules (Menu : Cell → Run All)
```

**Option B — Via Script Python (Plus rapide) :**

```bash
python scripts/train_model.py \
  --data data/raw/creditcard.csv \
  --output models/rf_smote_final \
  --smote-strategy 0.2
```

**Durée** : 5-10 minutes (dépend de votre CPU)

**Résultat attendu** :
- `models/rf_smote_final/pipeline.joblib` (~50-100 MB)
- `models/rf_smote_final/metrics_valid.json`
- `models/rf_smote_final/columns.json`
- `data/processed/X_train.csv`, `X_valid.csv`, `X_test.csv`, etc.

#### Étape 5 : Vérifier l'Installation

```bash
# Vérifier que le modèle existe
ls -lh models/rf_smote_final/
# Devrait afficher : pipeline.joblib, metrics_valid.json, columns.json

# Lancer les tests
pytest tests/ -v
# Devrait afficher : 22 passed ✅
```

---

## 🎮 Utilisation

### 1. Lancer l'Application Web

```bash
streamlit run app/streamlit_app.py
```

L'application s'ouvrira automatiquement à **http://localhost:8501**

**Fonctionnalités** :
- 🔍 **Analyse de transaction unique** : Formulaire interactif avec prédiction en temps réel
- 📁 **Analyse par lot (CSV)** : Upload de fichiers CSV, traitement par batch de 5000 lignes
- 📊 **Explications SHAP** : Top 5 facteurs influents pour chaque prédiction
- 🗄️ **Archivage automatique** : Sauvegarde dans `reports/predictions/`
- ⚙️ **Seuil ajustable** : Slider pour modifier le seuil de décision

### 2. Prédiction en Ligne de Commande

**Transaction unique :**

```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --transaction '{"Amount": 100.50, "Time": 50000}'
```

**Fichier CSV :**

```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --file data/examples/sample_transactions.csv \
  --output predictions.csv
```

### 3. Ré-entraîner le Modèle

```bash
python scripts/train_model.py \
  --data data/raw/creditcard.csv \
  --output models/my_model \
  --smote-strategy 0.2
```

### 4. Lancer les Tests

```bash
# Tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/test_predictor.py -v
pytest tests/test_loader.py -v
```

---

## 🏗️ Architecture du Projet

```
fraud-detection-pfe/
├── 📱 app/
│   └── streamlit_app.py          # Application web Streamlit (718 lignes)
│
├── 📓 notebooks/
│   ├── 01_eda.ipynb              # Analyse exploratoire des données
│   └── 02_preparation.ipynb      # Préparation, modélisation et évaluation
│
├── 🔧 scripts/
│   ├── setup.sh                  # Script d'installation automatique
│   ├── train_model.py            # Entraînement du modèle (CLI)
│   ├── predict.py                # Prédictions en ligne de commande
│   └── env_check.py              # Vérification de l'environnement
│
├── 📦 src/                        # Code source modulaire
│   ├── data/
│   │   └── loader.py             # ArtifactLoader : Chargement des artefacts
│   ├── models/
│   │   ├── predictor.py          # FraudPredictor : Prédictions
│   │   └── explainer.py          # FraudExplainer : Explications SHAP
│   ├── utils/
│   │   └── validation.py         # DataValidator : Validation des données
│   └── visualization/
│       └── plots.py              # FraudVisualizer : Graphiques Plotly
│
├── 🧪 tests/
│   ├── test_predictor.py         # Tests du prédicateur (8 tests)
│   ├── test_loader.py            # Tests du chargeur (4 tests)
│   └── test_validation.py        # Tests de validation (10 tests)
│
├── 📚 docs/
│   ├── USER_GUIDE.md             # Guide utilisateur complet
│   └── DEVELOPER_GUIDE.md        # Guide développeur (architecture, API)
│
├── 📊 data/
│   ├── raw/                      # Données brutes (non versionnées)
│   │   ├── README.md             # Instructions pour télécharger Kaggle
│   │   └── creditcard.csv        # Dataset Kaggle (150 MB, non inclus)
│   ├── processed/                # Données prétraitées (non versionnées)
│   │   ├── README.md
│   │   └── X_train.csv, y_train.csv, etc.
│   └── examples/                 # Exemples pour tests
│       ├── README.md
│       └── sample_transactions.csv  # 5 transactions d'exemple
│
├── 🤖 models/
│   ├── README.md                 # Instructions pour entraîner/charger
│   └── rf_smote_final/           # Modèle final (non versionné)
│       ├── pipeline.joblib       # Pipeline scikit-learn complet
│       ├── metrics_valid.json    # Métriques sur validation set
│       └── columns.json          # Métadonnées des colonnes
│
└── 📋 reports/
    └── predictions/              # Archives des prédictions batch
```

---

## 🎯 Fonctionnalités Détaillées

### 1. 🔍 Analyse de Transaction Unique

- **Formulaire intuitif** : Champs Amount, Time, V1-V28 (variables PCA)
- **Bouton "Charger Exemple"** : Charge une vraie fraude du test set
- **Prédiction en temps réel** avec 4 indicateurs :
  - 🚨 Verdict (FRAUDE DÉTECTÉE / NORMALE)
  - 📊 Probabilité de fraude (0-100%)
  - ⚠️ Niveau de risque (FAIBLE / MODÉRÉ / ÉLEVÉ / CRITIQUE)
  - 🎯 Seuil appliqué
- **Explications SHAP** : Top 5 facteurs influents avec impact positif/négatif
- **Visualisations** : Barre de progression, graphique probabilité vs seuil

### 2. 📁 Analyse par Lot (CSV)

- **Upload de fichiers CSV** (jusqu'à 100,000 lignes)
- **Validation automatique** avec `DataValidator`
- **Traitement par batch** : Chunks de 5,000 lignes pour gros fichiers
- **Barre de progression** en temps réel
- **4 onglets de résultats** :
  - 📋 Données complètes (avec highlighting des fraudes)
  - 🚨 Fraudes détectées uniquement
  - 📊 Distribution des probabilités (histogramme)
  - 🎯 Analyse par niveau de risque (pie chart)
- **Archivage automatique** dans `reports/predictions/` avec index
- **Export CSV** : Téléchargement du rapport complet

### 3. ⚙️ Configuration Avancée

- **Seuil ajustable** : Slider 0.00-0.50 (défaut: 0.0733)
- **Jauge visuelle** de sensibilité
- **Métriques du modèle** affichées en temps réel
- **Informations techniques** : Algorithme, features, pipeline

---

## 📈 Méthodologie ML

### Pipeline Complet

```
Données brutes (creditcard.csv)
    ↓
Split stratifié 70/15/15 (train/valid/test)
    ↓
Preprocessing : StandardScaler sur Amount/Time
    ↓
SMOTE : sampling_strategy=0.2 (199k normales → 39.8k fraudes synthétiques)
    ↓
Random Forest : 300 arbres, n_jobs=-1
    ↓
Validation croisée 5-fold
    ↓
Optimisation du seuil (max Recall avec Precision ≥ 20%)
    ↓
Évaluation finale sur test set
```

### Métriques Détaillées (Validation Set)

| Métrique | Valeur | Détails |
|----------|--------|---------|
| **True Negatives** | 42,404 | Transactions normales bien classées |
| **False Positives** | 243 | Fausses alertes (0.57% des normales) |
| **False Negatives** | 9 | Fraudes manquées (12.16% des fraudes) |
| **True Positives** | 65 | Fraudes détectées (87.84% des fraudes) |
| **Total** | 42,721 | 74 fraudes réelles dans le validation set |

**Interprétation** :
- Le modèle détecte **65 fraudes sur 74** (87.8% de rappel)
- Il génère **243 fausses alertes** sur 42,647 transactions normales (0.57%)
- **Seulement 9 fraudes manquées** → Excellent pour la sécurité bancaire
- **1 alerte sur 5 est vraie** (65/308) → Coût de vérification acceptable

---

## 🧪 Tests et Qualité du Code

### Tests Unitaires (22 tests)

```bash
pytest tests/ -v --cov=src
```

| Module | Tests | Couverture | Description |
|--------|-------|------------|-------------|
| `test_predictor.py` | 8 | 95% | Tests de FraudPredictor (predict_single, predict_batch, risk_level) |
| `test_loader.py` | 4 | 92% | Tests de ArtifactLoader (chargement, fallbacks, erreurs) |
| `test_validation.py` | 10 | 88% | Tests de DataValidator (validation, sanitization, types) |

### Architecture Modulaire

- ✅ **Séparation des responsabilités** : data / models / utils / visualization
- ✅ **Code DRY** : Aucune duplication (refactorisation complète de streamlit_app.py)
- ✅ **Docstrings** : Toutes les fonctions documentées
- ✅ **Type hints** : Annotations de types pour clarté
- ✅ **Error handling** : Gestion robuste des erreurs avec fallbacks

---

## 🐛 Résolution de Problèmes

### Erreur : `ModuleNotFoundError: No module named 'streamlit'`

**Cause** : Environnement virtuel non activé ou dépendances non installées

**Solution** :
```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Erreur : `FileNotFoundError: data/raw/creditcard.csv`

**Cause** : Dataset Kaggle non téléchargé

**Solution** : Téléchargez le dataset depuis [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) et placez-le dans `data/raw/`

### Erreur : `FileNotFoundError: models/rf_smote_final/pipeline.joblib`

**Cause** : Modèle non entraîné

**Solution** :
```bash
# Option 1 : Script automatique
python scripts/train_model.py --data data/raw/creditcard.csv

# Option 2 : Notebook Jupyter
jupyter notebook notebooks/02_preparation.ipynb
# Exécutez toutes les cellules jusqu'à la section 6.6
```

### L'application Streamlit ne charge pas le modèle

**Diagnostic** :
```bash
ls models/rf_smote_final/pipeline.joblib
# Si "No such file" → le modèle n'existe pas
```

**Solution** : Voir ci-dessus (entraîner le modèle)

### Tests échouent : `ModuleNotFoundError: No module named 'numpy'`

**Cause** : Dépendances de test non installées

**Solution** :
```bash
pip install -r requirements.txt
```

---

## 🎓 Utilisation Académique (Soutenance PFE)

### Démo Sans Données Complètes

Si vous n'avez **pas accès au dataset Kaggle** (150 MB) :

1. Utilisez le fichier d'exemple fourni :
   ```bash
   streamlit run app/streamlit_app.py
   # Section "Analyse par Lot" → Uploadez data/examples/sample_transactions.csv
   ```

2. Ou chargez un modèle pré-entraîné (si fourni séparément via Google Drive / GitHub Releases)

### Points Forts à Présenter

| Aspect | Ce qu'il faut dire |
|--------|-------------------|
| **Méthodologie** | *"Validation croisée 5-fold, split stratifié, optimisation du seuil basée sur le Recall"* |
| **Performances** | *"PR-AUC de 0.84 excellent pour données déséquilibrées (0.17% fraudes)"* |
| **Recall élevé** | *"87.8% de détection, seulement 9 fraudes manquées sur 74"* |
| **Architecture** | *"Code modulaire avec 22 tests unitaires, architecture refactorisée pour éliminer la duplication"* |
| **Interprétabilité** | *"Explications SHAP intégrées, top 5 facteurs influents pour chaque prédiction"* |
| **Reproductibilité** | *"Installation automatisée en 10-15 minutes via script Bash, documentation complète"* |

### Ordre de Présentation Recommandé

1. **Introduction** (2 min) : Problème de fraude bancaire, importance du Recall
2. **Données** (3 min) : Dataset Kaggle, déséquilibre extrême (0.17%), EDA
3. **Méthodologie** (5 min) : Pipeline, SMOTE, Random Forest, validation croisée
4. **Résultats** (5 min) : Métriques, matrice de confusion, comparaison des modèles
5. **Démonstration** (5 min) : Application Streamlit en live
6. **Architecture** (3 min) : Code modulaire, tests, reproductibilité
7. **Conclusion** (2 min) : Limitations, améliorations futures

---

## 📚 Documentation Complémentaire

- **Guide Utilisateur** : `docs/USER_GUIDE.md` (utilisation de l'application, CLI)
- **Guide Développeur** : `docs/DEVELOPER_GUIDE.md` (architecture, API, déploiement)
- **Notebooks Jupyter** :
  - `notebooks/01_eda.ipynb` : Analyse exploratoire complète
  - `notebooks/02_preparation.ipynb` : Préparation, modélisation, évaluation
- **README des dossiers** :
  - `data/raw/README.md` : Comment obtenir les données
  - `data/processed/README.md` : Fichiers générés automatiquement
  - `models/README.md` : Comment entraîner/charger le modèle

---

## 🔧 Technologies Utilisées

| Catégorie | Technologies |
|-----------|-------------|
| **ML/Data Science** | scikit-learn, XGBoost, imbalanced-learn (SMOTE), SHAP |
| **Visualisation** | Plotly, Matplotlib, Seaborn |
| **Web Framework** | Streamlit 1.38+ |
| **Data Processing** | pandas, NumPy |
| **Testing** | pytest |
| **Dev Tools** | Jupyter, Git, Bash |

**Versions exactes** : Voir `requirements.txt`

---

## 📝 License

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **Dataset** : [Credit Card Fraud Detection (Kaggle)](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) par ULB Machine Learning Group
- **Inspirations** : Documentation scikit-learn, SMOTE paper, SHAP paper
- **Encadrement** : [Votre encadrant/institution]

---

## 📞 Contact et Support

- **Auteur** : [Votre nom]
- **Email** : [Votre email]
- **GitHub** : https://github.com/Mariechanne/fraud-detection-pfe

**Problème non résolu ?** Consultez :
1. Les README dans chaque dossier (`data/*/README.md`, `models/README.md`)
2. La section "Résolution de Problèmes" ci-dessus
3. Les guides dans `docs/`

---

## ✅ Checklist Complète d'Installation

- [ ] Python 3.11+ installé (`python3 --version`)
- [ ] Projet cloné depuis GitHub
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Dataset Kaggle téléchargé dans `data/raw/creditcard.csv`
- [ ] Modèle entraîné (fichier `models/rf_smote_final/pipeline.joblib` existe)
- [ ] Tests passent (`pytest tests/ -v` → 22 passed ✅)
- [ ] Application lance (`streamlit run app/streamlit_app.py`)

**Si tous les points sont cochés** → ✅ **Votre projet est prêt pour la soutenance !**

---

<div align="center">

**Développé avec ❤️ pour la détection de fraudes bancaires**

⭐ **N'oubliez pas de mettre une étoile sur GitHub si ce projet vous a aidé !** ⭐

</div>
