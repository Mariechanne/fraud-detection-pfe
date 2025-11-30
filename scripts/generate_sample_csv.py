#!/usr/bin/env python3
"""
Script pour générer des fichiers CSV d'exemple à partir du test set.
Utile pour tester la fonctionnalité "Analyse par Lot" de l'application Streamlit.

Usage:
    python scripts/generate_sample_csv.py
"""

import sys
from pathlib import Path

import pandas as pd

# Ajouter le projet au PYTHONPATH
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def generate_sample_files():
    """Génère des fichiers CSV d'exemple de différentes tailles."""

    # Chemins
    test_x_path = ROOT / "data" / "processed" / "X_test.csv"
    test_y_path = ROOT / "data" / "processed" / "y_test.csv"
    examples_dir = ROOT / "data" / "examples"
    examples_dir.mkdir(parents=True, exist_ok=True)

    # Vérifier l'existence des fichiers
    if not test_x_path.exists():
        print(f"❌ Erreur: {test_x_path} n'existe pas")
        print("💡 Entraînez d'abord le modèle: python scripts/train_model.py --data data/raw/creditcard.csv")
        return

    if not test_y_path.exists():
        print(f"❌ Erreur: {test_y_path} n'existe pas")
        return

    print("📂 Chargement du test set...")
    X_test = pd.read_csv(test_x_path)
    y_test = pd.read_csv(test_y_path).squeeze()

    # Fusionner X et y pour faciliter l'échantillonnage stratifié
    test_data = X_test.copy()
    test_data["Class"] = y_test.values

    # Calculer les proportions
    n_total = len(test_data)
    n_frauds = int((test_data["Class"] == 1).sum())
    n_normals = n_total - n_frauds
    fraud_ratio = n_frauds / n_total

    print(f"✅ {n_total:,} transactions chargées")
    print(f"   - Fraudes: {n_frauds} ({fraud_ratio*100:.2f}%)")
    print(f"   - Normales: {n_normals} ({(1-fraud_ratio)*100:.2f}%)")
    print()

    # Définir les tailles de fichiers
    sizes = [
        ("sample_transactions_small.csv", 100, "Petit fichier pour tests rapides"),
        ("sample_transactions_medium.csv", 1000, "Fichier moyen pour démos"),
        ("sample_transactions_large.csv", 5000, "Fichier volumineux pour tester le batch processing"),
    ]

    # Générer les fichiers
    for filename, size, description in sizes:
        print(f"📝 Génération de {filename} ({size} lignes)...")

        # Échantillonnage stratifié pour garder la proportion fraudes/normales
        if size >= n_total:
            sample = test_data.sample(n=n_total, random_state=42)
            print(f"   ⚠️ Demande de {size} lignes mais seulement {n_total} disponibles")
        else:
            # Calculer combien de fraudes et normales inclure
            n_sample_frauds = max(1, int(size * fraud_ratio))
            n_sample_normals = size - n_sample_frauds

            # Échantillonner
            frauds = test_data[test_data["Class"] == 1].sample(
                n=min(n_sample_frauds, n_frauds), random_state=42
            )
            normals = test_data[test_data["Class"] == 0].sample(
                n=min(n_sample_normals, n_normals), random_state=42
            )

            # Combiner et mélanger
            sample = pd.concat([frauds, normals], ignore_index=True)
            sample = sample.sample(frac=1, random_state=42).reset_index(drop=True)

        # Retirer la colonne Class (on veut tester la prédiction, pas fournir la réponse)
        sample_x = sample.drop("Class", axis=1)

        # Sauvegarder
        output_path = examples_dir / filename
        sample_x.to_csv(output_path, index=False)

        # Stats du fichier
        actual_frauds = int((sample["Class"] == 1).sum())
        actual_normals = len(sample) - actual_frauds

        print(f"   ✅ {output_path}")
        print(f"   📊 {len(sample):,} transactions ({actual_frauds} fraudes, {actual_normals} normales)")
        print(f"   💡 {description}")
        print()

    # Créer un README dans examples/
    readme_content = """# Fichiers d'Exemple pour Tests

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
"""

    readme_path = examples_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"📄 {readme_path}")
    print()

    print("=" * 70)
    print("✅ GÉNÉRATION TERMINÉE AVEC SUCCÈS")
    print("=" * 70)
    print(f"\n📁 Fichiers créés dans: {examples_dir}")
    print("\n🚀 Pour tester dans l'application:")
    print("   1. Lancer: streamlit run app/streamlit_app.py")
    print("   2. Section: 📁 Analyse par Lot (CSV)")
    print("   3. Uploader: data/examples/sample_transactions_small.csv")
    print()


if __name__ == "__main__":
    generate_sample_files()