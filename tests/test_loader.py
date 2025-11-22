"""Tests pour le module loader."""

import json
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import joblib
import pytest

from src.data.loader import ArtifactLoader


@pytest.fixture
def temp_model_dir(tmp_path):
    """Crée un dossier temporaire pour les tests."""
    model_dir = tmp_path / "test_model"
    model_dir.mkdir()
    return model_dir


def test_loader_initialization(temp_model_dir):
    """Test l'initialisation du loader."""
    loader = ArtifactLoader(temp_model_dir)

    assert loader.model_dir == temp_model_dir
    assert loader.pipe_path == temp_model_dir / "pipeline.joblib"
    assert loader.metrics_path == temp_model_dir / "metrics_valid.json"
    assert loader.cols_path == temp_model_dir / "columns.json"


def test_load_artifacts_missing_pipeline(temp_model_dir):
    """Test que le loader lève une erreur si le pipeline est manquant."""
    loader = ArtifactLoader(temp_model_dir)

    with pytest.raises(FileNotFoundError):
        loader.load_artifacts()


def test_load_artifacts_with_fallbacks(temp_model_dir):
    """Test le chargement avec les valeurs par défaut."""
    # Créer un mock pipeline
    mock_pipeline = Mock()
    mock_pipeline.predict_proba = Mock(return_value=[[0.3, 0.7]])

    # Sauvegarder le pipeline
    pipe_path = temp_model_dir / "pipeline.joblib"
    joblib.dump(mock_pipeline, pipe_path)

    loader = ArtifactLoader(temp_model_dir)
    pipeline, metrics, columns, warnings = loader.load_artifacts()

    # Vérifier que le pipeline est chargé
    assert pipeline is not None

    # Vérifier les fallbacks
    assert metrics["threshold"] == 0.5
    assert "all_cols" in columns

    # Vérifier les warnings
    assert len(warnings) >= 2  # Métriques et colonnes manquantes


def test_load_artifacts_complete(temp_model_dir):
    """Test le chargement complet avec tous les fichiers."""
    # Créer un mock pipeline
    mock_pipeline = Mock()
    mock_pipeline.predict_proba = Mock(return_value=[[0.3, 0.7]])

    # Sauvegarder les artefacts
    pipe_path = temp_model_dir / "pipeline.joblib"
    metrics_path = temp_model_dir / "metrics_valid.json"
    cols_path = temp_model_dir / "columns.json"

    joblib.dump(mock_pipeline, pipe_path)

    with open(metrics_path, "w") as f:
        json.dump({"pr_auc": 0.9, "threshold": 0.7}, f)

    with open(cols_path, "w") as f:
        json.dump({"all_cols": ["Amount", "Time", "V1"]}, f)

    loader = ArtifactLoader(temp_model_dir)
    pipeline, metrics, columns, warnings = loader.load_artifacts()

    # Vérifier le chargement
    assert metrics["pr_auc"] == 0.9
    assert metrics["threshold"] == 0.7
    assert len(columns["all_cols"]) == 3

    # Pas de warnings si tout est présent
    assert len(warnings) == 0
