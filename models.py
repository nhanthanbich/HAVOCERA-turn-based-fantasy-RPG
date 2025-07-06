import random as rd
from stats import compute_combat_stats

def get_class_by_species(species):
    class_map = {
        "Witch": Witch,
        "Vampire": Vampire,
        "Werewolf": Werewolf,
    }
    return class_map.get(species, Character)

def create_character_from_dict(info):
    cls = get_class_by_species(info["species"])
    combat_stats = compute_combat_stats(info)

    return cls(
        info["name"],
        info["species"],
        combat_stats["atk"],
        info["stamina"],
        combat_stats["hp"],
        combat_stats["crit"],
        combat_stats["dodge"]
    )

class Character:
    def __init__(self, name, species, atk, stamina, hp, crit, dodge):
        self.name = name
        self.species = species
        self.atk = int(atk)
        self.stamina = int(stamina)
        self.max_hp = int(hp)
        self.hp = int(hp)
        self.crit = int(crit)
        self.dodge = int(dodge)
        self.current_stamina = int(stamina)

        self.logs = [] 

    def log(self, message):
        self.logs.append(message)

    def get_logs(self):
        return self.logs

    def clear_logs(self):
        self.logs = []

    def attack(self, enemy):
        self.clear_logs()

        if self.current_stamina < 10:
            self.log(f"⚠️ {self.name} đã kiệt sức, phải tạm lui về dưỡng thần.")
            self.rest()
            return

        crit_rate = 2 if rd.random() < self.crit / 100 else 1
        damage = rd.randint(1, 6) + self.atk * crit_rate

        if crit_rate == 2:
            self.log(f"💥 {self.name} tung đòn **CHÍ MẠNG** vào {enemy.name}, gây {damage} sát thương!")
        else:
            self.log(f"⚔️ {self.name} tấn công {enemy.name}, gây {damage} sát thương.")

        enemy.take_damage(damage, self)
        self.current_stamina = min(self.current_stamina + 5, self.stamina)
        self.log(f"🔋 {self.name} hồi 5 stamina → {self.current_stamina}/{self.stamina}")

    def rest(self):
        restored = int(self.stamina * 0.5)
        self.current_stamina = min(self.current_stamina + restored, self.stamina)
        self.log(f"😮‍💨 {self.name} nghỉ ngơi, hồi {restored} stamina → {self.current_stamina}/{self.stamina}")

    def take_damage(self, damage, attacker=None, ignore_dodge=False):
        if self.hp <= 0:
            return False

        if not ignore_dodge and rd.random() < self.dodge / 100:
            self.log(f"🌀 {self.name} né tránh đòn công kích một cách ngoạn mục!")
            return False
        else:
            self.hp = max(self.hp - damage, 0)
            self.log(f"💔 {self.name} chịu {damage} sát thương → HP: {self.hp}/{self.max_hp}")
            return damage

    def info(self):
        return f"{self.name} ({self.species}) - ATK: {self.atk}, HP: {self.hp}/{self.max_hp}, " \
               f"Stamina: {self.current_stamina}/{self.stamina}, Crit: {self.crit}%, Dodge: {self.dodge}%"

class Witch(Character):
    def __init__(self, name, species, atk, stamina, hp, crit, dodge):
        super().__init__(name, species, atk, stamina, hp, crit, dodge)
        self.so_lan_thoi_khong = 0
        self.dark_ritual_used = False
        self.turn_count = 0
        self.next_attack_buffed = False

    def attack(self, target):
        damage = self.atk
        is_crit = rd.random() < self.crit / 100
        if is_crit:
            damage = int(damage * 1.5)
        if getattr(self, "next_attack_buffed", False):
            damage = int(damage * 1.3)
            st.markdown("💥 Huyết ấn nghi lễ còn vang vọng! Đòn đánh này được cường hóa thêm 30%!")
            self.next_attack_buffed = False
        st.markdown(f"{self.name} tấn công {target.name} và gây {damage} sát thương!")
        target.take_damage(damage, self)

    def nguyen_rua(self, enemy):
        cost = 4
        if self.current_stamina < cost:
            st.markdown(f"{self.name} không đủ năng lượng để thi triển Nguyền rủa!")
            self.rest()
            return
        self.current_stamina -= cost
        old_atk = enemy.atk
        reduce = math.ceil(enemy.atk * (rd.randint(22, 28) / 100))
        enemy.atk = max(1, enemy.atk - reduce)
        self.crit = min(self.crit + 7, 50)
        st.markdown(f"🕯️ {self.name} nguyền rủa {enemy.name}, giảm {reduce} ATK ({old_atk} → {enemy.atk})")
        st.markdown(f"🔮 {self.name} tăng 7% chí mạng (Crit: {self.crit}%)")
        if self.crit >= 45 and rd.random() < 0.5:
            lost = rd.randint(4, 6)
            enemy.current_stamina = max(0, enemy.current_stamina - lost)
            st.markdown(f"💫 Lời nguyền hút cạn linh lực! {enemy.name} mất thêm {lost} ⚡")

    def doc_duoc(self, enemy):
        cost = 12
        if self.current_stamina < cost:
            st.markdown(f"{self.name} không đủ tinh lực để sử dụng Độc Dược!")
            self.rest()
            return
        self.current_stamina -= cost
        base_damage = math.ceil(self.atk * 0.5)
        percent_damage = math.ceil(enemy.hp * (rd.randint(20, 28) / 100))
        damage = base_damage + percent_damage
        is_crit = rd.random() < self.crit / 100
        if is_crit:
            damage *= 2
        st.markdown(f"☠️ {self.name} ném độc dược ăn mòn linh hồn!")
        result = enemy.take_damage(damage, self)
        if result:
            if is_crit:
                heal = math.ceil(damage * 0.2)
                self.hp = min(self.hp + heal, self.max_hp)
                st.markdown(f"💥 Chí mạng! {self.name} hồi lại {heal} HP từ năng lượng độc dược!")
            self.dodge = min(self.dodge + 5, 33)
            st.markdown(f"🌫️ Né tránh của {self.name} tăng lên {self.dodge}%!")
        else:
            st.markdown(f"💨 Nhưng {enemy.name} đã né kịp!")

    def thoi_khong(self):
        cost = 49
        if self.current_stamina < cost:
            st.markdown(f"{self.name} không đủ sức mạnh để bẻ cong thời gian...")
            self.rest()
            return
        self.current_stamina -= cost
        chance = 0.9 - self.so_lan_thoi_khong * 0.22
        if rd.random() < chance:
            self.so_lan_thoi_khong += 1
            self.hp = self.max_hp
            old_atk = self.atk
            self.atk = max(1, math.ceil(self.atk * 0.55))
            self.dodge = min(self.dodge + 10, 33)
            st.markdown(f"⏳ {self.name} đảo ngược số phận! Hồi đầy HP, ATK giảm còn {self.atk}, né tránh tăng {self.dodge}%!")
        else:
            penalty = rd.randint(5, 10)
            self.hp = max(1, self.hp - penalty)
            st.markdown(f"🌀 Thất bại! {self.name} bị tổn thương bởi nghịch lý thời gian ({penalty} HP mất). HP còn {self.hp}/{self.max_hp}")

    def nghi_le_hac_am(self):
        if self.dark_ritual_used:
            st.markdown(f"{self.name} đã thực hiện nghi lễ rồi – không thể tái diễn!")
            return
        if self.hp > 250:
            self.hp = 250  # auto giảm về 250
        if self.current_stamina < 10:
            st.markdown(f"{self.name} quá kiệt sức để thực hiện nghi lễ!")
            self.rest()
            return
        self.dark_ritual_used = True
        self.current_stamina = 0
        self.max_stamina = 0
        hp_sacrifice = math.ceil(rd.randint(1,10))
        self.hp = max(1, self.hp - hp_sacrifice)
        bonus_hp = rd.randint(10, 20)
        hp_recovery = math.ceil(self.max_hp * bonus_hp / 100)
        self.hp = min(self.hp + hp_recovery, self.max_hp)
        giam_yeu = self.so_lan_thoi_khong
        boost = rd.randint(8 + 6 * giam_yeu, 12 + 10 * giam_yeu)
        self.atk += (boost * 3)
        self.crit = min(self.crit + 10, 50)
        self.next_attack_buffed = True
        st.markdown(f"🩸 {self.name} thực hiện nghi thức hắc ám!")
        st.markdown(f"💀 Đánh đổi {hp_sacrifice} HP, hồi lại {hp_recovery} HP như phần thưởng.")
        st.markdown(f"🔥 Nhận +{boost * 3} ATK, +10% Crit. Đòn đánh tiếp theo sẽ được cường hóa!")

    def start_turn(self):
        self.turn_count += 1
        if self.turn_count <= 5:
            old_max_hp = self.max_hp
            old_hp = self.hp
            old_stamina = self.current_stamina
            old_max_stamina = self.max_stamina
    
            self.max_hp += 56
            self.hp = min(self.hp + 56, self.max_hp)
    
            self.max_stamina += 7
            self.current_stamina = min(self.current_stamina + 7, self.max_stamina)
    
            self.atk += 8
            self.crit = min(self.crit + 1, 50)
            self.dodge = min(self.dodge + 1, 33)
    
            st.markdown(f"🌓 **{self.name} hấp thụ hắc khí trong không gian:**")
            st.markdown(f"- ❤️ HP: `{old_hp}/{old_max_hp}` → `{self.hp}/{self.max_hp}`")
            st.markdown(f"- ⚡ Stamina: `{old_stamina}/{old_max_stamina}` → `{self.current_stamina}/{self.max_stamina}`")
            st.markdown(f"- 🔺 +8 ATK (`{self.atk}`), +1% Crit (`{self.crit}%`), +1% Dodge (`{self.dodge}%`)")

    def choose_skill(self, enemy, auto=False):
        self.start_turn()
    
        if self.max_stamina == 0:
            if auto:
                st.markdown(f"🤖 {self.name} không còn phép – **AI đánh thường.**")
            else:
                st.markdown(f"{self.name} không còn phép thuật – chỉ có thể đánh thường!")
            self.attack(enemy)
            return
    
        if auto:
            st.markdown(f"🤖 **{self.name} (AI – Witch) đang chọn kỹ năng...**")
    
            # 🔮 Dự đoán tình huống nguy hiểm
            potential_danger = enemy.atk * 1.5
            if self.hp > 250 and (self.hp - potential_danger) <= 250 and self.current_stamina < 49 and self.so_lan_thoi_khong < 3:
                st.markdown(f"⚠️ **{self.name} dự đoán nguy hiểm – nghỉ ngơi để hồi stamina chuẩn bị dùng Thời Không.**")
                self.rest()
                return
    
            if self.hp <= 250 and self.current_stamina >= 49 and self.so_lan_thoi_khong < 3:
                self.thoi_khong()
                return
    
            if enemy.hp <= 200:
                self.attack(enemy)
                return
    
            if not self.dark_ritual_used and self.hp <= 250 and self.so_lan_thoi_khong >= 3:
                self.nghi_le_hac_am()
                return
    
            if self.so_lan_thoi_khong == 0 and self.current_stamina >= 4:
                self.nguyen_rua(enemy)
                return
    
            if self.so_lan_thoi_khong >= 1 and self.current_stamina >= 12:
                self.doc_duoc(enemy)
                return
    
            if self.so_lan_thoi_khong < 3 and self.current_stamina >= 49 and self.hp < self.max_hp * 0.4:
                self.thoi_khong()
                return
    
            self.attack(enemy)
            return
    
        # 🎮 Chế độ người chơi – dùng giao diện Streamlit
        st.markdown(f"🧙 **{self.name} (Witch)** chọn kỹ năng:")
        options = ["👊 Đánh thường"]
    
        if self.max_stamina > 0:
            options.append("🕯️ Nguyền Rủa (4 Stamina)")
            options.append("☠️ Độc Dược (12 Stamina)")
            if self.so_lan_thoi_khong < 3:
                options.append("⏳ Thời Không (49 Stamina)")
            if not self.dark_ritual_used:
                options.append("🩸 Nghi Lễ Hắc Ám")
        options.append("⚑ Đầu hàng")
    
        choice = st.radio("➤ Hành động:", options)
    
        if st.button("Thi triển"):
            if choice.startswith("👊"):
                self.attack(enemy)
            elif choice.startswith("🕯️"):
                self.nguyen_rua(enemy)
            elif choice.startswith("☠️"):
                self.doc_duoc(enemy)
            elif choice.startswith("⏳"):
                self.thoi_khong()
            elif choice.startswith("🩸"):
                pre_hp = self.hp
                success = self.nghi_le_hac_am()
                if not success or self.hp == pre_hp:
                    st.warning("❌ Nghi lễ bị hủy hoặc thất bại. Vui lòng chọn lại kỹ năng.")
            elif choice.startswith("⚑"):
                self.hp = 0
                st.error(f"⚑ {self.name} đã **đầu hàng**!")

class Vampire(Character):
    def __init__(self, name, species, atk, stamina, hp, crit, dodge):
        super().__init__(name, species, atk, stamina, hp, crit, dodge)
        self.khat_mau = False
        self.huyet_cau = 0
        self.rebirth_uses = 0

    def take_damage(self, damage, attacker=None):
        if self.hp <= 0:
            st.markdown(f"💀 **{self.name}** đã bị hạ gục, linh hồn tạm thời yên nghỉ...")
            return False

        hit = super().take_damage(damage, attacker)

        if self.hp > 0 and self.hp < self.max_hp * 0.2 and not self.khat_mau:
            self.khat_mau = True
            self.atk = math.ceil(self.atk * 1.5)
            self.crit = min(50, self.crit + 5)
            recovered = min(math.ceil(self.hp + 250), self.max_hp)
            self.hp = recovered
            st.markdown(f"🩸 **{self.name}** gầm lên trong cơn đói khát – ***KHÁT MÁU*** trỗi dậy!")
            st.markdown(f"- 🔺 ATK tăng lên `{self.atk}`, Crit +5% → `{self.crit}%`")
            st.markdown(f"- ❤️ HP hồi thêm **250** → `{self.hp}/{self.max_hp}`")
        return hit

    def hap_huyet(self, enemy):
        cost = 2
        if self.current_stamina < cost:
            st.markdown(f"⚠️ **{self.name}** không đủ sức để Hấp Huyết!")
            self.rest()
            return
    
        crit_rate = 2 if rd.random() < self.crit / 100 else 1
        variation = rd.randint(math.ceil(-self.atk * 0.3), math.ceil(self.atk * 0.3))
        base_damage = self.atk + variation
        damage = math.ceil(base_damage * crit_rate) + 10
    
        st.markdown(f"🩸 **{self.name}** lao tới hút máu **{enemy.name}**!")
    
        if crit_rate == 2:
            st.markdown(f"💢 **CHÍ MẠNG!** Cú cắn thấm đẫm máu!")
    
        result = enemy.take_damage(damage, self)
    
        if result:
            heal = math.ceil(result * 0.85) + rd.randint(-10, 10)
            self.hp = min(self.hp + heal, self.max_hp)
            self.current_stamina = min(self.current_stamina + 1, self.stamina)
            st.markdown(f"❤️ Hút được **{heal} HP**, hiện tại: `{self.hp}/{self.max_hp}`")
            st.markdown(f"⚡ Hồi lại 1 stamina → `{self.current_stamina}/{self.stamina}`")
    
            if self.khat_mau:
                extra = heal
                self.hp = min(self.hp + extra, self.max_hp)
                self.atk += 3
                st.markdown(f"🔥 Trong cơn khát máu, hút thêm **{extra} HP**, ATK tăng lên `{self.atk}`")
    
        self.current_stamina -= cost
    
    def huyet_bao(self, enemy, auto=False):
        cost = 11
        max_te = math.ceil(self.max_hp * 0.07)
    
        if self.current_stamina < cost:
            st.markdown(f"⚠️ **{self.name}** không đủ stamina thi triển Huyết Bạo.")
            self.rest()
            return
    
        if auto:
            expected_hp = enemy.hp
            for s in reversed(range(1, max_te + 1)):
                predicted_dmg = math.ceil(s * (rd.randint(17, 22) / 10)) + rd.randint(-8, 8)
                if predicted_dmg >= expected_hp:
                    chosen = s
                    break
            else:
                chosen = max_te
        else:
            chosen = st.slider(f"🩸 Chọn lượng máu để tế (tối đa {max_te})", 1, min(max_te, self.hp))
    
        self.hp = max(self.hp - chosen, 0)
        self.huyet_cau = math.ceil(chosen * (rd.randint(13, 16) / 10)) + rd.randint(-8, 12)
        st.markdown(f"🧬 **{self.name}** hiến tế **{chosen} HP** → tạo Huyết Cầu **{self.huyet_cau} sát thương**")
    
        crit = 2 if rd.random() < 0.23 else 1
        damage = math.ceil(self.huyet_cau * crit) + rd.randint(-10, 10)
    
        if crit == 2:
            st.markdown("💥 **Huyết Cầu CHÍ MẠNG** phát nổ!")
        else:
            st.markdown("🔴 Huyết Cầu được phóng ra với uy lực rực máu!")
    
        result = enemy.take_damage(damage, self)
    
        if result:
            st.markdown(f"☠️ **{enemy.name}** dính **{result}** sát thương.")
        else:
            poison_dmg = math.ceil(damage * 0.3)
            enemy.hp = max(enemy.hp - poison_dmg, 0)
            st.markdown(f"💨 **{enemy.name}** né được... nhưng nhiễm huyết độc, chịu **{poison_dmg}** sát thương!")
    
        self.huyet_cau = 0
        self.current_stamina -= cost
    
    def tai_sinh(self):
        if self.rebirth_uses >= 3:
            st.markdown(f"⚠️ **{self.name}** đã vượt giới hạn luân hồi. Không thể Tái Sinh nữa.")
            self.rest()
            return
    
        cost = 21
        if self.current_stamina < cost:
            st.markdown(f"⚠️ **{self.name}** không đủ sức để Tái Sinh.")
            self.rest()
            return
    
        heal_amt = cost * rd.randint(6, 9) + rd.randint(-10, 10)
        chance = 1.0
        count = 0
    
        st.markdown(f"🔁 **{self.name}** bắt đầu nghi thức **TÁI SINH**!")
    
        while chance > 0:
            roll = rd.random()
            if roll < chance:
                self.hp = min(self.hp + heal_amt, self.max_hp)
                count += 1
                st.markdown(f"  💉 Lần thay máu **{count}**: hồi **{heal_amt} HP** → `{self.hp}/{self.max_hp}`")
                chance -= 0.25
            else:
                st.markdown(f"  ❌ Lần thay máu **{count+1}** thất bại – linh hồn từ chối phục sinh.")
                break
    
        self.current_stamina -= cost
        self.rebirth_uses += 1

    def choose_skill(self, enemy, auto=False):
        if auto:
            st.markdown(f"🤖 **{self.name}** (AI – Vampire) đang phân tích tình hình...")
    
            danger_threshold = self.max_hp * 0.2
            potential_danger = enemy.atk * 1.4 + 10
    
            # 1. Nếu còn Huyết Cầu → ném luôn
            if self.huyet_cau > 0:
                st.markdown("🔴 **Còn Huyết Cầu – ưu tiên ném ngay!**")
                self.huyet_bao(enemy, auto=True)
                return
    
            # 2. Nếu gần nguy hiểm, nhưng chưa đủ điều kiện Tái Sinh → nghỉ
            if (
                self.hp > danger_threshold and
                (self.hp - potential_danger) <= danger_threshold and
                self.rebirth_uses < 3 and
                self.current_stamina < 21 and
                not self.khat_mau
            ):
                st.markdown("⚠️ **Dự đoán nguy hiểm – nghỉ để chuẩn bị Tái Sinh hoặc Khát Máu**")
                self.rest()
                return
    
            # 3. Tái Sinh khi sắp chết hoặc đã Khát Máu
            if self.hp < danger_threshold and self.rebirth_uses < 3 and self.current_stamina >= 21:
                if self.khat_mau or (self.hp - potential_danger <= 0):
                    st.markdown("💀 **Kích hoạt Tái Sinh!**")
                    self.tai_sinh()
                    return
                else:
                    st.markdown("🔄 **Chờ Khát Máu – chưa vội Tái Sinh.**")
                    self.rest()
                    return
    
            # 4. Nếu đủ điều kiện an toàn và tránh né địch không cao → dùng Huyết Bạo
            if self.current_stamina >= 11:
                max_te = math.ceil(self.max_hp * 0.07)
                enemy_dodge_risk = enemy.dodge > 35
                vampire_safe = self.hp >= max_te + 10 and self.hp >= self.max_hp * 0.4
    
                if vampire_safe and not enemy_dodge_risk:
                    st.markdown("🩸 **Thời cơ hoàn hảo – thi triển Huyết Bạo!**")
                    self.huyet_bao(enemy, auto=True)
                    return
                else:
                    st.markdown("⏳ **Chưa nên dùng Huyết Bạo – quá rủi ro hoặc máu thấp.**")
    
            # 5. Máu thấp → ưu tiên Hấp Huyết
            if self.hp < self.max_hp * 0.3 and self.current_stamina >= 2:
                self.hap_huyet(enemy)
                return
    
            # 6. Có stamina → dùng Hấp Huyết
            if self.current_stamina >= 2:
                self.hap_huyet(enemy)
                return
    
            # 7. Không còn stamina → đánh thường
            self.attack(enemy)
            return
    
        # === Giao diện người chơi ===
        st.markdown(f"## 🧛 **{self.name} (Ma Cà Rồng)** – chọn kỹ năng")
        st.markdown(f"❤️ HP: `{self.hp}/{self.max_hp}` | ⚡ Stamina: `{self.current_stamina}/{self.stamina}` | 🔺 ATK: `{self.atk}` | 🎯 Crit: `{self.crit}%`")
    
        skill = st.radio("🎯 Chọn hành động", [
            "👊 Đánh thường",
            "🩸 Hấp Huyết (2 ⚡)",
            "🔥 Huyết Bạo (Hiến tế máu + ném Huyết Cầu – 11 ⚡)",
            "♻️ Tái Sinh (21 ⚡ – hồi HP ngẫu nhiên)",
            "⚑ Đầu hàng"
        ])
    
        if st.button("🕹️ Thi triển kỹ năng"):
            if skill == "⚑ Đầu hàng":
                self.hp = 0
                st.markdown(f"🏳️ **{self.name} đã đầu hàng!**")
            elif skill.startswith("👊"):
                self.attack(enemy)
            elif skill.startswith("🩸"):
                self.hap_huyet(enemy)
            elif skill.startswith("🔥"):
                self.huyet_bao(enemy)
            elif skill.startswith("♻️"):
                self.tai_sinh()

class Werewolf(Character):
    def __init__(self, name, species, atk, stamina, hp, crit, dodge):
        super().__init__(name, species, atk, stamina, hp, crit, dodge)
        self.is_wolf_form = False
        self.skill_1_usage_count = 0
        self.buff_stacking = 0

    def skill_1(self):
        if self.is_wolf_form:
            cost = 5
            if self.current_stamina < cost:
                st.markdown(f"⚡ **{self.name}** không đủ stamina để gầm rú! Hắn phải nghỉ ngơi lấy lại sức...")
                self.rest()
                return
            self.current_stamina -= cost
    
            atk_increase = rd.randint(4, 10) * (1 - 0.1 * self.skill_1_usage_count)
            crit_increase = rd.randint(7, 12) * (1 - 0.1 * self.skill_1_usage_count)
    
            atk_increase = max(1, math.ceil(atk_increase))
            crit_increase = max(1, math.ceil(crit_increase))
    
            self.atk += atk_increase
            self.crit = min(self.crit + crit_increase, 65)
    
            st.markdown(f"**{self.name}** tru lên một tiếng rùng rợn, đôi mắt rực sáng giữa màn đêm!")
            st.markdown(f"💢 **Lực chiến bộc phát**: +{atk_increase} ATK (hiện tại: {self.atk}), +{crit_increase}% chí mạng (Crit: {self.crit}%)")
            st.markdown(f"⚡ Tiêu hao 5 stamina. Còn lại: `{self.current_stamina}/{self.stamina}`")
            self.buff_stacking += 1
    
            if self.buff_stacking >= 3:
                buff = rd.randint(8, 12)
                self.atk += buff
                st.markdown(f"{self.name} rơi vào trạng thái **Hăng Máu** – ATK tăng thêm {buff}!")
    
        else:
            hp_increase = rd.randint(135, 165) * (1 - 0.03 * self.skill_1_usage_count)
            dodge_increase = rd.randint(6, 9) * (1 - 0.1 * self.skill_1_usage_count)
    
            hp_increase = max(10, math.ceil(hp_increase))
            dodge_increase = max(1, math.ceil(dodge_increase))
    
            self.hp = min(self.hp + hp_increase, self.max_hp)
            self.dodge = min(self.dodge + dodge_increase, 40)
    
            st.markdown(f"**{self.name}** rút lui vào màn sương, biến mất trong khoảnh khắc.")
            st.markdown(f"🌑 **Sức sống hồi phục**: +{hp_increase} HP ({self.hp}/{self.max_hp}), né tránh tăng +{dodge_increase}% (hiện tại: {self.dodge}%)")
    
        st.markdown(f"⚡ **Hiệu quả của chiêu này sẽ giảm dần sau mỗi lần sử dụng.**")
        self.skill_1_usage_count += 1

    def skill_2(self, target):
        if self.is_wolf_form:
            st.markdown(f"**{self.name}** nhếch mép, đôi mắt đỏ rực như lửa, máu dã thú bùng lên. Hắn lao vào cơn cuồng sát, không còn gì cản nổi!")
    
            total_damage = 0
            damage_base = self.atk * 0.7
            chance = 0.9
            multiplier = 1
            hits = 0
            crit_hits = 0
    
            # Giảm 1 nửa dodge của mục tiêu + trừ thêm nếu > 20
            original_target_dodge = target.dodge
            reduced_dodge = math.floor(original_target_dodge / 2)
            extra_dodge_reduction = 0
            if reduced_dodge > 20:
                extra_dodge_reduction = rd.randint(1, 3)
                reduced_dodge += extra_dodge_reduction
    
            target.dodge -= reduced_dodge
            st.markdown(f"👁️ **{target.name}** chịu áp lực từ dã thú, mất tạm thời {reduced_dodge}% dodge! (Còn: {target.dodge}%)")
    
            while True:
                if self.current_stamina < 3:
                    st.markdown(f"💨 **{self.name}** gầm lên trong tuyệt vọng, thân thể đuối sức, cơn điên loạn không thể duy trì!")
                    break
    
                self.current_stamina -= 3
                hits += 1
                damage = damage_base * multiplier
    
                is_crit = rd.random() < self.crit / 100
                if is_crit:
                    damage *= 2
                    crit_hits += 1
                    st.markdown(f"💥 Đòn chí mạng! Lần {hits} – sát thương: {math.ceil(damage)}!")
                else:
                    st.markdown(f"⚔️ Đòn cắn lần {hits}: sát thương: {math.ceil(damage)}.")
    
                total_damage += damage
    
                if rd.random() > chance:
                    st.markdown(f"❌ Cơn cuồng sát dừng lại tại đòn {hits}.")
                    break
    
                chance -= 0.12
                if chance <= 0:
                    break
                multiplier *= 0.75
    
            # Trả lại dodge ban đầu
            target.dodge = original_target_dodge
            st.markdown(f"♻️ **{target.name}** hồi phục lại dodge ban đầu: {target.dodge}%")
    
            # Giảm dodge bản thân
            divisor = rd.randint(9, 13)
            dodge_penalty = math.ceil(reduced_dodge / divisor) * hits
            old_dodge = self.dodge
            self.dodge = max(self.dodge - dodge_penalty, 0)
            st.markdown(f"😵 **{self.name}** bị rối loạn sau cơn điên, mất {dodge_penalty}% né tránh ({old_dodge}% → {self.dodge}%)")
    
            # Hồi máu từ crit ổn định hơn
            if crit_hits > 0:
                heal_amount = crit_hits * rd.randint(12, 17)
                self.hp = min(self.hp + heal_amount, self.max_hp)
                st.markdown(f"🩸 **{self.name}** hấp thụ sức mạnh từ {crit_hits} đòn chí mạng, hồi {heal_amount} HP. HP hiện tại: {self.hp}/{self.max_hp}")
    
            st.markdown(f"🩸 Tổng sát thương gây ra: {math.ceil(total_damage)}")
            st.markdown(f"⚡ Stamina còn lại: {self.current_stamina}/{self.stamina}")
            return math.ceil(total_damage)
    
        else:
            hp_increase = rd.randint(35, 45)
            self.hp = min(self.hp + hp_increase, self.max_hp)
            self.current_stamina = self.stamina
            st.markdown(f"**{self.name}** đứng tĩnh lặng, nhắm mắt cảm nhận tự nhiên.")
            st.markdown(f"🧘‍♂️ Vận công: +{hp_increase} HP ({self.hp}/{self.max_hp}), hồi phục toàn bộ stamina ({self.current_stamina}/{self.stamina})")
    
    def skill_3(self):
        cost = 10
        if not self.is_wolf_form:
            # 🐺 Biến thành sói
            if self.current_stamina < cost:
                st.markdown(f"💨 **{self.name}** nghiến răng... nhưng không đủ sức đánh thức con sói trong hắn!")
                self.rest()
                return True  # Mất lượt
    
            self.current_stamina -= cost
            self.is_wolf_form = True
    
            old_max_hp = self.max_hp
            old_hp = self.hp
            self.max_hp += 333
            self.hp = min(self.hp + 333, self.max_hp)
            self.atk += 33
            self.crit = min(self.crit + 5, 100)  # Tăng 5% crit
            self.dodge = max(self.dodge - 8, 0)  # Giảm 8% dodge (vì ở dạng sói)
    
            st.markdown(f"**{self.name}** tru lên gọi máu đêm! Biến hình hoàn tất.")
            st.markdown(f"🐺 +333 HP ({old_hp}/{old_max_hp} → {self.hp}/{self.max_hp}), +33 ATK (→ {self.atk}), +5% Crit (hiện tại: {self.crit}%), -8% Né tránh (hiện tại: {self.dodge}%)")
            st.markdown(f"⚡ Đã tiêu hao {cost} stamina. Còn lại: {self.current_stamina}/{self.stamina}")
            return False  # Vẫn được chọn thêm kỹ năng
    
        else:
            # 🧍 Về dạng người
            self.is_wolf_form = False
    
            old_atk = self.atk
            old_hp = self.hp
            old_max_hp = self.max_hp
    
            self.atk = max(self.atk - 33, 1)
            self.max_hp = max(self.max_hp - 333, 1)
            self.hp = min(max(self.hp - 333, 1), self.max_hp)
            self.dodge = min(self.dodge + 8, 45)  # Tăng 8% né tránh
            self.crit = max(self.crit - 3, 0)     # Giảm 3% crit
    
            st.markdown(f"🧍 **{self.name}** trở lại hình dạng người.")
            st.markdown(f"☠️ -333 HP ({old_hp}/{old_max_hp} → {self.hp}/{self.max_hp}), -33 ATK ({old_atk} → {self.atk}), -3% Crit (hiện tại: {self.crit}%), +8% Né tránh (hiện tại: {self.dodge}%)")
            return False
    
    def start_turn(self):
        if not self.is_wolf_form and self.hp < self.max_hp:
            regen = rd.randint(22, 44)
            self.hp = min(self.hp + regen, self.max_hp)
            st.markdown(f"🌿 **{self.name}** hồi phục tự nhiên {regen} HP khi ở dạng người. (HP: {self.hp}/{self.max_hp})")
    
    def choose_skill(self, enemy, auto=False):
        self.start_turn()
        if not auto:
            # Nếu là người chơi, gọi theo dạng input truyền thống
            st.markdown(f"\n🐺 **{self.name}** (Ma sói) – Hiện đang ở dạng {'🧍 Người' if not self.is_wolf_form else '🐺 Sói'}, lựa chọn kỹ năng:")
            st.markdown("1. 👊 Đánh Thường (Tấn công cơ bản, không tiêu tốn năng lượng) (0 ⚡)")
            
            if self.is_wolf_form:
                st.markdown("2. 🔥 Cuồng Nộ (Tăng ATK và tỉ lệ chí mạng trong vài lượt) (5 ⚡)")
                st.markdown("3. 🩸 Tất Sát (Tung liên hoàn đòn, mỗi đòn tốn 3 ⚡)")
                st.markdown("4. 🔁 Biến Hình (Chuyển về dạng người, giảm HP và ATK) (0 ⚡)")
            else:
                st.markdown("2. 🌫️ Ẩn Thân (Tăng HP và né tránh) (0 ⚡)")
                st.markdown("3. 💨 Vận Công (Hồi HP và Stamina) (0 ⚡)")
                st.markdown("4. 🐺 Biến Hình (Tăng HP tối đa và ATK) (10 ⚡)")
            
            st.markdown("0. ⚐ Đầu hàng")
    
            choice = st.text_input("➤ Chọn kỹ năng: ").strip()
            if choice == "0":
                self.hp = 0
                st.markdown(f"**{self.name}** đã đầu hàng!")
                return
            if choice == "1":
                self.attack(enemy)
            elif choice == "2":
                self.skill_1()
            elif choice == "3":
                result = self.skill_2(enemy)
                if self.is_wolf_form and result:
                    enemy.take_damage(result, self)
            elif choice == "4":
                turn_over = self.skill_3()
                if not turn_over:
                    self.choose_skill(enemy, auto=False)  # gọi lại nếu còn lượt
            else:
                st.markdown("Lựa chọn không hợp lệ. Tự động đánh thường.")
                self.attack(enemy)
            return
    
        # === AI CHO BOT ===
        st.markdown(f"\n🤖 **{self.name}** (AI Ma Sói) đang suy tính chiến thuật...")
    
        # Phân tích tình huống
        enemy_is_weak = enemy.max_hp < 1000
        enemy_is_dying = enemy.hp < 400
        self_is_dying = self.hp < self.max_hp * 0.33
        self_is_critical = self.hp < 300
        crit_ready = self.crit >= 55 or self.buff_stacking >= 2
        can_fury_strike = self.current_stamina >= 12
        fury_combo_ready = self.current_stamina >= 24
        stamina_safe = self.current_stamina >= 29
        hp_loss_when_revert = int(self.max_hp * 0.33)
        revert_would_kill = self.hp <= hp_loss_when_revert
    
        # === TÌNH HUỐNG SINH TỬ – ĐẶT CƯỢC SỐNG CÒN ===
        if self_is_critical:
            # Nếu có thể tất sát và có khả năng kết liễu
            if self.is_wolf_form and crit_ready and can_fury_strike and enemy.hp < 500:
                st.markdown("☠️ Nguy kịch! Liều mạng tung tất sát để hạ địch.")
                dmg = self.skill_2(enemy)
                if dmg:
                    enemy.take_damage(dmg, self)
                return
    
            # Nếu không thể kết liễu mà biết sẽ chết ⇒ tìm đường sống bằng ẩn thân
            if not self.is_wolf_form:
                st.markdown("🌫️ HP quá thấp, cầu may bằng Ẩn Thân.")
                self.skill_1()
                return
            else:
                st.markdown("🧍 HP cực thấp, về dạng người dù còn 1 HP để tìm cơ hội sống.")
                self.skill_3()  # về người
                self.skill_1()  # dùng Ẩn Thân luôn
                return
    
        # === GẶP ĐỊCH YẾU, ƯU TIÊN ÉP NHANH ===
        if enemy_is_weak:
            if not self.is_wolf_form:
                if self.current_stamina >= 10:
                    st.markdown("🐺 Gặp địch yếu, ưu tiên hóa sói.")
                    still_can_act = self.skill_3()
                    if still_can_act is False:
                        self.choose_skill(enemy, auto=True)
                    return
                else:
                    st.markdown("💨 Chưa hóa sói được, vận công.")
                    self.skill_2(enemy)
                    return
            else:
                if can_fury_strike:
                    st.markdown("🩸 Địch yếu, tất sát ngay.")
                    dmg = self.skill_2(enemy)
                    if dmg:
                        enemy.take_damage(dmg, self)
                    return
                elif self.current_stamina < 10:
                    if revert_would_kill:
                        st.markdown("🌫️ Không thể về người vì sẽ chết. Ưu tiên ẩn thân.")
                        self.skill_1()
                        return
                    st.markdown("🧍 Không còn sức, về dạng người hồi phục.")
                    self.skill_3()
                    self.skill_2(enemy)
                    return
    
        # === ĐANG Ở DẠNG SÓI ===
        if self.is_wolf_form:
            if self.current_stamina < 10:
                if revert_would_kill:
                    st.markdown("🌫️ Không thể về người vì sẽ chết. Ưu tiên ẩn thân.")
                    self.skill_1()
                    return
                st.markdown("🧍 Stamina thấp, về dạng người để hồi.")
                self.skill_3()
                self.skill_2(enemy)
                return
    
            if crit_ready and can_fury_strike and enemy_is_dying:
                st.markdown("🔥 Dứt điểm bằng tất sát!")
                dmg = self.skill_2(enemy)
                if dmg:
                    enemy.take_damage(dmg, self)
                return
    
            if self.buff_stacking < 3 and stamina_safe:
                st.markdown("💢 Tăng Cuồng Nộ để chuẩn bị combo.")
                self.skill_1()
                return
    
            if can_fury_strike:
                st.markdown("🩸 Tất sát vì đủ điều kiện.")
                dmg = self.skill_2(enemy)
                if dmg:
                    enemy.take_damage(dmg, self)
                return
    
            st.markdown("👊 Không có lựa chọn tối ưu, đánh thường.")
            self.attack(enemy)
            return
    
        # === ĐANG Ở DẠNG NGƯỜI ===
        if self_is_dying:
            if self.current_stamina < 10 or self.hp < self.max_hp * 0.25:
                st.markdown("🌫️ Nguy hiểm! Ưu tiên ẩn thân để sống sót.")
                self.skill_1()
                return
            elif self.current_stamina >= 10:
                st.markdown("🐺 Đủ năng lượng, hóa sói để lật kèo.")
                turn_over = self.skill_3()
                if turn_over is False:
                    self.choose_skill(enemy, auto=True)
                return
    
        if self.current_stamina < 10:
            st.markdown("💨 Thiếu stamina, vận công.")
            self.skill_2(enemy)
            return
    
        if self.current_stamina >= 10:
            st.markdown("🐺 Hóa sói để tấn công.")
            turn_over = self.skill_3()
            if turn_over is False:
                self.choose_skill(enemy, auto=True)
            return
    
        st.markdown("💨 Không còn lựa chọn nào, vận công hồi phục.")
        self.skill_2(enemy)
