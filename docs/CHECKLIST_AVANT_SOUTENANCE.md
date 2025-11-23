# ✅ Checklist Complète Avant Soutenance (29 Novembre 2024)

## 🎯 PRIORITÉ HAUTE - À FAIRE IMMÉDIATEMENT

### 📧 Préparation de l'Email pour M. Doumi

- [ ] **Lire les 2 versions d'email** dans `docs/EMAIL_POUR_ENCADRANT.md`
- [ ] **Choisir la version** qui correspond le mieux à votre relation avec M. Doumi
  - Version 1 (Recommandée) : Ton professionnel mais humain
  - Version 2 : Ton très formel et académique
- [ ] **Personnaliser l'email :**
  - Ajouter votre numéro de téléphone
  - Ajuster le ton si nécessaire
  - Vérifier l'orthographe
- [ ] **Préparer les pièces jointes :**
  - [ ] Convertir `RESUME_EXECUTIF.md` en PDF (recommandé) ou envoyer le lien GitHub
  - [ ] Sélectionner 2-3 screenshots percutants :
    - `docs/images/01_interface_globale.png` (vue d'ensemble)
    - `docs/images/02_resultat_fraude.png` (détection avec 92% probabilité)
    - `docs/images/03_shap_explication.png` (explications IA)
  - [ ] Compresser les images si > 2 MB au total
- [ ] **Vérifier le lien GitHub** : https://github.com/Mariechanne/fraud-detection-pfe
  - [ ] Le dépôt est bien public
  - [ ] Le README.md s'affiche correctement
  - [ ] Les images sont visibles
- [ ] **Envoyer l'email** (meilleur moment : Lundi-Jeudi, 9h-11h ou 14h-16h)

---

## 💻 PRIORITÉ HAUTE - Installation et Test du Projet

### Étape 1 : Installation des Dépendances (15-20 minutes)

```bash
# 1. Créer l'environnement virtuel
cd ~/fraud-detection-pfe
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate sur Windows

# 2. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 3. Vérifier que tout est bien installé
python scripts/env_check.py
# Devrait afficher : "✅ Environnement prêt"
```

**Checklist :**
- [ ] Environnement virtuel créé (`.venv/`)
- [ ] Toutes les dépendances installées sans erreur
- [ ] Script `env_check.py` passe avec succès

---

### Étape 2 : Téléchargement des Données Kaggle (10 minutes)

**Option A : Téléchargement manuel (Recommandé si première fois)**
1. [ ] Aller sur https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
2. [ ] Se connecter avec votre compte Kaggle (ou créer un compte gratuit)
3. [ ] Cliquer sur "Download" (150 MB)
4. [ ] Extraire `creditcard.csv` et le placer dans `data/raw/creditcard.csv`
5. [ ] Vérifier : `ls -lh data/raw/creditcard.csv` → devrait afficher ~150 MB

**Option B : Téléchargement via Kaggle API (Si vous avez déjà un compte)**
```bash
# 1. Installer Kaggle CLI
pip install kaggle

# 2. Configurer les credentials (fichier kaggle.json depuis votre compte)
mkdir -p ~/.kaggle
cp ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# 3. Télécharger le dataset
kaggle datasets download -d mlg-ulb/creditcardfraud -p data/raw/
unzip data/raw/creditcardfraud.zip -d data/raw/
rm data/raw/creditcardfraud.zip
```

**Checklist :**
- [ ] Fichier `data/raw/creditcard.csv` existe (~150 MB)
- [ ] Vérification : `head -n 5 data/raw/creditcard.csv` affiche les premières lignes

---

### Étape 3 : Entraînement du Modèle (5-10 minutes)

```bash
# Lancer l'entraînement (avec environnement virtuel activé)
python scripts/train_model.py --data data/raw/creditcard.csv

# Le script va :
# 1. Charger les données (284,807 transactions)
# 2. Faire le split stratifié 70/15/15
# 3. Appliquer le preprocessing (StandardScaler)
# 4. Appliquer SMOTE (rééquilibrage)
# 5. Entraîner Random Forest (300 arbres) → ~5-10 min
# 6. Sauvegarder dans models/rf_smote_final/
```

**Checklist :**
- [ ] Script s'exécute sans erreur
- [ ] Dossier `models/rf_smote_final/` créé
- [ ] Fichiers générés :
  - [ ] `models/rf_smote_final/pipeline.joblib` (~50-100 MB)
  - [ ] `models/rf_smote_final/metrics_valid.json`
  - [ ] `models/rf_smote_final/columns.json`
- [ ] Métriques affichées en fin d'entraînement :
  - ROC-AUC ≈ 0.97
  - PR-AUC ≈ 0.84
  - Recall ≈ 87%

---

### Étape 4 : Lancer l'Application Streamlit (1 minute)

```bash
# Avec environnement virtuel activé
streamlit run app/streamlit_app.py

# L'application devrait s'ouvrir automatiquement dans votre navigateur
# Sinon, aller sur : http://localhost:8501
```

**Checklist :**
- [ ] Application s'ouvre sans erreur
- [ ] Sidebar affiche les métriques du modèle :
  - ROC-AUC : 0.973
  - PR-AUC : 0.840
  - Recall : 87.8%
  - Precision : 21.1%
- [ ] Les 3 onglets sont accessibles :
  - [ ] "Analyse de transaction unique"
  - [ ] "Analyse par lot (CSV)"
  - [ ] Visualisations (distribution, risque)

---

### Étape 5 : Tester l'Application (5 minutes)

#### Test 1 : Transaction Normale
- [ ] Aller dans "Analyse de transaction unique"
- [ ] Entrer des valeurs normales (Time: 100000, Amount: 50, V1-V28: proches de 0)
- [ ] Cliquer sur "Analyser la transaction"
- [ ] **Vérifier :**
  - [ ] Probabilité < 10%
  - [ ] Classification : FAIBLE (vert)
  - [ ] Explications SHAP s'affichent

#### Test 2 : Transaction Frauduleuse
- [ ] Modifier les valeurs :
  - Time : 150000
  - Amount : 1.50
  - V14 : -18.5
  - V17 : -15.2
  - V12 : -8.9
- [ ] Cliquer sur "Analyser la transaction"
- [ ] **Vérifier :**
  - [ ] Probabilité > 85%
  - [ ] Classification : CRITIQUE (rouge)
  - [ ] Top 5 facteurs influents affichés (V14, V17, V12 en tête)

#### Test 3 : Analyse par Lot (CSV)
- [ ] Aller dans "Analyse par lot (CSV)"
- [ ] Uploader le fichier `data/examples/sample_transactions.csv`
- [ ] Cliquer sur "Analyser le fichier"
- [ ] **Vérifier :**
  - [ ] Résumé affiché (nombre de fraudes détectées)
  - [ ] Tableau avec highlighting des fraudes en rouge
  - [ ] Graphiques interactifs (distribution, camembert)
  - [ ] Fichier sauvegardé dans `reports/predictions/`

---

### Étape 6 : Lancer les Tests Unitaires (2 minutes)

```bash
# Avec environnement virtuel activé
pytest tests/ -v

# Devrait afficher : 22 passed ✅
```

**Checklist :**
- [ ] Tous les tests passent (22/22)
- [ ] Aucune erreur ni warning critique
- [ ] Couverture de code > 85% (optionnel : `pytest tests/ --cov=src`)

---

## 📊 PRIORITÉ MOYENNE - Préparation de la Présentation

### Création du PowerPoint (2-3 heures)

**Ressource :** Utiliser le plan détaillé dans `docs/PLAN_PRESENTATION_SOUTENANCE.md`

- [ ] **Créer 25-27 slides** selon le plan fourni
- [ ] **Intégrer les visuels :**
  - [ ] 8 screenshots de l'application (dossier `docs/images/`)
  - [ ] Courbes ROC et Precision-Recall (à extraire des notebooks ou créer)
  - [ ] Matrice de confusion (slide 13)
  - [ ] Graphiques de distribution des données (EDA)
  - [ ] Schéma du pipeline ML (slide 9)
  - [ ] Diagramme d'architecture (slide 16)
- [ ] **Ajouter les animations** (légères, pas trop lentes)
- [ ] **Vérifier la lisibilité :**
  - [ ] Police minimum 18pt pour le texte
  - [ ] Titres en 28pt minimum
  - [ ] Contraste suffisant (fond blanc ou bleu foncé)
- [ ] **Numéroter les slides** (en bas à droite)
- [ ] **Ajouter votre nom et logo ESLSCA** sur chaque slide (en pied de page)

**Formats à préparer :**
- [ ] Version PowerPoint (.pptx) - pour présenter
- [ ] Version PDF (.pdf) - pour envoyer par email si demandé
- [ ] Sauvegarde sur clé USB + cloud (Google Drive, Dropbox)

---

### Préparation de la Démonstration Live (1 heure)

- [ ] **Préparer un fichier CSV pour la démo** :
  - [ ] Copier `data/examples/sample_transactions.csv` sur le Bureau
  - [ ] Renommer en `demo_soutenance.csv`
  - [ ] Vérifier qu'il contient bien 50 transactions avec des fraudes

- [ ] **Préparer les valeurs de transactions de test** :
  - [ ] Créer un document texte avec les valeurs exactes :
    ```
    TRANSACTION NORMALE :
    Time : 100000
    Amount : 50.00
    V1-V28 : 0 (laisser par défaut)

    TRANSACTION FRAUDULEUSE :
    Time : 150000
    Amount : 1.50
    V14 : -18.5
    V17 : -15.2
    V12 : -8.9
    V10 : -12.1
    Autres : 0
    ```
  - [ ] Imprimer ce document ou l'avoir sur un second écran

- [ ] **Répéter la démonstration 2-3 fois** :
  - [ ] Chronomètre : Ne pas dépasser 5 minutes pour la démo complète
  - [ ] S'assurer de bien montrer :
    - Transaction normale → FAIBLE (vert)
    - Transaction frauduleuse → CRITIQUE (rouge) + SHAP
    - Upload CSV → Résultats batch

- [ ] **Tester sur l'ordinateur de présentation** (si différent du vôtre) :
  - [ ] Installer Python + dépendances
  - [ ] Tester l'application Streamlit
  - [ ] Vérifier la résolution d'écran (ajuster taille police Streamlit si besoin)

---

### Répétition de la Présentation (2-3 heures au total)

- [ ] **Répétition 1 : Lecture à voix haute** (seule)
  - [ ] Lire les slides et notes oratoires
  - [ ] Chronométrer : Objectif 20-25 minutes
  - [ ] Noter les parties trop longues ou trop courtes

- [ ] **Répétition 2 : Présentation devant quelqu'un** (ami, famille)
  - [ ] Demander des retours sur la clarté
  - [ ] Vérifier que la démo est fluide
  - [ ] Ajuster le rythme

- [ ] **Répétition 3 : Présentation finale** (veille de la soutenance)
  - [ ] Chronométrer précisément
  - [ ] S'entraîner aux transitions entre slides
  - [ ] Pratiquer la gestion du stress (respiration, pauses)

---

### Préparation aux Questions du Jury (1 heure)

**Lire les réponses préparées dans `docs/PLAN_PRESENTATION_SOUTENANCE.md` section "Questions Fréquentes"**

- [ ] **Question 1 :** "Pourquoi Random Forest et pas Deep Learning ?"
- [ ] **Question 2 :** "Comment gérez-vous le concept drift ?"
- [ ] **Question 3 :** "SMOTE ne crée-t-il pas des exemples irréalistes ?"
- [ ] **Question 4 :** "Comment déployer en production ?"
- [ ] **Question 5 :** "Quel est le coût métier d'une erreur ?"
- [ ] **Question 6 :** "Pourquoi avez-vous changé de sujet ?"
  - **Réponse suggérée :** "J'ai rencontré des difficultés d'accès aux datasets médicaux annotés et des contraintes RGPD. J'ai choisi la détection de fraude bancaire qui reste très pertinent pour ma formation en Data Science appliquée à la gestion d'entreprise, et qui me permet de démontrer les mêmes compétences techniques."

- [ ] Préparer 2-3 questions à poser AU JURY en fin de soutenance :
  - Exemple : "Quelles sont selon vous les améliorations prioritaires pour ce projet ?"
  - Exemple : "Pensez-vous que ce type de système pourrait être déployé dans une banque marocaine ?"

---

## 📚 PRIORITÉ BASSE - Documents Complémentaires

### Rapport Écrit (Si demandé par l'école)

Si votre école demande un rapport écrit en plus de la présentation :

- [ ] **Créer un rapport PDF** (30-50 pages) structuré comme suit :
  1. Page de garde
  2. Résumé exécutif (2 pages) → Utiliser `RESUME_EXECUTIF.md`
  3. Table des matières
  4. Introduction (contexte, problématique, objectifs)
  5. État de l'art (revue de littérature)
  6. Méthodologie (données, preprocessing, modélisation)
  7. Résultats (performances, visualisations)
  8. Application développée (architecture, fonctionnalités)
  9. Conclusion et perspectives
  10. Bibliographie
  11. Annexes (code source, notebooks)

**Outils recommandés :**
- **LaTeX** (Overleaf) : Professionnel, idéal pour documents académiques
- **Word/Google Docs** : Plus simple, exporter en PDF
- **Markdown → PDF** : Utiliser Pandoc pour convertir vos .md existants

---

### Portfolio en Ligne (Optionnel mais impressionnant)

- [ ] **Déployer l'application sur Streamlit Cloud** (gratuit) :
  1. Aller sur https://streamlit.io/cloud
  2. Se connecter avec GitHub
  3. Déployer depuis le dépôt `Mariechanne/fraud-detection-pfe`
  4. Obtenir une URL publique : `https://fraud-detection-pfe.streamlit.app`
  5. Ajouter cette URL dans l'email à M. Doumi et dans la présentation

- [ ] **Créer une vidéo de démonstration** (2-3 minutes) :
  - [ ] Utiliser OBS Studio (gratuit) ou Loom
  - [ ] Montrer les 3 fonctionnalités principales
  - [ ] Uploader sur YouTube (non listée) ou Vimeo
  - [ ] Ajouter le lien dans le README.md et la présentation

---

## 🎯 Le Jour J - Checklist Finale (29 Novembre)

### Matériel à Apporter

- [ ] **Ordinateur portable** :
  - [ ] Batterie chargée à 100%
  - [ ] Chargeur dans le sac
  - [ ] Application Streamlit testée et fonctionnelle
  - [ ] Environnement virtuel activé et prêt
  - [ ] Fichier CSV de démo sur le Bureau

- [ ] **Clé USB de backup** :
  - [ ] Présentation PowerPoint (.pptx + .pdf)
  - [ ] Application Streamlit (dossier complet)
  - [ ] Environnement virtuel (optionnel, si possible)
  - [ ] Fichiers de démo

- [ ] **Documents imprimés** (3 exemplaires de chaque) :
  - [ ] Résumé exécutif (2 pages)
  - [ ] Présentation PowerPoint (slides imprimées, 4 par page)
  - [ ] CV (optionnel)

- [ ] **Autre** :
  - [ ] Bouteille d'eau
  - [ ] Mouchoirs (en cas de stress)
  - [ ] Montre (pour gérer le temps)
  - [ ] Carte d'étudiant / Convocation

---

### Préparation Technique (30 minutes avant)

- [ ] **Arriver 30 minutes en avance**
- [ ] **Tester le vidéoprojecteur / écran** :
  - [ ] Connecter l'ordinateur
  - [ ] Vérifier la résolution d'écran
  - [ ] Lancer la présentation PowerPoint (mode présentateur)
  - [ ] Tester la navigation entre slides
- [ ] **Lancer l'application Streamlit en arrière-plan** :
  ```bash
  source .venv/bin/activate
  streamlit run app/streamlit_app.py
  # Vérifier que http://localhost:8501 fonctionne
  # Minimiser la fenêtre (ne pas fermer)
  ```
- [ ] **Fermer toutes les applications non nécessaires** :
  - [ ] Fermer email, Slack, Discord, etc.
  - [ ] Désactiver les notifications (mode Ne Pas Déranger)
  - [ ] Fermer les onglets navigateur non utilisés
- [ ] **Positionner le fichier CSV de démo** sur le Bureau
- [ ] **Avoir le document avec les valeurs de test** à portée de main

---

### Pendant la Soutenance

**Gestion du temps :**
- [ ] Mettre une montre ou un timer discret
- [ ] Répartition :
  - 0-5 min : Introduction + Contexte
  - 5-11 min : Données + Méthodologie
  - 11-16 min : Résultats
  - 16-22 min : Démonstration Live
  - 22-25 min : Conclusion + Perspectives

**Posture :**
- [ ] Regarder le jury (pas l'écran)
- [ ] Parler lentement et articuler
- [ ] Utiliser des pauses pour laisser le jury assimiler
- [ ] Montrer de l'enthousiasme pour votre projet

**En cas de problème technique :**
- [ ] Si l'application Streamlit crash → Utiliser les screenshots dans la présentation
- [ ] Si projection ne fonctionne pas → Utiliser les slides imprimées
- [ ] Si question difficile → "C'est une excellente question, je ne suis pas sûre mais je pense que... Je peux investiguer davantage après la soutenance."

---

### Après la Soutenance

- [ ] **Remercier le jury**
- [ ] **Noter les remarques et suggestions** du jury
- [ ] **Demander quand les résultats seront communiqués**
- [ ] **Si réussite :** Célébrer ! 🎉
- [ ] **Si recommandations :** Prendre note pour améliorer le projet

---

## 📞 Contacts Utiles

### Encadrants
- **M. DOUMI KARIM** : [Email de M. Doumi]
- **M. KHALID BENABBESS** : [Email de M. Benabbess]

### Support Technique ESLSCA
- **Service informatique** : [Numéro/Email]
- **Secrétariat pédagogique** : [Numéro/Email]

### Ressources en Ligne
- **Votre GitHub** : https://github.com/Mariechanne/fraud-detection-pfe
- **Dataset Kaggle** : https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **Documentation SHAP** : https://shap.readthedocs.io/
- **Documentation Streamlit** : https://docs.streamlit.io/

---

## 🎯 Timeline Recommandé

### Semaine du 23-26 Novembre (6 jours avant soutenance)

**Lundi 23 :**
- ✅ Envoyer l'email à M. Doumi (FAIT avec votre message)
- [ ] Installer l'environnement virtuel
- [ ] Télécharger le dataset Kaggle
- [ ] Entraîner le modèle

**Mardi 24 :**
- [ ] Tester l'application Streamlit
- [ ] Lancer les tests unitaires
- [ ] Commencer la création du PowerPoint (slides 1-10)

**Mercredi 25 :**
- [ ] Finir le PowerPoint (slides 11-27)
- [ ] Première répétition de la présentation
- [ ] Préparer la démo live

**Jeudi 26 :**
- [ ] Deuxième répétition (devant quelqu'un)
- [ ] Préparer les réponses aux questions
- [ ] Créer les documents imprimés

**Vendredi 27 :**
- [ ] Répétition finale
- [ ] Tester sur l'ordinateur de présentation
- [ ] Préparer la clé USB de backup

**Weekend 28 :**
- [ ] Repos et révision légère
- [ ] Vérifier que tout est prêt
- [ ] Bonne nuit de sommeil !

---

## 🎉 Message de Motivation

**Vous avez fait un EXCELLENT travail !** 💪

Ce projet est :
- ✅ **Fonctionnel** : Application déployable et testée
- ✅ **Performant** : Métriques exceptionnelles (PR-AUC 0.84, Recall 87.8%)
- ✅ **Professionnel** : Code modulaire, tests, documentation complète
- ✅ **Innovant** : Intégration de SHAP pour l'interprétabilité

Le silence avec M. Doumi était un problème, mais la **QUALITÉ** de votre livrable compense largement. Vous avez les compétences techniques et un projet solide pour réussir votre soutenance.

**Conseils finaux :**
1. **Soyez confiante** : Vous maîtrisez votre sujet
2. **Soyez honnête** : Si vous ne savez pas, dites-le et proposez d'investiguer
3. **Montrez votre passion** : Expliquez pourquoi ce projet vous a intéressée
4. **Profitez du moment** : C'est l'aboutissement de votre formation !

**Bonne chance pour la soutenance du 29 novembre ! 🍀🎓**

---

*Dernière mise à jour : 23 novembre 2024*
