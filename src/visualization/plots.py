"""Module pour créer des visualisations pour l'application de détection de fraude."""

from typing import List, Dict

import plotly.express as px
import plotly.graph_objects as go


class FraudVisualizer:
    """Crée des visualisations pour l'analyse de fraude."""

    # Palette de couleurs
    COLOR_FRAUD = "#e74c3c"
    COLOR_NORMAL = "#27ae60"
    COLOR_PRIMARY = "#3498db"
    COLOR_TEXT = "#2c3e50"
    COLOR_BG = "#f8f9fa"

    @staticmethod
    def create_gauge(value: float, title: str = "Sensibilité (%)") -> go.Figure:
        """
        Crée une jauge pour afficher un pourcentage.

        Args:
            value: Valeur en pourcentage (ex: 7.5 pour 7.5%)
            title: Titre de la jauge

        Returns:
            Figure Plotly
        """
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=value,  # Valeur déjà en pourcentage
                domain={"x": [0, 1], "y": [0, 1]},
                title={
                    "text": title,
                    "font": {"size": 16, "color": FraudVisualizer.COLOR_TEXT},
                },
                number={"suffix": "%", "font": {"size": 20, "color": FraudVisualizer.COLOR_TEXT}},
                gauge={
                    "axis": {"range": [0, 50], "tickcolor": "#7f8c8d"},
                    "bar": {"color": FraudVisualizer.COLOR_PRIMARY},
                    "bgcolor": "#ecf0f1",
                    "steps": [
                        {"range": [0, 15], "color": "#d5f4e6"},
                        {"range": [15, 30], "color": "#fff3cd"},
                        {"range": [30, 50], "color": "#f8d7da"},
                    ],
                    "threshold": {
                        "line": {"color": FraudVisualizer.COLOR_FRAUD, "width": 3},
                        "thickness": 0.75,
                        "value": value,  # Valeur déjà en pourcentage
                    },
                },
            )
        )

        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            font={"color": FraudVisualizer.COLOR_TEXT},
        )

        return fig

    @staticmethod
    def create_probability_bar(
        probability: float, threshold: float
    ) -> go.Figure:
        """
        Crée un graphique en barres pour afficher la probabilité vs le seuil.

        Args:
            probability: Probabilité de fraude
            threshold: Seuil de décision

        Returns:
            Figure Plotly
        """
        color = (
            FraudVisualizer.COLOR_FRAUD
            if probability >= threshold
            else FraudVisualizer.COLOR_NORMAL
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=["Score"],
                y=[probability],
                marker=dict(color=[color], line=dict(color=FraudVisualizer.COLOR_TEXT, width=2)),
                text=f"{probability*100:.2f}%",
                textposition="auto",
                textfont=dict(size=18, color="white"),
                hovertemplate="<b>Probabilité</b>: %{y:.4f}<br><extra></extra>",
            )
        )

        fig.add_hline(
            y=threshold,
            line_dash="dash",
            line_color=FraudVisualizer.COLOR_FRAUD,
            annotation_text=f"Seuil: {threshold:.4f}",
            annotation_position="right",
        )

        fig.update_layout(
            title="Score de fraude vs Seuil de décision",
            yaxis_title="Probabilité",
            yaxis=dict(range=[0, 1]),
            height=300,
            paper_bgcolor="white",
            plot_bgcolor=FraudVisualizer.COLOR_BG,
            font=dict(color=FraudVisualizer.COLOR_TEXT),
            showlegend=False,
        )

        return fig

    @staticmethod
    def create_shap_bar(features: List[Dict]) -> go.Figure:
        """
        Crée un graphique en barres des valeurs SHAP.

        Args:
            features: Liste de dicts avec keys 'feature', 'shap'

        Returns:
            Figure Plotly
        """
        feature_names = [f["feature"] for f in features]
        shap_values = [f["shap"] for f in features]
        colors = [
            FraudVisualizer.COLOR_FRAUD if v > 0 else FraudVisualizer.COLOR_NORMAL
            for v in shap_values
        ]

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                y=feature_names,
                x=shap_values,
                orientation="h",
                marker=dict(color=colors, line=dict(color=FraudVisualizer.COLOR_TEXT, width=1)),
                text=[f"{v:.4e}" for v in shap_values],
                textposition="auto",
                hovertemplate="<b>%{y}</b><br>SHAP: %{x:.4e}<extra></extra>",
            )
        )

        fig.update_layout(
            title="Contributions SHAP",
            xaxis_title="Impact sur la prédiction",
            height=300,
            paper_bgcolor="white",
            plot_bgcolor=FraudVisualizer.COLOR_BG,
            font=dict(color=FraudVisualizer.COLOR_TEXT),
            xaxis=dict(
                zeroline=True,
                zerolinecolor=FraudVisualizer.COLOR_TEXT,
                zerolinewidth=2,
            ),
        )

        return fig

    @staticmethod
    def create_histogram(probabilities, threshold: float) -> go.Figure:
        """
        Crée un histogramme des probabilités de fraude.

        Args:
            probabilities: Array ou Series de probabilités
            threshold: Seuil de décision

        Returns:
            Figure Plotly
        """
        fig = px.histogram(
            x=probabilities,
            nbins=50,
            title="Distribution des probabilités de fraude",
            labels={"x": "Probabilité de fraude"},
            color_discrete_sequence=[FraudVisualizer.COLOR_PRIMARY],
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor=FraudVisualizer.COLOR_BG,
            font=dict(color=FraudVisualizer.COLOR_TEXT),
        )

        fig.add_vline(
            x=threshold,
            line_dash="dash",
            line_color=FraudVisualizer.COLOR_FRAUD,
            annotation_text=f"Seuil: {threshold:.3f}",
            annotation_position="top",
        )

        return fig

    @staticmethod
    def create_risk_pie(risk_counts: dict) -> go.Figure:
        """
        Crée un camembert de la répartition des risques.

        Args:
            risk_counts: Dictionnaire {niveau: count}

        Returns:
            Figure Plotly
        """
        labels = list(risk_counts.keys())
        values = list(risk_counts.values())

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker=dict(colors=["#27ae60", "#f39c12", "#e67e22", "#e74c3c"]),
                    textinfo="label+percent",
                    textfont=dict(size=14),
                )
            ]
        )

        fig.update_layout(
            title="Répartition par niveau de risque",
            paper_bgcolor="white",
            font=dict(color=FraudVisualizer.COLOR_TEXT),
            height=400,
        )

        return fig