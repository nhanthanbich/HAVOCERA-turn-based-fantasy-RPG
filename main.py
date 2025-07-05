import streamlit as st
from utils import *
from manager import them_nhan_vat, sua_nhan_vat, xoa_nhan_vat

st.set_page_config(page_title="HAVOCERA Arena", layout="wide")

# File path (sửa nếu đổi chỗ file)
CHARACTER_PATH = "data/HAVOCERA_Characters.xlsx"
BASE_PATH = "data/HAVOCERA.xlsx"

# Dữ liệu ban đầu
if "characters" not in st.session_state:
    st.session_state.characters = load_characters(CHARACTER_PATH)
    st.session_state.valid_classes = get_species_list(CHARACTER_PATH)
    st.session_state.player1 = None
    st.session_state.player2 = None
    st.session_state.mode = None
    st.session_state.tab_index = 0

# --- Tab điều hướng ---
tab_labels = ["📖 Giới thiệu", "🛠️ Quản lý nhân vật", "🎮 Chọn chế độ", "🧬 Chọn nhân vật", "⚔️ Chiến đấu"]
selected_tab = st.sidebar.radio("📂 Điều hướng", tab_labels, index=st.session_state.tab_index)

# ========== TAB 1: Giới thiệu ==========
if selected_tab == "📖 Giới thiệu":
    st.title("🧠 HAVOCERA – Chiến đấu chiến thuật theo lượt")
    st.markdown("""
    Chào mừng đến với đấu trường HAVOCERA – nơi các sinh vật kỳ dị tranh tài trong các trận chiến căng thẳng!  
    Bạn có thể chiến đấu theo chế độ PvP hoặc PvE. Mỗi nhân vật thuộc một `Species` với bộ chỉ số và kỹ năng riêng.

    👉 **Các tính năng:**
    - Tạo mới/sửa/xoá nhân vật
    - Chọn chế độ chơi và điều khiển bot thông minh
    - Giao diện đẹp & tương tác trực tiếp

    🔗 **Mô tả chi tiết nhân vật:** [Link tải về hoặc Google Docs (gửi sau)]
    """)

# ========== TAB 2: Thêm/Sửa/Xoá ==========
elif selected_tab == "🛠️ Quản lý nhân vật":
    st.title("🧑‍🔧 Quản lý nhân vật")

    option = st.selectbox("Chọn thao tác", ["Thêm nhân vật", "Sửa nhân vật", "Xoá nhân vật"])

    if option == "Thêm nhân vật":
        them_nhan_vat_gui(st, CHARACTER_PATH)
    elif option == "Sửa nhân vật":
        sua_nhan_vat_gui(st, CHARACTER_PATH)
    elif option == "Xoá nhân vật":
        xoa_nhan_vat_gui(st, CHARACTER_PATH)

# ========== TAB 3: Chọn chế độ ==========
elif selected_tab == "🎮 Chọn chế độ":
    st.title("🎮 Chọn chế độ chơi")

    mode = st.radio("Bạn muốn chơi chế độ nào?", ["PvP – Người với người", "PvE – Đấu máy"])

    if mode:
        st.session_state.mode = "pvp" if "PvP" in mode else "pve"
        st.success(f"Đã chọn chế độ: {'PvP' if st.session_state.mode == 'pvp' else 'PvE'}")
        st.session_state.tab_index = 3  # Sang tab chọn nhân vật

# ========== TAB 4: Chọn nhân vật ==========
elif selected_tab == "🧬 Chọn nhân vật":
    st.title("🧬 Chọn nhân vật")

    valid_classes = st.session_state.valid_classes
    characters = load_character_classes(CHARACTER_PATH)

    # Người chơi 1
    st.header("🧑 Người chơi 1 chọn nhân vật")
    species1 = st.selectbox("Chọn Species cho người chơi 1", valid_classes, key="sp1")
    chars1_df = characters.get(species1)
    if chars1_df is not None:
        name1 = st.selectbox("Chọn tên nhân vật", chars1_df["Name"].tolist(), key="char1")
        if name1 and st.button("✅ Chọn người chơi 1"):
            all_chars = load_characters_by_species(species1)
            st.session_state.player1 = next((c for c in all_chars if c.name == name1), None)
            st.success(f"Đã chọn: {name1} ({species1})")

    # Người chơi 2 hoặc bot
    if st.session_state.mode == "pvp":
        st.header("🧑 Người chơi 2 chọn nhân vật")
        species2 = st.selectbox("Chọn Species cho người chơi 2", valid_classes, key="sp2")
        chars2_df = characters.get(species2)
        if chars2_df is not None:
            name2 = st.selectbox("Chọn tên nhân vật", chars2_df["Name"].tolist(), key="char2")
            if name2 and st.button("✅ Chọn người chơi 2"):
                all_chars = load_characters_by_species(species2)
                st.session_state.player2 = next((c for c in all_chars if c.name == name2), None)
                st.success(f"Đã chọn: {name2} ({species2})")
    else:
        st.header("🤖 Bot sẽ tự chọn...")
        if st.button("🤖 Random bot"):
            sp = rd.choice(valid_classes)
            bot_chars = load_characters_by_species(sp)
            st.session_state.player2 = rd.choice(bot_chars)
            st.success(f"Bot chọn: {st.session_state.player2.name} ({sp})")

    # Khi chọn xong cả hai
    if st.session_state.player1 and st.session_state.player2:
        st.success("🎉 Cả hai người chơi đã chọn xong!")
        st.session_state.tab_index = 4  # Sang tab chiến đấu

# ========== TAB 5: Chiến đấu ==========
elif selected_tab == "⚔️ Chiến đấu":
    st.title("⚔️ Trận chiến bắt đầu")

    p1, p2 = st.session_state.player1, st.session_state.player2
    if p1 and p2:
        col1, col2 = st.columns(2)
        with col1:
            show_info(p1)
        with col2:
            show_info(p2)

        st.markdown("### 🎲 Tung xúc xắc để chọn người đi trước")
        if st.button("🎲 Tung xúc xắc"):
            p1_roll = roll_dice()
            p2_roll = roll_dice()
            st.write(f"{p1.name} tung được 🎲 {p1_roll}")
            st.write(f"{p2.name} tung được 🎲 {p2_roll}")
            first = p1 if p1_roll >= p2_roll else p2
            st.success(f"🛡️ {first.name.upper()} đi trước!")

        st.warning("🚧 Chức năng chiến đấu chi tiết sẽ bổ sung sau khi có class nhân vật.")
    else:
        st.info("Vui lòng chọn đầy đủ 2 nhân vật ở tab trước.")
