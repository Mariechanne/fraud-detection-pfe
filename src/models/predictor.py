"""Module pour effectuer des prédictions de fraude."""

from typing import List, Tuple

import numpy as np
import pandas as pd


class FraudPredictor:
    """Prédicateur de fraude utilisant le pipeline ML."""

    def __init__(self, pipeline, expected_columns: List[str], threshold: float = 0.5):
        """
        Initialise le prédicateur.

        Args:
            pipeline: Pipeline sklearn entraîné
            expected_columns: Liste des colonnes attendues
            threshold: Seuil de décision pour la classification
        """
        self.pipeline = pipeline
        self.expected_columns = expected_columns
        self.threshold = threshold

    def ensure_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        S'assure que le DataFrame contient toutes les colonnes attendues.

        Args:
            data: DataFrame à valider

        Returns:
            DataFrame avec toutes les colonnes requises
        """
        df = data.copy()
        for col in self.expected_columns:
            if col not in df.columns:
                df[col] = 0.0
        return df[self.expected_columns].fillna(0.0)

    def predict_single(
        self, transaction: dict, threshold: float = None
    ) -> Tuple[float, int]:
        """
        Prédit si une transaction unique est frauduleuse.

        Args:
            transaction: Dictionnaire contenant les features de la transaction
            threshold: Seuil de décision (optionnel, utilise self.threshold par défaut)

        Returns:
            Tuple (probabilité, prédiction)
        """
        df = pd.DataFrame([transaction])
        df = self.ensure_columns(df)
        proba, pred = self.predict(df, threshold)
        return float(proba[0]), int(pred[0])

    def predict(
        self, data: pd.DataFrame, threshold: float = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prédit sur un ensemble de transactions.

        Args:
            data: DataFrame contenant les transactions
            threshold: Seuil de décision (optionnel)

        Returns:
            Tuple (probabilités, prédictions)
        """
        thr = self.threshold if threshold is None else threshold
        df = self.ensure_columns(data)

        # Prédire les probabilités
        probabilities = self.pipeline.predict_proba(df)[:, 1]

        # Appliquer le seuil
        predictions = (probabilities >= thr).astype(int)

        return probabilities, predictions

    def predict_batch(
        self, data: pd.DataFrame, chunk_size: int = 5000, threshold: float = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prédit sur un grand ensemble de transactions par chunks.

        Args:
            data: DataFrame contenant les transactions
            chunk_size: Taille des chunks pour le traitement par batch
            threshold: Seuil de décision (optionnel)

        Returns:
            Tuple (probabilités, prédictions)
        """
        n_rows = len(data)

        if n_rows <= chunk_size:
            return self.predict(data, threshold)

        all_proba = []
        all_pred = []

        for i in range(0, n_rows, chunk_size):
            chunk = data.iloc[i : i + chunk_size]
            chunk_proba, chunk_pred = self.predict(chunk, threshold)
            all_proba.extend(chunk_proba)
            all_pred.extend(chunk_pred)

        return np.array(all_proba), np.array(all_pred)

    def get_risk_level(self, probability: float) -> str:
        """
        Détermine le niveau de risque basé sur la probabilité.

        Args:
            probability: Probabilité de fraude

        Returns:
            Niveau de risque (FAIBLE, MODÉRÉ, ÉLEVÉ, CRITIQUE)
        """
        if probability >= 0.8:
            return "CRITIQUE"
        elif probability >= 0.5:
            return "ÉLEVÉ"
        elif probability >= 0.3:
            return "MODÉRÉ"
        else:
            return "FAIBLE"
