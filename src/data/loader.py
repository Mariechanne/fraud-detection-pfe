"""Module pour charger les artefacts du modèle de détection de fraude."""

import json
from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import pandas as pd


class ArtifactLoader:
    """Chargeur d'artefacts pour le modèle de détection de fraude."""

    def __init__(self, model_dir: Path):
        """
        Initialise le chargeur d'artefacts.

        Args:
            model_dir: Chemin vers le dossier contenant les artefacts du modèle
        """
        self.model_dir = Path(model_dir)
        self.pipe_path = self.model_dir / "pipeline.joblib"
        self.metrics_path = self.model_dir / "metrics_valid.json"
        self.cols_path = self.model_dir / "columns.json"

    def load_artifacts(self) -> Tuple[object, Dict, Dict, List[str]]:
        """
        Charge tous les artefacts nécessaires au modèle.

        Returns:
            Tuple contenant (pipeline, metrics, columns, warnings)

        Raises:
            FileNotFoundError: Si le fichier pipeline est manquant
        """
        errors = []
        warnings = []

        # Vérifier l'existence des fichiers critiques
        if not self.pipe_path.exists():
            errors.append(f"❌ Fichier modèle manquant: {self.pipe_path}")

        if not self.metrics_path.exists():
            warnings.append(f"⚠️ Fichier métriques manquant: {self.metrics_path}")

        if not self.cols_path.exists():
            warnings.append(f"⚠️ Fichier colonnes manquant: {self.cols_path}")

        if errors:
            raise FileNotFoundError("\n".join(errors))

        # Charger le pipeline
        pipeline = joblib.load(self.pipe_path)

        # Charger les métriques (avec fallback)
        if self.metrics_path.exists():
            with open(self.metrics_path, "r", encoding="utf-8") as f:
                metrics = json.load(f)
        else:
            metrics = {
                "pr_auc": 0.0,
                "roc_auc": 0.0,
                "recall": 0.0,
                "precision": 0.0,
                "threshold": 0.5,
            }
            warnings.append("📊 Métriques par défaut utilisées")

        # Charger les colonnes (avec fallback)
        if self.cols_path.exists():
            with open(self.cols_path, "r", encoding="utf-8") as f:
                columns = json.load(f)
        else:
            columns = {"all_cols": ["Amount", "Time"] + [f"V{i}" for i in range(1, 29)]}
            warnings.append("📋 Colonnes par défaut utilisées")

        # Vérifier la cohérence du pipeline
        try:
            test_df = pd.DataFrame(
                [[0.0] * len(columns.get("all_cols", []))],
                columns=columns.get("all_cols", []),
            )
            _ = pipeline.predict_proba(test_df)
        except Exception as e:
            warnings.append(f"⚠️ Divergence pipeline/colonnes détectée: {str(e)[:100]}")

        return pipeline, metrics, columns, warnings
