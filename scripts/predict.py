#!/usr/bin/env python3
"""
Script de prédiction pour le modèle de détection de fraude.

Usage:
    # Prédire sur un fichier CSV
    python scripts/predict.py --input data/test.csv --model models/rf_smote_final

    # Prédire une transaction unique
    python scripts/predict.py --model models/rf_smote_final --amount 100.5 --time 3600
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

# Ajouter le dossier parent au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.loader import ArtifactLoader
from src.models.predictor import FraudPredictor


def main():
    """Fonction principale."""
    parser = argparse.ArgumentParser(description="Prédire les fraudes sur de nouvelles transactions")
    parser.add_argument(
        "--model", type=str, required=True, help="Dossier contenant le modèle"
    )
    parser.add_argument(
        "--input", type=str, help="Fichier CSV contenant les transactions"
    )
    parser.add_argument(
        "--output", type=str, help="Fichier de sortie pour les prédictions"
    )
    parser.add_argument("--amount", type=float, help="Montant de la transaction unique")
    parser.add_argument("--time", type=float, help="Temps de la transaction unique")
    parser.add_argument(
        "--threshold", type=float, help="Seuil de décision personnalisé"
    )

    args = parser.parse_args()

    # Charger les artefacts
    print(f"📂 Chargement du modèle depuis {args.model}...")
    loader = ArtifactLoader(Path(args.model))

    try:
        pipeline, metrics, columns, warnings = loader.load_artifacts()

        # Afficher les warnings
        for warning in warnings:
            print(f"   {warning}")

        if not warnings:
            print("✅ Modèle chargé avec succès")

    except FileNotFoundError as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

    # Créer le prédicateur
    threshold = args.threshold if args.threshold else metrics.get("threshold", 0.5)
    predictor = FraudPredictor(pipeline, columns["all_cols"], threshold)

    print(f"🎯 Seuil de décision: {threshold:.4f}")
    print()

    # Prédiction sur fichier ou transaction unique
    if args.input:
        # Prédiction sur fichier CSV
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ Erreur: {input_path} n'existe pas")
            sys.exit(1)

        print(f"📊 Prédiction sur {input_path}...")
        df = pd.read_csv(input_path)
        print(f"   {len(df):,} transactions à analyser")

        # Prédire
        probas, preds = predictor.predict_batch(df)

        # Ajouter les résultats
        df["fraud_proba"] = probas
        df["fraud_pred"] = preds
        df["risk_level"] = [predictor.get_risk_level(p) for p in probas]

        # Résumé
        n_fraudes = preds.sum()
        print(f"\n📈 Résultats:")
        print(f"   Total: {len(df):,} transactions")
        print(f"   Fraudes détectées: {n_fraudes} ({n_fraudes/len(df)*100:.2f}%)")
        print(f"   Probabilité moyenne: {probas.mean():.4f}")

        # Sauvegarder
        if args.output:
            output_path = Path(args.output)
            df.to_csv(output_path, index=False)
            print(f"\n💾 Résultats sauvegardés dans {output_path}")
        else:
            print("\n📋 Aperçu des résultats:")
            print(df.head(10))

    elif args.amount is not None and args.time is not None:
        # Prédiction sur transaction unique
        transaction = {"Amount": args.amount, "Time": args.time}

        print(f"💳 Analyse de la transaction:")
        print(f"   Montant: {args.amount:.2f}€")
        print(f"   Temps: {args.time:.0f}s")

        proba, pred = predictor.predict_single(transaction, threshold)
        risk = predictor.get_risk_level(proba)

        print(f"\n📊 Résultat:")
        print(f"   Probabilité de fraude: {proba*100:.2f}%")
        print(f"   Prédiction: {'🚨 FRAUDE' if pred == 1 else '✅ NORMALE'}")
        print(f"   Niveau de risque: {risk}")

    else:
        print("❌ Erreur: Spécifiez --input ou (--amount et --time)")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
