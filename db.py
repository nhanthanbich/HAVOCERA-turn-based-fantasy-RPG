import sqlite3
import pandas as pd

DB_NAME = "nhanvat.db"

def create_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_table():
    with create_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                species TEXT,
                role TEXT,
                strength INTEGER,
                stamina INTEGER,
                vitality INTEGER,
                dexterity INTEGER,
                agility INTEGER
            )
        """)


def insert_character(char):
    with create_connection() as conn:
        conn.execute("""
            INSERT INTO characters (name, species, role, strength, stamina, vitality, dexterity, agility)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            char["name"],
            char["species"],
            char["role"],
            char["strength"],
            char["stamina"],
            char["vitality"],
            char["dexterity"],
            char["agility"]
        ))

def get_all_characters():
    with create_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM characters", conn)
        df.columns = df.columns.str.lower()
        return df

def delete_character(char_id):
    with create_connection() as conn:
        conn.execute("DELETE FROM characters WHERE id = ?", (char_id,))
