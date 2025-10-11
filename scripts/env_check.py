import sys, platform

print("Python:", sys.version.split()[0])
print("Platform:", platform.platform())

# Imports critiques
import pandas, sklearn, xgboost, imblearn, shap, streamlit

print("pandas:", pandas.__version__)
print("scikit-learn:", sklearn.__version__)
print("xgboost:", xgboost.__version__)
print("imbalanced-learn:", imblearn.__version__)
print("shap:", shap.__version__)
print("streamlit:", streamlit.__version__)

print("\n✅ Environnement OK : imports et versions détectés.")
