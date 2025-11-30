# Fichiers d'Exemple pour Tests

Ce dossier contient des fichiers CSV d'exemple générés à partir du test set.
Ils permettent de tester la fonctionnalité "Analyse par Lot (CSV)" de l'application Streamlit.

## Fichiers Disponibles

### `sample_transactions_small.csv` (100 lignes)
- **Usage** : Tests rapides, démos courtes
- **Contenu** : Échantillon stratifié du test set
- **Temps traitement** : < 1 seconde

### `sample_transactions_medium.csv` (1,000 lignes)
- **Usage** : Démonstrations standards, présentations
- **Contenu** : Échantillon représentatif avec fraudes et transactions normales
- **Temps traitement** : 1-2 secondes

### `sample_transactions_large.csv` (5,000 lignes)
- **Usage** : Test du batch processing, démo performance
- **Contenu** : Grand échantillon pour tester la scalabilité
- **Temps traitement** : 3-5 secondes (traitement par chunks de 5000)

## Génération

Ces fichiers sont générés automatiquement avec :

```bash
python scripts/generate_sample_csv.py
```

**Prérequis** : Le modèle doit être entraîné (fichiers `data/processed/X_test.csv` et `y_test.csv` doivent exister).

## Format

Tous les fichiers contiennent les colonnes suivantes :
- `Amount` : Montant de la transaction (€)
- `Time` : Temps écoulé depuis la première transaction (secondes)
- `V1` à `V28` : Variables PCA pour confidentialité

**Note** : La colonne `Class` (fraude/normale) est **volontairement absente** pour tester la prédiction du modèle.

## Utilisation dans l'App Streamlit

1. Lancer l'application : `streamlit run app/streamlit_app.py`
2. Descendre à la section "📁 Analyse par Lot (CSV)"
3. Uploader l'un des fichiers d'exemple
4. Observer les résultats : détections, visualisations, export

## Régénération

Pour régénérer les fichiers avec de nouveaux échantillons :

```bash
rm data/examples/sample_*.csv
python scripts/generate_sample_csv.py
```
