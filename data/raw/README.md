# 📁 data/raw/

Ce dossier contient les **données brutes** du projet.

## Données requises

### 1. Dataset Credit Card Fraud Detection

**Fichier attendu :** `creditcard.csv`

**Source :** [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

**Caractéristiques :**
- 284 807 transactions
- 31 colonnes (Time, V1-V28, Amount, Class)
- Taille : ~150 MB

## Comment obtenir les données

### Option 1 : Téléchargement manuel (recommandé)

1. Créez un compte Kaggle (gratuit)
2. Téléchargez le dataset : https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
3. Décompressez et placez `creditcard.csv` dans ce dossier

### Option 2 : Kaggle API (avancé)

```bash
# Installez la CLI Kaggle
pip install kaggle

# Configurez vos credentials Kaggle (voir https://www.kaggle.com/docs/api)
# Téléchargez le dataset
kaggle datasets download -d mlg-ulb/creditcardfraud -p data/raw/ --unzip
```

## Vérification

Une fois le fichier placé, vérifiez :

```bash
ls -lh data/raw/creditcard.csv
# Devrait afficher : creditcard.csv (~150 MB)
```

## Note

Ce fichier n'est **pas versionné dans Git** (`.gitignore`) en raison de sa taille.
