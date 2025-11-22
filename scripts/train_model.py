#!/usr/bin/env python3
"""
Script d'entraînement du modèle de détection de fraude.

Usage:
    python scripts/train_model.py --data data/raw/creditcard.csv --output models/my_model
"""

import argparse
import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    auc,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def load_data(data_path: Path) -> pd.DataFrame:
    """Charge les données."""
    print(f"📂 Chargement des données depuis {data_path}...")
    df = pd.read_csv(data_path)
    print(f"✅ {len(df):,} transactions chargées")
    return df


def split_data(df: pd.DataFrame, test_size: float = 0.3, random_state: int = 42):
    """Sépare les données en train/valid/test."""
    print("\n📊 Séparation des données...")

    # Séparer features et cible
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Train/temp split (70/30)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Valid/Test split (15/15)
    X_valid, X_test, y_valid, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=random_state, stratify=y_temp
    )

    print(f"   Train: {len(X_train):,} | Valid: {len(X_valid):,} | Test: {len(X_test):,}")
    print(f"   Fraudes - Train: {y_train.sum()} | Valid: {y_valid.sum()} | Test: {y_test.sum()}")

    return X_train, X_valid, X_test, y_train, y_valid, y_test


def build_pipeline(smote_strategy: float = 0.2, random_state: int = 42) -> Pipeline:
    """Construit le pipeline ML."""
    print("\n🔧 Construction du pipeline...")

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[("scaler", StandardScaler(), ["Amount", "Time"])],
        remainder="passthrough",
    )

    # Pipeline
    pipeline = Pipeline(
        [
            ("prep", preprocessor),
            ("smote", SMOTE(sampling_strategy=smote_strategy, random_state=random_state)),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=100,
                    max_depth=20,
                    min_samples_split=10,
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print("✅ Pipeline créé: StandardScaler → SMOTE → RandomForest")
    return pipeline


def train_model(pipeline: Pipeline, X_train, y_train):
    """Entraîne le modèle."""
    print("\n🎯 Entraînement du modèle...")
    pipeline.fit(X_train, y_train)
    print("✅ Modèle entraîné")
    return pipeline


def evaluate_model(pipeline: Pipeline, X_valid, y_valid):
    """Évalue le modèle et trouve le seuil optimal."""
    print("\n📈 Évaluation sur l'ensemble de validation...")

    # Prédictions
    y_proba = pipeline.predict_proba(X_valid)[:, 1]

    # ROC-AUC
    roc_auc = roc_auc_score(y_valid, y_proba)

    # Precision-Recall curve
    precision, recall, thresholds = precision_recall_curve(y_valid, y_proba)
    pr_auc = auc(recall, precision)

    # Trouver le seuil optimal (Recall >= 85%, max Precision)
    target_recall = 0.85
    valid_indices = recall >= target_recall
    if valid_indices.any():
        best_idx = np.argmax(precision[valid_indices])
        optimal_threshold = thresholds[valid_indices][best_idx]
        optimal_precision = precision[valid_indices][best_idx]
        optimal_recall = recall[valid_indices][best_idx]
    else:
        optimal_threshold = 0.5
        optimal_precision = precision_score(y_valid, y_proba >= 0.5)
        optimal_recall = recall_score(y_valid, y_proba >= 0.5)

    metrics = {
        "roc_auc": float(roc_auc),
        "pr_auc": float(pr_auc),
        "threshold": float(optimal_threshold),
        "precision": float(optimal_precision),
        "recall": float(optimal_recall),
    }

    print(f"   ROC-AUC: {roc_auc:.4f}")
    print(f"   PR-AUC: {pr_auc:.4f}")
    print(f"   Seuil optimal: {optimal_threshold:.4f}")
    print(f"   Precision: {optimal_precision:.4f}")
    print(f"   Recall: {optimal_recall:.4f}")

    return metrics


def save_model(pipeline: Pipeline, metrics: dict, columns: list, output_dir: Path):
    """Sauvegarde le modèle et les artefacts."""
    print(f"\n💾 Sauvegarde dans {output_dir}...")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Sauvegarder le pipeline
    joblib.dump(pipeline, output_dir / "pipeline.joblib")

    # Sauvegarder les métriques
    with open(output_dir / "metrics_valid.json", "w") as f:
        json.dump(metrics, f, indent=2)

    # Sauvegarder les colonnes
    with open(output_dir / "columns.json", "w") as f:
        json.dump({"all_cols": columns}, f, indent=2)

    print("✅ Modèle sauvegardé avec succès")


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Entraîner le modèle de détection de fraude")
    parser.add_argument(
        "--data", type=str, required=True, help="Chemin vers les données CSV"
    )
    parser.add_argument(
        "--output", type=str, default="models/rf_smote_final", help="Dossier de sortie"
    )
    parser.add_argument(
        "--smote-strategy", type=float, default=0.2, help="Stratégie SMOTE (default: 0.2)"
    )
    parser.add_argument(
        "--random-state", type=int, default=42, help="Random state (default: 42)"
    )

    args = parser.parse_args()

    # Chemins
    data_path = Path(args.data)
    output_dir = Path(args.output)

    if not data_path.exists():
        print(f"❌ Erreur: {data_path} n'existe pas")
        sys.exit(1)

    print("=" * 70)
    print("🕵️  ENTRAÎNEMENT DU MODÈLE DE DÉTECTION DE FRAUDE")
    print("=" * 70)

    # Pipeline complet
    df = load_data(data_path)
    X_train, X_valid, X_test, y_train, y_valid, y_test = split_data(df)
    pipeline = build_pipeline(smote_strategy=args.smote_strategy, random_state=args.random_state)
    pipeline = train_model(pipeline, X_train, y_train)
    metrics = evaluate_model(pipeline, X_valid, y_valid)
    save_model(pipeline, metrics, list(X_train.columns), output_dir)

    print("\n" + "=" * 70)
    print("✅ ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS")
    print("=" * 70)
    print(f"\n📁 Modèle disponible dans: {output_dir}")
    print(f"🎯 PR-AUC: {metrics['pr_auc']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f}")


if __name__ == "__main__":
    main()
