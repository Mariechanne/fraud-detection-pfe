#!/usr/bin/env python3
"""
Script d'entraînement du modèle de détection de fraude.
Basé sur le notebook 02_preparation.ipynb

Usage:
    python scripts/train_model.py --data data/raw/creditcard.csv
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_recall_curve,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score,
    average_precision_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(data_path: Path) -> pd.DataFrame:
    """Charge les données."""
    print(f"📂 Chargement des données depuis {data_path}...")
    df = pd.read_csv(data_path)
    print(f"✅ {len(df):,} transactions chargées")
    return df


def split_data(df: pd.DataFrame, test_size: float = 0.30, random_state: int = 42):
    """Sépare les données en train/valid/test (70/15/15)."""
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


def build_pipeline(smote_strategy: float = 0.2, random_state: int = 42, all_cols: list = None) -> ImbPipeline:
    """
    Construit le pipeline ML exactement comme dans le notebook.
    Pipeline: ColumnTransformer (scale Amount/Time) → SMOTE → RandomForest
    """
    print("\n🔧 Construction du pipeline...")

    scale_cols = ["Amount", "Time"]
    
    # ColumnTransformer : scale Amount/Time, le reste passe tel quel
    preprocessor = ColumnTransformer(
        transformers=[("scale_amt_time", StandardScaler(), scale_cols)],
        remainder="passthrough"
    )

    # Random Forest avec les mêmes paramètres que le notebook
    rf = RandomForestClassifier(
        n_estimators=300,
        n_jobs=-1,
        random_state=random_state
    )

    # Pipeline imblearn (supporte SMOTE)
    pipeline = ImbPipeline(steps=[
        ("prep", preprocessor),
        ("smote", SMOTE(sampling_strategy=smote_strategy, random_state=random_state, k_neighbors=5)),
        ("model", rf),
    ])

    print("✅ Pipeline créé: ColumnTransformer → SMOTE → RandomForest")
    return pipeline


def choose_threshold_by_precision_recall(y_true, y_proba, precision_min=0.20):
    """
    Choisit le seuil optimal basé sur Precision >= precision_min et Recall max.
    Code exactement du notebook (Cell 22).
    """
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_proba)
    
    # IMPORTANT: Aligner les tailles comme dans le notebook
    thresholds = np.append(thresholds, 1.0)
    
    mask = precisions >= precision_min

    if not np.any(mask):
        # Fallback: meilleur F1 si aucune config n'atteint la précision cible
        f1s = 2 * (precisions * recalls) / (precisions + recalls + 1e-12)
        idx = np.nanargmax(f1s)
        return float(thresholds[idx]), {
            "precision": float(precisions[idx]),
            "recall": float(recalls[idx]),
            "strategy": "best_f1_fallback"
        }

    recalls_masked = recalls.copy()
    recalls_masked[~mask] = -1
    idx = np.argmax(recalls_masked)
    
    return float(thresholds[idx]), {
        "precision": float(precisions[idx]),
        "recall": float(recalls[idx]),
        "strategy": "max_recall_at_precision>=0.20"
    }


def train_model(pipeline: ImbPipeline, X_train, y_train):
    """Entraîne le modèle."""
    print("\n🎯 Entraînement du modèle...")
    print("   Cela peut prendre 5-10 minutes... ☕")
    
    pipeline.fit(X_train, y_train)
    
    print("✅ Modèle entraîné")
    return pipeline


def evaluate_model(pipeline: ImbPipeline, X_valid, y_valid, precision_min: float = 0.20):
    """Évalue le modèle et trouve le seuil optimal."""
    print("\n📈 Évaluation sur l'ensemble de validation...")

    # Prédictions
    y_proba = pipeline.predict_proba(X_valid)[:, 1]

    # Trouver le seuil optimal
    best_thr, thr_info = choose_threshold_by_precision_recall(y_valid, y_proba, precision_min=precision_min)
    
    # Prédictions avec le seuil optimal
    y_pred = (y_proba >= best_thr).astype(int)

    # Matrice de confusion
    cm = confusion_matrix(y_valid, y_pred)
    tn, fp, fn, tp = cm.ravel()

    # Métriques
    metrics = {
        "threshold": float(best_thr),
        "threshold_selection": thr_info,
        "precision": float(precision_score(y_valid, y_pred, zero_division=0)),
        "recall": float(recall_score(y_valid, y_pred, zero_division=0)),
        "f1": float(f1_score(y_valid, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_valid, y_proba)),
        "pr_auc": float(average_precision_score(y_valid, y_proba)),
        "support_fraud": int(y_valid.sum()),
        "support_normal": int((1 - y_valid).sum()),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }

    print(f"\n📊 Métriques (seuil optimal = {best_thr:.4f}):")
    print(f"   ROC-AUC:    {metrics['roc_auc']:.4f}")
    print(f"   PR-AUC:     {metrics['pr_auc']:.4f}")
    print(f"   Precision:  {metrics['precision']:.4f} ({tp}/{tp+fp})")
    print(f"   Recall:     {metrics['recall']:.4f} ({tp}/{tp+fn})")
    print(f"   F1-Score:   {metrics['f1']:.4f}")
    print(f"\n🔢 Matrice de confusion:")
    print(f"   TN: {tn:,} | FP: {fp:,}")
    print(f"   FN: {fn:,} | TP: {tp:,}")
    print(f"\n💡 Stratégie de seuil: {thr_info['strategy']}")

    return metrics


def save_model(pipeline: ImbPipeline, metrics: dict, columns: list, output_dir: Path):
    """Sauvegarde le modèle et les artefacts (format du notebook)."""
    print(f"\n💾 Sauvegarde dans {output_dir}...")

    output_dir.mkdir(parents=True, exist_ok=True)

    # 1) Sauvegarder le pipeline
    joblib.dump(pipeline, output_dir / "pipeline.joblib")
    print("   ✅ pipeline.joblib")

    # 2) Sauvegarder les métriques
    with open(output_dir / "metrics_valid.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print("   ✅ metrics_valid.json")

    # 3) Info colonnes (comme dans le notebook)
    cols_info = {
        "scale_cols": ["Amount", "Time"],
        "all_cols": columns,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
    }
    with open(output_dir / "columns.json", "w", encoding="utf-8") as f:
        json.dump(cols_info, f, indent=2, ensure_ascii=False)
    print("   ✅ columns.json")

    print("\n✅ Modèle sauvegardé avec succès")


def save_processed_splits(X_train, X_valid, X_test, y_train, y_valid, y_test):
    """Sauvegarde les splits pour analyse ultérieure."""
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n💾 Sauvegarde des splits...")
    X_train.to_csv(processed_dir / "X_train.csv", index=False)
    X_valid.to_csv(processed_dir / "X_valid.csv", index=False)
    X_test.to_csv(processed_dir / "X_test.csv", index=False)
    
    y_train.to_csv(processed_dir / "y_train.csv", index=False)
    y_valid.to_csv(processed_dir / "y_valid.csv", index=False)
    y_test.to_csv(processed_dir / "y_test.csv", index=False)
    
    print("   ✅ Splits sauvegardés dans data/processed/")


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Entraîner le modèle de détection de fraude")
    parser.add_argument(
        "--data", type=str, required=True, help="Chemin vers creditcard.csv"
    )
    parser.add_argument(
        "--output", type=str, default="models/rf_smote_final", help="Dossier de sortie"
    )
    parser.add_argument(
        "--smote-strategy", type=float, default=0.2, help="Stratégie SMOTE (default: 0.2)"
    )
    parser.add_argument(
        "--precision-min", type=float, default=0.20, help="Precision minimale pour seuil (default: 0.20)"
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
        print(f"\n💡 Téléchargez le dataset depuis:")
        print(f"   https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud")
        sys.exit(1)

    print("=" * 70)
    print("🕵️  ENTRAÎNEMENT DU MODÈLE DE DÉTECTION DE FRAUDE")
    print("=" * 70)

    # Pipeline complet
    df = load_data(data_path)
    X_train, X_valid, X_test, y_train, y_valid, y_test = split_data(df, random_state=args.random_state)
    
    # Sauvegarder les splits
    save_processed_splits(X_train, X_valid, X_test, y_train, y_valid, y_test)
    
    # Construire et entraîner
    pipeline = build_pipeline(
        smote_strategy=args.smote_strategy, 
        random_state=args.random_state,
        all_cols=X_train.columns.tolist()
    )
    pipeline = train_model(pipeline, X_train, y_train)
    
    # Évaluer
    metrics = evaluate_model(pipeline, X_valid, y_valid, precision_min=args.precision_min)
    
    # Sauvegarder
    save_model(pipeline, metrics, X_train.columns.tolist(), output_dir)

    print("\n" + "=" * 70)
    print("✅ ENTRAÎNEMENT TERMINÉ AVEC SUCCÈS")
    print("=" * 70)
    print(f"\n📁 Modèle disponible dans: {output_dir}")
    print(f"🎯 Performances:")
    print(f"   - PR-AUC:    {metrics['pr_auc']:.4f}")
    print(f"   - ROC-AUC:   {metrics['roc_auc']:.4f}")
    print(f"   - Recall:    {metrics['recall']:.1%}")
    print(f"   - Precision: {metrics['precision']:.1%}")
    print(f"\n🚀 Pour lancer l'application:")
    print(f"   streamlit run app/streamlit_app.py")


if __name__ == "__main__":
    main()