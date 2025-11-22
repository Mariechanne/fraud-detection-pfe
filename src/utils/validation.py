"""Module pour valider les données d'entrée."""

from typing import List, Tuple

import pandas as pd


class DataValidator:
    """Valide les données d'entrée pour le modèle de fraude."""

    def __init__(self, expected_columns: List[str], max_rows: int = 100_000):
        """
        Initialise le validateur.

        Args:
            expected_columns: Liste des colonnes attendues
            max_rows: Nombre maximum de lignes autorisées
        """
        self.expected_columns = expected_columns
        self.max_rows = max_rows

    def validate_dataframe(self, data: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Valide un DataFrame.

        Args:
            data: DataFrame à valider

        Returns:
            Tuple (is_valid, liste d'erreurs)
        """
        errors = []

        # Vérifier le nombre de lignes
        if len(data) > self.max_rows:
            errors.append(
                f"Fichier trop volumineux: {len(data):,} lignes. "
                f"Maximum autorisé: {self.max_rows:,} lignes."
            )

        # Vérifier que le DataFrame n'est pas vide
        if len(data) == 0:
            errors.append("Le fichier est vide.")

        # Vérifier les colonnes manquantes critiques
        critical_cols = ["Amount", "Time"]
        missing_critical = [col for col in critical_cols if col not in data.columns]
        if missing_critical:
            errors.append(f"Colonnes critiques manquantes: {', '.join(missing_critical)}")

        # Vérifier les valeurs manquantes
        null_counts = data[data.columns.intersection(critical_cols)].isnull().sum()
        if null_counts.sum() > 0:
            null_info = null_counts[null_counts > 0].to_dict()
            errors.append(f"Valeurs manquantes détectées: {null_info}")

        # Vérifier les types de données
        numeric_cols = data.columns.intersection(self.expected_columns)
        non_numeric = []
        for col in numeric_cols:
            if not pd.api.types.is_numeric_dtype(data[col]):
                non_numeric.append(col)

        if non_numeric:
            errors.append(f"Colonnes non-numériques: {', '.join(non_numeric)}")

        return len(errors) == 0, errors

    def validate_transaction(self, transaction: dict) -> Tuple[bool, List[str]]:
        """
        Valide une transaction unique.

        Args:
            transaction: Dictionnaire représentant une transaction

        Returns:
            Tuple (is_valid, liste d'erreurs)
        """
        errors = []

        # Vérifier les champs critiques
        if "Amount" not in transaction:
            errors.append("Le champ 'Amount' est manquant.")
        elif not isinstance(transaction["Amount"], (int, float)):
            errors.append("Le champ 'Amount' doit être numérique.")
        elif transaction["Amount"] < 0:
            errors.append("Le montant ne peut pas être négatif.")

        if "Time" not in transaction:
            errors.append("Le champ 'Time' est manquant.")
        elif not isinstance(transaction["Time"], (int, float)):
            errors.append("Le champ 'Time' doit être numérique.")

        return len(errors) == 0, errors

    def sanitize_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoie et prépare un DataFrame pour l'inférence.

        Args:
            data: DataFrame brut

        Returns:
            DataFrame nettoyé
        """
        df = data.copy()

        # Ajouter les colonnes manquantes avec 0.0
        for col in self.expected_columns:
            if col not in df.columns:
                df[col] = 0.0

        # Remplacer les valeurs manquantes
        df = df[self.expected_columns].fillna(0.0)

        # Convertir en float
        for col in self.expected_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

        return df
