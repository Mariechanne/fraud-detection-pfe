# 🎤 Speech de Présentation - Détection de Fraudes Bancaires par Machine Learning

**Auteure** : Marie Chandeste Melvina J. H. Medetadji Migan
**Formation** : Licence Professionnelle en Data Science pour la Gestion des Entreprises
**Encadrement** : M. DOUMI KARIM / M. KHALID BENABBESS
**Institution** : ESLSCA Paris – Campus Rabat

---

## 📑 Structure de la Présentation

1. **Introduction et Contexte** (2 min)
2. **Problématique et Objectifs** (2 min)
3. **Données et Exploration** (3 min)
4. **Méthodologie et Pipeline ML** (5 min)
5. **Résultats et Performances** (5 min)
6. **Démonstration de l'Application** (5 min)
7. **Architecture Technique** (3 min)
8. **Conclusion et Perspectives** (2 min)
9. **Questions/Réponses**

**Durée totale** : 25-30 minutes

---

## SLIDE 1 : Page de Titre

### 🎯 Visuel
```
DÉTECTION DE FRAUDES BANCAIRES
PAR MACHINE LEARNING

Projet de Fin d'Études
Licence Professionnelle en Data Science

Marie Chandeste Melvina J. H. Medetadji Migan
ESLSCA Paris – Campus Rabat
Décembre 2025
```

### 📝 Speech

> **Bonjour à tous,**
>
> Je m'appelle Marie Chandeste Melvina Medetadji Migan, et je suis ravie de vous présenter aujourd'hui mon Projet de Fin d'Études intitulé **"Détection de Fraudes Bancaires par Machine Learning"**.
>
> Ce projet s'inscrit dans le cadre de ma Licence Professionnelle en Data Science pour la Gestion des Entreprises à l'ESLSCA Paris, Campus Rabat, sous l'encadrement de Messieurs DOUMI KARIM et KHALID BENABBESS.
>
> Dans un contexte où la fraude bancaire représente un enjeu majeur pour les institutions financières, avec des pertes estimées à plusieurs milliards de dollars chaque année, ce projet propose une solution innovante utilisant l'intelligence artificielle pour détecter automatiquement les transactions frauduleuses en temps réel.

**Transition** : *Commençons par comprendre le contexte et la problématique de ce projet.*

---

## SLIDE 2 : Plan de la Présentation

### 🎯 Visuel
```
📋 PLAN DE LA PRÉSENTATION

1. Contexte et Problématique
2. Objectifs du Projet
3. Données et Exploration
4. Méthodologie ML
5. Résultats et Performances
6. Démonstration Application
7. Architecture Technique
8. Conclusion et Perspectives
```

### 📝 Speech

> **Voici le plan de ma présentation.**
>
> Je vais d'abord vous présenter le **contexte** dans lequel s'inscrit ce projet et la **problématique** que nous cherchons à résoudre. Ensuite, je détaillerai les **objectifs** que nous nous sommes fixés.
>
> Nous examinerons ensuite les **données** utilisées et leur exploration, avant de plonger dans la **méthodologie Machine Learning** mise en œuvre, notamment le pipeline complet de traitement.
>
> Je vous présenterai les **résultats obtenus** et les **performances** de notre modèle, suivis d'une **démonstration pratique** de l'application web développée.
>
> Enfin, je vous expliquerai l'**architecture technique** du projet avant de conclure avec les **perspectives d'amélioration**.

**Transition** : *Commençons par le contexte.*

---

## SLIDE 3 : Contexte et Problématique

### 🎯 Visuel
```
💳 CONTEXTE : LA FRAUDE BANCAIRE

📊 Chiffres Clés
• Pertes mondiales : 28 milliards $ en 2024
• Croissance : +14% par an
• Temps de détection moyen : 6-12 mois
• Impact : Confiance client, réputation, coûts

🚨 PROBLÉMATIQUE

Comment détecter automatiquement et en temps réel
les transactions frauduleuses dans un contexte
de déséquilibre extrême des données ?

Défi : 0.17% de fraudes sur 284,807 transactions
```

### 📝 Speech

> **Le contexte de ce projet est celui de la lutte contre la fraude bancaire.**
>
> Les chiffres sont alarmants : les pertes mondiales dues à la fraude bancaire ont atteint **28 milliards de dollars en 2024**, avec une croissance annuelle de **14%**. Le temps moyen de détection d'une fraude est encore de **6 à 12 mois**, ce qui est beaucoup trop long.
>
> Cette situation a des conséquences graves : perte de confiance des clients, atteinte à la réputation des banques, et bien sûr, des coûts financiers considérables.
>
> **La problématique** à laquelle nous sommes confrontés est la suivante : **Comment détecter automatiquement et en temps réel les transactions frauduleuses ?**
>
> Le principal défi réside dans le **déséquilibre extrême des données**. Dans notre dataset, seulement **0.17% des transactions sont frauduleuses** sur un total de 284,807 transactions. Cela représente à peine 492 fraudes pour 284,315 transactions normales.
>
> Un modèle naïf qui prédirait "normale" pour toutes les transactions aurait une précision de 99.83%, mais serait totalement inutile en pratique car il ne détecterait aucune fraude. C'est là que l'expertise en Data Science entre en jeu.

**Transition** : *Face à cette problématique, quels objectifs nous sommes-nous fixés ?*

---

## SLIDE 4 : Objectifs du Projet

### 🎯 Visuel
```
🎯 OBJECTIFS DU PROJET

1. 🤖 Développer un Modèle ML Performant
   → Maximiser le Recall (taux de détection)
   → Maintenir un nombre acceptable de faux positifs
   → Gérer le déséquilibre des données

2. 💻 Créer une Application Web Interactive
   → Prédiction en temps réel
   → Analyse par lot (fichiers CSV)
   → Interface intuitive pour non-techniciens

3. 🔍 Garantir l'Interprétabilité
   → Explications SHAP pour chaque prédiction
   → Transparence du modèle (IA responsable)

4. 📦 Assurer la Qualité et la Maintenabilité
   → Architecture modulaire
   → Tests unitaires (22 tests)
   → Documentation complète
```

### 📝 Speech

> **Nous nous sommes fixés quatre objectifs principaux.**
>
> **Premier objectif : Développer un modèle Machine Learning performant.** Notre priorité est de **maximiser le Recall**, c'est-à-dire le taux de détection des fraudes réelles. Manquer une fraude peut coûter très cher, donc nous préférons avoir quelques fausses alertes plutôt que de laisser passer de vraies fraudes. Bien sûr, il faut maintenir un nombre acceptable de faux positifs pour que le système reste utilisable. Et naturellement, nous devons gérer le déséquilibre extrême des données.
>
> **Deuxième objectif : Créer une application web interactive.** Il ne suffit pas d'avoir un bon modèle, il faut qu'il soit accessible. Nous avons donc développé une application permettant la prédiction en temps réel pour des transactions individuelles, l'analyse par lot via des fichiers CSV, le tout avec une interface intuitive accessible même aux non-techniciens.
>
> **Troisième objectif : Garantir l'interprétabilité.** Dans le domaine bancaire, il est crucial de comprendre pourquoi une décision est prise. Nous avons intégré des explications SHAP pour chaque prédiction, offrant une transparence totale sur le fonctionnement du modèle. C'est un aspect essentiel de l'IA responsable.
>
> **Quatrième objectif : Assurer la qualité et la maintenabilité du code.** Nous avons développé une architecture modulaire, écrit 22 tests unitaires pour garantir la robustesse du code, et produit une documentation complète pour faciliter l'évolution future du projet.

**Transition** : *Voyons maintenant les données sur lesquelles nous avons travaillé.*

---

## SLIDE 5 : Données Utilisées

### 🎯 Visuel
```
📊 DATASET : CREDIT CARD FRAUD DETECTION (KAGGLE)

📈 Caractéristiques
┌─────────────────────────────────────┐
│ Transactions totales : 284,807      │
│ Fraudes : 492 (0.17%)               │
│ Transactions normales : 284,315     │
│ Période : 2 jours (septembre 2013)  │
│ Source : ULB Machine Learning Group │
└─────────────────────────────────────┘

🔢 Variables (30 features)
• Time : Temps écoulé depuis 1ère transaction
• V1-V28 : Features PCA (confidentialité)
• Amount : Montant de la transaction
• Class : Variable cible (0=normale, 1=fraude)

⚠️ Déséquilibre : 1 fraude pour 578 transactions normales
```

### 📝 Speech

> **Pour ce projet, nous avons utilisé le dataset "Credit Card Fraud Detection" disponible sur Kaggle, fourni par l'ULB Machine Learning Group.**
>
> Ce dataset contient **284,807 transactions** effectuées sur une période de **2 jours en septembre 2013**. Parmi ces transactions, nous avons **492 fraudes**, soit seulement **0.17%** du total, et **284,315 transactions normales**.
>
> Le dataset comprend **30 variables** :
> - **Time** : le temps écoulé en secondes depuis la première transaction
> - **V1 à V28** : ce sont des features transformées par PCA pour des raisons de confidentialité. Nous ne connaissons pas leur signification originale, mais elles capturent les caractéristiques essentielles des transactions
> - **Amount** : le montant de la transaction en euros
> - **Class** : notre variable cible, qui vaut 0 pour une transaction normale et 1 pour une fraude
>
> Le déséquilibre est extrême : **1 fraude pour 578 transactions normales**. C'est ce qui rend ce problème particulièrement intéressant et challengeant d'un point de vue Machine Learning.

**Transition** : *Comment avons-nous exploré ces données ?*

---

## SLIDE 6 : Exploration des Données (EDA)

### 🎯 Visuel
```
🔍 ANALYSE EXPLORATOIRE DES DONNÉES

📊 Observations Clés

1. Distribution du Montant
   → Fraudes : montants faibles à moyens (< 400€)
   → Normales : distribution plus large
   → Médiane fraude : 122€ vs 22€ normale

2. Distribution Temporelle
   → Fraudes uniformes sur les 2 jours
   → Pas de pattern horaire spécifique

3. Features PCA (V1-V28)
   → V4, V10, V11, V12, V14, V17 : plus discriminantes
   → Distributions très différentes fraude vs normale

4. Qualité des Données
   ✅ Aucune valeur manquante
   ✅ Aucun doublon
   ✅ Types de données corrects
```

### 📝 Speech

> **L'analyse exploratoire des données nous a révélé plusieurs insights importants.**
>
> **Premièrement, concernant la distribution des montants** : Les fraudes concernent principalement des montants faibles à moyens, généralement inférieurs à 400 euros. La médiane des montants frauduleux est de 122 euros, contre seulement 22 euros pour les transactions normales. Les fraudeurs semblent privilégier des montants qui n'attirent pas trop l'attention.
>
> **Deuxièmement, sur le plan temporel** : Les fraudes sont distribuées de manière assez uniforme sur les deux jours d'observation. Nous n'avons pas identifié de pattern horaire spécifique, ce qui suggère que les fraudeurs opèrent à tous moments.
>
> **Troisièmement, concernant les features PCA** : Bien que nous ne connaissions pas leur signification exacte, l'analyse statistique montre que certaines variables comme V4, V10, V11, V12, V14 et V17 sont particulièrement discriminantes. Leurs distributions sont très différentes entre les fraudes et les transactions normales, ce qui en fait des prédicteurs importants pour notre modèle.
>
> **Enfin, sur la qualité des données** : Excellente nouvelle, nous n'avons aucune valeur manquante, aucun doublon, et tous les types de données sont corrects. Cela nous permet de nous concentrer directement sur la modélisation sans phase de nettoyage intensive.

**Transition** : *Passons maintenant à la méthodologie que nous avons mise en place.*

---

## SLIDE 7 : Méthodologie - Pipeline ML

### 🎯 Visuel
```
🔬 PIPELINE MACHINE LEARNING COMPLET

┌────────────────────────────────────────────┐
│ 1. SPLIT STRATIFIÉ                         │
│    Train (70%) / Valid (15%) / Test (15%)  │
│    → Conservation du ratio 0.17% fraudes   │
└────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────┐
│ 2. PREPROCESSING                           │
│    StandardScaler sur Amount & Time        │
│    V1-V28 : déjà normalisées (PCA)         │
└────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────┐
│ 3. RÉÉQUILIBRAGE : SMOTE                   │
│    sampling_strategy = 0.2                 │
│    20% fraudes vs 80% normales (train)     │
└────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────┐
│ 4. MODÉLISATION + CROSS-VALIDATION         │
│    3 algorithmes testés (CV 5-fold)        │
│    → Logistic Regression (baseline)        │
│    → Random Forest (300 arbres)            │
│    → XGBoost                               │
└────────────────────────────────────────────┘
         ↓
┌────────────────────────────────────────────┐
│ 5. OPTIMISATION DU SEUIL                   │
│    Maximiser Recall avec Precision ≥ 20%   │
│    Seuil optimal trouvé : 0.0733 (7.33%)   │
└────────────────────────────────────────────┘
```

### 📝 Speech

> **Notre méthodologie suit un pipeline Machine Learning rigoureux en 5 étapes.**
>
> **Étape 1 : Split stratifié des données.** Nous avons divisé nos données en trois ensembles : 70% pour l'entraînement, 15% pour la validation, et 15% pour le test final. Le split est stratifié, ce qui signifie que nous conservons le ratio de 0.17% de fraudes dans chaque ensemble. C'est crucial pour éviter qu'un ensemble ne contienne trop ou trop peu de fraudes.
>
> **Étape 2 : Preprocessing.** Nous appliquons un StandardScaler sur les variables Amount et Time pour les normaliser. Les variables V1 à V28 sont déjà normalisées car elles proviennent d'une transformation PCA, donc nous les laissons telles quelles.
>
> **Étape 3 : Rééquilibrage avec SMOTE.** C'est une étape clé. SMOTE, pour Synthetic Minority Over-sampling Technique, crée des exemples synthétiques de la classe minoritaire (les fraudes) en interpolant entre des exemples existants. Nous utilisons un sampling_strategy de 0.2, ce qui signifie qu'après SMOTE, notre ensemble d'entraînement contient 20% de fraudes et 80% de transactions normales. Attention : SMOTE est appliqué **uniquement sur l'ensemble d'entraînement** pour éviter toute fuite de données.
>
> **Étape 4 : Modélisation avec Cross-Validation.** Nous avons testé trois algorithmes avec une validation croisée 5-fold : la Régression Logistique comme baseline, Random Forest avec 300 arbres, et XGBoost. La cross-validation nous permet d'obtenir des estimations robustes des performances et de vérifier la stabilité des modèles.
>
> **Étape 5 : Optimisation du seuil de décision.** Par défaut, un classificateur prédit "fraude" si la probabilité dépasse 50%. Mais avec des données déséquilibrées, ce n'est pas optimal. Nous avons donc optimisé le seuil pour maximiser le Recall tout en maintenant une Precision d'au moins 20%. Le seuil optimal trouvé est de **7.33%** : toute transaction avec une probabilité supérieure à 7.33% est classée comme fraude.

**Transition** : *Quels modèles avons-nous comparés et lequel avons-nous retenu ?*

---

## SLIDE 8 : Comparaison des Modèles

### 🎯 Visuel
```
📊 RÉSULTATS CROSS-VALIDATION 5-FOLD

┌──────────────────┬──────────┬─────────┬─────────┬───────────┬──────────┐
│ Modèle           │ ROC-AUC  │ PR-AUC  │ Recall  │ Precision │ F1-Score │
├──────────────────┼──────────┼─────────┼─────────┼───────────┼──────────┤
│ Log. Regression  │ 0.98±0.01│ 0.78±0.04│ 88.7±2.5│ 22.7±1.6 │ 0.36±0.02│
│ 🏆 Random Forest │ 0.98±0.01│ 0.86±0.02│ 82.9±1.1│ 87.0±3.1 │ 0.85±0.01│
│ XGBoost          │ 0.98±0.01│ 0.85±0.02│ 83.4±2.0│ 81.7±3.5 │ 0.83±0.02│
└──────────────────┴──────────┴─────────┴─────────┴───────────┴──────────┘

✅ MODÈLE RETENU : RANDOM FOREST
→ Meilleur PR-AUC (0.8646) → Excellent pour déséquilibre
→ Meilleur F1-Score (0.848) → Équilibre Recall/Precision
→ Plus faible variance (±1.1%) → Très stable
→ Precision élevée (87%) → Peu de fausses alertes

📈 VALIDATION SET (avec seuil optimisé 7.33%)
┌──────────────────┬─────────┬─────────┬───────────┬─────────┬───────────┐
│ Modèle           │ Détectées│ Manquées│ F. Alertes│ Recall  │ PR-AUC    │
├──────────────────┼─────────┼─────────┼───────────┼─────────┼───────────┤
│ Log. Regression  │ 62/74   │ 12      │ 248       │ 83.78%  │ 0.6594    │
│ 🏆 Random Forest │ 65/74   │ 9       │ 243       │ 87.84%  │ 0.8335    │
│ XGBoost          │ 63/74   │ 11      │ 252       │ 85.14%  │ 0.8262    │
└──────────────────┴─────────┴─────────┴───────────┴─────────┴───────────┘

💡 Random Forest détecte +3 fraudes vs baseline, avec -5 fausses alertes
```

### 📝 Speech

> **Nous avons comparé trois modèles de manière rigoureuse avec une validation croisée 5-fold.**
>
> **Les résultats de la cross-validation montrent que** :
> - Les trois modèles ont un ROC-AUC excellent autour de 0.98
> - Cependant, le **Random Forest se distingue clairement** avec un PR-AUC de **0.86**, significativement supérieur à la régression logistique (0.78)
> - Le F1-Score du Random Forest est également le meilleur à **0.85**
> - Surtout, le Random Forest montre la plus faible variance avec seulement ±1.1% sur le Recall, ce qui indique un modèle très stable
>
> **Pourquoi le PR-AUC est-il si important ?** Le PR-AUC, ou Area Under Precision-Recall Curve, est LA métrique de référence pour les données déséquilibrées. Contrairement au ROC-AUC qui peut être trompeur avec des classes déséquilibrées, le PR-AUC nous donne une vraie mesure de la capacité du modèle à détecter les fraudes.
>
> **Sur le validation set avec le seuil optimisé à 7.33%**, le Random Forest détecte **65 fraudes sur 74**, soit un Recall de **87.84%**. Comparé à la régression logistique qui en détecte 62, c'est **3 fraudes supplémentaires détectées**. Et en bonus, nous avons **5 fausses alertes en moins** !
>
> Le PR-AUC du Random Forest sur le validation set est de **0.8335**, soit une amélioration de **+26% par rapport à la régression logistique**. C'est pour toutes ces raisons que nous avons retenu le **Random Forest comme modèle final**.

**Transition** : *Examinons maintenant les performances finales de notre modèle.*

---

## SLIDE 9 : Résultats et Performances Finales

### 🎯 Visuel
```
🎯 PERFORMANCES FINALES - RANDOM FOREST

📊 MÉTRIQUES VALIDATION SET
┌─────────────────┬──────────┬─────────────────────────────────────┐
│ Métrique        │ Valeur   │ Interprétation                      │
├─────────────────┼──────────┼─────────────────────────────────────┤
│ ROC-AUC         │ 0.973    │ ⭐⭐⭐⭐⭐ Excellente discrimination   │
│ PR-AUC          │ 0.833    │ ⭐⭐⭐⭐⭐ Excellent (déséquilibre)    │
│ Recall          │ 87.84%   │ 65/74 fraudes détectées (9 manquées)│
│ Precision       │ 21.10%   │ 65/308 alertes sont vraies          │
│ F1-Score        │ 0.340    │ Bon équilibre avec priorité Recall  │
│ Seuil optimal   │ 0.0733   │ 7.33% (optimisé pour max Recall)    │
└─────────────────┴──────────┴─────────────────────────────────────┘

🎭 MATRICE DE CONFUSION (42,721 transactions)
                    Prédiction
                 Normale    Fraude
    Réalité  ┌───────────┬─────────┐
    Normale  │  42,404   │   243   │  (0.57% faux positifs)
    (42,647) │    TN     │   FP    │
             ├───────────┼─────────┤
    Fraude   │     9     │   65    │  (87.84% détection)
    (74)     │    FN     │   TP    │
             └───────────┴─────────┘

✅ STABILITÉ VALID ↔ TEST
┌──────────┬─────────┬────────┬──────┐
│ Métrique │ Valid   │ Test   │ Δ    │
├──────────┼─────────┼────────┼──────┤
│ ROC-AUC  │ 0.9729  │ 0.9752 │ ✅   │
│ PR-AUC   │ 0.8326  │ 0.8404 │ ✅   │
│ Recall   │ 87.84%  │ 86.49% │ ✅   │
└──────────┴─────────┴────────┴──────┘

Pas de surapprentissage ! 🎉
```

### 📝 Speech

> **Voici les performances finales de notre modèle Random Forest.**
>
> **Les métriques sur le validation set sont excellentes** :
> - Un **ROC-AUC de 0.973**, ce qui est exceptionnel et signifie que le modèle discrimine très bien entre fraudes et transactions normales
> - Un **PR-AUC de 0.833**, qui est notre métrique phare pour ce problème de données déséquilibrées. C'est un score excellent qui confirme la robustesse du modèle
> - Un **Recall de 87.84%**, ce qui signifie que nous détectons **65 fraudes sur 74**. Seulement **9 fraudes nous échappent**
> - Une **Precision de 21.10%**, ce qui signifie qu'une alerte sur cinq est une vraie fraude. En production, cela signifie environ **243 fausses alertes** à vérifier manuellement, ce qui est un volume raisonnable et acceptable pour une banque
> - Le **seuil optimal** a été fixé à **7.33%**, optimisé pour maximiser le Recall
>
> **La matrice de confusion nous donne une vue complète** :
> Sur 42,721 transactions dans le validation set :
> - **42,404 vrais négatifs** : transactions normales correctement identifiées
> - **243 faux positifs** : seulement 0.57% des transactions normales sont signalées à tort
> - **9 faux négatifs** : les fraudes manquées, que nous cherchons à minimiser
> - **65 vrais positifs** : les fraudes correctement détectées
>
> **Point crucial : la stabilité entre validation et test.** Les performances sur le test set sont cohérentes avec celles du validation set : ROC-AUC de 0.9752, PR-AUC de 0.8404, Recall de 86.49%. Les métriques sont très proches, ce qui prouve qu'il n'y a **pas de surapprentissage**. Notre modèle généralise bien à de nouvelles données.

**Transition** : *Maintenant, permettez-moi de vous montrer comment ce modèle est déployé dans une application concrète.*

---

## SLIDE 10 : Démonstration de l'Application - Vue d'Ensemble

### 🎯 Visuel
```
💻 APPLICATION WEB STREAMLIT

[CAPTURE D'ÉCRAN : Interface complète de l'application]

🎨 Composants Principaux
┌─────────────────────────────────────────────────┐
│ 📱 SIDEBAR                                      │
│   • Configuration du seuil (slider 0-50%)       │
│   • Affichage des métriques du modèle           │
│   • Options d'archivage                         │
├─────────────────────────────────────────────────┤
│ 🔍 ONGLET 1 : TRANSACTION UNIQUE                │
│   • Formulaire de saisie (Amount, Time, V1-V28) │
│   • Bouton "Charger Exemple"                    │
│   • Prédiction en temps réel                    │
├─────────────────────────────────────────────────┤
│ 📁 ONGLET 2 : ANALYSE PAR LOT (CSV)             │
│   • Upload de fichier (max 100k transactions)   │
│   • Traitement par batch (5000 lignes)          │
│   • Téléchargement des résultats                │
└─────────────────────────────────────────────────┘

🚀 Technologies
• Framework : Streamlit 1.38+
• Visualisations : Plotly (interactif)
• ML : scikit-learn + SHAP
• Déploiement : Local / Cloud ready
```

### 📝 Speech

> **Passons maintenant à la démonstration de l'application web que nous avons développée.**
>
> L'application est construite avec **Streamlit**, un framework Python moderne qui permet de créer rapidement des interfaces web interactives pour des applications de Data Science.
>
> **L'interface se compose de trois parties principales** :
>
> **La sidebar sur la gauche** contient la configuration :
> - Un slider pour ajuster le seuil de décision entre 0 et 50%
> - L'affichage des métriques du modèle (PR-AUC, ROC-AUC, Recall, Precision)
> - Les options d'archivage automatique des prédictions
>
> **Le premier onglet "Transaction Unique"** permet d'analyser une transaction individuelle en temps réel :
> - Un formulaire de saisie pour le montant, le temps, et optionnellement les 28 variables PCA
> - Un bouton "Charger Exemple" qui pré-remplit le formulaire avec une vraie transaction frauduleuse du dataset pour tester rapidement
> - La prédiction s'affiche instantanément avec la probabilité et le niveau de risque
>
> **Le second onglet "Analyse par Lot"** permet de traiter des fichiers CSV :
> - Upload de fichiers contenant jusqu'à 100,000 transactions
> - Traitement optimisé par batch de 5,000 lignes pour gérer les gros volumes
> - Téléchargement des résultats avec toutes les prédictions
>
> L'application utilise **Plotly pour les visualisations interactives** et intègre **SHAP pour l'explainability**. Elle est prête pour un déploiement local ou cloud.

**Transition** : *Voyons concrètement comment fonctionne la prédiction sur une transaction unique.*

---

## SLIDE 11 : Démonstration - Prédiction Transaction Unique

### 🎯 Visuel
```
🔍 PRÉDICTION TRANSACTION UNIQUE

[CAPTURE D'ÉCRAN : Résultat d'une fraude détectée]

INPUT
┌────────────────────────────────────┐
│ Amount : 406.85 €                  │
│ Time : 79,265 secondes             │
│ V1-V28 : (values from real fraud)  │
└────────────────────────────────────┘

OUTPUT
┌────────────────────────────────────────────────┐
│ 🚨 FRAUDE DÉTECTÉE                             │
│                                                │
│ Probabilité : 92.33%                           │
│ Niveau de risque : 🔴 CRITIQUE                 │
│                                                │
│ [JAUGE VISUELLE : 92.33%]                      │
│ [BARRE DE PROBABILITÉ avec seuil à 7.33%]     │
└────────────────────────────────────────────────┘

📊 TOP 5 FACTEURS INFLUENTS (SHAP)
┌────────┬─────────────────────┬──────────┐
│ Feature│ Valeur              │ Impact   │
├────────┼─────────────────────┼──────────┤
│ V4     │ -2.312              │ +0.524 🔴│
│ V17    │ -1.856              │ +0.389 🔴│
│ V14    │ -8.142              │ +0.312 🔴│
│ V10    │ -15.430             │ +0.287 🔴│
│ Amount │ 406.85              │ +0.156 🔴│
└────────┴─────────────────────┴──────────┘

🔴 Impact positif = Augmente le risque de fraude
🟢 Impact négatif = Réduit le risque de fraude
```

### 📝 Speech

> **Permettez-moi de vous montrer un exemple concret de prédiction.**
>
> Nous avons ici une transaction réelle du dataset :
> - **Montant : 406.85 euros**
> - **Time : 79,265 secondes**, soit environ 22 heures après le début de la période d'observation
> - Les valeurs V1 à V28 proviennent d'une vraie fraude du dataset
>
> **Le résultat de la prédiction est sans appel** :
> - **Probabilité de fraude : 92.33%**
> - **Classification : FRAUDE DÉTECTÉE**
> - **Niveau de risque : CRITIQUE** (représenté en rouge)
>
> La jauge visuelle et la barre de probabilité montrent clairement que nous sommes **très largement au-dessus du seuil de 7.33%**. Cette transaction nécessiterait une investigation immédiate en production.
>
> **Mais ce qui est vraiment puissant, c'est l'explainability avec SHAP.** Le tableau affiche les **Top 5 facteurs qui ont influencé cette prédiction** :
> - **V4 = -2.312** a l'impact le plus fort avec **+0.524** sur le score de fraude
> - **V17 = -1.856** contribue également fortement avec **+0.389**
> - **V14**, **V10**, et le **montant de 406.85€** complètent les facteurs influents
>
> Tous ces impacts sont **positifs** (en rouge), ce qui signifie qu'ils augmentent la probabilité de fraude. Si un analyste devait vérifier cette transaction, il saurait exactement quels aspects examiner en priorité.
>
> **C'est un exemple parfait d'IA responsable** : non seulement nous détectons la fraude, mais nous expliquons pourquoi. Cela permet aux analystes humains de comprendre et valider les décisions du modèle.

**Transition** : *L'application permet aussi d'analyser des volumes importants de transactions. Voyons comment.*

---

## SLIDE 12 : Démonstration - Analyse par Lot (CSV)

### 🎯 Visuel
```
📁 ANALYSE PAR LOT - FICHIER CSV

[CAPTURE D'ÉCRAN : Interface d'upload CSV + Résultats]

ÉTAPE 1 : UPLOAD
┌──────────────────────────────────────┐
│ 📄 Fichier : transactions_2025.csv   │
│ 📊 Taille : 15,234 transactions      │
│ ⏱️ Temps de traitement : 3.2 sec     │
└──────────────────────────────────────┘

ÉTAPE 2 : RÉSULTATS GLOBAUX
┌─────────────────────────────────────────────┐
│ ✅ Transactions normales : 14,987 (98.4%)   │
│ 🚨 Fraudes détectées : 247 (1.6%)           │
│                                             │
│ Niveaux de risque :                         │
│ 🟢 FAIBLE : 14,823 (97.3%)                  │
│ 🟡 MODÉRÉ : 164 (1.1%)                      │
│ 🟠 ÉLEVÉ : 183 (1.2%)                       │
│ 🔴 CRITIQUE : 64 (0.4%)                     │
└─────────────────────────────────────────────┘

ÉTAPE 3 : VISUALISATIONS
┌─────────────────────────────────────────────┐
│ TAB 1 : Données complètes (fraudes en 🔴)  │
│ TAB 2 : Fraudes uniquement (247 lignes)    │
│ TAB 3 : Distribution des probabilités      │
│ TAB 4 : Analyse par risque (pie chart)     │
└─────────────────────────────────────────────┘

📥 EXPORT
• Bouton téléchargement → CSV complet avec prédictions
• Archivage automatique dans reports/predictions/
• Index CSV pour traçabilité
```

### 📝 Speech

> **L'application permet également d'analyser des volumes importants de transactions via des fichiers CSV.**
>
> **Le processus est très simple en trois étapes** :
>
> **Étape 1 : Upload du fichier.** L'utilisateur sélectionne son fichier CSV. Dans cet exemple, nous avons 15,234 transactions. Le traitement prend seulement **3.2 secondes** grâce à notre optimisation par batch de 5,000 lignes. L'application peut gérer jusqu'à **100,000 transactions** en une seule fois.
>
> **Étape 2 : Résultats globaux.** L'application affiche immédiatement un résumé :
> - **14,987 transactions normales** (98.4%)
> - **247 fraudes détectées** (1.6%)
> - La répartition par niveau de risque : 97.3% à risque FAIBLE, 1.1% MODÉRÉ, 1.2% ÉLEVÉ, et 0.4% CRITIQUE
>
> Ces chiffres donnent une vue d'ensemble instantanée permettant à un analyste de prioriser son travail : les 64 transactions critiques nécessitent une attention immédiate, tandis que les 183 à risque élevé peuvent être vérifiées dans un second temps.
>
> **Étape 3 : Visualisations interactives.** Quatre onglets de visualisation :
> - **Données complètes** : Tableau avec toutes les transactions, les fraudes surlignées en rouge pour faciliter l'identification visuelle
> - **Fraudes uniquement** : Vue filtrée sur les 247 fraudes pour analyse approfondie
> - **Distribution des probabilités** : Histogramme montrant la répartition des scores de fraude, avec la ligne de seuil à 7.33%
> - **Analyse par risque** : Graphique en camembert et tableau détaillé par niveau de risque
>
> **Export et traçabilité** :
> - Un bouton permet de télécharger le CSV complet avec toutes les prédictions et probabilités
> - L'application archive automatiquement chaque analyse dans le dossier `reports/predictions/` avec timestamp
> - Un fichier index CSV maintient la traçabilité de toutes les analyses effectuées
>
> Cette fonctionnalité est particulièrement utile pour le traitement batch de nuit ou pour analyser les transactions d'une journée complète.

**Transition** : *Voyons maintenant l'architecture technique qui rend tout cela possible.*

---

## SLIDE 13 : Architecture Technique

### 🎯 Visuel
```
🏗️ ARCHITECTURE MODULAIRE

fraud-detection-pfe/
├── 📱 app/
│   └── streamlit_app.py           # Application web (718 lignes)
│
├── 🧩 src/                         # Code réutilisable
│   ├── data/loader.py              # Chargement artefacts
│   ├── models/predictor.py         # Prédictions
│   ├── models/explainer.py         # Explications SHAP
│   ├── utils/validation.py         # Validation données
│   └── visualization/plots.py      # Graphiques Plotly
│
├── 🧪 tests/                       # 22 tests unitaires
│   ├── test_predictor.py           # 8 tests (95% coverage)
│   ├── test_loader.py              # 4 tests (92% coverage)
│   └── test_validation.py          # 10 tests (88% coverage)
│
├── 📓 notebooks/                   # Analyse et recherche
│   ├── 01_eda.ipynb                # Exploration données
│   └── 02_preparation.ipynb        # Modélisation complète
│
├── 🛠️ scripts/                     # Automatisation
│   ├── setup.sh                    # Installation auto
│   ├── train_model.py              # Entraînement
│   └── predict.py                  # Prédictions CLI
│
└── 💾 models/rf_smote_final/       # Artefacts ML
    ├── pipeline.joblib             # Pipeline sklearn
    ├── metrics_valid.json          # Métriques
    └── columns.json                # Schéma données

✅ QUALITÉ DU CODE
• Architecture modulaire (DRY principle)
• 22 tests unitaires (pytest)
• Documentation complète (docstrings)
• Type hints pour clarté
• Error handling robuste
```

### 📝 Speech

> **L'architecture technique du projet a été conçue pour être modulaire, maintenable et professionnelle.**
>
> **Le dossier `app/`** contient l'application Streamlit. Le fichier principal `streamlit_app.py` fait 718 lignes et orchestre tous les composants de l'interface utilisateur.
>
> **Le cœur du projet est le dossier `src/`** qui contient des modules réutilisables :
> - **data/loader.py** : Gère le chargement du pipeline, des métriques et des métadonnées
> - **models/predictor.py** : Contient la classe FraudPredictor qui effectue les prédictions, gère le preprocessing et le traitement par batch
> - **models/explainer.py** : Implémente FraudExplainer pour les explications SHAP
> - **utils/validation.py** : DataValidator qui valide et nettoie les données d'entrée
> - **visualization/plots.py** : FraudVisualizer qui crée tous les graphiques Plotly
>
> Cette séparation permet de **réutiliser le code facilement** et de **tester chaque composant indépendamment**.
>
> **Le dossier `tests/`** contient **22 tests unitaires** avec pytest :
> - 8 tests pour le predictor (95% de couverture)
> - 4 tests pour le loader (92% de couverture)
> - 10 tests pour la validation (88% de couverture)
>
> Ces tests garantissent que chaque modification du code ne casse pas les fonctionnalités existantes.
>
> **Les `notebooks/`** Jupyter documentent tout le processus de recherche :
> - `01_eda.ipynb` : L'exploration complète des données avec toutes les visualisations
> - `02_preparation.ipynb` : Le preprocessing, la modélisation, la comparaison des algorithmes, et l'évaluation finale
>
> **Les `scripts/`** automatisent les tâches courantes :
> - `setup.sh` : Installation complète du projet en une commande
> - `train_model.py` : Entraînement du modèle avec paramètres configurables
> - `predict.py` : Interface en ligne de commande pour des prédictions rapides
>
> **Enfin, le dossier `models/`** stocke les artefacts ML :
> - Le pipeline sklearn complet avec preprocessing et modèle
> - Les métriques de validation au format JSON
> - Le schéma des colonnes attendues
>
> **Cette architecture respecte les bonnes pratiques** :
> - Principe DRY (Don't Repeat Yourself) : pas de duplication de code
> - Tests automatisés pour la fiabilité
> - Documentation exhaustive avec docstrings Google style
> - Type hints Python pour la clarté
> - Gestion d'erreurs robuste avec fallbacks

**Transition** : *Terminons par les conclusions et perspectives d'amélioration.*

---

## SLIDE 14 : Conclusion et Perspectives

### 🎯 Visuel
```
🎯 CONCLUSION

✅ OBJECTIFS ATTEINTS
• Modèle performant : 87.84% Recall, PR-AUC 0.833
• Application web intuitive et interactive
• Explainability avec SHAP (IA responsable)
• Code de qualité production (tests, docs, architecture)

💡 APPORTS DU PROJET
• Traitement de données déséquilibrées (SMOTE)
• Optimisation de seuil adaptée au métier
• Pipeline ML complet de bout en bout
• Application déployable en production

🚀 PERSPECTIVES D'AMÉLIORATION

Court Terme (0-3 mois)
• Déploiement cloud (Streamlit Cloud / AWS)
• API REST pour intégration système bancaire
• Monitoring des prédictions en production
• Alerting automatique (email/SMS pour CRITIQUE)

Moyen Terme (3-6 mois)
• Réentraînement automatique mensuel
• Détection de drift des données
• Dashboard analytics pour managers
• A/B testing de nouveaux modèles

Long Terme (6-12 mois)
• Deep Learning (LSTM pour séquences temporelles)
• Features engineering avancé
• Détection d'anomalies (Isolation Forest, Autoencoder)
• Intégration GraphDB (réseaux de fraude)
```

### 📝 Speech

> **En conclusion, je suis fière de dire que tous les objectifs fixés ont été atteints.**
>
> **Nous avons développé un modèle performant** avec un Recall de 87.84% et un PR-AUC de 0.833, ce qui est excellent pour des données aussi déséquilibrées. **L'application web** est intuitive et accessible aux non-techniciens. **L'explainability est garantie** grâce aux explications SHAP, répondant aux exigences d'IA responsable. Et **le code est de qualité production** avec tests, documentation et architecture modulaire.
>
> **Les apports de ce projet sont multiples** :
> - J'ai maîtrisé le traitement de données extrêmement déséquilibrées avec SMOTE
> - J'ai appris à optimiser un seuil de décision en fonction des besoins métier (maximiser le Recall)
> - J'ai développé un pipeline ML complet de A à Z
> - J'ai créé une application déployable en production
>
> **Mais ce projet n'est qu'un début. Voici les perspectives d'amélioration** :
>
> **À court terme**, dans les 0 à 3 mois :
> - **Déploiement cloud** sur Streamlit Cloud ou AWS pour rendre l'application accessible depuis internet
> - **Développement d'une API REST** pour permettre l'intégration dans les systèmes bancaires existants
> - **Mise en place de monitoring** pour suivre les performances du modèle en production
> - **Alerting automatique** par email ou SMS pour les transactions critiques
>
> **À moyen terme**, dans les 3 à 6 mois :
> - **Réentraînement automatique** du modèle chaque mois avec les nouvelles données
> - **Détection de drift** pour identifier quand les patterns de fraude changent et que le modèle doit être adapté
> - **Dashboard analytics** pour les managers avec KPIs et tendances
> - **A/B testing** pour comparer de nouveaux modèles en production
>
> **À long terme**, dans les 6 à 12 mois :
> - **Deep Learning** : utiliser des LSTM pour capturer les séquences temporelles de transactions
> - **Feature engineering avancé** : créer de nouvelles variables à partir des données brutes
> - **Techniques d'anomaly detection** comme Isolation Forest ou Autoencoders
> - **Intégration de bases de données graphes** pour détecter les réseaux de fraude et les comportements collectifs suspects
>
> Ce projet démontre qu'avec une méthodologie rigoureuse et les bons outils, il est possible de résoudre des problèmes complexes de détection de fraude tout en garantissant transparence et explainability.

**Transition** : *Je vous remercie pour votre attention.*

---

## SLIDE 15 : Questions et Remerciements

### 🎯 Visuel
```
💙 MERCI POUR VOTRE ATTENTION

[IMAGE : Carte bancaire]

👥 REMERCIEMENTS
• M. DOUMI KARIM - Encadrant
• M. KHALID BENABBESS - Encadrant
• ESLSCA Paris - Campus Rabat
• ULB Machine Learning Group (dataset)

📞 CONTACT
Marie Chandeste Melvina J. H. Medetadji Migan
📧 melvinamedetadji@gmail.com
🔗 GitHub : github.com/Mariechanne/fraud-detection-pfe
🔗 Kaggle : kaggle.com/melvinamedetadji

❓ QUESTIONS ?

💡 Je reste à votre disposition pour toute question
   sur la méthodologie, les résultats, l'application,
   ou les perspectives du projet.
```

### 📝 Speech

> **Je vous remercie pour votre attention.**
>
> **Je tiens à remercier chaleureusement** :
> - **Mes encadrants, Monsieur DOUMI KARIM et Monsieur KHALID BENABBESS**, pour leurs conseils précieux et leur soutien tout au long de ce projet
> - **L'ESLSCA Paris, Campus Rabat**, pour la qualité de la formation en Data Science
> - **L'ULB Machine Learning Group** pour la mise à disposition du dataset qui a rendu ce projet possible
>
> **Pour me contacter** :
> - Email : melvinamedetadji@gmail.com
> - Le code source complet est disponible sur mon GitHub : github.com/Mariechanne/fraud-detection-pfe
> - Mon profil Kaggle : kaggle.com/melvinamedetadji
>
> **Je suis maintenant à votre disposition pour répondre à vos questions**, que ce soit sur :
> - La méthodologie Machine Learning utilisée
> - Les résultats et performances du modèle
> - L'architecture de l'application
> - Les choix techniques effectués
> - Les perspectives d'amélioration
> - Ou tout autre aspect du projet
>
> **Merci encore, et je serai ravie d'échanger avec vous.**

---

## 📚 ANNEXE : Questions Fréquentes Anticipées

### Q1 : Pourquoi avoir choisi Random Forest plutôt que XGBoost ?

**Réponse** :
> Excellente question. Bien que XGBoost soit souvent considéré comme plus performant, dans notre cas, Random Forest s'est révélé supérieur pour trois raisons :
> 1. **Meilleur PR-AUC** (0.8646 vs 0.8528) : différence significative pour des données déséquilibrées
> 2. **Plus grande stabilité** : variance de ±1.1% contre ±2.0% pour XGBoost en cross-validation
> 3. **Meilleur F1-Score** (0.848 vs 0.825) : meilleur équilibre Recall/Precision
>
> De plus, Random Forest est plus simple à interpréter et plus robuste au surapprentissage sans nécessiter autant de tuning d'hyperparamètres.

### Q2 : Comment gérez-vous le risque de surapprentissage avec SMOTE ?

**Réponse** :
> Point très pertinent. Nous avons pris plusieurs précautions :
> 1. **SMOTE uniquement sur le train set** : jamais sur validation ou test
> 2. **Cross-validation 5-fold** : validation robuste des performances
> 3. **Comparaison VALID ↔ TEST** : les métriques sont cohérentes (ROC-AUC 0.9729 vs 0.9752), preuve qu'il n'y a pas de surapprentissage
> 4. **Stratégie SMOTE modérée** : 0.2 (20% fraudes) au lieu d'équilibrer à 50/50, pour rester proche de la distribution réelle

### Q3 : 21% de Precision, n'est-ce pas trop faible ?

**Réponse** :
> C'est une excellente question qui touche au cœur du trade-off Recall vs Precision.
>
> Dans le contexte de la fraude bancaire, **manquer une fraude coûte beaucoup plus cher qu'une fausse alerte**. Une fraude de 500€ non détectée = 500€ de perte. Vérifier une fausse alerte = quelques minutes d'un analyste.
>
> Avec 21% de Precision et 87.84% de Recall :
> - Nous détectons **65/74 fraudes** (seulement 9 manquées)
> - Nous générons **243 fausses alertes** sur 42,647 transactions normales (0.57%)
> - Cela représente environ **50 fausses alertes par jour** pour une banque, ce qui est gérable
>
> Si nous augmentions le seuil pour avoir 50% de Precision, nous manquerions **20-25 fraudes supplémentaires**, ce qui serait inacceptable. Le seuil de 7.33% est optimisé pour **maximiser le Recall avec une Precision minimale de 20%**, ce qui est un compromis standard dans l'industrie.

### Q4 : Comment le modèle gère-t-il les nouvelles techniques de fraude ?

**Réponse** :
> C'est effectivement un défi important. Nous avons prévu plusieurs stratégies :
>
> **Court terme** :
> - **Monitoring continu** : suivre les taux de détection réels en production
> - **Feedback loop** : les analystes confirment ou infirment chaque alerte, ces données servent au réentraînement
>
> **Moyen terme** :
> - **Réentraînement mensuel** : le modèle apprend les nouveaux patterns
> - **Détection de drift** : alertes automatiques si les distributions changent significativement
>
> **Long terme** :
> - **Modèles d'anomaly detection** (Isolation Forest, Autoencoder) qui détectent des comportements jamais vus
> - **Transfer learning** : utiliser des modèles pré-entraînés sur d'autres datasets de fraude
>
> Le modèle actuel capture les patterns généraux de fraude (montants, features PCA), qui restent relativement stables, mais une surveillance active est essentielle.

### Q5 : Pourquoi ne pas utiliser de Deep Learning ?

**Réponse** :
> Très bonne question. Nous avons privilégié Random Forest pour plusieurs raisons :
>
> 1. **Taille du dataset** : 284k transactions, c'est suffisant pour RF mais un peu limité pour DL qui nécessite des millions d'exemples pour vraiment exceller
>
> 2. **Interprétabilité** : Random Forest + SHAP offre des explications claires et précises. Les réseaux de neurones sont plus opaques, ce qui est problématique dans le secteur bancaire régulé
>
> 3. **Temps d'entraînement** : RF s'entraîne en quelques minutes, DL prendrait des heures voire des jours
>
> 4. **Performances** : Avec PR-AUC de 0.833, nous avons déjà d'excellentes performances. Le gain potentiel avec DL serait marginal
>
> **Cela dit**, dans les perspectives à long terme, j'ai mentionné l'utilisation de **LSTM** pour capturer les séquences temporelles de transactions (par exemple, détecter qu'un utilisateur fait 10 petites transactions suivies d'une grosse, ce qui est suspect). Cela ferait sens avec plus de données historiques par client.

### Q6 : Comment déploieriez-vous ce modèle en production ?

**Réponse** :
> Voici l'architecture de déploiement que je recommande :
>
> **Option 1 : API REST (Recommandé pour intégration système)**
> ```
> Client (système bancaire)
>   → API Flask/FastAPI
>   → Load Balancer
>   → Multiple instances du modèle
>   → Base de données (logs + feedback)
> ```
>
> **Option 2 : Streamlit Cloud (Rapide pour POC)**
> - Déploiement en 1 clic sur Streamlit Cloud
> - Accès web direct pour les analystes
> - Bon pour phase pilote
>
> **Option 3 : Conteneurisation Docker + Kubernetes**
> - Scalabilité automatique
> - Haute disponibilité
> - Convient aux grandes banques
>
> **Composants essentiels** :
> - **Monitoring** : Prometheus + Grafana pour suivre latence, throughput, taux de détection
> - **Logging** : Toutes les prédictions dans une DB pour audit et réentraînement
> - **A/B testing** : Framework pour tester de nouveaux modèles sur 10% du trafic avant rollout complet
> - **Alerting** : PagerDuty/Slack pour transactions critiques
>
> Le code actuel est déjà **production-ready** grâce à l'architecture modulaire et aux tests unitaires.

---

## 🎯 CONSEILS POUR LA SOUTENANCE

### Avant la présentation
1. **Tester l'application** : S'assurer qu'elle fonctionne parfaitement, avoir des exemples pré-chargés
2. **Préparer les démos** : Screenshots clairs, transitions fluides
3. **Chronomètre** : Respecter le timing de chaque slide (25-30 min total)
4. **Backup plan** : PDF des notebooks en cas de problème technique

### Pendant la présentation
1. **Contact visuel** : Regarder le jury, pas seulement les slides
2. **Enthusiasm** : Montrer votre passion pour le projet
3. **Clarté** : Utiliser des analogies pour expliquer les concepts techniques
4. **Honnêteté** : Admettre les limitations du projet, cela montre la maturité

### Pendant les questions
1. **Écouter attentivement** : Reformuler la question si nécessaire
2. **Prendre son temps** : Respirer, réfléchir 5 secondes avant de répondre
3. **Structurer** : "Excellente question. Trois points : Premièrement... Deuxièmement... Troisièmement..."
4. **Honnêteté** : Si vous ne savez pas, dites "C'est une excellente question, je n'ai pas exploré cet aspect en détail, mais voici ce que je pense..."

### Points à souligner
- **Rigueur méthodologique** : CV 5-fold, split stratifié, optimisation de seuil
- **Gestion du déséquilibre** : SMOTE, PR-AUC comme métrique
- **IA responsable** : Explainability avec SHAP
- **Qualité du code** : Tests, architecture, documentation
- **Vision produit** : Application déployable, perspectives claires

---

**Bonne chance pour votre soutenance ! 🎓✨**
