"""Tests pour le module loader."""

import json
from pathlib import Path
import numpy as np
import joblib
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from imblearn.pipeline import Pipeline as ImbPipeline

from src.data.loader import ArtifactLoader


@pytest.fixture
def temp_model_dir(tmp_path):
    """Crée un dossier temporaire pour les tests."""
    model_dir = tmp_path / "test_model"
    model_dir.mkdir()
    return model_dir


def create_simple_pipeline():
    """Crée un pipeline simple réel pour les tests (au lieu d'un Mock)."""
    # Pipeline simple qui peut être sérialisé avec joblib
    pipeline = ImbPipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=10, random_state=42))
    ])
    
    # Entraîner avec des données fictives minimales
    X_dummy = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y_dummy = np.array([0, 0, 1, 1])
    pipeline.fit(X_dummy, y_dummy)
    
    return pipeline


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
    # Créer un VRAI pipeline au lieu d'un Mock
    real_pipeline = create_simple_pipeline()

    # Sauvegarder le pipeline
    pipe_path = temp_model_dir / "pipeline.joblib"
    joblib.dump(real_pipeline, pipe_path)

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
    # Créer un VRAI pipeline
    real_pipeline = create_simple_pipeline()

    # Sauvegarder les artefacts
    pipe_path = temp_model_dir / "pipeline.joblib"
    metrics_path = temp_model_dir / "metrics_valid.json"
    cols_path = temp_model_dir / "columns.json"

    joblib.dump(real_pipeline, pipe_path)

    with open(metrics_path, "w") as f:
        json.dump({"pr_auc": 0.9, "threshold": 0.7}, f)

    # IMPORTANT: Le pipeline a été entraîné avec 2 features, donc on doit déclarer 2 colonnes
    with open(cols_path, "w") as f:
        json.dump({"all_cols": ["Amount", "Time"]}, f)

    loader = ArtifactLoader(temp_model_dir)
    pipeline, metrics, columns, warnings = loader.load_artifacts()

    # Vérifier le chargement
    assert metrics["pr_auc"] == 0.9
    assert metrics["threshold"] == 0.7
    assert len(columns["all_cols"]) == 2  # 2 colonnes, pas 3

    # Pas de warnings si tout est cohérent
    assert len(warnings) == 0