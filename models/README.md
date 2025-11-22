# 📁 models/

Ce dossier contient les **modèles entraînés** et leurs artefacts.

## Structure attendue

```
models/
└── rf_smote_final/              # Modèle Random Forest final
    ├── pipeline.joblib          # Pipeline scikit-learn complet
    ├── metrics_valid.json       # Métriques sur validation set
    └── columns.json             # Métadonnées des colonnes
```

## Modèle final : `rf_smote_final`

**Architecture :**
- **Preprocessing :** StandardScaler sur Amount/Time
- **Resampling :** SMOTE (sampling_strategy=0.2)
- **Modèle :** Random Forest (300 arbres, n_jobs=-1)

**Performances (validation set) :**
- **ROC-AUC :** 0.9729
- **PR-AUC :** 0.8326
- **Recall :** 87.8% (détecte 65/74 fraudes)
- **Precision :** 21.1% (1 alerte sur 5 est vraie fraude)
- **Seuil optimal :** 0.0733

## Comment générer le modèle

### Méthode 1 : Exécuter le notebook 02_preparation.ipynb

Le notebook entraîne et sauvegarde automatiquement le modèle final.

```bash
jupyter notebook notebooks/02_preparation.ipynb
# Exécutez toutes les cellules jusqu'à la section "6.6 Sauvegarde du modèle"
```

### Méthode 2 : Script d'entraînement

```bash
python scripts/train_model.py \
  --data data/raw/creditcard.csv \
  --output models/rf_smote_final \
  --smote-strategy 0.2
```

## Charger le modèle

### En Python

```python
import joblib
import json

# Charger le pipeline
pipe = joblib.load("models/rf_smote_final/pipeline.joblib")

# Charger les métriques
with open("models/rf_smote_final/metrics_valid.json", "r") as f:
    metrics = json.load(f)
    threshold = metrics["threshold"]  # 0.0733

# Prédiction
proba = pipe.predict_proba(X)[:, 1]
pred = (proba >= threshold).astype(int)
```

### Dans l'application Streamlit

L'app charge automatiquement depuis `models/rf_smote_final/` au démarrage.

## Taille des fichiers

- `pipeline.joblib` : ~50-100 MB (contient le RandomForest entraîné)
- `metrics_valid.json` : ~1 KB
- `columns.json` : ~1 KB

## Note

Ces fichiers ne sont **pas versionnés dans Git** (`.gitignore`) en raison de leur taille.

**Pour partager le modèle :**
- **Option 1 :** GitHub Releases (upload manuel)
- **Option 2 :** Google Drive / Dropbox (lien public)
- **Option 3 :** Réentraîner localement (5-10 min)
