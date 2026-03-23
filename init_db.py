import sqlite3
import pandas as pd
import os

DB_PATH = "yas.db"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def init_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    with sqlite3.connect(DB_PATH) as conn:
        for table in ["faq", "offres"]:
            pd.read_csv(os.path.join(DATA_DIR, f"{table}.csv")).to_sql(
                table, conn, if_exists="replace", index=False
            )

if __name__ == "__main__":
    init_database()
