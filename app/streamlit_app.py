# app/streamlit_app.py — Application professionnelle pour la détection de fraudes bancaires
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Import des modules src/
from src.data.loader import ArtifactLoader
from src.models.predictor import FraudPredictor
from src.models.explainer import FraudExplainer
from src.visualization.plots import FraudVisualizer
from src.utils.validation import DataValidator

# =========================
# Configuration UI
# =========================
st.set_page_config(
    page_title="Fraud Detector Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS personnalisé pour un design professionnel
st.markdown(
    """
    <style>
    /* Fond blanc propre */
    .stApp {
        background-color: #ffffff;
    }
    /* Sidebar professionnelle */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }
    /* Headers professionnels */
    h1 {
        color: #1a1a1a;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #2c3e50;
        font-weight: 600;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    h3 {
        color: #34495e;
        font-weight: 600;
        font-size: 1.3rem;
    }
    /* Métriques professionnelles */
    [data-testid="stMetricValue"] {
        font-size: 24px;
        font-weight: 600;
        color: #2c3e50;
    }
    [data-testid="stMetricLabel"] {
        color: #7f8c8d;
        font-size: 14px;
        font-weight: 500;
    }
    /* Boutons professionnels */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
    }
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
    }
    /* Tabs professionnels */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #e0e0e0;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        color: #7f8c8d;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }
    /* Cartes professionnelles */
    .info-card {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    /* Alertes stylisées */
    .stAlert {
        border-radius: 8px;
        border-left-width: 4px;
    }
    /* Progress bar professionnelle */
    .stProgress > div > div > div > div {
        background-color: #3498db;
    }
    /* Dataframe professionnel */
    [data-testid="stDataFrame"] {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }
    /* Expander professionnel */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        font-weight: 600;
        color: #2c3e50;
    }
    /* Input fields */
    .stNumberInput input, .stTextInput input {
        border-radius: 4px;
        border: 1px solid #d0d0d0;
    }
    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #d0d0d0;
        border-radius: 8px;
        padding: 2rem;
        background-color: #f8f9fa;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Chemins des artefacts
# =========================
ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models" / "rf_smote_final"
PIPE_PATH = MODEL_DIR / "pipeline.joblib"
METRICS_PATH = MODEL_DIR / "metrics_valid.json"
COLS_PATH = MODEL_DIR / "columns.json"

# =========================
# Header professionnel
# =========================
col_header1, col_header2 = st.columns([3, 1])

with col_header1:
    st.title("🛡️ Fraud Detection System")
    st.markdown(
        "**Système de détection de fraudes bancaires par Intelligence Artificielle**"
    )

with col_header2:
    st.markdown(f"**Date**: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.markdown("**Version**: 3.0")

st.markdown("---")


# =========================
# Chargement des artefacts avec vérification de santé
# =========================
@st.cache_resource(show_spinner=False)
def load_artifacts():
    """Charge les artefacts en utilisant ArtifactLoader."""
    loader = ArtifactLoader(MODEL_DIR)
    pipe, m, cols, warnings = loader.load_artifacts()
    return pipe, m, cols, warnings


with st.spinner("Chargement du modèle..."):
    pipe, metrics_valid, cols, artifact_warnings = load_artifacts()

# Afficher les warnings s'il y en a
if artifact_warnings:
    with st.expander("⚠️ Alertes de santé des artefacts", expanded=True):
        for warning in artifact_warnings:
            st.warning(warning)
else:
    st.success("✅ Modèle chargé avec succès")

# Initialiser le prédicateur et l'explainer
THRESHOLD = float(metrics_valid["threshold"])
EXPECTED_COLS = cols["all_cols"]
predictor = FraudPredictor(pipe, EXPECTED_COLS, threshold=THRESHOLD)
explainer = FraudExplainer(pipe)

# =========================
# Sidebar professionnelle
# =========================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    st.info(
        "🎯 **Seuil actif**: Toutes les prédictions utilisent le seuil défini ci-dessous"
    )

    # Seuil avec slider
    user_thr = st.slider(
        "Seuil de décision",
        min_value=0.0,
        max_value=0.5,
        value=float(THRESHOLD),
        step=0.005,
        help="Probabilité minimale pour classifier une transaction comme frauduleuse",
    )

    # Option d'archivage automatique
    archive_on = st.checkbox(
        "🗄️ Archiver automatiquement les rapports CSV",
        value=True,
        help="Sauvegarde chaque lot analysé dans reports/predictions/ et met à jour l'index.",
    )

    # Jauge visuelle professionnelle
    fig_gauge = FraudVisualizer.create_gauge(user_thr * 100, title="Sensibilité (%)")
    st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")

    # Métriques de performance
    st.markdown("### 📊 Performance du Modèle")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="PR-AUC",
            value=f"{metrics_valid.get('pr_auc', 0):.3f}",
            help="Précision-Rappel Area Under Curve",
        )
        st.metric(
            label="Recall",
            value=f"{metrics_valid.get('recall', 0):.3f}",
            help="Taux de détection des fraudes",
        )

    with col2:
        st.metric(
            label="ROC-AUC",
            value=f"{metrics_valid.get('roc_auc', 0):.3f}",
            help="Receiver Operating Characteristic AUC",
        )
        st.metric(
            label="Precision",
            value=f"{metrics_valid.get('precision', 0):.3f}",
            help="Précision des prédictions de fraude",
        )

    st.markdown("---")

    # Informations techniques
    with st.expander("ℹ️ Informations Techniques"):
        st.markdown(
            f"""
        **Algorithme**: Random Forest + SMOTE  
        **Features**: {len(cols.get('all_cols', []))}  
        **Seuil optimal**: {THRESHOLD:.4f}  
        **Pipeline**: StandardScaler → SMOTE → RF  
        **Session**: {datetime.now().strftime('%d/%m/%Y à %H:%M')}
        """
        )

    st.caption(
        "💡 Un seuil plus élevé réduit les faux positifs mais peut manquer certaines fraudes."
    )

# =========================
# Transaction unique
# =========================
st.markdown("## 🔍 Analyse de Transaction Unique")

# Bouton exemple
try:
    DEMO_X = pd.read_csv(ROOT / "data" / "processed" / "X_test.csv")
    DEMO_y = pd.read_csv(ROOT / "data" / "processed" / "y_test.csv").squeeze()
except Exception:
    DEMO_X, DEMO_y = None, None

col_demo1, col_demo2, col_demo3 = st.columns([2, 1, 2])

with col_demo2:
    if DEMO_X is not None:
        if st.button("⚡ Charger Exemple", use_container_width=True):
            fraud_idx = int(DEMO_y[DEMO_y == 1].index[0])
            row = DEMO_X.iloc[fraud_idx].to_dict()
            st.session_state["_demo_payload"] = row
            st.rerun()

with st.form("single_tx_form"):
    # Initialisation des valeurs
    if "_demo_payload" in st.session_state:
        demo_data = st.session_state["_demo_payload"]
        default_amount = demo_data.get("Amount", 0.0)
        default_time = demo_data.get("Time", 0.0)
    else:
        default_amount = 0.0
        default_time = 0.0

    # Champs principaux
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        amount = st.number_input(
            "Montant (€)", value=float(default_amount), step=1.0, format="%.2f"
        )

    with col2:
        time = st.number_input(
            "Temps (secondes)", value=float(default_time), step=1.0, format="%.0f"
        )

    with col3:
        st.write("")
        st.write("")
        show_more = st.checkbox("Variables avancées", value=False)

    # Variables V1-V28
    vvals = {}
    if show_more:
        st.markdown("### Variables PCA (V1-V28)")
        tabs_v = st.tabs([f"V{i}-V{i+6}" for i in range(1, 29, 7)])

        for tab_idx, tab in enumerate(tabs_v):
            with tab:
                cols = st.columns(4)
                for i in range(7):
                    v_num = tab_idx * 7 + i + 1
                    if v_num <= 28:
                        with cols[i % 4]:
                            if "_demo_payload" in st.session_state:
                                default_v = st.session_state["_demo_payload"].get(
                                    f"V{v_num}", 0.0
                                )
                            else:
                                default_v = 0.0
                            vvals[f"V{v_num}"] = st.number_input(
                                f"V{v_num}",
                                value=float(default_v),
                                step=0.1,
                                format="%.4f",
                                key=f"v_{v_num}",
                            )

    submitted = st.form_submit_button("🔍 Analyser", use_container_width=True)

# Traitement et affichage des résultats
if submitted:
    if "_demo_payload" in st.session_state:
        payload = dict(st.session_state.pop("_demo_payload"))
    else:
        payload = {"Amount": amount, "Time": time}
        payload.update(vvals)

    # Utiliser FraudPredictor
    proba, pred = predictor.predict_single(payload, threshold=user_thr)

    st.markdown("---")
    st.markdown("## 📋 Résultat de l'Analyse")

    # Résultats principaux
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if pred == 1:
            st.error("**🚨 FRAUDE DÉTECTÉE**")
        else:
            st.success("**✅ TRANSACTION NORMALE**")

    with col2:
        st.metric("Probabilité", f"{proba*100:.2f}%")

    with col3:
        risk_level = predictor.get_risk_level(proba)
        st.metric("Niveau de risque", risk_level)

    with col4:
        st.metric("Seuil appliqué", f"{user_thr*100:.2f}%")

    # Barre de progression
    st.markdown("#### Score de fraude")
    st.progress(float(min(proba, 1.0)))

    # Graphique de probabilité
    fig_proba = FraudVisualizer.create_probability_bar(proba, user_thr)
    st.plotly_chart(fig_proba, use_container_width=True)

    # Recommandation
    if proba >= 0.8:
        st.error("⚠️ **ALERTE CRITIQUE** - Investigation immédiate recommandée")
    elif proba >= 0.5:
        st.warning("⚠️ **ALERTE** - Vérification manuelle conseillée")
    elif proba >= 0.3:
        st.info("ℹ️ **SURVEILLANCE** - Transaction à surveiller")
    else:
        st.success("✅ **NORMAL** - Transaction conforme")

    # Explications SHAP
    with st.expander("📊 Analyse détaillée des facteurs", expanded=True):
        # Utiliser FraudExplainer
        x_df = pd.DataFrame([payload])
        reasons, error = explainer.explain(x_df, top_k=5)

        if error:
            st.warning(
                "⚠️ L'analyse détaillée n'est pas disponible pour cette transaction."
            )
            st.caption(f"Détails techniques: {error}")
        elif not reasons:
            st.info("ℹ️ Aucune contribution significative détectée.")
        else:
            col_exp1, col_exp2 = st.columns([1, 1])

            with col_exp1:
                st.markdown("#### Top 5 facteurs influents")

                for idx, r in enumerate(reasons, 1):
                    impact_color = "#e74c3c" if "↑" in r["direction"] else "#27ae60"
                    impact_text = "Augmente" if "↑" in r["direction"] else "Réduit"

                    st.markdown(
                        f"""
                    **{idx}. {r['feature']}**  
                    Valeur: `{r['value']:.4f}` | Impact: <span style='color:{impact_color};font-weight:600;'>{impact_text}</span> le risque  
                    Contribution SHAP: `{r['shap']:.4e}`
                    """,
                        unsafe_allow_html=True,
                    )
                    st.markdown("---")

            with col_exp2:
                # Graphique SHAP avec FraudVisualizer
                fig_shap = FraudVisualizer.create_shap_bar(reasons)
                st.plotly_chart(fig_shap, use_container_width=True)

            st.info(
                "💡 **Interprétation**: Les valeurs SHAP positives (rouge) augmentent la probabilité de fraude, les valeurs négatives (vert) la diminuent."
            )

# =========================
# Prédictions par lot (CSV)
# =========================
st.markdown("---")
st.markdown("## 📁 Analyse par Lot (CSV)")

st.info(
    "**Format accepté**: Fichier CSV contenant les colonnes Amount, Time, et optionnellement V1-V28"
)
st.caption(
    "⚠️ Limite: 100 000 lignes maximum | Les fichiers volumineux sont traités par batch de 5000 lignes"
)

up = st.file_uploader("Sélectionner un fichier CSV", type=["csv"])

if up is not None:
    try:
        # Lecture initiale
        df_in = pd.read_csv(up)

        # Validation avec DataValidator
        validator = DataValidator(EXPECTED_COLS, max_rows=100_000)
        is_valid, errors = validator.validate_dataframe(df_in)

        if not is_valid:
            for error in errors:
                st.error(f"❌ {error}")
            st.info(
                "💡 Conseil: Divisez votre fichier en plusieurs parties ou vérifiez le format des données."
            )
            st.stop()

        # Nettoyer les données
        df = validator.sanitize_dataframe(df_in)
        n_rows = len(df)

        if n_rows > 10_000:
            st.warning(
                f"⚠️ Fichier volumineux détecté: {n_rows:,} lignes. Le traitement peut prendre quelques minutes."
            )

    except Exception as e:
        st.error(f"Erreur de lecture du fichier: {e}")
        st.stop()

    # Utiliser FraudPredictor pour les prédictions par batch
    CHUNK_SIZE = 5000

    if n_rows > CHUNK_SIZE:
        st.info(f"📦 Traitement par batch de {CHUNK_SIZE:,} lignes...")

        progress_bar = st.progress(0)
        status_text = st.empty()

        # Callback pour mise à jour de progression
        def update_progress(current, total):
            progress = current / total
            progress_bar.progress(progress)
            status_text.text(f"Traité: {current:,} / {total:,} lignes")

        # Utiliser predict_batch qui gère automatiquement les chunks
        proba, pred = predictor.predict_batch(df, chunk_size=CHUNK_SIZE, threshold=user_thr)

        # Simuler la progression pour l'affichage
        for i in range(0, n_rows, CHUNK_SIZE):
            update_progress(min(i + CHUNK_SIZE, n_rows), n_rows)

        progress_bar.empty()
        status_text.empty()
        st.success(f"✅ {n_rows:,} transactions analysées avec succès")

    else:
        # Traitement direct pour petits fichiers
        with st.spinner("Analyse en cours..."):
            proba, pred = predictor.predict(df, threshold=user_thr)

    # Résultats
    out = df_in.copy()
    out["fraud_proba"] = proba
    out["fraud_pred"] = pred
    # Utiliser get_risk_level du predictor
    out["risk_level"] = out["fraud_proba"].apply(predictor.get_risk_level)

    n_alertes = int((pred == 1).sum())
    n_total = len(out)
    pct_alertes = (n_alertes / n_total * 100) if n_total > 0 else 0

    # === Archivage automatique ===
    if archive_on:
        ARCHIVE_DIR = ROOT / "reports" / "predictions"
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_path = ARCHIVE_DIR / f"fraud_analysis_{ts}.csv"

        # On ajoute le seuil utilisé pour audit
        out_to_save = out.copy()
        out_to_save["threshold_used"] = float(user_thr)

        # 1) Sauvegarde du CSV archivé
        out_to_save.to_csv(archive_path, index=False)

        # 2) Mise à jour / création de l'index des archives
        index_path = ARCHIVE_DIR / "_index.csv"
        row_idx = pd.DataFrame(
            [
                {
                    "timestamp": ts,
                    "file": archive_path.name,
                    "rows": int(len(out_to_save)),
                    "alerts": int((out_to_save["fraud_pred"] == 1).sum()),
                    "mean_proba": float(out_to_save["fraud_proba"].mean()),
                    "threshold": float(user_thr),
                }
            ]
        )

        if index_path.exists():
            idx = pd.read_csv(index_path)
            idx = pd.concat([idx, row_idx], ignore_index=True)
        else:
            idx = row_idx

        idx.to_csv(index_path, index=False)

        # 3) Garder seulement les 100 dernières archives
        archives = sorted(ARCHIVE_DIR.glob("fraud_analysis_*.csv"))
        if len(archives) > 100:
            for old in archives[:-100]:
                old.unlink()
            # Nettoyer aussi l'index pour garder seulement les 100 dernières entrées
            idx = idx.tail(100)
            idx.to_csv(index_path, index=False)

        st.success(f"📦 Archivé automatiquement : `reports/predictions/{archive_path.name}`")

    # Statistiques principales
    st.markdown("### 📊 Résumé de l'analyse")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Transactions analysées", n_total)

    with col2:
        st.metric("Fraudes détectées", n_alertes, delta=f"{pct_alertes:.1f}%")

    with col3:
        st.metric("Transactions normales", n_total - n_alertes)

    with col4:
        avg_proba = out["fraud_proba"].mean()
        st.metric("Probabilité moyenne", f"{avg_proba:.3f}")

    if n_alertes > 0:
        st.warning(f"⚠️ {n_alertes} transaction(s) suspecte(s) identifiée(s)")
    else:
        st.success("✅ Aucune fraude détectée")

    # Visualisations
    st.markdown("### 📈 Visualisations")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Données complètes", "Fraudes détectées", "Distribution", "Analyse par risque"]
    )

    with tab1:
        # Tableau avec highlighting
        def highlight_fraud(row):
            if row["fraud_pred"] == 1:
                return ["background-color: #f8d7da"] * len(row)
            return [""] * len(row)

        st.dataframe(
            out.style.apply(highlight_fraud, axis=1),
            use_container_width=True,
            height=400,
        )

    with tab2:
        fraudes = out[out["fraud_pred"] == 1]
        if len(fraudes) > 0:
            st.dataframe(fraudes, use_container_width=True, height=400)

            st.markdown("#### Statistiques des fraudes")
            col_f1, col_f2, col_f3 = st.columns(3)

            with col_f1:
                st.metric(
                    "Montant moyen",
                    (
                        f"{fraudes['Amount'].mean():.2f} €"
                        if "Amount" in fraudes.columns
                        else "N/A"
                    ),
                )
            with col_f2:
                st.metric(
                    "Montant maximum",
                    (
                        f"{fraudes['Amount'].max():.2f} €"
                        if "Amount" in fraudes.columns
                        else "N/A"
                    ),
                )
            with col_f3:
                st.metric("Probabilité moyenne", f"{fraudes['fraud_proba'].mean():.4f}")
        else:
            st.success("Aucune fraude dans ce lot")

    with tab3:
        # Histogramme avec FraudVisualizer
        fig_hist = FraudVisualizer.create_histogram(out["fraud_proba"].values, user_thr)
        st.plotly_chart(fig_hist, use_container_width=True)

        # Statistiques
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("Moyenne", f"{out['fraud_proba'].mean():.4f}")
        col_s2.metric("Médiane", f"{out['fraud_proba'].median():.4f}")
        col_s3.metric("Écart-type", f"{out['fraud_proba'].std():.4f}")
        col_s4.metric("Maximum", f"{out['fraud_proba'].max():.4f}")

    with tab4:
        # Camembert des risques avec FraudVisualizer
        risk_counts = out["risk_level"].value_counts().to_dict()
        fig_pie = FraudVisualizer.create_risk_pie(risk_counts)
        st.plotly_chart(fig_pie, use_container_width=True)

        # Tableau récapitulatif
        st.markdown("#### Récapitulatif par niveau de risque")
        risk_summary = (
            out.groupby("risk_level")
            .agg({"fraud_proba": ["count", "mean", "min", "max"]})
            .round(4)
        )
        st.dataframe(risk_summary, use_container_width=True)

    # Export
    st.markdown("### 💾 Export des résultats")

    csv_bytes = out.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger le rapport (CSV)",
        data=csv_bytes,
        file_name=f"fraud_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True,
    )

# =========================
# Footer professionnel
# =========================
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 1rem; color: #7f8c8d;">
        <p><strong>Fraud Detection System v3.0</strong></p>
        <p style="font-size: 0.9em;">Développé avec Streamlit | Propulsé par Random Forest & SHAP</p>
        <p style="font-size: 0.8em;">© 2025 - Tous droits réservés</p>
    </div>
""",
    unsafe_allow_html=True,
)