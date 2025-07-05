import streamlit as st
from db import create_table, insert_character, get_all_characters, delete_character, create_connection
from stats import species_base_stats, rand_stat
from models import Witch, Vampire, Werewolf, get_class_by_species, create_character_from_dict

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

# ===== TAB 1: Hướng dẫn =====
with tab1:
    st.markdown("""
    ## 📖 Hướng Dẫn
    - Tạo nhân vật ở tab 2
    - Chọn nhân vật ở tab 3 để mở tab Chiến đấu
    """)

# ===== TAB 2: Quản lý nhân vật =====
with tab2:
    st.subheader("🧬 Tạo nhân vật mới")

    ten = st.text_input("Tên nhân vật")
    chon_species = st.selectbox("Chọn loài", list(species_base_stats.keys()))

    if st.button("🎲 Tạo nhân vật"):
        if ten:
            base = species_base_stats[chon_species]
            char = {
                "name": ten,
                "species": chon_species,
                "role": base["role"],
            }
            for attr in ["strength", "stamina", "vitality", "dexterity", "agility"]:
                char[attr] = rand_stat(attr, base[attr])

            insert_character(char)
            st.success(f"✅ Đã tạo nhân vật {ten}")
        else:
            st.warning("⚠️ Nhập tên trước nghen!")

    st.divider()
    st.subheader("📋 Danh sách nhân vật")

    df = get_all_characters()
    species_list = list(species_base_stats.keys())
    species_filter = st.selectbox("🔍 Lọc theo loài", ["Tất cả"] + species_list)

    if species_filter != "Tất cả":
        df = df[df["species"] == species_filter]

    # Biểu tượng & màu theo loài
    def get_species_icon(species):
        return {
            "Witch": "🧙‍♀️",
            "Vampire": "🧛",
            "Werewolf": "🐺"
        }.get(species, "❓")

    def style_row_by_species(species):
        return f"background-color: { {
            'Witch': '#fef9e7',
            'Vampire': '#fdecea',
            'Werewolf': '#eafaf1'
        }.get(species, '#fff') }"

    if not df.empty:
        df["🧬 Species"] = df["species"].apply(lambda s: f"{get_species_icon(s)} {s}")
        df_view = df[["id", "name", "🧬 Species", "role", "strength", "stamina", "vitality", "dexterity", "agility"]]

        styled_df = df_view.style.apply(
            lambda row: [style_row_by_species(df.loc[row.name]["species"])] * len(row),
            axis=1
        )
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("⚠️ Không có nhân vật nào phù hợp.")

    st.divider()
    st.subheader("🗑️ Xoá nhân vật")

    if not df.empty and "id" in df.columns:
        del_id = st.selectbox("Chọn ID để xoá", df["id"])
        if st.button("🗑️ Xoá"):
            delete_character(del_id)
            st.success("🧹 Đã xoá thành công!")
    else:
        st.info("⛔ Không có nhân vật nào để xoá!")

# ===== TAB 3: Bắt đầu =====
with tab3:
    st.header("🚀 Chuẩn bị Trận Đấu")

    # Reset flag
    st.session_state.battle_started = False

    if "player1" not in st.session_state:
        st.session_state.player1 = None
    if "player2" not in st.session_state:
        st.session_state.player2 = None
    if "is_bot" not in st.session_state:
        st.session_state.is_bot = False

    mode = st.radio("🎮 Chọn chế độ chơi", ["PvP – Người vs Người", "PvE – Người vs Máy"])
    is_bot = mode == "PvE – Người vs Máy"
    st.session_state.is_bot = is_bot

    col1, col2 = st.columns(2)

    # === Người chơi 1 ===
    with col1:
        st.markdown("### 🧙 Người chơi 1")
        species1 = st.selectbox("🔮 Chọn chủng loài", list(species_base_stats.keys()), key="sp1-select")
        df1 = get_all_characters()
        df1 = df1[df1["species"] == species1]

        if not df1.empty:
            name1 = st.selectbox("🧬 Chọn nhân vật", df1["name"].tolist(), key="char1-select")
            if st.button("🎲 Random NV 1"):
                name1 = df1.sample(1)["name"].values[0]
                st.session_state["char1-select"] = name1
                st.success(f"✅ Đã random: {name1}")
        else:
            st.warning("⚠️ Không có nhân vật cho species này.")
            name1 = None

    # === Người chơi 2 hoặc Bot ===
    with col2:
        title = "🤖 Bot" if is_bot else "🧙 Người chơi 2"
        st.markdown(f"### {title}")
        species2 = st.selectbox("🔮 Chọn chủng loài", list(species_base_stats.keys()), key="sp2-select")
        df2 = get_all_characters()
        df2 = df2[df2["species"] == species2]

        if not df2.empty:
            name2 = st.selectbox("🧬 Chọn nhân vật", df2["name"].tolist(), key="char2-select")
            if st.button("🎲 Random NV 2"):
                name2 = df2.sample(1)["name"].values[0]
                st.session_state["char2-select"] = name2
                st.success(f"✅ Đã random: {name2}")
        else:
            st.warning("⚠️ Không có nhân vật cho species này.")
            name2 = None

    # === Bắt đầu chiến đấu ===
    if st.button("🚀 Bắt đầu chiến đấu") and name1 and name2:
        df = get_all_characters()
        info1 = df[df["name"] == name1].iloc[0].to_dict()
        info2 = df[df["name"] == name2].iloc[0].to_dict()

        player1 = create_character_from_dict(info1)
        player2 = create_character_from_dict(info2)

        st.session_state.battle_ready = True
        st.success("🎯 Chiến đấu sẵn sàng! Hãy sang Tab Chiến Đấu!")
    else:
        st.info("📌 Hãy chọn đủ hai nhân vật trước khi bắt đầu.")

# ===== TAB 4: Chiến đấu =====
if tab4:
    with tab4:
        st.header("⚔️ Trận Chiến Bắt Đầu!")

        if not st.session_state.get("battle_started", False):
            st.info("💡 Hãy chọn nhân vật và nhấn 'Bắt đầu chiến đấu' ở Tab 3 trước khi vào trận.")
        else:
            atk = st.session_state.attacker
            dfd = st.session_state.defender
            round_idx = st.session_state.round_index

            st.markdown(f"## 🔥 Vòng {round_idx} – {atk.name} ra tay trước!")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader(f"🧍 {atk.name} ({atk.species})")
                st.markdown(f"""
                - 🎭 Vai trò: **{atk.role}**  
                - 🗡️ Sức mạnh: **{atk.atk}**  
                - 🔋 Mana: **{atk.current_stamina}/{atk.stamina}**  
                - ❤️ Máu: **{atk.hp}/{atk.max_hp}**  
                - 🎯 Crit: **{atk.crit}%**  
                - 🌀 Né đòn: **{atk.dodge}%**
                """)

            with col2:
                st.subheader(f"🧍 {dfd.name} ({dfd.species})")
                st.markdown(f"""
                - 🎭 Vai trò: **{dfd.role}**  
                - 🗡️ Sức mạnh: **{dfd.atk}**  
                - 🔋 Mana: **{dfd.current_stamina}/{dfd.stamina}**  
                - ❤️ Máu: **{dfd.hp}/{dfd.max_hp}**  
                - 🎯 Crit: **{dfd.crit}%**  
                - 🌀 Né đòn: **{dfd.dodge}%**
                """)

            # ===== THỰC HIỆN HÀNH ĐỘNG =====
            st.divider()
            st.subheader("🎬 Hành động đang diễn ra...")

            # Gọi hành động chiến đấu
            if st.session_state.is_bot and atk == st.session_state.player2:
                atk.choose_skill(dfd, auto=True)
            else:
                if hasattr(atk, "choose_skill"):
                    atk.choose_skill(dfd)
                else:
                    atk.attack(dfd)

            # Lưu nhật ký
            st.session_state.combat_logs += atk.get_logs()
            atk.clear_logs()

            # ===== KIỂM TRA KẾT THÚC =====
            if atk.hp <= 0 and dfd.hp <= 0:
                st.error("☠️ Cả hai chiến binh đã gục ngã cùng lúc. Hòa nhau!")
                st.session_state.battle_started = False
            elif dfd.hp <= 0:
                st.success(f"🏆 {atk.name} CHIẾN THẮNG TUYỆT ĐỐI!")
                st.session_state.battle_started = False
            elif atk.hp <= 0:
                st.success(f"🏆 {dfd.name} LẬT KÈO CHIẾN THẮNG!")
                st.session_state.battle_started = False
            else:
                # Hoán đổi lượt
                st.session_state.attacker, st.session_state.defender = dfd, atk
                st.session_state.turn += 1
                if st.session_state.turn % 2 == 1:
                    st.session_state.round_index += 1

            # ===== HIỂN THỊ NHẬT KÝ =====
            st.divider()
            st.subheader("📜 Nhật ký chiến đấu")
            for log in st.session_state.combat_logs[::-1][:10]:  # hiển thị 10 dòng gần nhất
                st.markdown(f"- {log}")

            # ===== CẬP NHẬT THÊM =====
            if st.session_state.turn >= 41:
                decay_hp = ((st.session_state.turn - 21) // 20) * 100
                for p in [atk, dfd]:
                    if p.hp > 200:
                        p.hp = max(1, p.hp - decay_hp)
                        st.warning(f"🌫️ {p.name} mất {decay_hp} HP do sương mù tử khí bao phủ đấu trường!")

# ===== KHÔNG TAB! Reset DB Ẩn Ở Góc Khuất =====
with st.sidebar.expander("🔐"):
    password = st.text_input("Xác thực admin", type="password", label_visibility="collapsed")
    if password == "duyanh":
        if st.button("💥 Reset toàn bộ dữ liệu"):
            conn = create_connection()
            conn.execute("DELETE FROM characters")
            conn.commit()
            conn.close()
            st.success("💣 Đã reset toàn bộ database!")
