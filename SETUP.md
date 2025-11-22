# 🚀 Guide d'Installation et de Configuration

Ce guide vous permettra de **configurer complètement** le projet `fraud-detection-pfe` depuis zéro.

---

## 📋 Prérequis

- **Python 3.11+** (testé avec Python 3.11.14)
- **Git** pour cloner le projet
- **~500 MB d'espace disque** (données + modèle)
- **(Optionnel)** Compte [Kaggle](https://www.kaggle.com) pour télécharger les données

---

## 📥 Étape 1 : Cloner le Projet

```bash
git clone https://github.com/Mariechanne/fraud-detection-pfe.git
cd fraud-detection-pfe
```

---

## 🐍 Étape 2 : Créer un Environnement Virtuel

### Sur Linux/macOS :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Sur Windows :

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 📦 Étape 3 : Installer les Dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Vérification :**

```bash
python scripts/env_check.py
# Devrait afficher : ✅ Toutes les dépendances sont installées
```

---

## 📊 Étape 4 : Obtenir les Données

Le dataset n'est **pas inclus dans Git** (150 MB, licence Kaggle).

### Option A : Téléchargement Manuel (Recommandé)

1. Créez un compte gratuit sur [Kaggle](https://www.kaggle.com)

2. Téléchargez le dataset :
   👉 https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

3. Décompressez et placez le fichier :
   ```bash
   mv ~/Downloads/creditcard.csv data/raw/
   ```

4. Vérifiez :
   ```bash
   ls -lh data/raw/creditcard.csv
   # Devrait afficher : creditcard.csv (~150 MB, 284 807 lignes)
   ```

### Option B : Kaggle API (Avancé)

```bash
# Installez la CLI Kaggle
pip install kaggle

# Configurez vos credentials (~/.kaggle/kaggle.json)
# Voir : https://www.kaggle.com/docs/api

# Téléchargez automatiquement
kaggle datasets download -d mlg-ulb/creditcardfraud -p data/raw/ --unzip
```

---

## 🔧 Étape 5 : Préparer les Données

### Option A : Via Jupyter Notebook (Recommandé pour comprendre le pipeline)

```bash
jupyter notebook notebooks/02_preparation.ipynb
```

Exécutez **toutes les cellules** (Menu : `Cell` → `Run All`)

**Résultat attendu :**
- Création de `data/processed/X_train.csv`, `X_valid.csv`, `X_test.csv`, etc.
- Entraînement et sauvegarde du modèle dans `models/rf_smote_final/`

### Option B : Via Script (Plus rapide)

```bash
python scripts/train_model.py \
  --data data/raw/creditcard.csv \
  --output models/rf_smote_final \
  --smote-strategy 0.2
```

**Durée estimée :** 5-10 minutes (dépend de votre CPU)

---

## ✅ Étape 6 : Vérifier l'Installation

```bash
# Vérifier que le modèle existe
ls -lh models/rf_smote_final/
# Devrait afficher :
#   pipeline.joblib (~50-100 MB)
#   metrics_valid.json
#   columns.json

# Vérifier les données prétraitées
ls -lh data/processed/
# Devrait afficher :
#   X_train.csv, y_train.csv
#   X_valid.csv, y_valid.csv
#   X_test.csv, y_test.csv
```

---

## 🚀 Étape 7 : Lancer l'Application

### Application Web Streamlit

```bash
streamlit run app/streamlit_app.py
```

Ouvrez votre navigateur : **http://localhost:8501**

### Scripts CLI

**Prédiction sur une transaction unique :**

```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --transaction '{"Amount": 100, "Time": 5000}'
```

**Prédiction sur un fichier CSV :**

```bash
python scripts/predict.py \
  --model models/rf_smote_final \
  --file data/processed/X_test.csv \
  --output predictions.csv
```

---

## 🧪 Étape 8 : Exécuter les Tests

```bash
# Tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/test_predictor.py -v
pytest tests/test_loader.py -v
pytest tests/test_validation.py -v
```

**Résultat attendu :** 22 tests passent ✅

---

## 📚 Structure du Projet Après Installation

```
fraud-detection-pfe/
├── data/
│   ├── raw/
│   │   └── creditcard.csv          ✅ Téléchargé manuellement
│   └── processed/
│       ├── X_train.csv             ✅ Généré par notebook/script
│       ├── y_train.csv
│       └── ...
├── models/
│   └── rf_smote_final/
│       ├── pipeline.joblib         ✅ Généré par notebook/script
│       ├── metrics_valid.json
│       └── columns.json
├── notebooks/
│   ├── 01_eda.ipynb                📊 Analyses exploratoires
│   └── 02_preparation.ipynb        🔧 Préparation + modélisation
├── app/
│   └── streamlit_app.py            🌐 Application web
└── src/                            📦 Code source modulaire
```

---

## 🐛 Résolution de Problèmes

### Erreur : `ModuleNotFoundError: No module named 'streamlit'`

**Solution :** Réactivez l'environnement virtuel

```bash
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Erreur : `FileNotFoundError: data/raw/creditcard.csv`

**Solution :** Téléchargez le dataset Kaggle (voir Étape 4)

### Erreur : `FileNotFoundError: models/rf_smote_final/pipeline.joblib`

**Solution :** Entraînez le modèle (voir Étape 5)

```bash
jupyter notebook notebooks/02_preparation.ipynb
# Ou
python scripts/train_model.py --data data/raw/creditcard.csv
```

### L'application Streamlit ne charge pas le modèle

**Diagnostic :**

```bash
ls models/rf_smote_final/pipeline.joblib
# Si erreur → le modèle n'existe pas
```

**Solution :** Exécutez le notebook `02_preparation.ipynb` jusqu'à la section 6.6

---

## 🎓 Utilisation Académique (Soutenance PFE)

### Démo Rapide Sans Données Kaggle

Si vous n'avez pas accès au dataset complet :

1. Utilisez les données d'exemple (si disponibles) :
   ```bash
   cp data/examples/sample_transactions.csv data/test_input.csv
   ```

2. Chargez le modèle pré-entraîné (si fourni séparément)

3. Lancez l'app en mode démo

### Présenter le Projet

1. **Notebooks Jupyter** : Montrez les analyses (`01_eda.ipynb`)
2. **Architecture modulaire** : Expliquez `src/` (loader, predictor, explainer)
3. **Application Streamlit** : Démo live de détection de fraude
4. **Tests** : Montrez la couverture (`pytest tests/ -v`)
5. **Métriques** : Insistez sur **Recall 87.8%** et **PR-AUC 0.83**

---

## 📞 Support

**Problème non résolu ?**

1. Vérifiez les fichiers README dans chaque dossier :
   - `data/raw/README.md`
   - `data/processed/README.md`
   - `models/README.md`

2. Consultez la documentation :
   - `docs/USER_GUIDE.md` (utilisation)
   - `docs/DEVELOPER_GUIDE.md` (architecture)

3. Ouvrez une issue GitHub (si applicable)

---

## ✅ Checklist Complète

- [ ] Python 3.11+ installé
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Dataset Kaggle téléchargé (`data/raw/creditcard.csv`)
- [ ] Notebook `02_preparation.ipynb` exécuté OU script `train_model.py`
- [ ] Modèle généré (`models/rf_smote_final/pipeline.joblib` existe)
- [ ] Tests passent (`pytest tests/ -v`)
- [ ] Application lance (`streamlit run app/streamlit_app.py`)

**Si tous les points sont cochés → ✅ Votre projet est prêt pour la démo !**
