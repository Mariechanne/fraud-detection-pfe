"""Tests pour le module predictor."""

import numpy as np
import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.models.predictor import FraudPredictor


@pytest.fixture
def mock_pipeline():
    """Crée un pipeline simple pour les tests."""
    # Créer un pipeline basique
    pipeline = Pipeline(
        [
            ("prep", StandardScaler()),
            ("model", RandomForestClassifier(n_estimators=10, random_state=42)),
        ]
    )

    # Entraîner sur des données fictives
    X = np.random.rand(100, 30)
    y = np.random.randint(0, 2, 100)
    pipeline.fit(X, y)

    return pipeline


@pytest.fixture
def predictor(mock_pipeline):
    """Crée un FraudPredictor pour les tests."""
    expected_cols = ["Amount", "Time"] + [f"V{i}" for i in range(1, 29)]
    return FraudPredictor(mock_pipeline, expected_cols, threshold=0.5)


def test_predictor_initialization(predictor):
    """Test l'initialisation du prédicateur."""
    assert predictor.threshold == 0.5
    assert len(predictor.expected_columns) == 30


def test_ensure_columns(predictor):
    """Test que les colonnes manquantes sont ajoutées."""
    # DataFrame partiel
    df = pd.DataFrame({"Amount": [100], "Time": [500]})

    # Assurer les colonnes
    result = predictor.ensure_columns(df)

    # Vérifier que toutes les colonnes sont présentes
    assert len(result.columns) == 30
    assert "V1" in result.columns
    assert result["V1"].iloc[0] == 0.0


def test_predict_single(predictor):
    """Test la prédiction sur une transaction unique."""
    transaction = {"Amount": 100.0, "Time": 500.0}

    proba, pred = predictor.predict_single(transaction)

    # Vérifier les types et valeurs
    assert isinstance(proba, float)
    assert isinstance(pred, int)
    assert 0 <= proba <= 1
    assert pred in [0, 1]


def test_predict_batch(predictor):
    """Test la prédiction sur un DataFrame."""
    df = pd.DataFrame(
        {"Amount": [100, 200, 300], "Time": [500, 600, 700]}
    )

    probas, preds = predictor.predict(df)

    # Vérifier les dimensions
    assert len(probas) == 3
    assert len(preds) == 3

    # Vérifier les valeurs
    assert all(0 <= p <= 1 for p in probas)
    assert all(p in [0, 1] for p in preds)


def test_predict_batch_chunked(predictor):
    """Test la prédiction par chunks."""
    # Créer un grand DataFrame
    df = pd.DataFrame(
        {"Amount": np.random.rand(10), "Time": np.random.rand(10)}
    )

    probas, preds = predictor.predict_batch(df, chunk_size=3)

    # Vérifier les dimensions
    assert len(probas) == 10
    assert len(preds) == 10


def test_get_risk_level(predictor):
    """Test la classification du niveau de risque."""
    assert predictor.get_risk_level(0.9) == "CRITIQUE"
    assert predictor.get_risk_level(0.6) == "ÉLEVÉ"
    assert predictor.get_risk_level(0.4) == "MODÉRÉ"
    assert predictor.get_risk_level(0.1) == "FAIBLE"


def test_custom_threshold(predictor):
    """Test l'utilisation d'un seuil personnalisé."""
    transaction = {"Amount": 100.0, "Time": 500.0}

    # Tester avec différents seuils
    proba1, pred1 = predictor.predict_single(transaction, threshold=0.1)
    proba2, pred2 = predictor.predict_single(transaction, threshold=0.9)

    # Les probabilités doivent être identiques
    assert proba1 == proba2

    # Mais les prédictions peuvent différer selon le seuil
    assert isinstance(pred1, int)
    assert isinstance(pred2, int)
