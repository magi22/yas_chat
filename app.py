import streamlit as st
import os

st.set_page_config(page_title="Yas Sénégal — Assistant", page_icon="📱", layout="centered")

# Injection clé Groq
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

if not os.environ.get("GROQ_API_KEY"):
    st.error("⚠️ Clé API manquante. Ajoutez `GROQ_API_KEY` dans Settings → Secrets.")
    st.stop()

# Initialisation base de données
if not os.path.exists("yas.db"):
    with st.spinner("Chargement…"):
        from init_db import init_database
        init_database()

from src.chains import run_chatbot

# En-tête
st.markdown("## 📱 Assistant Yas Sénégal")
st.markdown("Posez vos questions sur nos forfaits, agences et services.")
st.markdown("---")

# Exemples cliquables
st.markdown("**Exemples de questions :**")
col1, col2 = st.columns(2)
examples = [
    "Quels forfaits internet avez-vous ?",
    "Où est l'agence de Dakar ?",
    "Comment activer ma SIM ?",
    "Comment recharger mon crédit ?",
]
for i, ex in enumerate(examples):
    col = col1 if i % 2 == 0 else col2
    with col:
        if st.button(ex, use_container_width=True, key=f"ex_{i}"):
            st.session_state.pending = ex

st.markdown("---")

# Historique
WELCOME = "Bonjour ! Comment puis-je vous aider aujourd'hui ?"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Traitement question (saisie ou bouton exemple)
question = st.session_state.pop("pending", None) or st.chat_input("Écrivez votre question…")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("…"):
            response = run_chatbot(question)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

# Pied de page
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🔄 Réinitialiser", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
        st.rerun()

st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.85rem;margin-top:0.5rem;'>"
    "📞 <strong>1212</strong> (gratuit depuis Yas) | "
    "<a href='https://yas.sn' target='_blank'>yas.sn</a></div>",
    unsafe_allow_html=True,
)
