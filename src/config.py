import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "yas.db")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"
