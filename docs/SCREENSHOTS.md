# 📸 Guide pour Prendre les Captures d'Écran

Ce guide vous explique **quelles captures d'écran prendre** et **comment les ajouter au README**.

---

## 🎯 Captures d'Écran Nécessaires

### 1. **app-overview.png** — Vue d'ensemble de l'application

**Ce qu'il faut montrer :**
- Sidebar avec le seuil et les métriques du modèle
- Section "Analyse de Transaction Unique" visible
- Header avec le logo et la date

**Comment capturer :**
1. Lancez l'application : `streamlit run app/streamlit_app.py`
2. Attendez le chargement complet
3. Capturez la page d'accueil (plein écran recommandé)

**Résolution recommandée :** 1920x1080 ou 1600x900

---

### 2. **single-transaction-form.png** — Formulaire de transaction unique

**Ce qu'il faut montrer :**
- Champs Amount et Time remplis
- Bouton "Charger Exemple" visible
- Variables avancées (V1-V28) en mode replié ou ouvert

**Comment capturer :**
1. Remplissez les champs Amount (ex: 150.00) et Time (ex: 50000)
2. Cochez "Variables avancées" pour montrer V1-V28
3. Capturez avant de cliquer sur "Analyser"

---

### 3. **single-transaction-result.png** — Résultat de l'analyse

**Ce qu'il faut montrer :**
- Verdict (FRAUDE DÉTECTÉE ou NORMALE)
- Les 4 métriques : Probabilité, Niveau de risque, Seuil
- Barre de progression
- Graphique "Score de fraude vs Seuil"
- Recommandation (alerte)

**Comment capturer :**
1. Cliquez sur "Charger Exemple" puis "Analyser"
2. Scrollez pour voir tout le résultat
3. Capturez toute la section résultats

---

### 4. **shap-explanation.png** — Explications SHAP

**Ce qu'il faut montrer :**
- Section "Analyse détaillée des facteurs" (expander ouvert)
- Top 5 facteurs influents (gauche)
- Graphique SHAP (droite)
- Interprétation en bas

**Comment capturer :**
1. Après avoir analysé une transaction
2. Ouvrez l'expander "📊 Analyse détaillée des facteurs"
3. Capturez les deux colonnes (texte + graphique)

---

### 5. **batch-analysis.png** — Analyse par lot (CSV)

**Ce qu'il faut montrer :**
- Section "Analyse par Lot (CSV)"
- Fichier uploadé (data/examples/sample_transactions.csv)
- Statistiques principales (4 métriques)
- Alertes si fraudes détectées

**Comment capturer :**
1. Scrollez vers la section "Analyse par Lot"
2. Uploadez `data/examples/sample_transactions.csv`
3. Attendez l'analyse
4. Capturez le résumé (avant les onglets)

---

### 6. **batch-results-tabs.png** — Onglets de résultats batch

**Ce qu'il faut montrer :**
- Les 4 onglets : "Données complètes", "Fraudes détectées", "Distribution", "Analyse par risque"
- Graphique visible (histogramme ou pie chart)

**Comment capturer :**
1. Après analyse du CSV
2. Cliquez sur l'onglet "Distribution" ou "Analyse par risque"
3. Capturez l'onglet actif avec le graphique

---

### 7. **sidebar-config.png** — Configuration et métriques (optionnel)

**Ce qu'il faut montrer :**
- Slider de seuil
- Jauge visuelle
- Métriques du modèle (PR-AUC, ROC-AUC, etc.)
- Informations techniques

**Comment capturer :**
1. Zoomez sur la sidebar (panneau gauche)
2. Capturez toute la sidebar

---

## 🛠️ Outils pour Capturer

### Sur Windows :
- **Outil Capture d'écran** (Touche Windows + Shift + S)
- **Snipping Tool**
- **ShareX** (gratuit, recommandé)

### Sur macOS :
- **Cmd + Shift + 4** (zone sélectionnée)
- **Cmd + Shift + 3** (plein écran)

### Sur Linux :
- **Flameshot** (recommandé)
- **GNOME Screenshot**
- **Spectacle** (KDE)

---

## 📁 Où Sauvegarder les Images

Sauvegardez toutes les captures d'écran dans :

```
docs/images/
├── app-overview.png
├── single-transaction-form.png
├── single-transaction-result.png
├── shap-explanation.png
├── batch-analysis.png
├── batch-results-tabs.png
└── sidebar-config.png (optionnel)
```

**Format recommandé :** PNG (meilleure qualité)
**Taille maximale :** 500 KB par image (optimisez si nécessaire)

---

## 🖼️ Optimiser les Images (Optionnel)

Si les images sont trop lourdes (>500 KB), utilisez :

### En ligne :
- **TinyPNG** : https://tinypng.com/ (gratuit, excellent)
- **Squoosh** : https://squoosh.app/ (by Google)

### Outil CLI :
```bash
# Installer
pip install pillow

# Optimiser toutes les images
python scripts/optimize_images.py docs/images/
```

---

## ✅ Checklist Avant de Commit

- [ ] 6-7 images prises (au moins les 5 premières)
- [ ] Images sauvegardées dans `docs/images/`
- [ ] Noms de fichiers corrects (kebab-case, .png)
- [ ] Images optimisées (<500 KB chacune)
- [ ] Images claires et lisibles (résolution suffisante)
- [ ] Pas d'informations sensibles visibles
- [ ] Application en mode clair (pas dark mode)

---

## 🚀 Après Avoir Pris les Captures

Une fois les images dans `docs/images/`, dites-moi et je mettrai à jour le README.md pour les afficher automatiquement !

Les images seront ajoutées dans la section "📸 Aperçu" du README avec :
```markdown
![Nom de l'image](docs/images/nom-fichier.png)
```

---

**Astuce** : Prenez vos captures en **plein écran** pour une meilleure qualité, puis recadrez si nécessaire.
