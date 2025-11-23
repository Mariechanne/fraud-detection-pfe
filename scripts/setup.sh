#!/bin/bash

# =============================================================================
# Script d'installation et de configuration du projet fraud-detection-pfe
# =============================================================================
# Usage: bash scripts/setup.sh
# =============================================================================

set -e  # Arrêt en cas d'erreur

echo "=================================="
echo "🚀 Fraud Detection PFE - Setup"
echo "=================================="
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# =============================================================================
# 1. Vérifier Python
# =============================================================================
echo -e "${BLUE}[1/7]${NC} Vérification de Python..."

# Détecter quelle commande Python est disponible
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ Python 3 n'est pas installé${NC}"
    echo "   Installez Python 3.11+ depuis https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅${NC} Python $PYTHON_VERSION détecté (commande: $PYTHON_CMD)"
echo ""

# =============================================================================
# 2. Créer la structure de dossiers
# =============================================================================
echo -e "${BLUE}[2/7]${NC} Création de la structure de dossiers..."

mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/examples
mkdir -p models/rf_smote_final
mkdir -p reports/predictions

echo -e "${GREEN}✅${NC} Structure créée"
echo ""

# =============================================================================
# 3. Créer et activer l'environnement virtuel
# =============================================================================
echo -e "${BLUE}[3/7]${NC} Configuration de l'environnement virtuel..."

if [ ! -d ".venv/bin" ] && [ ! -d ".venv/Scripts" ]; then
    echo "   Création de l'environnement virtuel..."
    $PYTHON_CMD -m venv .venv
fi

# Activer l'environnement virtuel (selon l'OS)
if [ -f ".venv/Scripts/activate" ]; then
    # Windows (Git Bash)
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    # Linux/macOS
    source .venv/bin/activate
else
    echo -e "${RED}❌ Impossible de trouver le script d'activation${NC}"
    exit 1
fi

echo -e "${GREEN}✅${NC} Environnement virtuel activé"
echo ""

# =============================================================================
# 4. Installer les dépendances
# =============================================================================
echo -e "${BLUE}[4/7]${NC} Installation des dépendances Python..."

$PYTHON_CMD -m pip install --upgrade pip --quiet
$PYTHON_CMD -m pip install -r requirements.txt --quiet

echo -e "${GREEN}✅${NC} Dépendances installées"
echo ""

# =============================================================================
# 5. Vérifier les données
# =============================================================================
echo -e "${BLUE}[5/7]${NC} Vérification des données..."

if [ ! -f "data/raw/creditcard.csv" ]; then
    echo -e "${YELLOW}⚠️  Dataset manquant${NC}"
    echo ""
    echo "   Le fichier 'creditcard.csv' n'a pas été trouvé."
    echo "   Vous devez le télécharger manuellement depuis Kaggle :"
    echo ""
    echo "   👉 https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud"
    echo ""
    echo "   Puis placez-le dans : data/raw/creditcard.csv"
    echo ""
    echo -e "${YELLOW}⏸️  Installation en pause${NC}"
    echo "   Après avoir ajouté les données, relancez :"
    echo "   bash scripts/setup.sh"
    exit 0
else
    if command -v du &> /dev/null; then
        FILE_SIZE=$(du -h data/raw/creditcard.csv 2>/dev/null | cut -f1)
        echo -e "${GREEN}✅${NC} Dataset trouvé ($FILE_SIZE)"
    else
        echo -e "${GREEN}✅${NC} Dataset trouvé"
    fi
fi
echo ""

# =============================================================================
# 6. Préparer les données et entraîner le modèle
# =============================================================================
echo -e "${BLUE}[6/7]${NC} Préparation des données et entraînement du modèle..."

if [ ! -f "models/rf_smote_final/pipeline.joblib" ]; then
    echo "   🔧 Entraînement du modèle (5-10 minutes)..."
    echo "   Patientez..."

    $PYTHON_CMD scripts/train_model.py \
        --data data/raw/creditcard.csv \
        --output models/rf_smote_final \
        --smote-strategy 0.2

    # Vérifier immédiatement le résultat
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅${NC} Modèle entraîné et sauvegardé"
    else
        echo -e "${RED}❌ Erreur lors de l'entraînement${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅${NC} Modèle déjà entraîné"
fi
echo ""

# =============================================================================
# 7. Vérification finale
# =============================================================================
echo -e "${BLUE}[7/7]${NC} Vérification finale..."

# Vérifier le modèle
if [ -f "models/rf_smote_final/pipeline.joblib" ]; then
    if command -v du &> /dev/null; then
        MODEL_SIZE=$(du -h models/rf_smote_final/pipeline.joblib 2>/dev/null | cut -f1)
        echo -e "${GREEN}✅${NC} Modèle : $MODEL_SIZE"
    else
        echo -e "${GREEN}✅${NC} Modèle présent"
    fi
else
    echo -e "${RED}❌${NC} Modèle manquant"
    exit 1
fi

# Vérifier les données prétraitées
if [ -f "data/processed/X_train.csv" ]; then
    echo -e "${GREEN}✅${NC} Données prétraitées"
else
    echo -e "${YELLOW}⚠️${NC}  Données prétraitées manquantes"
fi

# Exécuter les tests (si pytest est disponible)
if command -v pytest &> /dev/null; then
    echo ""
    echo "   Exécution des tests..."
    if pytest tests/ -q --tb=no 2>/dev/null; then
        echo -e "${GREEN}✅${NC} Tests réussis"
    else
        echo -e "${YELLOW}⚠️${NC}  Certains tests ont échoué (mais l'installation est OK)"
    fi
else
    echo -e "${YELLOW}⚠️${NC}  pytest non disponible (ignoré)"
fi

echo ""
echo "=================================="
echo -e "${GREEN}✅ Installation terminée !${NC}"
echo "=================================="
echo ""
echo "🚀 Pour lancer l'application :"
echo ""
if [ -f ".venv/Scripts/activate" ]; then
    # Instructions Windows
    echo "   # Windows PowerShell"
    echo "   .venv\\Scripts\\Activate.ps1"
    echo "   \$env:PYTHONPATH = \".\""
    echo "   streamlit run app/streamlit_app.py"
elif [ -f ".venv/bin/activate" ]; then
    # Instructions Linux/macOS
    echo "   source .venv/bin/activate"
    echo "   export PYTHONPATH=\".\""
    echo "   streamlit run app/streamlit_app.py"
fi
echo ""
echo "   Puis ouvrez : http://localhost:8501"
echo ""
echo "📚 Documentation :"
echo "   - Guide complet : README.md"
echo "   - Guide utilisateur : docs/USER_GUIDE.md"
echo "   - Guide développeur : docs/DEVELOPER_GUIDE.md"
echo ""
echo "🎓 Bon courage pour votre soutenance !"
echo ""