# 📁 data/processed/

Ce dossier contient les **données prétraitées** générées par les notebooks.

## Fichiers générés automatiquement

Après exécution du notebook `notebooks/02_preparation.ipynb`, ce dossier contiendra :

### Ensembles d'entraînement, validation et test

```
X_train.csv          # Features d'entraînement (199 364 lignes)
y_train.csv          # Labels d'entraînement
X_valid.csv          # Features de validation (42 721 lignes)
y_valid.csv          # Labels de validation
X_test.csv           # Features de test (42 722 lignes)
y_test.csv           # Labels de test

X_train_scaled.csv   # (optionnel) Features normalisées
X_valid_scaled.csv
X_test_scaled.csv
```

## Comment générer ces fichiers

### Méthode 1 : Exécuter le notebook 02_preparation.ipynb

```bash
jupyter notebook notebooks/02_preparation.ipynb
# Exécutez toutes les cellules (Cell > Run All)
```

### Méthode 2 : Script Python (si disponible)

```bash
python scripts/prepare_data.py --input data/raw/creditcard.csv
```

## Split stratifié

- **Train :** 70% (~199k transactions, 344 fraudes)
- **Validation :** 15% (~43k transactions, 74 fraudes)
- **Test :** 15% (~43k transactions, 74 fraudes)

Le split est **stratifié** pour maintenir ~0.17% de fraudes dans chaque ensemble.

## Note

Ces fichiers ne sont **pas versionnés dans Git** (`.gitignore`) car :
- Générés automatiquement
- Taille importante (~100 MB au total)
- Dépendent des données brutes `data/raw/creditcard.csv`
