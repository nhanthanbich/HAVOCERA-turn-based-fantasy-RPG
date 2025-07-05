import streamlit as st
import pandas as pd
import random as rd
import sqlite3
from abc import ABC, abstractmethod

# --- Setup database ---
conn = sqlite3.connect("characters.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS characters (
    Name TEXT PRIMARY KEY,
    Species TEXT,
    Role TEXT,
    Strength INTEGER,
    Stamina INTEGER,
    Vitality INTEGER,
    Dexterity INTEGER,
    Agility INTEGER
)''')
conn.commit()

# --- Base Stats ---
species_base_stats = {
    "Witch":     {"Role(s)": "Pháp sư, Cấu rỉa", "Strength": 41, "Stamina": 177, "Vitality": 711, "Dexterity": 44, "Agility": 15},
    "Vampire":   {"Role(s)": "Pháp sư",           "Strength": 67, "Stamina": 54,  "Vitality": 1455,"Dexterity": 10, "Agility": 20},
    "Werewolf":  {"Role(s)": "Sát thủ",           "Strength": 98, "Stamina": 34,  "Vitality": 819, "Dexterity": 45, "Agility": 29},
}

def rand_stat(attr, base):
    if attr == "Vitality":
        delta = 115
    elif attr in ["Dexterity", "Agility"]:
        delta = 5
    else:
        delta = 15
    return max(0, base + rd.randint(-delta, delta))

# --- Character Base Class ---
class Character(ABC):
    def __init__(self, name, species, role, strength, stamina, vitality, dexterity, agility):
        self.name = name
        self.species = species
        self.role = role
        self.strength = strength
        self.stamina = stamina
        self.vitality = vitality
        self.dexterity = dexterity
        self.agility = agility

    @abstractmethod
    def skill(self):
        pass

class Witch(Character):
    def skill(self):
        return f"{self.name} dùng Hỏa Cầu Thuật!"

class Vampire(Character):
    def skill(self):
        return f"{self.name} hút máu địch và hồi phục!"

class Werewolf(Character):
    def skill(self):
        return f"{self.name} tung đòn chớp nhoáng với móng vuốt!"

# --- App Layout ---
st.set_page_config(page_title="Turn-Based Battle Game")
tabs = st.tabs(["📘 Hướng dẫn", "🛠️ Quản lý nhân vật", "🚀 Bắt đầu", "⚔️ Chiến đấu"])

# --- Tab 1: Hướng dẫn ---
tabs[0].markdown("""
## 📘 Hướng dẫn
- **Tạo/sửa/xoá** nhân vật ở tab 2.
- **Chọn** nhân vật để bắt đầu trận đấu ở tab 3.
- Khi chọn xong, hệ thống sẽ **tự động chuyển sang tab 4** để chiến đấu!
""")

# --- Tab 2: Quản lý nhân vật ---
with tabs[1]:
    st.subheader("Tạo nhân vật mới")
    ten = st.text_input("Tên nhân vật")
    chon_species = st.selectbox("Chọn loài", list(species_base_stats.keys()))

    if st.button("Tạo nhân vật") and ten:
        base = species_base_stats[chon_species]
        nv = {
            "Name": ten,
            "Species": chon_species,
            "Role": base["Role(s)"],
            "Strength": rand_stat("Strength", base["Strength"]),
            "Stamina": rand_stat("Stamina", base["Stamina"]),
            "Vitality": rand_stat("Vitality", base["Vitality"]),
            "Dexterity": rand_stat("Dexterity", base["Dexterity"]),
            "Agility": rand_stat("Agility", base["Agility"]),
        }
        try:
            cursor.execute("INSERT INTO characters VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                tuple(nv.values()))
            conn.commit()
            st.success("Đã tạo nhân vật thành công!")
        except sqlite3.IntegrityError:
            st.error("Tên nhân vật đã tồn tại!")

    st.subheader("Danh sách nhân vật")
    df = pd.read_sql_query("SELECT * FROM characters", conn)
    st.dataframe(df)

    st.subheader("Xoá nhân vật")
    name_to_delete = st.selectbox("Chọn tên để xoá", df["Name"] if not df.empty else [])
    if st.button("Xoá") and name_to_delete:
        cursor.execute("DELETE FROM characters WHERE Name = ?", (name_to_delete,))
        conn.commit()
        st.warning(f"Đã xoá nhân vật {name_to_delete}")

# --- Tab 3: Bắt đầu ---
with tabs[2]:
    st.subheader("Chọn nhân vật để chiến đấu")
    df = pd.read_sql_query("SELECT * FROM characters", conn)
    if not df.empty:
        name_options = df["Name"].tolist()
        selected_name = st.selectbox("Chọn nhân vật", name_options)
        if st.button("Vào trận"):
            st.session_state["selected_character"] = df[df["Name"] == selected_name].iloc[0].to_dict()
            st.experimental_set_query_params(tab=3)
            st.success("Đang chuyển sang chiến đấu...")
    else:
        st.info("Chưa có nhân vật nào, hãy tạo ở tab trước!")

# --- Tab 4: Chiến đấu ---
with tabs[3]:
    st.subheader("Trận chiến bắt đầu!")
    if "selected_character" in st.session_state:
        char = st.session_state["selected_character"]
        if char["Species"] == "Witch":
            fighter = Witch(**char)
        elif char["Species"] == "Vampire":
            fighter = Vampire(**char)
        elif char["Species"] == "Werewolf":
            fighter = Werewolf(**char)
        else:
            st.error("Loài không hợp lệ!")
            st.stop()

        st.write(f"**{fighter.name}** vào trận với kỹ năng đặc biệt:")
        st.info(fighter.skill())
    else:
        st.warning("Hãy chọn nhân vật ở tab \"🚀 Bắt đầu\" để bắt đầu!")
