# 🛠️ Guide Développeur - Système de Détection de Fraude

## 📦 Architecture du Projet

### Modules Réutilisables

Le projet est organisé en modules Python réutilisables pour faciliter la maintenance et l'extension:

```
src/
├── data/          # Chargement des artefacts
├── models/        # Prédiction et explication
├── utils/         # Validation des données
└── visualization/ # Graphiques et visualisations
```

### Composants Principaux

#### 1. `src/data/loader.py` - Chargement des Artefacts

```python
from src.data.loader import ArtifactLoader

# Charger le modèle
loader = ArtifactLoader("models/rf_smote_final")
pipeline, metrics, columns, warnings = loader.load_artifacts()
```

**Responsabilités:**
- Charger le pipeline sklearn
- Charger les métriques de validation
- Charger la liste des colonnes attendues
- Vérifier la cohérence du modèle

#### 2. `src/models/predictor.py` - Prédictions

```python
from src.models.predictor import FraudPredictor

# Initialiser le prédicateur
predictor = FraudPredictor(pipeline, columns, threshold=0.073)

# Prédire sur une transaction
transaction = {"Amount": 100.0, "Time": 500.0}
proba, pred = predictor.predict_single(transaction)

# Prédire sur un DataFrame
probas, preds = predictor.predict(dataframe)

# Traiter un gros fichier par chunks
probas, preds = predictor.predict_batch(dataframe, chunk_size=5000)
```

**Responsabilités:**
- Assurer la présence de toutes les colonnes
- Prédire les probabilités de fraude
- Appliquer le seuil de décision
- Gérer le traitement par batch

#### 3. `src/models/explainer.py` - Explications SHAP

```python
from src.models.explainer import FraudExplainer

# Initialiser l'explainer
explainer = FraudExplainer(pipeline)

# Expliquer une prédiction
features, error = explainer.explain(dataframe, top_k=5)

# Obtenir l'importance globale des features
importance = explainer.get_feature_importance()
```

**Responsabilités:**
- Initialiser SHAP TreeExplainer
- Calculer les valeurs SHAP
- Extraire les features les plus importantes
- Gérer les erreurs gracieusement

#### 4. `src/utils/validation.py` - Validation

```python
from src.utils.validation import DataValidator

# Initialiser le validateur
validator = DataValidator(expected_columns, max_rows=100_000)

# Valider un DataFrame
is_valid, errors = validator.validate_dataframe(dataframe)

# Valider une transaction
is_valid, errors = validator.validate_transaction(transaction)

# Nettoyer les données
clean_df = validator.sanitize_dataframe(dataframe)
```

**Responsabilités:**
- Vérifier la taille des fichiers
- Valider les colonnes requises
- Vérifier les types de données
- Nettoyer et normaliser les données

#### 5. `src/visualization/plots.py` - Visualisations

```python
from src.visualization.plots import FraudVisualizer

# Créer une jauge
fig = FraudVisualizer.create_gauge(value=0.073, title="Seuil")

# Créer un graphique de probabilité
fig = FraudVisualizer.create_probability_bar(proba, threshold)

# Créer un graphique SHAP
fig = FraudVisualizer.create_shap_bar(features)

# Créer un histogramme
fig = FraudVisualizer.create_histogram(probabilities, threshold)

# Créer un camembert des risques
fig = FraudVisualizer.create_risk_pie(risk_counts)
```

**Responsabilités:**
- Créer des graphiques Plotly cohérents
- Appliquer le style professionnel
- Gérer les couleurs et le branding

---

## 🧪 Tests

### Exécuter les Tests

```bash
# Tous les tests
pytest tests/ -v

# Tests avec couverture
pytest tests/ --cov=src --cov-report=html

# Tests d'un module spécifique
pytest tests/test_predictor.py -v

# Tests avec mode verbose
pytest tests/ -vv
```

### Écrire de Nouveaux Tests

```python
import pytest
from src.models.predictor import FraudPredictor

def test_my_feature():
    """Test ma nouvelle fonctionnalité."""
    # Arrange
    predictor = FraudPredictor(...)

    # Act
    result = predictor.my_method()

    # Assert
    assert result == expected_value
```

### Fixtures Pytest

```python
@pytest.fixture
def mock_pipeline():
    """Crée un pipeline mock pour les tests."""
    # Votre code ici
    return pipeline

def test_with_fixture(mock_pipeline):
    """Utilise la fixture."""
    predictor = FraudPredictor(mock_pipeline, ...)
    # Votre test
```

---

## 🔧 Développement

### Configuration de l'Environnement

```bash
# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

# Installer en mode développement
pip install -e .
pip install -r requirements.txt

# Installer les outils de qualité de code
pip install black isort flake8 pytest
```

### Formatage du Code

```bash
# Black - Formattage automatique
black src/ tests/ scripts/

# isort - Trier les imports
isort src/ tests/ scripts/

# flake8 - Linter
flake8 src/ tests/ scripts/
```

### Conventions de Code

**Style:**
- Suivre PEP 8
- Max 100 caractères par ligne (configuré dans `pyproject.toml`)
- Docstrings Google style

**Exemple de docstring:**
```python
def predict_single(self, transaction: dict) -> tuple[float, int]:
    """
    Prédit si une transaction unique est frauduleuse.

    Args:
        transaction: Dictionnaire contenant les features

    Returns:
        Tuple (probabilité, prédiction)

    Raises:
        ValueError: Si les colonnes requises sont manquantes
    """
    pass
```

---

## 📊 Pipeline ML

### Architecture du Pipeline

```
Données brutes (CSV)
    ↓
Séparation Train/Valid/Test (70/15/15)
    ↓
Preprocessing (StandardScaler sur Amount & Time)
    ↓
SMOTE (Rééquilibrage à 20%)
    ↓
RandomForest (100 arbres, max_depth=20)
    ↓
Optimisation du seuil (Recall >= 85%)
    ↓
Modèle final
```

### Hyperparamètres par Défaut

```python
SMOTE:
  - sampling_strategy: 0.2
  - k_neighbors: 5

RandomForest:
  - n_estimators: 100
  - max_depth: 20
  - min_samples_split: 10
  - random_state: 42
  - n_jobs: -1

Preprocessing:
  - StandardScaler sur [Amount, Time]
  - V1-V28 non transformées (déjà PCA)
```

---

## 🚀 Déploiement

### Option 1: Streamlit Cloud

```bash
# 1. Créer requirements.txt minimal
# 2. Push sur GitHub
# 3. Connecter à Streamlit Cloud
# 4. Déployer app/streamlit_app.py
```

### Option 2: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit_app.py"]
```

```bash
# Build
docker build -t fraud-detector .

# Run
docker run -p 8501:8501 fraud-detector
```

### Option 3: Serveur Local

```bash
# Avec gunicorn (pour production)
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# Avec Streamlit (développement)
streamlit run app/streamlit_app.py --server.port 8501
```

---

## 📈 Améliorer le Modèle

### 1. Ajouter de Nouvelles Features

```python
# Dans le pipeline
feature_engineering = FunctionTransformer(add_features)
pipeline = Pipeline([
    ('features', feature_engineering),
    ('prep', preprocessor),
    ('smote', SMOTE()),
    ('model', RandomForestClassifier())
])
```

### 2. Tester d'Autres Algorithmes

```python
from xgboost import XGBClassifier

# Remplacer RandomForest par XGBoost
model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    scale_pos_weight=(y_train==0).sum()/(y_train==1).sum()
)
```

### 3. Optimiser les Hyperparamètres

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'model__n_estimators': [50, 100, 200],
    'model__max_depth': [10, 20, 30],
    'smote__sampling_strategy': [0.1, 0.2, 0.3]
}

grid = GridSearchCV(pipeline, param_grid, cv=5, scoring='average_precision')
grid.fit(X_train, y_train)
```

---

## 🐛 Debugging

### Logs Streamlit

```python
import streamlit as st

# Activer le debug
st.set_option('client.showErrorDetails', True)

# Logger des messages
st.write("Debug:", variable)
```

### Profiling

```python
import cProfile
import pstats

# Profiler une fonction
profiler = cProfile.Profile()
profiler.enable()

# Votre code
result = my_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.print_stats()
```

---

## 📚 Ressources

- **Streamlit**: https://docs.streamlit.io/
- **Scikit-learn**: https://scikit-learn.org/
- **SHAP**: https://shap.readthedocs.io/
- **Imbalanced-learn**: https://imbalanced-learn.org/
- **Plotly**: https://plotly.com/python/

---

**Mainteneur**: Marie Chandeste Melvina J. H. Medetadji Migan
**Dernière mise à jour**: Novembre 2025
