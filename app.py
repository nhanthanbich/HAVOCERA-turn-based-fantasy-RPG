import streamlit as st
import sqlite3
import pandas as pd
import random as rd

# =========================== DATABASE ===========================
def create_connection():
    return sqlite3.connect("characters.db", check_same_thread=False)

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
    df.columns = [c.lower() for c in df.columns]  # Chuẩn hóa tên cột
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

# =========================== CHARACTER CLASS ===========================
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
st.set_page_config(page_title="Game Chiến Đấu", layout="wide")
st.title("⚔️ Game Chiến Đấu Theo Lượt")

create_table()

if "selected_character" not in st.session_state:
    st.session_state.selected_character = None

tab1, tab2, tab3 = st.tabs(["📘 Hướng Dẫn", "🛠️ Quản Lý Nhân Vật", "🎯 Bắt Đầu"])

# ======================= TAB 1: Hướng Dẫn ========================
with tab1:
    st.markdown("""
    ## 📖 Hướng Dẫn Chơi

    - **Tạo nhân vật** ở tab thứ 2: chọn tên + loài
    - **Chọn nhân vật** ở tab thứ 3 để bắt đầu
    - Khi chọn xong, hệ thống sẽ hiện tab **Chiến Đấu**
    """)

# ======================= TAB 2: Quản lý nhân vật ========================
with tab2:
    st.subheader("🧬 Tạo nhân vật mới")
    ten = st.text_input("Tên nhân vật")
    chon_species = st.selectbox("Chọn loài", list(species_base_stats.keys()))
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
            st.warning("⚠️ Nhập tên trước nghen!")

    st.subheader("📋 Danh sách nhân vật")
    df = get_all_characters()
    st.dataframe(df)

    if not df.empty:
        del_id = st.selectbox("Chọn ID để xoá", df["id"])
        if st.button("🗑️ Xoá nhân vật"):
            delete_character(del_id)
            st.success("🧹 Đã xoá thành công!")

# ======================= TAB 3: Bắt đầu ========================
with tab3:
    st.subheader("🚀 Chọn nhân vật để bắt đầu")
    df = get_all_characters()
    if not df.empty:
        char_names = df["name"].tolist()
        selected_name = st.selectbox("Tên nhân vật", char_names)
        if st.button("✅ Vào trận"):
            info = df[df["name"] == selected_name].iloc[0].to_dict()
            st.session_state.selected_character = info
            st.success(f"🎉 Đã chọn {selected_name}! Tab chiến đấu đã mở 🔥")
    else:
        st.warning("⚠️ Chưa có nhân vật nào!")

# ======================= TAB 4: Chiến đấu (chỉ hiển thị khi đã chọn) ========================
if st.session_state.selected_character:
    st.markdown("---")
    with st.expander("⚔️ Chiến Đấu", expanded=True):
        char = st.session_state.selected_character
        st.subheader(f"🔥 {char['name']} ({char['species']}) sẵn sàng chiến đấu!")

        st.markdown(f"""
        - 🎭 Vai trò: **{char['role']}**
        - 🗡️ Sức mạnh: **{char['strength']}**
        - 🔋 Mana: **{char['stamina']}**
        - ❤️ Máu: **{char['vitality']}**
        - 🎯 Crit: **{char['dexterity']}%**
        - 🌀 Né đòn: **{char['agility']}%**
        """)
        st.info("💡 Bạn có thể thêm hệ thống skill, địch và combat ở đây.")
else:
    st.markdown("### 🔒 Tab chiến đấu sẽ xuất hiện sau khi chọn nhân vật.")
