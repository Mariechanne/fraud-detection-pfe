# 📁 data/examples/

Ce dossier contient des **exemples de données** pour tester l'application sans le dataset complet.

## Fichiers

### `sample_transactions.csv`

Petit échantillon de 5 transactions du dataset original, utilisable pour :
- Tester l'interface Streamlit (upload CSV)
- Démontrer les prédictions batch
- Vérifier que l'application fonctionne

**Format :** Identique au dataset complet (30 colonnes : Time, V1-V28, Amount)

**Utilisation :**

```bash
# Dans l'application Streamlit
# 1. Lancez l'app : streamlit run app/streamlit_app.py
# 2. Section "Analyse par Lot (CSV)"
# 3. Uploadez : data/examples/sample_transactions.csv

# Ou en ligne de commande
python scripts/predict.py \
  --model models/rf_smote_final \
  --file data/examples/sample_transactions.csv \
  --output predictions.csv
```

## Créer vos propres exemples

Si vous avez accès au dataset complet :

```python
import pandas as pd

# Charger le dataset
df = pd.read_csv("data/raw/creditcard.csv")

# Extraire un échantillon
sample = df.sample(n=10, random_state=42)

# Retirer la colonne Class pour tester les prédictions
X_sample = sample.drop(columns=["Class"])
X_sample.to_csv("data/examples/my_sample.csv", index=False)
```

## Note

Ces fichiers d'exemple **peuvent être versionnés dans Git** car ils sont petits (<1 KB).
