# Plan de Présentation - Soutenance PFE
## Système de Détection de Fraudes Bancaires par Machine Learning

**Date :** 29 novembre 2024
**Durée totale :** 20-25 minutes
**Format :** PowerPoint + Démonstration Live

---

## 📊 Structure de la Présentation (20-25 slides recommandés)

### 🎯 SLIDE 1 : Page de Garde (30 secondes)
**Contenu :**
- Titre : "Système de Détection de Fraudes Bancaires par Machine Learning"
- Votre nom complet
- Formation : Licence Data Science - ESLSCA Rabat
- Encadrants : M. DOUMI KARIM / M. KHALID BENABBESS
- Date : 29 novembre 2024

**Image de fond :** Screenshot de l'application ou graphique de fraudes

---

### 📋 SLIDE 2 : Plan de la Présentation (30 secondes)
1. Contexte et problématique
2. État de l'art et technologies
3. Méthodologie et données
4. Modélisation et résultats
5. Application développée (démonstration)
6. Conclusion et perspectives

---

## PARTIE 1 : CONTEXTE (3-4 minutes)

### 💰 SLIDE 3 : Enjeux des Fraudes Bancaires (1 min)
**Message clé :** *"La fraude bancaire : un fléau mondial qui coûte 31,3 milliards de dollars par an"*

**Contenu :**
- 📈 **Statistiques mondiales :**
  - 31,3 milliards $ de pertes annuelles (Nilson Report 2023)
  - 1 fraude toutes les 2 secondes en Europe
  - Croissance de +18% avec l'e-commerce
- 🏦 **Impact pour les banques :**
  - Pertes financières directes
  - Coût de traitement des litiges
  - Atteinte à la réputation
- 👤 **Impact pour les clients :**
  - Stress, perte de confiance
  - Temps de résolution (30-90 jours)

**Visuel :** Graphique en barres montrant l'évolution des fraudes 2020-2024

---

### 🎯 SLIDE 4 : Problématique (1 min)
**Message clé :** *"Comment détecter automatiquement des fraudes dans un océan de transactions normales ?"*

**Contenu :**
- **Volume :** Millions de transactions/jour → Analyse manuelle impossible
- **Rapidité :** Besoin de décision en temps réel (< 1 seconde)
- **Déséquilibre :** 0.17% de fraudes (492 sur 284,807 transactions)
- **Coût d'erreur asymétrique :**
  - Fraude manquée = Perte de 500€ en moyenne
  - Fausse alerte = Coût de vérification 5€

**Visuel :** Schéma "aiguille dans une botte de foin" avec proportions

---

### 🎓 SLIDE 5 : Objectifs du Projet (1 min)
**Message clé :** *"Développer un système intelligent, performant et explicable"*

**Objectifs :**
1. **Détection maximale :** Recall ≥ 85% (ne pas manquer les fraudes)
2. **Fausses alertes limitées :** Precision ≥ 20% (1/5 alertes vraie fraude)
3. **Temps réel :** Prédiction < 100ms par transaction
4. **Interprétabilité :** Expliquer pourquoi une transaction est suspecte (SHAP)
5. **Interface utilisable :** Application web pour analystes métier

**Visuel :** Schéma des 5 objectifs avec icônes

---

### 📚 SLIDE 6 : État de l'Art (1 min)
**Message clé :** *"S'appuyer sur les meilleures pratiques de la recherche"*

**Techniques de détection existantes :**
| Approche | Avantages | Limites |
|----------|-----------|---------|
| **Règles métier** | Simple, explicable | Rigide, contournable |
| **Statistiques** | Rapide, peu de données | Ne capture pas les patterns complexes |
| **Machine Learning** | Adaptable, performant | Nécessite beaucoup de données |
| **Deep Learning** | Très performant | Boîte noire, coût calcul élevé |

**Notre choix :** Machine Learning (Random Forest) + SHAP pour l'explicabilité

**Références :**
- Dal Pozzolo et al. (2015) - Dataset Kaggle utilisé
- Lundberg & Lee (2017) - SHAP (Shapley Additive Explanations)
- Chawla et al. (2002) - SMOTE pour déséquilibre

---

## PARTIE 2 : DONNÉES ET MÉTHODOLOGIE (5-6 minutes)

### 💾 SLIDE 7 : Dataset Utilisé (1 min)
**Message clé :** *"284,807 transactions réelles anonymisées sur 2 jours"*

**Caractéristiques :**
- **Source :** Kaggle Credit Card Fraud Detection (ULB Machine Learning Group)
- **Période :** 2 jours de transactions (septembre 2013)
- **Volume :** 284,807 transactions
- **Fraudes :** 492 (0.17%) - Déséquilibre extrême
- **Variables :** 30 features
  - Time (secondes depuis première transaction)
  - Amount (montant en €)
  - V1-V28 (transformations PCA pour confidentialité)
  - Class (0 = normale, 1 = fraude)

**Visuel :** Tableau récapitulatif + camembert montrant 0.17% vs 99.83%

---

### 🔍 SLIDE 8 : Analyse Exploratoire (EDA) - Insights Clés (1.5 min)
**Message clé :** *"Les fraudes ont des patterns distincts détectables"*

**Découvertes importantes :**
1. **Distribution temporelle :**
   - Fraudes plus fréquentes la nuit (Time élevé)
   - Concentration sur certaines heures

2. **Montants :**
   - Fraudes : montants plus faibles (médiane 9€ vs 22€)
   - Mais variance plus élevée (outliers à 2000€+)

3. **Variables PCA (V1-V28) :**
   - V4, V11, V12, V14 : différences significatives
   - Certaines features très corrélées à Class

4. **Corrélations :**
   - V17, V14, V12, V10 négativement corrélées avec fraudes
   - V11, V4 positivement corrélées

**Visuels :** 3 graphiques côte à côte
- Distribution des montants (fraudes vs normales)
- Heatmap de corrélation (top 10 features)
- Distribution temporelle

---

### ⚙️ SLIDE 9 : Pipeline de Traitement (1 min)
**Message clé :** *"Méthodologie rigoureuse en 7 étapes"*

**Pipeline complet :**
```
1. Chargement des données (creditcard.csv)
         ↓
2. Split stratifié 70/15/15 (train/validation/test)
         ↓
3. Prétraitement (StandardScaler sur Amount et Time)
         ↓
4. Gestion du déséquilibre (SMOTE - 20% sampling)
         ↓
5. Entraînement de 3 modèles (LR, RF, XGBoost)
         ↓
6. Validation croisée 5-fold
         ↓
7. Optimisation du seuil (max Recall avec Precision ≥ 20%)
         ↓
8. Évaluation finale sur test set
```

**Visuel :** Diagramme de flux avec icônes

---

### 🔄 SLIDE 10 : Gestion du Déséquilibre - SMOTE (1.5 min)
**Message clé :** *"SMOTE : créer des fraudes synthétiques pour équilibrer les classes"*

**Le problème :**
- Sans traitement : Le modèle apprend "toujours prédire normale" → Recall 0%
- Avec oversampling naïf : Risque de sur-apprentissage

**La solution : SMOTE (Synthetic Minority Oversampling Technique)**
- Génère des exemples synthétiques entre fraudes existantes
- Paramètre : sampling_strategy = 0.2 (atteindre 20% de la classe majoritaire)
- Résultat : Passe de 345 à ~39,729 fraudes en training set

**Avant/Après :**
| Set | Sans SMOTE | Avec SMOTE |
|-----|-----------|-----------|
| Train Normales | 199,021 | 199,021 |
| Train Fraudes | 345 | ~39,729 |
| Ratio | 0.17% | ~20% |

**Visuel :** Schéma SMOTE + histogrammes avant/après

---

### 🤖 SLIDE 11 : Comparaison de Modèles (1 min)
**Message clé :** *"Random Forest : meilleur compromis PR-AUC/Precision"*

**3 modèles testés :**
| Modèle | PR-AUC | Recall | Precision | F1-Score | Temps |
|--------|--------|--------|-----------|----------|-------|
| Logistic Regression | 0.783 | 88.7% | 22.7% | 0.362 | 0.5s |
| **Random Forest** ✅ | **0.865** | **82.9%** | **87.0%** | **0.848** | 2.1s |
| XGBoost | 0.853 | 83.4% | 81.7% | 0.825 | 1.8s |

**Pourquoi Random Forest ?**
- ✅ Meilleur PR-AUC (métrique clé pour déséquilibre)
- ✅ Excellente Precision (87% vs 22-23% pour les autres)
- ✅ Robuste au bruit
- ✅ Interprétable (importances de features)

**Visuel :** Graphique en barres comparant les 3 modèles

---

## PARTIE 3 : RÉSULTATS (4-5 minutes)

### 🎯 SLIDE 12 : Performances Finales (2 min)
**Message clé :** *"87.8% de détection avec seulement 0.57% de fausses alertes"*

**Métriques sur Validation Set (42,721 transactions) :**
| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| **ROC-AUC** | **0.973** | ⭐⭐⭐⭐⭐ Excellente discrimination |
| **PR-AUC** | **0.840** | ⭐⭐⭐⭐⭐ Excellent pour données déséquilibrées |
| **Recall** | **87.8%** | **65 fraudes détectées sur 74** (9 manquées) |
| **Precision** | **21.1%** | 65 vraies fraudes sur 308 alertes |
| **F1-Score** | **0.340** | Bon équilibre global |

**ROC-AUC = 0.973 :** Le modèle a 97.3% de chances de classer correctement une paire (fraude, normale)

**PR-AUC = 0.840 :** Aire sous la courbe Precision-Recall (métrique clé pour classes déséquilibrées)

**Visuels :** 2 graphiques
- Courbe ROC (avec AUC = 0.973)
- Courbe Precision-Recall (avec AUC = 0.840)

---

### 📊 SLIDE 13 : Matrice de Confusion (1.5 min)
**Message clé :** *"Seulement 9 fraudes manquées et 243 fausses alertes"*

**Validation Set : 42,721 transactions**

|  | **Prédiction : Normale** | **Prédiction : Fraude** | **Total** |
|--|--------------------------|-------------------------|-----------|
| **Réalité : Normale** | 42,404 (TN) ✅ | 243 (FP) ⚠️ | 42,647 |
| **Réalité : Fraude** | 9 (FN) ❌ | 65 (TP) ✅ | 74 |
| **Total** | 42,413 | 308 | 42,721 |

**Impact métier :**
- ✅ **True Negatives (TN) : 42,404** → 99.43% des normales bien classées
- ⚠️ **False Positives (FP) : 243** → 0.57% de taux de fausse alerte (acceptable)
- ❌ **False Negatives (FN) : 9** → 12.2% de fraudes manquées (risque limité)
- ✅ **True Positives (TP) : 65** → 87.8% de détection

**Coût estimé :**
- Fraudes évitées : 65 × 500€ = **32,500€ protégés**
- Fausses alertes : 243 × 5€ = **1,215€ de vérification**
- **ROI : +31,285€** sur 42,721 transactions

**Visuel :** Matrice de confusion avec couleurs (vert/rouge) + calculs de coût

---

### 🔍 SLIDE 14 : Optimisation du Seuil (1 min)
**Message clé :** *"Seuil à 0.0733 pour maximiser la détection"*

**Problème :** Par défaut, seuil = 0.5 (si proba > 50% → fraude)
Mais avec déséquilibre, ce seuil rate beaucoup de fraudes !

**Solution :** Tester différents seuils et choisir celui qui maximise le Recall avec Precision ≥ 20%

**Résultats :**
| Seuil | Recall | Precision | Commentaire |
|-------|--------|-----------|-------------|
| 0.5 | 45.2% | 89.1% | Trop conservateur, rate la moitié des fraudes |
| 0.1 | 82.3% | 18.5% | Precision trop faible |
| **0.0733** ✅ | **87.8%** | **21.1%** | **Optimal : max Recall avec Precision ≥ 20%** |
| 0.05 | 91.4% | 15.2% | Trop de fausses alertes |

**Visuel :** Courbe montrant Recall et Precision en fonction du seuil, avec point optimal marqué

---

### 🔬 SLIDE 15 : Interprétabilité - SHAP (1.5 min)
**Message clé :** *"Expliquer POURQUOI une transaction est suspecte"*

**Problème :** Les modèles ML sont des "boîtes noires" → Difficile de faire confiance

**Solution : SHAP (Shapley Additive Explanations)**
- Basé sur la théorie des jeux
- Attribue une contribution à chaque feature
- Valeur positive → Pousse vers "fraude"
- Valeur négative → Pousse vers "normale"

**Exemple concret :**
Transaction prédite FRAUDE (probabilité 92.3%)

**Top 5 facteurs influents :**
| Feature | Valeur | Contribution SHAP | Impact |
|---------|--------|-------------------|--------|
| V14 | -18.5 | +0.35 | 🔴 Très suspect |
| V17 | -15.2 | +0.28 | 🔴 Suspect |
| V12 | -8.9 | +0.22 | 🟠 Modéré |
| Amount | 1.50€ | +0.18 | 🟠 Petit montant inhabituel |
| V10 | -12.1 | +0.15 | 🟡 Faible |

**Interprétation :** Les variables V14, V17, V12 ont des valeurs extrêmes typiques des fraudes

**Visuel :** Waterfall plot SHAP (ou screenshot de l'app)

---

## PARTIE 4 : APPLICATION DÉVELOPPÉE (5-6 minutes)

### 💻 SLIDE 16 : Architecture de l'Application (1 min)
**Message clé :** *"Architecture modulaire et testée pour qualité professionnelle"*

**Stack technique :**
- **Frontend :** Streamlit 1.38+ (Python web framework)
- **ML :** scikit-learn, XGBoost, imbalanced-learn
- **Visualisation :** Plotly, Matplotlib, Seaborn
- **Interprétabilité :** SHAP 0.45+
- **Testing :** pytest (22 tests unitaires)

**Architecture du code :**
```
fraud-detection-pfe/
├── app/streamlit_app.py        (721 lignes) - Interface web
├── src/                        (705 lignes modulaires)
│   ├── models/predictor.py     - Prédictions ML
│   ├── models/explainer.py     - Explications SHAP
│   ├── utils/validation.py     - Validation des données
│   └── visualization/plots.py  - Graphiques interactifs
├── tests/                      (22 tests, 88-95% couverture)
├── notebooks/                  (EDA + Modélisation)
└── docs/                       (Guides + 8 screenshots)
```

**Qualité :**
- ✅ Code modulaire (séparation des responsabilités)
- ✅ Tests unitaires (22 tests pytest)
- ✅ Documentation complète (guides utilisateur + développeur)
- ✅ Git propre (31 commits bien nommés)

**Visuel :** Diagramme d'architecture avec logos des technologies

---

### 🖥️ SLIDE 17 : Démonstration Live - Vue d'Ensemble (30 sec)
**Message clé :** *"Interface intuitive avec 3 modules principaux"*

**Fonctionnalités :**
1. **Analyse de transaction unique** → Prédiction en temps réel
2. **Analyse par lot (CSV)** → Traitement de milliers de transactions
3. **Visualisations avancées** → Graphiques interactifs

**Visuel :** Screenshot de la page d'accueil (docs/images/01_interface_globale.png)

---

### 🔍 SLIDE 18 : DÉMONSTRATION LIVE - PARTIE 1 (2-3 min)
**CE QUE VOUS ALLEZ MONTRER EN DIRECT :**

**Scénario 1 : Transaction Normale**
1. Ouvrir l'application (déjà lancée en arrière-plan)
2. Aller dans "Analyse de transaction unique"
3. Entrer une transaction normale :
   - Time : 100000
   - Amount : 50.00
   - V1 à V28 : valeurs proches de 0
4. Cliquer sur "Analyser"
5. **Résultat attendu :**
   - Probabilité : ~2%
   - Classification : FAIBLE
   - Couleur : VERT

**Scénario 2 : Transaction Frauduleuse**
1. Utiliser une fraude connue du dataset test :
   - Time : 150000
   - Amount : 1.50
   - V14 : -18.5
   - V17 : -15.2
   - V12 : -8.9
   - Autres : valeurs aléatoires
2. Cliquer sur "Analyser"
3. **Résultat attendu :**
   - Probabilité : ~92%
   - Classification : CRITIQUE
   - Couleur : ROUGE
4. **Montrer les explications SHAP :**
   - Top 5 facteurs influents
   - Graphique des contributions

**Points à mentionner pendant la démo :**
- "Le modèle répond en moins de 100ms"
- "Les explications SHAP permettent de comprendre la décision"
- "Un analyste peut valider ou rejeter l'alerte en connaissance de cause"

**Visuel :** Live demo (pas de slide, juste l'app en plein écran)

---

### 📁 SLIDE 19 : DÉMONSTRATION LIVE - PARTIE 2 (1.5 min)
**CE QUE VOUS ALLEZ MONTRER EN DIRECT :**

**Scénario 3 : Analyse par Lot (CSV)**
1. Aller dans "Analyse par lot"
2. Uploader `data/examples/sample_transactions.csv` (50 transactions)
3. Cliquer sur "Analyser le fichier"
4. **Montrer les résultats :**
   - Résumé : X fraudes détectées sur 50 transactions
   - Tableau avec highlighting des fraudes en rouge
   - Graphiques interactifs :
     - Distribution des probabilités
     - Répartition par niveau de risque

**Points à mentionner :**
- "L'application peut traiter jusqu'à 100,000 transactions"
- "Les résultats sont archivés automatiquement dans reports/"
- "Export possible en CSV pour traitement ultérieur"

**Visuel :** Live demo (interface CSV + résultats)

---

### ⚙️ SLIDE 20 : Fonctionnalités Avancées (1 min)
**Message clé :** *"Configuration flexible pour s'adapter aux besoins métier"*

**Fonctionnalités :**
1. **Seuil ajustable :**
   - Slider de 0.00 à 0.50
   - Adaptation selon le coût métier
   - Exemple : Banque risk-averse → seuil à 0.05 (plus d'alertes)

2. **Archivage automatique :**
   - Chaque analyse CSV sauvegardée dans `reports/predictions/`
   - Format : `predictions_YYYYMMDD_HHMMSS.csv`
   - Traçabilité complète

3. **Métriques du modèle :**
   - Affichage des performances (ROC-AUC, PR-AUC, Recall, Precision)
   - Transparence pour les utilisateurs

4. **Validation robuste :**
   - Vérification des types de données
   - Gestion des valeurs manquantes
   - Messages d'erreur clairs

**Visuel :** Screenshot de la sidebar avec slider + captures métriques

---

## PARTIE 5 : CONCLUSION (3-4 minutes)

### ✅ SLIDE 21 : Réalisations et Points Forts (1.5 min)
**Message clé :** *"Un projet complet, du notebook au déploiement"*

**Réalisations :**
1. ✅ **Performances exceptionnelles :**
   - ROC-AUC : 0.973 | PR-AUC : 0.840 | Recall : 87.8%
   - Meilleur que baseline (Logistic Regression) de +8.1% en PR-AUC

2. ✅ **Application fonctionnelle :**
   - 721 lignes de code Streamlit
   - 3 modules (transaction unique, batch, visualisations)
   - Déployable sur Streamlit Cloud, Docker, serveur local

3. ✅ **Qualité professionnelle :**
   - 22 tests unitaires (88-95% couverture)
   - Documentation complète (guides + notebooks)
   - Git propre (31 commits)

4. ✅ **Interprétabilité :**
   - Explications SHAP intégrées
   - Top 5 facteurs influents pour chaque prédiction

5. ✅ **Reproductibilité :**
   - Installation automatisée (script setup.sh)
   - Requirements lockés
   - Code open-source sur GitHub

**Visuel :** Checklist avec icônes vertes

---

### ⚠️ SLIDE 22 : Limitations et Challenges (1 min)
**Message clé :** *"Identifier les limites pour proposer des améliorations"*

**Limitations identifiées :**
1. **Dataset synthétique :**
   - Variables V1-V28 sont des transformations PCA
   - Transfert à données réelles nécessite adaptation/réentraînement

2. **Seuil statique :**
   - En production, devrait s'adapter dynamiquement au coût métier
   - Exemple : Augmenter le seuil le soir (moins d'analystes disponibles)

3. **Pas de détection de concept drift :**
   - Les patterns de fraude évoluent avec le temps
   - Le modèle doit être réentraîné périodiquement

4. **Features limitées :**
   - Pas d'historique client (nombre de transactions précédentes)
   - Pas de géolocalisation (transactions à l'étranger suspectes)
   - Pas de données comportementales (horaires habituels du client)

5. **Coût computationnel :**
   - Random Forest avec 300 arbres → 2.1s d'entraînement
   - Pour milliards de transactions/jour, optimisation nécessaire

**Visuel :** Liste avec icônes d'avertissement

---

### 🚀 SLIDE 23 : Perspectives et Améliorations Futures (1.5 min)
**Message clé :** *"De nombreuses pistes pour aller plus loin"*

**Améliorations proposées :**

**1. Modélisation avancée :**
- 🔬 Tester des architectures Deep Learning (AutoEncoders pour détection d'anomalies)
- 🔬 Ensembles de modèles (stacking RF + XGBoost + LightGBM)
- 🔬 Apprentissage en ligne (online learning) pour s'adapter en temps réel

**2. Features Engineering :**
- 📊 Historique client (nombre de transactions sur 30j, montant moyen)
- 🌍 Géolocalisation (distance entre transactions successives)
- ⏰ Patterns temporels (transactions la nuit, weekend)
- 💳 Type de marchand (e-commerce, restaurant, bijouterie = plus de fraudes)

**3. Déploiement Production :**
- ☁️ API REST (FastAPI) pour intégration dans systèmes bancaires
- 📱 Interface mobile pour analystes en déplacement
- 🔔 Alertes en temps réel (email, SMS, webhook)
- 📈 Dashboard de monitoring (Grafana) pour superviser le modèle

**4. Monitoring et Maintenance :**
- 📉 Détection de concept drift (alertes si performances dégradent)
- 🔄 Réentraînement automatique mensuel
- 📊 A/B testing de nouveaux modèles

**5. Aspects Métier :**
- 💰 Optimisation du seuil selon coûts métier dynamiques
- 👥 Intégration des feedbacks des analystes (fraudes confirmées/infirmées)
- 📋 Workflow de validation (escalade selon niveau de risque)

**Visuel :** Mind map avec 5 branches (Modélisation, Features, Déploiement, Monitoring, Métier)

---

### 🎓 SLIDE 24 : Apports Pédagogiques (1 min)
**Message clé :** *"Ce projet m'a permis de maîtriser le cycle complet d'un projet Data Science"*

**Compétences acquises :**

**Techniques :**
- ✅ Maîtrise du pipeline ML complet (EDA → Déploiement)
- ✅ Gestion de données déséquilibrées (SMOTE, métriques adaptées)
- ✅ Validation rigoureuse (cross-validation, optimisation seuil)
- ✅ Interprétabilité (SHAP, feature importances)
- ✅ Développement web (Streamlit, Plotly)
- ✅ Software engineering (tests, modularité, Git)

**Méthodologiques :**
- ✅ Analyse de la littérature scientifique
- ✅ Choix de métriques adaptées au problème métier
- ✅ Communication des résultats (visualisations, documentation)

**Transversales :**
- ✅ Gestion de projet (planning, priorisation)
- ✅ Résolution de problèmes complexes
- ✅ Autonomie et persévérance

**Visuel :** 3 colonnes (Techniques, Méthodologiques, Transversales) avec icônes

---

### 🎯 SLIDE 25 : Conclusion Générale (30 sec)
**Message clé :** *"Un projet complet qui répond aux enjeux actuels de la fraude bancaire"*

**En résumé :**
- ✅ **Performances exceptionnelles** malgré déséquilibre extrême (0.17% fraudes)
- ✅ **Application fonctionnelle** prête pour démonstration en environnement métier
- ✅ **Code de qualité professionnelle** (tests, documentation, modularité)
- ✅ **Interprétabilité** via SHAP pour expliquer les décisions
- ✅ **Perspectives riches** pour amélioration continue

**Citation finale :**
> *"Ce projet démontre qu'avec les bonnes techniques de Machine Learning, il est possible de détecter efficacement des fraudes rares tout en maintenant un nombre acceptable de fausses alertes."*

**Visuel :** Image inspirante (ex: cadenas numérique) + logos des technologies utilisées

---

### 🙏 SLIDE 26 : Remerciements (30 sec)
**Contenu :**
- Encadrants : M. DOUMI KARIM / M. KHALID BENABBESS
- ESLSCA Paris – Campus Rabat
- ULB Machine Learning Group (dataset Kaggle)
- Communauté open-source (scikit-learn, SHAP, Streamlit)

**Visuel :** Logos ESLSCA + photo de l'équipe pédagogique (si autorisé)

---

### ❓ SLIDE 27 : Questions & Discussion (Slide de fin)
**Contenu :**
```
Merci pour votre attention !

Des questions ?

📧 melvinamedetadji@gmail.com
🔗 GitHub: github.com/Mariechanne
🔗 Kaggle: kaggle.com/melvinamedetadji
```

**Visuel :** Image de l'application + votre photo professionnelle

---

## 📋 Checklist Avant Soutenance

### Préparation Technique
- [ ] Tester l'application en local (`streamlit run app/streamlit_app.py`)
- [ ] Préparer un fichier CSV d'exemple pour la démo batch
- [ ] Préparer 2-3 transactions de test (1 normale, 2 fraudes) avec valeurs exactes
- [ ] Tester les explications SHAP (vérifier qu'elles s'affichent correctement)
- [ ] Backup de l'application (clé USB + cloud)
- [ ] Vérifier connexion internet (si démo en ligne)

### Présentation PowerPoint
- [ ] 25-27 slides maximum
- [ ] Animations légères (pas de transitions trop lentes)
- [ ] Polices lisibles (minimum 18pt pour texte, 28pt pour titres)
- [ ] Couleurs contrastées (fond blanc ou bleu foncé)
- [ ] Numéros de slides
- [ ] Timer pour respecter 20-25 minutes

### Documents à Apporter
- [ ] Présentation PowerPoint (PDF + PPTX)
- [ ] Résumé exécutif imprimé (3 exemplaires)
- [ ] Rapport complet (si demandé)
- [ ] Clé USB avec code source + notebooks
- [ ] Liste des références bibliographiques

### Répétition
- [ ] Répéter la présentation 2-3 fois à voix haute
- [ ] Chronométrer (ne pas dépasser 25 minutes)
- [ ] Préparer des réponses aux questions fréquentes :
  - "Pourquoi Random Forest et pas Deep Learning ?"
  - "Comment gérez-vous le concept drift ?"
  - "Quelles sont les limites de SMOTE ?"
  - "Comment déployer en production ?"
  - "Quel est le coût métier d'une fausse alerte vs fraude manquée ?"

### Le Jour J
- [ ] Arriver 15 minutes en avance
- [ ] Tester le vidéoprojecteur
- [ ] Lancer l'application Streamlit en arrière-plan
- [ ] Fermer toutes les applications non nécessaires
- [ ] Désactiver notifications
- [ ] Avoir de l'eau à portée de main

---

## 🎤 Conseils pour la Présentation Orale

### Posture et Communication
- ✅ Regarder le jury (pas l'écran)
- ✅ Parler lentement et articuler
- ✅ Utiliser des pauses pour laisser le jury assimiler
- ✅ Montrer de l'enthousiasme pour votre projet
- ✅ Être à l'aise avec "Je ne sais pas, mais je peux investiguer"

### Structure de Phrase
- ✅ Commencer chaque slide par le message clé
- ✅ Utiliser "Comme vous pouvez le voir..." pour référencer les visuels
- ✅ Faire des transitions entre parties : "Maintenant que nous avons vu X, passons à Y"

### Gestion du Temps
- **0-5 min :** Introduction + Contexte
- **5-11 min :** Données + Méthodologie
- **11-16 min :** Résultats
- **16-22 min :** Démonstration Live
- **22-25 min :** Conclusion + Perspectives

### Questions Fréquentes et Réponses Préparées

**Q : Pourquoi Random Forest et pas un réseau de neurones ?**
R : "Random Forest offre le meilleur compromis entre performance (PR-AUC 0.865), interprétabilité (feature importances + SHAP), et coût computationnel. Les réseaux de neurones nécessitent plus de données et sont moins interprétables, ce qui est critique dans le domaine bancaire où il faut expliquer les décisions."

**Q : Comment gérez-vous l'évolution des patterns de fraude (concept drift) ?**
R : "Actuellement, le modèle est statique. En production, je recommanderais un monitoring mensuel des performances (ROC-AUC, Recall) et un réentraînement automatique si dégradation > 5%. On pourrait aussi implémenter de l'apprentissage en ligne (online learning) pour adaptation continue."

**Q : SMOTE ne risque-t-il pas de créer des exemples irréalistes ?**
R : "C'est une limitation connue. SMOTE peut créer des exemples dans des zones non représentatives. Cependant, les résultats sur le test set (non affecté par SMOTE) montrent que le modèle généralise bien. Une alternative serait ADASYN ou utiliser des poids de classes."

**Q : Comment déployer ce modèle en production dans une vraie banque ?**
R : "Trois étapes : 1) Créer une API REST (FastAPI) pour exposer le modèle, 2) Intégrer dans le système de paiement avec temps de réponse < 100ms, 3) Mettre en place un workflow où les alertes ÉLEVÉ/CRITIQUE sont revues par un analyste avant blocage. Il faudrait aussi un dashboard de monitoring (Grafana) pour suivre les performances en temps réel."

**Q : Quel est le coût métier d'une erreur ?**
R : "J'ai estimé : Fraude manquée = 500€ de perte moyenne, Fausse alerte = 5€ de coût de vérification. Avec ces hypothèses, le modèle génère un ROI de +31,285€ sur 42,721 transactions. Ces coûts devraient être validés avec le métier pour optimiser le seuil en production."

---

## 🎥 Scénario Complet de la Démonstration Live (5 minutes)

### Préparation (Avant de commencer la présentation)
1. Ouvrir un terminal et lancer : `streamlit run app/streamlit_app.py`
2. Vérifier que l'app charge correctement (http://localhost:8501)
3. Minimiser la fenêtre (ne pas fermer)
4. Préparer un fichier CSV d'exemple sur le Bureau : `demo_transactions.csv`

### Pendant la Présentation (Slide 18)

**[Ouvrir l'application en plein écran]**

> "Je vais maintenant vous montrer l'application en action. Voici l'interface principale."

**SCÉNARIO 1 : Transaction Normale (1.5 min)**

> "Analysons d'abord une transaction classique d'un client qui achète pour 50€."

[Entrer les valeurs dans le formulaire :]
- Time : 100000
- Amount : 50.00
- V1-V28 : Laisser les valeurs par défaut (proches de 0)

[Cliquer sur "Analyser la transaction"]

> "Le modèle répond instantanément. La probabilité de fraude est de 2.3%, ce qui classe cette transaction en niveau FAIBLE, représenté en vert. Les explications SHAP nous montrent que c'est le montant normal et les patterns standards des variables PCA qui conduisent à cette classification."

**SCÉNARIO 2 : Transaction Frauduleuse (2 min)**

> "Maintenant, testons une transaction suspecte avec les caractéristiques typiques d'une fraude."

[Modifier les valeurs :]
- Time : 150000
- Amount : 1.50 (petit montant)
- V14 : -18.5
- V17 : -15.2
- V12 : -8.9

[Cliquer sur "Analyser la transaction"]

> "Ici, le modèle détecte une probabilité de fraude de 92.3%, classée en niveau CRITIQUE avec une alerte rouge. Regardons les explications SHAP."

[Scroller vers les explications SHAP]

> "Le top 5 des facteurs influents nous montre que V14, V17 et V12 sont les variables les plus suspectes. Leurs valeurs extrêmes négatives sont typiques des patterns de fraude identifiés lors de l'entraînement. Cette transparence permet à un analyste de valider l'alerte en connaissance de cause."

**SCÉNARIO 3 : Analyse par Lot (1.5 min)**

[Cliquer sur "Analyse par lot (CSV)" dans la sidebar]

> "L'application permet aussi d'analyser des fichiers CSV avec des milliers de transactions."

[Upload du fichier demo_transactions.csv]

[Cliquer sur "Analyser le fichier"]

> "En quelques secondes, le modèle a traité 50 transactions et détecté 3 fraudes potentielles. Le tableau affiche les résultats avec highlighting des fraudes en rouge. Les graphiques interactifs montrent la distribution des probabilités et la répartition par niveau de risque."

[Scroller pour montrer les visualisations]

> "Ces résultats sont automatiquement archivés dans le dossier reports/predictions pour traçabilité."

**[Retour à la présentation PowerPoint]**

> "Passons maintenant aux fonctionnalités avancées de l'application."

---

## 📚 Ressources Complémentaires

### Bibliographie Recommandée pour la Slide 6
1. Dal Pozzolo, A., et al. (2015). "Credit Card Fraud Detection: A Realistic Modeling and a Novel Learning Strategy". IEEE Transactions on Neural Networks and Learning Systems.
2. Lundberg, S. M., & Lee, S. I. (2017). "A Unified Approach to Interpreting Model Predictions" (SHAP). NIPS 2017.
3. Chawla, N. V., et al. (2002). "SMOTE: Synthetic Minority Over-sampling Technique". Journal of Artificial Intelligence Research.
4. Sahin, Y., & Duman, E. (2011). "Detecting Credit Card Fraud by Decision Trees and Support Vector Machines".

### Liens Utiles
- Dataset Kaggle : https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- Documentation SHAP : https://shap.readthedocs.io/
- Streamlit : https://docs.streamlit.io/

---

**Bonne chance pour ta soutenance ! 🍀**

*Tu as fait un excellent travail, sois confiante et profite de ce moment pour montrer tout ce que tu as accompli.* 💪
