"""
Fonctions de visualisation pour l'évaluation des modèles de détection de fraude
Auteur: Chandeste
Date: Novembre 2024
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve
import pandas as pd

# Configuration du style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


def plot_confusion_matrix(y_true, y_pred, model_name="Modèle", threshold=0.5, ax=None):
    """
    Affiche la matrice de confusion avec des annotations détaillées
    
    Paramètres:
    -----------
    y_true : array-like
        Vraies étiquettes
    y_pred : array-like
        Prédictions du modèle (0 ou 1)
    model_name : str
        Nom du modèle pour le titre
    threshold : float
        Seuil utilisé pour la classification
    ax : matplotlib axis, optionnel
        Axe matplotlib pour le tracé
    
    Retourne:
    ---------
    ax : matplotlib axis
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    # Calculer la matrice de confusion
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    # Créer un DataFrame pour une meilleure visualisation
    cm_df = pd.DataFrame(cm, 
                         index=['Normal (0)', 'Fraude (1)'],
                         columns=['Prédit Normal', 'Prédit Fraude'])
    
    # Heatmap
    sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues', 
                cbar_kws={'label': 'Nombre de transactions'},
                ax=ax, square=True, linewidths=2, linecolor='black')
    
    # Ajouter des annotations détaillées
    ax.text(0.5, 0.15, f'TN = {tn:,}', ha='center', va='center', 
            fontsize=10, color='darkblue', weight='bold', transform=ax.transAxes)
    ax.text(1.5, 0.15, f'FP = {fp:,}', ha='center', va='center', 
            fontsize=10, color='darkred', weight='bold', transform=ax.transAxes)
    ax.text(0.5, 0.85, f'FN = {fn:,}', ha='center', va='center', 
            fontsize=10, color='darkred', weight='bold', transform=ax.transAxes)
    ax.text(1.5, 0.85, f'TP = {tp:,}', ha='center', va='center', 
            fontsize=10, color='darkgreen', weight='bold', transform=ax.transAxes)
    
    # Calculer les métriques
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Titre avec métriques
    ax.set_title(f'Matrice de Confusion - {model_name}\n' + 
                 f'Seuil = {threshold:.3f} | Accuracy = {accuracy:.2%} | ' +
                 f'Precision = {precision:.2%} | Recall = {recall:.2%}',
                 fontsize=12, weight='bold', pad=20)
    
    ax.set_ylabel('Vraie classe', fontsize=11, weight='bold')
    ax.set_xlabel('Classe prédite', fontsize=11, weight='bold')
    
    return ax


def plot_roc_curve(y_true, y_proba, model_name="Modèle", ax=None):
    """
    Affiche la courbe ROC avec l'aire sous la courbe (AUC)
    
    Paramètres:
    -----------
    y_true : array-like
        Vraies étiquettes
    y_proba : array-like
        Probabilités prédites pour la classe positive
    model_name : str
        Nom du modèle pour le titre
    ax : matplotlib axis, optionnel
        Axe matplotlib pour le tracé
    
    Retourne:
    ---------
    ax : matplotlib axis
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    # Calculer la courbe ROC
    fpr, tpr, thresholds = roc_curve(y_true, y_proba)
    roc_auc = auc(fpr, tpr)
    
    # Tracer la courbe ROC
    ax.plot(fpr, tpr, color='darkorange', lw=2.5, 
            label=f'{model_name} (AUC = {roc_auc:.4f})')
    
    # Ligne de référence (classificateur aléatoire)
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', 
            label='Classificateur aléatoire (AUC = 0.5000)')
    
    # Marquer le point optimal (seuil de Youden)
    optimal_idx = np.argmax(tpr - fpr)
    optimal_threshold = thresholds[optimal_idx]
    optimal_fpr = fpr[optimal_idx]
    optimal_tpr = tpr[optimal_idx]
    
    ax.plot(optimal_fpr, optimal_tpr, 'ro', markersize=10, 
            label=f'Point optimal (seuil = {optimal_threshold:.3f})')
    
    # Configuration des axes
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('Taux de Faux Positifs (FPR)', fontsize=11, weight='bold')
    ax.set_ylabel('Taux de Vrais Positifs (TPR / Recall)', fontsize=11, weight='bold')
    ax.set_title(f'Courbe ROC - {model_name}', fontsize=12, weight='bold', pad=15)
    
    # Grille et légende
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc="lower right", fontsize=10, framealpha=0.9)
    
    # Ajouter des annotations
    ax.text(0.6, 0.2, f'AUC = {roc_auc:.4f}', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=12, weight='bold')
    
    return ax


def plot_precision_recall_curve(y_true, y_proba, model_name="Modèle", ax=None):
    """
    Affiche la courbe Precision-Recall avec l'aire sous la courbe (PR-AUC)
    
    Paramètres:
    -----------
    y_true : array-like
        Vraies étiquettes
    y_proba : array-like
        Probabilités prédites pour la classe positive
    model_name : str
        Nom du modèle pour le titre
    ax : matplotlib axis, optionnel
        Axe matplotlib pour le tracé
    
    Retourne:
    ---------
    ax : matplotlib axis
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    # Calculer la courbe Precision-Recall
    precision, recall, thresholds = precision_recall_curve(y_true, y_proba)
    pr_auc = auc(recall, precision)
    
    # Tracer la courbe
    ax.plot(recall, precision, color='darkorange', lw=2.5,
            label=f'{model_name} (PR-AUC = {pr_auc:.4f})')
    
    # Ligne de base (proportion de fraudes dans le dataset)
    baseline = y_true.sum() / len(y_true)
    ax.plot([0, 1], [baseline, baseline], color='navy', lw=2, 
            linestyle='--', label=f'Baseline (Prop. fraudes = {baseline:.4f})')
    
    # Trouver le meilleur F1-score
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
    best_f1_idx = np.argmax(f1_scores)
    best_f1 = f1_scores[best_f1_idx]
    best_precision = precision[best_f1_idx]
    best_recall = recall[best_f1_idx]
    
    ax.plot(best_recall, best_precision, 'ro', markersize=10,
            label=f'Meilleur F1 = {best_f1:.3f}')
    
    # Configuration des axes
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('Recall (Taux de Vrais Positifs)', fontsize=11, weight='bold')
    ax.set_ylabel('Precision', fontsize=11, weight='bold')
    ax.set_title(f'Courbe Precision-Recall - {model_name}', 
                 fontsize=12, weight='bold', pad=15)
    
    # Grille et légende
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc="best", fontsize=10, framealpha=0.9)
    
    # Ajouter des annotations
    ax.text(0.6, 0.9, f'PR-AUC = {pr_auc:.4f}', 
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5),
            fontsize=12, weight='bold')
    
    return ax


def plot_model_evaluation_complete(y_true, y_proba, y_pred, model_name="Modèle", 
                                   threshold=0.5, figsize=(18, 5)):
    """
    Affiche une vue complète de l'évaluation du modèle avec 3 graphiques :
    - Matrice de confusion
    - Courbe ROC
    - Courbe Precision-Recall
    
    Paramètres:
    -----------
    y_true : array-like
        Vraies étiquettes
    y_proba : array-like
        Probabilités prédites pour la classe positive
    y_pred : array-like
        Prédictions binaires (0 ou 1)
    model_name : str
        Nom du modèle
    threshold : float
        Seuil de classification utilisé
    figsize : tuple
        Taille de la figure
    
    Retourne:
    ---------
    fig, axes : matplotlib figure et axes
    """
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    
    # 1. Matrice de confusion
    plot_confusion_matrix(y_true, y_pred, model_name, threshold, ax=axes[0])
    
    # 2. Courbe ROC
    plot_roc_curve(y_true, y_proba, model_name, ax=axes[1])
    
    # 3. Courbe Precision-Recall
    plot_precision_recall_curve(y_true, y_proba, model_name, ax=axes[2])
    
    plt.tight_layout()
    return fig, axes


def compare_models_roc(models_dict, y_true, figsize=(10, 8)):
    """
    Compare plusieurs modèles sur une seule courbe ROC
    
    Paramètres:
    -----------
    models_dict : dict
        Dictionnaire {nom_modèle: y_proba}
    y_true : array-like
        Vraies étiquettes
    figsize : tuple
        Taille de la figure
    
    Retourne:
    ---------
    fig, ax : matplotlib figure et axis
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = ['darkorange', 'green', 'red', 'purple', 'brown']
    
    for i, (model_name, y_proba) in enumerate(models_dict.items()):
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        roc_auc = auc(fpr, tpr)
        
        ax.plot(fpr, tpr, color=colors[i % len(colors)], lw=2.5,
                label=f'{model_name} (AUC = {roc_auc:.4f})')
    
    # Ligne de référence
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--',
            label='Classificateur aléatoire (AUC = 0.5000)')
    
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('Taux de Faux Positifs (FPR)', fontsize=12, weight='bold')
    ax.set_ylabel('Taux de Vrais Positifs (TPR)', fontsize=12, weight='bold')
    ax.set_title('Comparaison des Courbes ROC des Modèles', 
                 fontsize=14, weight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc="lower right", fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    return fig, ax


def print_classification_report_styled(y_true, y_pred, model_name="Modèle"):
    """
    Affiche un rapport de classification stylisé avec toutes les métriques importantes
    
    Paramètres:
    -----------
    y_true : array-like
        Vraies étiquettes
    y_pred : array-like
        Prédictions du modèle
    model_name : str
        Nom du modèle
    """
    from sklearn.metrics import classification_report, accuracy_score, balanced_accuracy_score
    
    print("=" * 70)
    print(f"📊 RAPPORT DE CLASSIFICATION - {model_name.upper()}")
    print("=" * 70)
    print()
    
    # Matrice de confusion
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("📋 Matrice de Confusion:")
    print(f"   True Negatives  (TN): {tn:,}")
    print(f"   False Positives (FP): {fp:,}")
    print(f"   False Negatives (FN): {fn:,}")
    print(f"   True Positives  (TP): {tp:,}")
    print()
    
    # Métriques globales
    accuracy = accuracy_score(y_true, y_pred)
    balanced_acc = balanced_accuracy_score(y_true, y_pred)
    
    print("📈 Métriques Globales:")
    print(f"   Accuracy         : {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   Balanced Accuracy: {balanced_acc:.4f} ({balanced_acc*100:.2f}%)")
    print()
    
    # Rapport détaillé par classe
    print("📊 Rapport Détaillé par Classe:")
    print(classification_report(y_true, y_pred, 
                                target_names=['Normal (0)', 'Fraude (1)'],
                                digits=4))
    print("=" * 70)


# Exemple d'utilisation dans un notebook:
"""
# Après avoir entraîné votre modèle et obtenu les prédictions:

# Import des fonctions
from visualizations_models import (
    plot_model_evaluation_complete, 
    compare_models_roc,
    print_classification_report_styled
)

# 1. Visualisation complète pour un modèle
fig, axes = plot_model_evaluation_complete(
    y_true=y_valid,
    y_proba=valid_proba,
    y_pred=valid_pred,
    model_name="Logistic Regression + SMOTE",
    threshold=best_thr
)
plt.show()

# 2. Rapport de classification stylisé
print_classification_report_styled(y_valid, valid_pred, "Logistic Regression + SMOTE")

# 3. Comparaison de plusieurs modèles
models_dict = {
    'Logistic Regression': logreg_proba,
    'Random Forest': rf_proba,
    'XGBoost': xgb_proba
}
fig, ax = compare_models_roc(models_dict, y_valid)
plt.show()
"""
