"""Module pour expliquer les prédictions avec SHAP."""

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import shap


class FraudExplainer:
    """Explique les prédictions du modèle de détection de fraude."""

    def __init__(self, pipeline):
        """
        Initialise l'explainer SHAP.

        Args:
            pipeline: Pipeline sklearn contenant le modèle
        """
        self.pipeline = pipeline
        self.model = pipeline.named_steps["model"]
        self.preprocessor = pipeline.named_steps["prep"]

        # Extraire les noms de features
        try:
            feat_out = self.preprocessor.get_feature_names_out()
            self.feature_names = [name.split("__")[-1] for name in feat_out]
        except Exception:
            self.feature_names = ["Amount", "Time"] + [f"V{i}" for i in range(1, 29)]

        # Créer l'explainer SHAP
        self.explainer = shap.TreeExplainer(self.model)

    def explain(
        self, data: pd.DataFrame, top_k: int = 5
    ) -> Tuple[List[Dict], Optional[str]]:
        """
        Explique les prédictions pour un ensemble de données.

        Args:
            data: DataFrame à expliquer
            top_k: Nombre de features les plus importantes à retourner

        Returns:
            Tuple (liste des features importantes, message d'erreur ou None)
        """
        try:
            # Transformer les données
            x_transformed = self.preprocessor.transform(data)
            if hasattr(x_transformed, "toarray"):
                x_transformed = x_transformed.toarray()
            else:
                x_transformed = np.asarray(x_transformed)

            # Calculer les valeurs SHAP
            shap_values = self.explainer.shap_values(x_transformed)

            # Gérer le format de sortie de SHAP
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # Classe positive

            shap_values = np.array(shap_values)

            # Gérer les dimensions
            if shap_values.ndim == 3:
                shap_values = shap_values.sum(axis=2)

            # Prendre la première ligne
            sv = shap_values[0]

            # Trier par importance absolue
            indices = np.argsort(np.abs(sv))[::-1][:top_k]

            # Créer la liste des features importantes
            important_features = []
            for idx in indices:
                important_features.append(
                    {
                        "feature": self.feature_names[int(idx)],
                        "value": float(x_transformed[0, int(idx)]),
                        "shap": float(sv[int(idx)]),
                        "direction": "↑ risque" if sv[int(idx)] > 0 else "↓ risque",
                    }
                )

            return important_features, None

        except Exception as e:
            return [], f"Erreur SHAP: {str(e)[:200]}"

    def get_feature_importance(self) -> Dict[str, float]:
        """
        Retourne l'importance globale des features.

        Returns:
            Dictionnaire {feature: importance}
        """
        try:
            if hasattr(self.model, "feature_importances_"):
                importances = self.model.feature_importances_
                return {
                    feature: float(importance)
                    for feature, importance in zip(self.feature_names, importances)
                }
        except Exception:
            pass
        return {}
