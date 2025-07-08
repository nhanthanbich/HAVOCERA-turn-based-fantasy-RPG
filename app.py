import streamlit as st
from db import create_table, insert_character, get_all_characters, delete_character, create_connection
from stats import species_base_stats, rand_stat
from models import Witch, Vampire, Werewolf, get_class_by_species, create_character_from_dict
import random as rd

st.markdown("""
<h1 style='font-size: 42px; font-weight: normal;'>
🌀 <span style="
    background: linear-gradient(90deg, #8B0000, #800080);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;">
    Havocera 1.0
</span> : The rising of havoc ⚔️
</h1>
""", unsafe_allow_html=True)

create_table()

if "selected_character" not in st.session_state:
    st.session_state.selected_character = None

# Định nghĩa các tab chính
tabs = ["📘 Hướng dẫn", "🛠️ Tạo nhân vật", "👥 Danh sách nhân Vật", "🎯 Bắt đầu"]

# Thêm Tab "Chiến Đấu" nếu có nhân vật được chọn
if st.session_state.selected_character:
    tabs.append("⚔️ Chiến đấu")

# Tạo các đối tượng tab
tab_objects = st.tabs(tabs)

# Cập nhật các tab theo thứ tự mới
tab1, tab2, tab3, tab4 = tab_objects[:4]
tab5 = tab_objects[4] if len(tab_objects) > 4 else None

# ===== TAB 1: Hướng dẫn =====
with tab1:
    st.markdown("""
    ## 📖 Hướng dẫn
    - Tạo nhân vật ở tab 2
    - Chọn nhân vật ở tab 3 để mở tab Chiến đấu
    """)

# ===== TAB 2: Tạo nhân vật =====
with tab2:
    st.subheader("🧬 Tạo nhân vật mới")

    ten = st.text_input("Tên nhân vật")
    chon_species = st.selectbox("Chọn loài", list(species_base_stats.keys()))

    # Kiểm tra tên nhân vật đã tồn tại chưa
    existing_characters = get_all_characters()  # Lấy tất cả nhân vật
    existing_names = existing_characters["name"].tolist()  # Danh sách tên nhân vật

    if st.button("🎲 Tạo nhân vật"):
        if ten:
            if ten in existing_names:
                st.warning(f"⚠️ Tên '{ten}' đã tồn tại, vui lòng chọn tên khác.")
            else:
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

# ===== TAB 3: Danh Sách Nhân Vật =====
with tab3:
    st.subheader("📋 Danh sách nhân vật")

    # Lấy toàn bộ dữ liệu
    df = get_all_characters()

    # Lọc theo loài
    species_list = list(species_base_stats.keys())
    species_filter = st.selectbox("🔍 Lọc theo loài", ["Tất cả"] + species_list)

    if species_filter != "Tất cả":
        df = df[df["species"] == species_filter]

    # Khởi tạo trạng thái tìm kiếm nếu chưa có
    if "name_search" not in st.session_state:
        st.session_state.name_search = ""

    # Giao diện tìm kiếm + nút bấm 🔍
    col1, col2 = st.columns([10, 1])
    with col1:
        name_input = st.text_input("🔎 Tìm theo tên nhân vật", value=st.session_state.name_search, label_visibility="collapsed", placeholder="Nhập tên...")
    with col2:
        if st.button("🔍", help="Bấm để lọc theo tên"):
            st.session_state.name_search = name_input

    # Lọc theo tên nếu có
    if st.session_state.name_search:
        df = df[df["name"].str.lower().str.contains(st.session_state.name_search.lower())]

    # Biểu tượng & màu theo loài
    def get_species_icon(species):
        return {
            "Witch": "🧙‍♀️",
            "Vampire": "🧛",
            "Werewolf": "🐺",
            "Skeleton": "💀",
            "Demon": "😈",
            "Scarecrow": "🎃",
            "Butcher": "🔪",
            "Yeti": "🧊",
        }.get(species, "❓")

    def style_row_by_species(species):
        return f"background-color: { {
            'Witch': '#fef9e7',
            'Vampire': '#fdecea',
            'Werewolf': '#eafaf1',
            'Skeleton': '#f0f0f0',
            'Demon': '#fce4ec',
            'Scarecrow': '#f3e5f5',
            'Butcher': '#fbe9e7',
            'Yeti': '#e0f7fa',
        }.get(species, '#ffffff') }"

    # Hiển thị bảng
    if not df.empty:
        df["🧬 Species"] = df["species"].apply(lambda s: f"{get_species_icon(s)} {s}")
        df_view = df[["id", "name", "🧬 Species", "role", "strength", "stamina", "vitality", "dexterity", "agility"]]

        styled_df = df_view.style.apply(
            lambda row: [style_row_by_species(df.loc[row.name]["species"])] * len(row),
            axis=1
        )
        st.dataframe(styled_df, use_container_width=True)
    else:
        st.info("⚠️ Không có nhân vật nào phù hợp với bộ lọc.")

# ===== TAB 4: Bắt đầu =====
with tab4:
    st.header("🚀 Chuẩn bị Trận Đấu")
    import random as rd

    # ===== Khởi tạo session state =====
    defaults = {
        "player1": None, "player2": None, "attacker": None, "defender": None,
        "round_index": 1, "turn": 1, "combat_logs": [],
        "is_bot": False, "dice_rolled": False, "selected_character": False,
        "p1_roll": None, "p2_roll": None, "p1_done": False, "p2_done": False,
        "battle_started": False,
        "prev_name1": None, "prev_name2": None
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    species_icon_map = {
        "Witch": "🧙", "Vampire": "🧛", "Werewolf": "🐺", "Skeleton": "💀",
        "Demon": "😈", "Scarecrow": "🎃", "Butcher": "🔪", "Yeti": "🧊",
    }

    def reset_dice_state():
        for k in ["p1_roll", "p2_roll", "p1_done", "p2_done", "dice_rolled", "battle_started"]:
            st.session_state[k] = False if isinstance(defaults[k], bool) else None

    def build_players():
        from models import create_character_from_dict
        df_all = get_all_characters()
        info1 = df_all[df_all["name"] == st.session_state.name1].iloc[0].to_dict()
        info2 = df_all[df_all["name"] == st.session_state.name2].iloc[0].to_dict()
        st.session_state.player1 = create_character_from_dict(info1)
        st.session_state.player2 = create_character_from_dict(info2)

    # ===== Chế độ chơi =====
    mode = st.radio("🎮 Chọn chế độ chơi", ["PvP – Người vs Người", "PvE – Người vs Máy"])
    is_bot = mode == "PvE – Người vs Máy"
    st.session_state.is_bot = is_bot

    col1, col2 = st.columns(2)

    # ===== Người chơi 1 =====
    with col1:
        species1 = st.selectbox("🔮 Chọn loài", ["--- Chọn loài ---"] + list(species_base_stats.keys()), key="sp1")
        st.session_state.name1 = None
        if species1 != "--- Chọn loài ---":
            df1 = get_all_characters()
            df1 = df1[df1["species"] == species1]
            icon1 = species_icon_map.get(species1, "❓")
            st.markdown(f"### {icon1} Người chơi 1")
            if df1.empty:
                st.warning("⚠️ Loài này chưa có nhân vật.")
                st.stop()
            else:
                name1 = st.selectbox("🧬 Nhân vật", ["--- Chọn nhân vật ---"] + df1["name"].tolist(), key="char1")
                if name1 != "--- Chọn nhân vật ---":
                    st.session_state.name1 = name1

    # ===== Người chơi 2 / Bot =====
    with col2:
        species2 = st.selectbox("🔮 Chọn loài", ["--- Chọn loài ---"] + list(species_base_stats.keys()), key="sp2")
        st.session_state.name2 = None
        if species2 != "--- Chọn loài ---":
            df2 = get_all_characters()
            df2 = df2[df2["species"] == species2]
            icon2 = species_icon_map.get(species2, "❓")
            title2 = "🤖 Bot" if is_bot else f"{icon2} Người chơi 2"
            st.markdown(f"### {title2}")
            if df2.empty:
                st.warning("⚠️ Loài này chưa có nhân vật.")
                st.stop()
            else:
                name2 = st.selectbox("🧬 Nhân vật", ["--- Chọn nhân vật ---"] + df2["name"].tolist(), key="char2")
                if name2 != "--- Chọn nhân vật ---":
                    st.session_state.name2 = name2

    # ===== Reset nếu chọn lại nhân vật =====
    if st.session_state.prev_name1 != st.session_state.name1 or st.session_state.prev_name2 != st.session_state.name2:
        reset_dice_state()
        st.session_state.prev_name1 = st.session_state.name1
        st.session_state.prev_name2 = st.session_state.name2

    # ===== PvE =====
    if is_bot and st.session_state.name1 and st.session_state.name2:
        if not st.session_state.dice_rolled:
            if st.button("🎲 Tung xúc xắc để bắt đầu"):
                build_players()
                st.session_state.p1_roll = rd.randint(1, 6)
                st.session_state.p2_roll = rd.randint(1, 6)
                st.session_state.dice_rolled = True

        if st.session_state.dice_rolled:
            st.success(f"🎲 Bạn tung: {st.session_state.p1_roll}, 🤖 Bot tung: {st.session_state.p2_roll}")
            attacker = st.session_state.name1 if st.session_state.p1_roll >= st.session_state.p2_roll else st.session_state.name2
            st.info(f"🎯 {attacker} sẽ tấn công trước!")

            if st.button("✅ Bắt đầu trận đấu"):
                p1 = st.session_state.player1
                p2 = st.session_state.player2
                st.session_state.attacker = p1 if st.session_state.p1_roll >= st.session_state.p2_roll else p2
                st.session_state.defender = p2 if st.session_state.attacker == p1 else p1
                st.session_state.battle_started = True
                st.session_state.selected_character = True
                st.rerun()

    # ===== PvP =====
    elif not is_bot and st.session_state.name1 and st.session_state.name2:
        build_players()
        col3, col4 = st.columns(2)
        with col3:
            if not st.session_state.p1_done and st.button("🎲 Người chơi 1 tung"):
                st.session_state.p1_roll = rd.randint(1, 6)
                st.session_state.p1_done = True
        with col4:
            if not st.session_state.p2_done and st.button("🎲 Người chơi 2 tung"):
                st.session_state.p2_roll = rd.randint(1, 6)
                st.session_state.p2_done = True

        if st.session_state.p1_done:
            st.info(f"🧙 Người chơi 1 tung được: 🎲 {st.session_state.p1_roll}")
        if st.session_state.p2_done:
            st.info(f"🧙 Người chơi 2 tung được: 🎲 {st.session_state.p2_roll}")

        if st.session_state.p1_done and st.session_state.p2_done and not st.session_state.dice_rolled:
            attacker = st.session_state.name1 if st.session_state.p1_roll >= st.session_state.p2_roll else st.session_state.name2
            st.info(f"🎯 {attacker} sẽ tấn công trước!")

            if st.button("✅ Bắt đầu trận đấu"):
                p1 = st.session_state.player1
                p2 = st.session_state.player2
                st.session_state.attacker = p1 if st.session_state.p1_roll >= st.session_state.p2_roll else p2
                st.session_state.defender = p2 if st.session_state.attacker == p1 else p1
                st.session_state.round_index = 1
                st.session_state.turn = 1
                st.session_state.combat_logs = []
                st.session_state.battle_started = True
                st.session_state.selected_character = True
                st.session_state.dice_rolled = True
                st.rerun()

    elif not (st.session_state.name1 and st.session_state.name2):
        st.info("📌 Hãy chọn đủ loài và nhân vật.")

# === BẮT ĐẦU TAB 5 ===
if tab5:
    with tab5:
        st.header("⚔️ Trận Chiến Bắt Đầu!")

        # ===== Kiểm tra đã bắt đầu chưa =====
        if not st.session_state.get("battle_started", False):
            st.info("💡 Hãy chọn nhân vật và nhấn 'Bắt đầu trận đấu' ở Tab 4 trước khi vào trận.")
            st.stop()

        # ===== Gán attacker/defender =====
        atk = st.session_state.attacker
        dfd = st.session_state.defender
        round_idx = st.session_state.round_index

        # ===== Hiển thị thông tin nhân vật =====
        def show_info(p):
            try:
                st.subheader(f"🧍 {p.name} ({p.species})")
                st.markdown(f"""
                - 🎭 Vai trò: **{p.role}**  
                - 🗡️ Sức mạnh: **{p.atk}**  
                - 🔋 Mana: **{p.current_stamina}/{p.stamina}**  
                - ❤️ Máu: **{p.hp}/{p.max_hp}**  
                - 🎯 Crit: **{p.crit}%**  
                - 🌀 Né đòn: **{p.dodge}%**
                """)
            except Exception as e:
                st.error(f"💥 Không thể hiển thị thông tin nhân vật: {e}")
                st.stop()

        try:
            col1, col2 = st.columns(2)
            with col1:
                show_info(atk)
            with col2:
                show_info(dfd)
        except Exception as e:
            st.error(f"🚫 Không thể tạo layout nhân vật: {e}")
            st.stop()

        # ===== Header vòng đấu =====
        st.markdown(f"## 🔥 Vòng {round_idx} – {atk.name} hành động!")
        st.divider()
        st.subheader("🎬 Hành động đang diễn ra...")

        # ===== Kích hoạt lượt mới (nếu có hàm) =====
        if hasattr(atk, "start_turn"):
            atk.start_turn()

        # ===== Bot hoặc Người chơi điều khiển hành động =====
        if st.session_state.is_bot and atk == st.session_state.player2:
            atk.choose_skill(dfd, auto=True)
        else:
            if hasattr(atk, "choose_skill"):
                atk.choose_skill(dfd)
            else:
                atk.attack(dfd)

        # ===== Ghi log chiến đấu =====
        st.session_state.combat_logs += atk.get_logs()
        atk.clear_logs()

        # ===== Xử lý kết thúc trận =====
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
            # Đổi lượt, tăng round nếu cần
            st.session_state.attacker, st.session_state.defender = dfd, atk
            st.session_state.turn += 1
            if st.session_state.turn % 2 == 1:
                st.session_state.round_index += 1

        # ===== Fog Decay (sương mù) =====
        if st.session_state.turn >= 41:
            decay = ((st.session_state.turn - 21) // 20) * 100
            st.caption(f"🌫️ Lượt {st.session_state.turn}: Sương mù gây {decay} sát thương nếu máu > 200")
            for p in [atk, dfd]:
                if p.hp > 200:
                    p.hp = max(1, p.hp - decay)
                    st.warning(f"🌫️ {p.name} mất {decay} HP do sương mù tử khí!")

        # ===== Nhật ký chiến đấu =====
        st.divider()
        st.subheader("📜 Nhật ký chiến đấu")
        for log in st.session_state.combat_logs[::-1][:10]:
            st.markdown(f"- {log}")

# ===== KHÔNG TAB! Reset DB Ẩn Ở Góc Khuất =====
with st.sidebar.expander("🔐 Quản Trị Hệ Thống", expanded=False):
    st.markdown("### 🔐 Xác Thực Admin")

    # Sử dụng session_state để theo dõi trạng thái xác thực
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        password = st.text_input("Nhập mật khẩu", type="password")
        if st.button("🔓 Xác thực"):
            if password == "duyanh":
                st.session_state.admin_authenticated = True
                st.success("✅ Đã xác thực quyền admin!")
                st.rerun()  
            else:
                st.error("❌ Sai mật khẩu!")
        st.stop()

    # ✅ Sau khi xác thực: hiển thị tất cả tùy chọn quản trị
    st.success("✅ Đang ở chế độ quản trị!")

    # --- Xoá toàn bộ database ---
    st.markdown("#### 💣 Reset toàn bộ dữ liệu")
    if st.button("💥 Xoá tất cả nhân vật"):
        conn = create_connection()
        conn.execute("DELETE FROM characters")
        conn.commit()
        conn.close()
        st.success("💣 Đã reset toàn bộ database!")

    # --- Xoá toàn bộ nhân vật của một loài ---
    st.markdown("#### 🧹 Xoá toàn bộ nhân vật theo loài")
    species_list = list(species_base_stats.keys())
    selected_species = st.selectbox("🧬 Chọn loài để xoá", ["--- Chọn loài ---"] + species_list)

    if selected_species != "--- Chọn loài ---":
        if st.button("🗑️ Xoá tất cả nhân vật thuộc loài này"):
            conn = create_connection()
            conn.execute("DELETE FROM characters WHERE species = ?", (selected_species,))
            conn.commit()
            conn.close()
            st.success(f"🗑️ Đã xoá toàn bộ nhân vật của loài {selected_species}!")

    st.markdown("---")

    # --- Tuỳ chỉnh nâng cao ---
    st.markdown("#### ✏️ Tuỳ chỉnh nâng cao")

    df = get_all_characters()

    if df.empty:
        st.info("⚠️ Chưa có nhân vật nào trong hệ thống.")
    else:
        species_available = sorted(df["species"].unique().tolist())
        species_edit = st.selectbox("🔍 Chọn loài để chỉnh sửa", ["--- Chọn loài ---"] + species_available, key="edit_species")

        if species_edit != "--- Chọn loài ---":
            df_filtered = df[df["species"] == species_edit]
            names_in_species = df_filtered["name"].tolist()

            if not names_in_species:
                st.info("⚠️ Không có nhân vật nào thuộc loài này.")
            else:
                name_edit = st.selectbox("🧬 Chọn nhân vật", ["--- Chọn nhân vật ---"] + names_in_species, key="edit_name")

                if name_edit != "--- Chọn nhân vật ---":
                    char_info = df_filtered[df_filtered["name"] == name_edit].iloc[0]

                    st.markdown("##### ✍️ Chỉnh sửa thông tin")

                    # Nhập tên mới
                    new_name = st.text_input("🆕 Đổi tên nhân vật", value=char_info["name"], key="edit_name_input")

                    # Nhập chỉ số mới
                    attrs = ["strength", "stamina", "vitality", "dexterity", "agility"]
                    new_values = {}
                    for attr in attrs:
                        new_values[attr] = st.number_input(
                            f"{attr.capitalize()}", value=int(char_info[attr]), min_value=0, step=1, key=f"{attr}_edit"
                        )

                    # Lưu thay đổi
                    if st.button("💾 Lưu chỉnh sửa"):
                        conn = create_connection()
                        conn.execute("UPDATE characters SET name = ? WHERE id = ?", (new_name, int(char_info["id"])))
                        for attr, val in new_values.items():
                            conn.execute(f"UPDATE characters SET {attr} = ? WHERE id = ?", (val, int(char_info["id"])))
                        conn.commit()
                        conn.close()
                        st.success("✅ Đã lưu thay đổi!")

                    # Xoá nhân vật
                    if st.button("❌ Xoá nhân vật này"):
                        delete_character(char_info["id"])
                        st.success("🗑️ Đã xoá nhân vật thành công!")
