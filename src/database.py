import sqlite3
from src.config import DB_PATH

_STOP_WORDS = {
    "le", "la", "les", "un", "une", "des", "de", "du", "et", "en",
    "est", "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
    "mon", "ma", "mes", "ton", "ta", "tes", "son", "sa", "ses",
    "que", "qui", "quoi", "comment", "où", "quand", "pourquoi",
    "pour", "par", "avec", "sur", "sous", "dans", "au", "aux",
    "ce", "cet", "cette", "ces", "se", "si", "ne", "pas", "plus",
    "ou", "car", "mais", "donc", "or", "ni", "aussi",
    "ya", "yas", "sénégal",
}

def _keywords(text):
    return list({
        w.strip("?.,!;:\"'()")
        for w in text.lower().split()
        if len(w.strip("?.,!;:\"'()")) > 3 and w.lower() not in _STOP_WORDS
    })

def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def search(table, search_cols, select_cols, question, limit, fallback=None):
    kw = _keywords(question)
    if not kw:
        return []
    cond = " OR ".join([" OR ".join(f"LOWER({c}) LIKE ?" for c in search_cols)] * len(kw))
    params = [f"%{k}%" for k in kw for _ in search_cols]
    with _conn() as conn:
        rows = conn.execute(
            f"SELECT {', '.join(select_cols)} FROM {table} WHERE {cond} LIMIT {limit}",
            params
        ).fetchall()
    if not rows and fallback:
        with _conn() as conn:
            rows = conn.execute(fallback).fetchall()
    return [dict(r) for r in rows]
