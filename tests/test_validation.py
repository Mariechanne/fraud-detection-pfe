"""Tests pour le module validation."""

import pandas as pd
import pytest

from src.utils.validation import DataValidator


@pytest.fixture
def validator():
    """Crée un validateur pour les tests."""
    expected_cols = ["Amount", "Time"] + [f"V{i}" for i in range(1, 29)]
    return DataValidator(expected_cols, max_rows=1000)


def test_validator_initialization(validator):
    """Test l'initialisation du validateur."""
    assert validator.max_rows == 1000
    assert len(validator.expected_columns) == 30


def test_validate_dataframe_valid(validator):
    """Test la validation d'un DataFrame valide."""
    df = pd.DataFrame({"Amount": [100], "Time": [500]})

    is_valid, errors = validator.validate_dataframe(df)

    assert is_valid is True
    assert len(errors) == 0


def test_validate_dataframe_too_large(validator):
    """Test la validation d'un DataFrame trop grand."""
    df = pd.DataFrame(
        {"Amount": range(2000), "Time": range(2000)}
    )

    is_valid, errors = validator.validate_dataframe(df)

    assert is_valid is False
    assert any("trop volumineux" in err for err in errors)


def test_validate_dataframe_empty(validator):
    """Test la validation d'un DataFrame vide."""
    df = pd.DataFrame()

    is_valid, errors = validator.validate_dataframe(df)

    assert is_valid is False
    assert any("vide" in err for err in errors)


def test_validate_dataframe_missing_critical_columns(validator):
    """Test la validation avec colonnes critiques manquantes."""
    df = pd.DataFrame({"V1": [100]})

    is_valid, errors = validator.validate_dataframe(df)

    assert is_valid is False
    assert any("manquantes" in err for err in errors)


def test_validate_transaction_valid(validator):
    """Test la validation d'une transaction valide."""
    transaction = {"Amount": 100.0, "Time": 500.0}

    is_valid, errors = validator.validate_transaction(transaction)

    assert is_valid is True
    assert len(errors) == 0


def test_validate_transaction_missing_amount(validator):
    """Test la validation d'une transaction sans montant."""
    transaction = {"Time": 500.0}

    is_valid, errors = validator.validate_transaction(transaction)

    assert is_valid is False
    assert any("Amount" in err for err in errors)


def test_validate_transaction_negative_amount(validator):
    """Test la validation d'une transaction avec montant négatif."""
    transaction = {"Amount": -100.0, "Time": 500.0}

    is_valid, errors = validator.validate_transaction(transaction)

    assert is_valid is False
    assert any("négatif" in err for err in errors)


def test_sanitize_dataframe(validator):
    """Test le nettoyage d'un DataFrame."""
    df = pd.DataFrame(
        {"Amount": [100, None], "Time": [500, 600], "Extra": ["x", "y"]}
    )

    result = validator.sanitize_dataframe(df)

    # Vérifier que les colonnes manquantes sont ajoutées
    assert "V1" in result.columns

    # Vérifier que les NaN sont remplacés
    assert result["Amount"].isna().sum() == 0

    # Vérifier que les colonnes extra sont supprimées
    assert "Extra" not in result.columns


def test_sanitize_dataframe_type_conversion(validator):
    """Test la conversion de types lors du nettoyage."""
    df = pd.DataFrame({"Amount": ["100", "200"], "Time": ["500", "invalid"]})

    result = validator.sanitize_dataframe(df)

    # Vérifier que Amount est numérique (int64 ou float64, les deux sont acceptables)
    assert pd.api.types.is_numeric_dtype(result["Amount"])
    
    # Vérifier que les valeurs sont correctes (peuvent être int ou float)
    assert result["Amount"].iloc[0] in [100, 100.0]
    assert result["Amount"].iloc[1] in [200, 200.0]

    # Vérifier que Time est numérique
    assert pd.api.types.is_numeric_dtype(result["Time"])
    
    # Les valeurs invalides doivent être remplacées par 0
    assert result["Time"].iloc[1] in [0, 0.0]