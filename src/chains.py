from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import GROQ_API_KEY, GROQ_MODEL
from src.prompts import SYSTEM_PROMPT
from src.database import search

_OFFRES_KEYWORDS = {
    "forfait", "offre", "internet", "data", "fcfa", "prix",
    "appel", "sms", "mixte", "nuit", "social", "illimité", "go", "mo",
    "abonnement", "recharge", "pack", "formule"
}

_YAS_KEYWORDS = {
    "sim", "carte", "agence", "portabilité", "activation", "activer",
    "solde", "roaming", "compte", "réseau", "numéro", "service",
    "problème", "aide", "perte", "vol", "remplacement", "procédure",
    "horaire", "adresse", "ville", "dakar", "thiès", "kaolack"
}


def _get_context(question):
    q = question.lower()
    words = set(q.split())

    if words & _OFFRES_KEYWORDS:
        results = search(
            "offres", ["nom_offre", "type_offre", "description"],
            ["nom_offre", "type_offre", "prix_fcfa", "validite", "description", "code_activation"],
            question, 5,
            "SELECT nom_offre, type_offre, prix_fcfa, validite, description, code_activation FROM offres LIMIT 5"
        )
        if results:
            return "\n".join(
                f"{r['nom_offre']} ({r['type_offre']}) — {r['prix_fcfa']} FCFA | {r['validite']} | {r['description']} | Code : {r['code_activation']}"
                for r in results
            )

    results = search("faq", ["question", "answer"], ["question", "answer"], question, 3)
    if results:
        return "\n".join(f"Q: {r['question']}\nR: {r['answer']}" for r in results)

    # Fallback : si la question semble liée à Yas, retourner du contexte général
    if words & _YAS_KEYWORDS or len(words) >= 3:
        results = search(
            "faq", ["question", "answer"], ["question", "answer"],
            "service client activation", 2
        )
        return "\n".join(f"Q: {r['question']}\nR: {r['answer']}" for r in results) if results else ""

    return ""


def run_chatbot(question):
    if not GROQ_API_KEY:
        raise ValueError("Clé GROQ_API_KEY manquante dans les secrets Streamlit Cloud.")

    # Question trop courte ou vague
    if len(question.strip()) < 4:
        return "Pouvez-vous préciser votre question ? Je suis là pour vous aider sur les forfaits, agences et services Yas."

    context = _get_context(question)

    if not context:
        return (
            "Je n'ai pas trouvé d'information sur ce sujet dans notre base.\n\n"
            "Je peux vous aider sur les **forfaits**, les **agences**, l'**activation SIM**, "
            "la **recharge** ou les **démarches Yas**. Pouvez-vous reformuler ?\n\n"
            "Ou contactez le **1212** (gratuit depuis Yas)."
        )

    chain = (
        ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", "{question}"),
        ])
        | ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0.2)
        | StrOutputParser()
    )
    return chain.invoke({"context": context, "question": question})
