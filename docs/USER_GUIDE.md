# 📖 Guide Utilisateur - Système de Détection de Fraude

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le projet
git clone https://github.com/Mariechanne/fraud-detection-pfe.git
cd fraud-detection-pfe

# Installer les dépendances
pip install -r requirements.txt

# Vérifier l'environnement
python scripts/env_check.py
```

---

## 🎯 Utilisation de l'Application Streamlit

### Lancer l'application

```bash
streamlit run app/streamlit_app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Fonctionnalités principales

#### 1. **Analyse de Transaction Unique** 🔍

- Entrez le **montant** et le **temps** de la transaction
- Cliquez sur **"Variables avancées"** pour saisir les features V1-V28 (optionnel)
- Utilisez le bouton **"⚡ Charger Exemple"** pour tester avec une vraie fraude
- Cliquez sur **"🔍 Analyser"**

**Résultats affichés:**
- ✅/🚨 Prédiction (NORMALE ou FRAUDE)
- 📊 Probabilité de fraude
- 🎯 Niveau de risque (FAIBLE, MODÉRÉ, ÉLEVÉ, CRITIQUE)
- 📈 Graphiques de score
- 🔍 Top 5 facteurs influents (SHAP)

#### 2. **Analyse par Lot (CSV)** 📁

**Format du fichier CSV:**
```csv
Amount,Time,V1,V2,V3,...,V28
100.50,500,0.1,-0.2,0.3,...,0.05
250.00,1200,-0.5,0.7,-0.1,...,0.12
```

**Colonnes requises:**
- `Amount` (obligatoire)
- `Time` (obligatoire)
- `V1` à `V28` (optionnel, mis à 0 si absents)

**Utilisation:**
1. Cliquez sur **"Sélectionner un fichier CSV"**
2. Uploadez votre fichier (max 100 000 lignes)
3. L'analyse démarre automatiquement

**Résultats:**
- 📊 Résumé statistique
- 📈 4 onglets de visualisation:
  - **Données complètes** (fraudes surlignées en rouge)
  - **Fraudes détectées** uniquement
  - **Distribution** des probabilités
  - **Analyse par risque** (camembert + tableau)
- 💾 Bouton de téléchargement du rapport CSV
- 🗄️ Archivage automatique dans `reports/predictions/`

#### 3. **Configuration** ⚙️

**Seuil de décision (Sidebar):**
- Ajustez le curseur entre 0% et 50%
- Un seuil **plus bas** détecte plus de fraudes (+ faux positifs)
- Un seuil **plus haut** réduit les faux positifs (- détection)
- Le seuil optimal par défaut est **~7.3%** (85% Recall, 20% Precision)

**Archivage automatique:**
- ✅ Activé par défaut
- Sauvegarde chaque analyse dans `reports/predictions/`
- Index CSV maintenu dans `_index.csv`
- Conservation des 100 dernières archives

---

## 🛠️ Scripts en Ligne de Commande

### 1. Entraîner un nouveau modèle

```bash
python scripts/train_model.py \
  --data data/raw/creditcard.csv \
  --output models/my_new_model \
  --smote-strategy 0.2 \
  --random-state 42
```

**Arguments:**
- `--data`: Chemin vers le fichier CSV de données
- `--output`: Dossier de sortie pour le modèle
- `--smote-strategy`: Stratégie de rééquilibrage SMOTE (default: 0.2)
- `--random-state`: Seed pour la reproductibilité (default: 42)

**Sortie:**
- `models/my_new_model/pipeline.joblib` - Pipeline sklearn complet
- `models/my_new_model/metrics_valid.json` - Métriques de validation
- `models/my_new_model/columns.json` - Colonnes attendues

### 2. Prédire sur de nouvelles données

**Sur un fichier CSV:**
```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --input data/new_transactions.csv \
  --output results/predictions.csv
```

**Sur une transaction unique:**
```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --amount 250.50 \
  --time 3600
```

**Arguments:**
- `--model`: Dossier contenant le modèle
- `--input`: Fichier CSV à analyser (optionnel)
- `--output`: Fichier de sortie pour les résultats (optionnel)
- `--amount`: Montant pour une transaction unique (optionnel)
- `--time`: Temps pour une transaction unique (optionnel)
- `--threshold`: Seuil de décision personnalisé (optionnel)

---

## 📊 Interprétation des Résultats

### Niveaux de Risque

| Niveau | Probabilité | Action recommandée |
|--------|-------------|-------------------|
| 🟢 **FAIBLE** | < 30% | Transaction normale, aucune action |
| 🟡 **MODÉRÉ** | 30-50% | Surveillance recommandée |
| 🟠 **ÉLEVÉ** | 50-80% | Vérification manuelle conseillée |
| 🔴 **CRITIQUE** | > 80% | Investigation immédiate requise |

### Métriques du Modèle

- **PR-AUC (0.86)**: Performance sur données déséquilibrées - **EXCELLENT**
- **ROC-AUC (0.97)**: Capacité de discrimination - **EXCELLENT**
- **Recall (0.86)**: Détecte 86% des fraudes réelles - **BON**
- **Precision (0.20)**: 1 alerte sur 5 est une vraie fraude - **ACCEPTABLE**

### Explications SHAP

Les **valeurs SHAP** indiquent l'impact de chaque variable sur la prédiction:

- **Valeurs positives (🔴)** : Augmentent la probabilité de fraude
- **Valeurs négatives (🟢)** : Diminuent la probabilité de fraude
- **Features clés** : V4, V17, V14, V10, Amount

---

## 🧪 Tests

Lancer les tests unitaires:

```bash
# Installer pytest si nécessaire
pip install pytest

# Lancer tous les tests
pytest tests/ -v

# Lancer un fichier de test spécifique
pytest tests/test_predictor.py -v
```

---

## 📁 Structure des Fichiers

```
fraud-detection-pfe/
├── app/
│   └── streamlit_app.py          # Application web
├── data/
│   ├── raw/                       # Données brutes (gitignored)
│   └── processed/                 # Données prétraitées (gitignored)
├── models/
│   └── rf_smote_final/            # Modèle entraîné (gitignored)
│       ├── pipeline.joblib
│       ├── metrics_valid.json
│       └── columns.json
├── notebooks/
│   ├── 01_eda.ipynb              # Exploration des données
│   └── 02_preparation.ipynb      # Préparation et modélisation
├── reports/
│   └── predictions/               # Archives des prédictions
├── scripts/
│   ├── train_model.py            # Script d'entraînement
│   ├── predict.py                # Script de prédiction
│   └── env_check.py              # Vérification environnement
├── src/
│   ├── data/
│   │   └── loader.py             # Chargement des artefacts
│   ├── models/
│   │   ├── predictor.py          # Prédictions
│   │   └── explainer.py          # Explications SHAP
│   ├── utils/
│   │   └── validation.py         # Validation des données
│   └── visualization/
│       └── plots.py              # Graphiques
└── tests/                         # Tests unitaires
    ├── test_predictor.py
    ├── test_loader.py
    └── test_validation.py
```

---

## ❓ FAQ

**Q: L'application Streamlit ne démarre pas**
```bash
# Vérifier que Streamlit est installé
pip install streamlit

# Vérifier la version de Python
python --version  # Doit être >= 3.10
```

**Q: Le modèle n'est pas trouvé**
- Assurez-vous que le dossier `models/rf_smote_final/` existe
- Vérifiez que `pipeline.joblib` est présent
- Réentraînez le modèle avec `scripts/train_model.py`

**Q: Comment changer le seuil de décision?**
- Dans l'app Streamlit: Utilisez le slider dans la sidebar
- En ligne de commande: Utilisez `--threshold 0.1` avec `predict.py`

**Q: Les tests échouent**
```bash
# Installer toutes les dépendances de test
pip install pytest scikit-learn imbalanced-learn

# Vérifier l'installation
pytest --version
```

**Q: Comment obtenir le dataset Kaggle?**
1. Téléchargez depuis: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
2. Placez `creditcard.csv` dans `data/raw/`
3. Le fichier doit contenir ~285k lignes

---

## 🆘 Support

Pour tout problème ou question:
1. Consultez la documentation dans `scripts/README`
2. Vérifiez les issues GitHub
3. Contactez l'équipe de développement

---

**Version**: 3.0
**Dernière mise à jour**: Novembre 2025
