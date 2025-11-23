# =============================================================================
# Script d'installation et de configuration du projet fraud-detection-pfe (Windows)
# =============================================================================
# Usage: .\scripts\setup.ps1
# =============================================================================

$ErrorActionPreference = "Stop"

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "🚀 Fraud Detection PFE - Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# =============================================================================
# 1. Vérifier Python
# =============================================================================
Write-Host "[1/7] Vérification de Python..." -ForegroundColor Blue

try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion détecté" -ForegroundColor Green
} catch {
    Write-Host "❌ Python 3 n'est pas installé" -ForegroundColor Red
    Write-Host "   Installez Python 3.11+ depuis https://www.python.org/downloads/"
    exit 1
}
Write-Host ""

# =============================================================================
# 2. Créer la structure de dossiers
# =============================================================================
Write-Host "[2/7] Création de la structure de dossiers..." -ForegroundColor Blue

$folders = @(
    "data/raw",
    "data/processed",
    "data/examples",
    "models/rf_smote_final",
    "reports/predictions"
)

foreach ($folder in $folders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
    }
}

Write-Host "✅ Structure créée" -ForegroundColor Green
Write-Host ""

# =============================================================================
# 3. Créer et activer l'environnement virtuel
# =============================================================================
Write-Host "[3/7] Configuration de l'environnement virtuel..." -ForegroundColor Blue

if (-not (Test-Path ".venv")) {
    Write-Host "   Création de l'environnement virtuel..."
    python -m venv .venv
}

# Activer l'environnement virtuel
& .\.venv\Scripts\Activate.ps1

Write-Host "✅ Environnement virtuel activé" -ForegroundColor Green
Write-Host ""

# =============================================================================
# 4. Installer les dépendances
# =============================================================================
Write-Host "[4/7] Installation des dépendances Python..." -ForegroundColor Blue

python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

Write-Host "✅ Dépendances installées" -ForegroundColor Green
Write-Host ""

# =============================================================================
# 5. Vérifier les données
# =============================================================================
Write-Host "[5/7] Vérification des données..." -ForegroundColor Blue

if (-not (Test-Path "data/raw/creditcard.csv")) {
    Write-Host "⚠️  Dataset manquant" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Le fichier 'creditcard.csv' n'a pas été trouvé."
    Write-Host "   Vous devez le télécharger manuellement depuis Kaggle :"
    Write-Host ""
    Write-Host "   👉 https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   Puis placez-le dans : data/raw/creditcard.csv"
    Write-Host ""
    Write-Host "⏸️  Installation en pause" -ForegroundColor Yellow
    Write-Host "   Après avoir ajouté les données, relancez :"
    Write-Host "   .\scripts\setup.ps1" -ForegroundColor Cyan
    exit 0
} else {
    $fileSize = (Get-Item "data/raw/creditcard.csv").Length / 1MB
    Write-Host "✅ Dataset trouvé ($([math]::Round($fileSize, 2)) MB)" -ForegroundColor Green
}
Write-Host ""

# =============================================================================
# 6. Préparer les données et entraîner le modèle
# =============================================================================
Write-Host "[6/7] Préparation des données et entraînement du modèle..." -ForegroundColor Blue

if (-not (Test-Path "models/rf_smote_final/pipeline.joblib")) {
    Write-Host "   🔧 Entraînement du modèle (5-10 minutes)..."
    Write-Host "   Patientez..."

    python scripts/train_model.py `
        --data data/raw/creditcard.csv `
        --output models/rf_smote_final `
        --smote-strategy 0.2

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Modèle entraîné et sauvegardé" -ForegroundColor Green
    } else {
        Write-Host "❌ Erreur lors de l'entraînement" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ Modèle déjà entraîné" -ForegroundColor Green
}
Write-Host ""

# =============================================================================
# 7. Vérification finale
# =============================================================================
Write-Host "[7/7] Vérification finale..." -ForegroundColor Blue

# Vérifier le modèle
if (Test-Path "models/rf_smote_final/pipeline.joblib") {
    $modelSize = (Get-Item "models/rf_smote_final/pipeline.joblib").Length / 1MB
    Write-Host "✅ Modèle : $([math]::Round($modelSize, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "❌ Modèle manquant" -ForegroundColor Red
    exit 1
}

# Vérifier les données prétraitées
if (Test-Path "data/processed/X_train.csv") {
    Write-Host "✅ Données prétraitées" -ForegroundColor Green
} else {
    Write-Host "⚠️  Données prétraitées manquantes" -ForegroundColor Yellow
}

# Exécuter les tests
Write-Host ""
Write-Host "   Exécution des tests..."
pytest tests/ -q --tb=no

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tests réussis" -ForegroundColor Green
} else {
    Write-Host "⚠️  Certains tests ont échoué (mais l'installation est OK)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "✅ Installation terminée !" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Pour lancer l'application :" -ForegroundColor Cyan
Write-Host ""
Write-Host "   `$env:PYTHONPATH = `".`""
Write-Host "   streamlit run app/streamlit_app.py"
Write-Host ""
Write-Host "   Puis ouvrez : http://localhost:8501"
Write-Host ""
Write-Host "📚 Documentation :" -ForegroundColor Cyan
Write-Host "   - Guide complet : README.md"
Write-Host "   - Guide utilisateur : docs/USER_GUIDE.md"
Write-Host "   - Guide développeur : docs/DEVELOPER_GUIDE.md"
Write-Host ""
Write-Host "🎓 Bon courage pour votre soutenance !" -ForegroundColor Cyan
Write-Host ""