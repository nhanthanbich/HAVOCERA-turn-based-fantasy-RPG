import streamlit as st
import sqlite3
import pandas as pd
import random as rd

# =========================== DATABASE ===========================
def create_connection():
    conn = sqlite3.connect("characters.db", check_same_thread=False)
    return conn

def create_table():
    conn = create_connection()
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
    conn.commit()
    conn.close()

def insert_character(char):
    conn = create_connection()
    conn.execute("""
        INSERT INTO characters (name, species, role, strength, stamina, vitality, dexterity, agility)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        char["Name"],
        char["Species"],
        char["Role(s)"],
        char["Strength"],
        char["Stamina"],
        char["Vitality"],
        char["Dexterity"],
        char["Agility"]
    ))
    conn.commit()
    conn.close()

def get_all_characters():
    conn = create_connection()
    df = pd.read_sql_query("SELECT * FROM characters", conn)
    conn.close()
    return df

def delete_character(char_id):
    conn = create_connection()
    conn.execute("DELETE FROM characters WHERE id = ?", (char_id,))
    conn.commit()
    conn.close()

# =========================== BASE STATS ===========================
species_base_stats = {
    "Witch":     {"Role(s)": "Pháp sư, Cấu rỉa", "Strength": 41, "Stamina": 177, "Vitality": 711, "Dexterity": 44, "Agility": 15},
    "Vampire":   {"Role(s)": "Pháp sư",           "Strength": 67, "Stamina": 54,  "Vitality": 1455, "Dexterity": 10, "Agility": 20},
    "Werewolf":  {"Role(s)": "Sát thủ",           "Strength": 98, "Stamina": 34,  "Vitality": 819,  "Dexterity": 45, "Agility": 29},
}

def rand_stat(attr, base):
    if attr == "Vitality":
        delta = 115
    elif attr in ["Dexterity", "Agility"]:
        delta = 5
    else:
        delta = 15
    return max(0, base + rd.randint(-delta, delta))

# =========================== CLASS CHARACTER ===========================
class Character:
    def __init__(self, info):
        self.name = info["name"]
        self.species = info["species"]
        self.role = info["role"]
        self.strength = info["strength"]
        self.stamina = info["stamina"]
        self.vitality = info["vitality"]
        self.dexterity = info["dexterity"]
        self.agility = info["agility"]

class Witch(Character): pass
class Vampire(Character): pass
class Werewolf(Character): pass

# =========================== STREAMLIT UI ===========================
st.set_page_config(page_title="Chiến Đấu Theo Lượt", layout="wide")
st.title("⚔️ Game Chiến Đấu Theo Lượt")

create_table()

if "selected_character" not in st.session_state:
    st.session_state.selected_character = None

tab1, tab2, tab3 = st.tabs(["📘 Hướng Dẫn", "🛠️ Quản Lý Nhân Vật", "🎯 Bắt Đầu"])

# TAB 1: Hướng dẫn
with tab1:
    st.markdown("""
    ### 📖 Hướng dẫn chơi
    1. Tạo nhân vật theo 1 trong 3 loài: Witch 🧙, Vampire 🧛, Werewolf 🐺.
    2. Mỗi loài có chỉ số riêng. Khi tạo, chỉ số sẽ biến thiên nhẹ quanh giá trị gốc.
    3. Chọn nhân vật để bắt đầu chiến đấu.
    4. Tab "Chiến đấu" sẽ mở khi đã chọn nhân vật thành công.
    """)

# TAB 2: Tạo/sửa/xoá
with tab2:
    st.subheader("🧬 Tạo nhân vật mới")
    ten = st.text_input("Tên nhân vật")
    chon_species = st.selectbox("Chọn chủng tộc", list(species_base_stats.keys()))
    if st.button("🎲 Tạo nhân vật"):
        if ten:
            base = species_base_stats[chon_species]
            char = {
                "Name": ten,
                "Species": chon_species,
                "Role(s)": base["Role(s)"],
                "Strength": rand_stat("Strength", base["Strength"]),
                "Stamina": rand_stat("Stamina", base["Stamina"]),
                "Vitality": rand_stat("Vitality", base["Vitality"]),
                "Dexterity": rand_stat("Dexterity", base["Dexterity"]),
                "Agility": rand_stat("Agility", base["Agility"]),
            }
            insert_character(char)
            st.success(f"✅ Đã tạo nhân vật {ten}")
        else:
            st.warning("⚠️ Nhập tên đã nghen")

    st.subheader("🗃️ Danh sách nhân vật")
    df = get_all_characters()
    st.dataframe(df)

    char_id_to_delete = st.number_input("ID cần xoá", step=1, min_value=1)
    if st.button("🗑️ Xoá nhân vật"):
        delete_character(char_id_to_delete)
        st.success(f"🚮 Đã xoá ID {char_id_to_delete}")

# TAB 3: Bắt đầu chọn nhân vật
with tab3:
    st.subheader("🚀 Chọn nhân vật để bắt đầu")
    df = get_all_characters()
    if not df.empty:
        char_names = df["name"].tolist()
        chon = st.selectbox("Chọn nhân vật", char_names)
        if st.button("✅ Xác nhận chọn"):
            info = df[df["name"] == chon].iloc[0].to_dict()
            st.session_state.selected_character = info
            st.success(f"🎉 Đã chọn {chon}! Qua tab Chiến đấu nào~")
    else:
        st.warning("⚠️ Chưa có nhân vật nào! Tạo ở tab Quản lý nha.")

# TAB 4: Chiến đấu (chỉ hiển thị nếu đã chọn)
if st.session_state.selected_character:
    with st.expander("⚔️ Chiến Đấu", expanded=True):
        char_info = st.session_state.selected_character
        st.subheader(f"🔥 {char_info['name']} sẵn sàng chiến đấu!")
        st.markdown(f"""
        - Chủng tộc: **{char_info['species']}**
        - Vai trò: **{char_info['role']}**
        - Sức mạnh: {char_info['strength']}
        - Mana (Stamina): {char_info['stamina']}
        - Máu (Vitality): {char_info['vitality']}
        - Tỉ lệ chí mạng: {char_info['dexterity']}%
        - Né tránh: {char_info['agility']}%
        """)
        st.info("💡 Đây là nơi bạn sẽ chiến đấu khi thêm kẻ địch và hệ thống combat!")
