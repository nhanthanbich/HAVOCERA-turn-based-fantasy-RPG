import streamlit as st
from db import create_table, insert_character, get_all_characters, delete_character
from stats import species_base_stats, rand_stat

st.set_page_config(page_title="Game Chiến Đấu", layout="wide")
st.title("⚔️ Game Chiến Đấu Theo Lượt")

create_table()

if "selected_character" not in st.session_state:
    st.session_state.selected_character = None

tabs = ["📘 Hướng Dẫn", "🛠️ Quản Lý Nhân Vật", "🎯 Bắt Đầu"]
if st.session_state.selected_character:
    tabs.append("⚔️ Chiến Đấu")

tab_objects = st.tabs(tabs)
tab1, tab2, tab3 = tab_objects[:3]
tab4 = tab_objects[3] if len(tab_objects) > 3 else None

# Tab 1: Hướng dẫn
with tab1:
    st.markdown("""
    ## 📖 Hướng Dẫn
    - Tạo nhân vật ở tab 2
    - Chọn nhân vật ở tab 3 để mở tab Chiến đấu
    """)

# Tab 2: Quản lý
with tab2:
    st.subheader("🧬 Tạo nhân vật mới")
    ten = st.text_input("Tên nhân vật")
    chon_species = st.selectbox("Chọn loài", list(species_base_stats.keys()))
    if st.button("🎲 Tạo nhân vật"):
        if ten:
            base = species_base_stats[chon_species]
            char = {"name": ten, "species": chon_species, "role": base["role"]}
            for attr in ["strength", "stamina", "vitality", "dexterity", "agility"]:
                char[attr] = rand_stat(attr, base[attr])
            insert_character(char)
            st.success(f"✅ Đã tạo nhân vật {ten}")
        else:
            st.warning("⚠️ Nhập tên trước đã!")

    st.subheader("📋 Danh sách")
    df = get_all_characters()
    st.dataframe(df)

    st.subheader("🗑️ Xoá nhân vật")
    if not df.empty and "id" in df.columns:
        del_id = st.selectbox("Chọn ID để xoá", df["id"])
        if st.button("🗑️ Xoá"):
            delete_character(del_id)
            st.success("🧹 Đã xoá!")

# Tab 3: Bắt đầu
with tab3:
    st.subheader("🚀 Chọn nhân vật để bắt đầu")
    df = get_all_characters()
    if not df.empty and "name" in df.columns:
        char_names = df["name"].tolist()
        selected_name = st.selectbox("Chọn tên", char_names)
        if st.button("✅ Vào trận"):
            info = df[df["name"] == selected_name].iloc[0].to_dict()
            st.session_state.selected_character = info
            st.success(f"🎉 Đã chọn {selected_name}! Tab Chiến Đấu mở!")

# Tab 4: Chiến đấu
if tab4:
    with tab4:
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
        st.info("💡 Đây là nơi bạn có thể thêm hệ thống chiến đấu sau.")
