# 📱 Yas Sénégal — Chatbot Service Clientèle

🚀 **Application en ligne** : [yas-chat.streamlit.app](https://yas-chat.streamlit.app/)
💻 **Code source** : [github.com/magi22/yas_chat](https://github.com/magi22/yas_chat)

Chatbot de service clientèle pour **Yas Sénégal** construit avec **LangChain** + **Gemini API** + **SQLite** + **Streamlit**.

## 🏗️ Architecture

```
Question utilisateur
   ↓
Classification de l'intention (LangChain + Gemini)
   ↓
Recherche dans SQLite (faq / offres / agences / procédures)
   ↓
Construction d'un contexte court
   ↓
Génération de réponse (Gemini API)
   ↓
Réponse finale — ou refus si hors contexte
```

## 📁 Structure du projet

```
yas_chatbot/
├── app.py              ← Interface Streamlit
├── init_db.py          ← Création de la base SQLite
├── requirements.txt    ← Dépendances Python
├── .env.example        ← Template de configuration
├── .gitignore
├── .python-version     ← Python 3.11
├── README.md
├── data/
│   ├── faq.csv         ← Questions fréquentes
│   ├── offres.csv      ← Forfaits Yas
│   ├── agences.csv     ← Agences Yas au Sénégal
│   └── procedures.csv  ← Démarches clients
└── src/
    ├── config.py       ← Chargement des variables d'environnement
    ├── prompts.py      ← Prompts du classificateur et du générateur
    ├── database.py     ← Recherche dans SQLite
    └── chains.py       ← Pipeline LangChain complet
```

## 🚀 Installation et lancement

### 1. Cloner le projet

```bash
git clone https://github.com/votre-username/yas_chatbot.git
cd yas_chatbot
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# ou
.venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la clé API Gemini

Créez un fichier `.env` à la racine du projet :

```bash
cp .env.example .env
```

Puis éditez `.env` et renseignez votre clé :

```
GOOGLE_API_KEY=votre_cle_api_gemini_ici
```

> 💡 Obtenez une clé gratuite sur [aistudio.google.com](https://aistudio.google.com/app/apikey)

### 5. Initialiser la base de données

```bash
python init_db.py
```

Cette commande crée le fichier `yas.db` à partir des CSV dans `data/`.

### 6. Lancer l'application

```bash
streamlit run app.py
```

L'interface s'ouvre automatiquement sur `http://localhost:8501`.

---

## 🧪 Exemples de questions à tester

| Catégorie   | Exemple de question |
|-------------|---------------------|
| FAQ         | "Comment recharger mon crédit ?" |
| FAQ         | "Quel est le numéro du service client ?" |
| Offres      | "Quels forfaits internet avez-vous à 1000 FCFA ?" |
| Offres      | "Je cherche une offre mixte appels et data" |
| Agences     | "Où se trouve l'agence Yas de Thiès ?" |
| Agences     | "Quels sont les horaires de votre agence à Dakar ?" |
| Procédures  | "Comment faire la portabilité ?" |
| Procédures  | "J'ai perdu ma SIM, que faire ?" |
| Hors sujet  | "Qui a gagné la CAN 2024 ?" |

---

## 🛠️ Technologies utilisées

| Composant      | Technologie               |
|----------------|---------------------------|
| Modèle LLM     | Gemini 2.0 Flash Lite     |
| Orchestration  | LangChain 0.3             |
| Base de données| SQLite (via Python stdlib)|
| Interface      | Streamlit                 |
| Données        | CSV → SQLite              |
| Langage        | Python 3.11               |

## 📊 Base de données

La base SQLite contient 2 tables :

- **faq** (12 entrées) — Questions fréquentes, agences et procédures regroupées par catégorie
- **offres** (10 entrées) — Forfaits internet, voix et mixtes

## 📝 Pourquoi cette approche ?

Ce projet utilise une base **SQLite structurée** plutôt qu'un système RAG avec base vectorielle, pour plusieurs raisons :

- ✅ **Contrôle total** des réponses : les données sont structurées et vérifiables
- ✅ **Pas d'hallucinations** : le LLM ne génère que depuis le contexte fourni
- ✅ **Refus automatique** des questions hors périmètre Yas
- ✅ **Déploiement simple** : API cloud, pas de modèle local (Ollama)
- ✅ **Facile à expliquer** : pipeline clair en 4 étapes

## ☁️ Déploiement sur Streamlit Community Cloud

1. Pousser le dépôt sur GitHub (en excluant `.env` et `yas.db` via `.gitignore`).
2. Sur [share.streamlit.io](https://share.streamlit.io), créer une nouvelle app pointant vers `app.py`.
3. Dans **Settings → Secrets**, ajouter :

```toml
GOOGLE_API_KEY = "votre_cle_api_gemini_ici"
```

> Streamlit Cloud expose automatiquement ces secrets comme variables d'environnement, compatibles avec `os.getenv("GOOGLE_API_KEY")` dans `config.py`.

4. La base `yas.db` est générée au démarrage : ajouter dans `app.py` ou via un `@st.cache_resource` si nécessaire, ou lancer `init_db.py` en amont.

---

## 🤝 Contribution

Les données dans `data/*.csv` peuvent être enrichies librement pour améliorer la couverture du chatbot.
