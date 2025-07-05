class Witch(Character):
    def __init__(self, name, species, atk, stamina, hp, crit, dodge):
        super().__init__(name, species, atk, stamina, hp, crit, dodge)
        self.so_lan_thoi_khong = 0
        self.dark_ritual_used = False
        self.max_stamina = stamina
        self.turn_count = 0

    def attack(self, target):
        damage = self.atk
        is_crit = rd.random() < self.crit / 100
        if is_crit:
            damage = int(damage * 1.5)

        if getattr(self, "next_attack_buffed", False):
            damage = int(damage * 1.3)
            print("💥 Huyết ấn nghi lễ còn vang vọng! Đòn đánh này được cường hóa thêm 30% sức mạnh!")
            self.next_attack_buffed = False

        print(f"{self.name} tấn công {target.name} và gây {damage} sát thương!")
        target.take_damage(damage, self)

    def nguyen_rua(self, enemy):
        cost = 4
        if self.current_stamina < cost:
            print(f"{self.name} không đủ năng lượng để thi triển Nguyền rủa!")
            self.rest()
            return

        self.current_stamina -= cost

        old_atk = enemy.atk
        reduce = math.ceil(enemy.atk * (rd.randint(22, 28) / 100))
        enemy.atk = max(1, enemy.atk - reduce)

        self.crit = min(self.crit + 7, 50)  # 👈 Giới hạn crit
        print(f"🕯️ {self.name} nguyền rủa {enemy.name}, giảm {reduce} ATK ({old_atk} → {enemy.atk})")
        print(f"🔮 {self.name} tăng 7% chí mạng (Crit: {self.crit}%)")

        if self.crit >= 45 and rd.random() < 0.5:
            lost = rd.randint(4, 6)
            enemy.current_stamina = max(0, enemy.current_stamina - lost)
            print(f"💫 Lời nguyền hút cạn linh lực! {enemy.name} mất thêm {lost} ⚡")

    def doc_duoc(self, enemy):
        cost = 12
        if self.current_stamina < cost:
            print(f"{self.name} không đủ tinh lực để sử dụng Độc Dược!")
            self.rest()
            return

        self.current_stamina -= cost
        base_damage = math.ceil(self.atk * 0.5)
        percent_damage = math.ceil(enemy.hp * (rd.randint(20, 28) / 100))
        damage = base_damage + percent_damage

        is_crit = rd.random() < self.crit / 100
        if is_crit:
            damage *= 2

        print(f"☠️ {self.name} ném độc dược ăn mòn linh hồn!")
        result = enemy.take_damage(damage, self)

        if result is not False:
            if is_crit:
                heal = math.ceil(damage * 0.2)
                self.hp = min(self.hp + heal, self.max_hp)
                print(f"💥 Chí mạng! {self.name} hồi lại {heal} HP từ năng lượng độc dược!")
            self.dodge = min(self.dodge + 5, 33)  # 👈 Giới hạn dodge
            print(f"🌫️ Né tránh của {self.name} tăng lên {self.dodge}%!")
        else:
            print(f"💨 Nhưng {enemy.name} đã né kịp!")

    def thoi_khong(self, enemy=None):
        cost = 49
        if self.current_stamina < cost:
            print(f"{self.name} không đủ sức mạnh để bẻ cong thời gian...")
            self.rest()
            return

        self.current_stamina -= cost
        chance = 0.9 - self.so_lan_thoi_khong * 0.22

        if rd.random() < chance:
            self.so_lan_thoi_khong += 1
            self.hp = self.max_hp
            old_atk = self.atk
            self.atk = max(1, math.ceil(self.atk * 0.55))
            self.dodge = min(self.dodge + 10, 33)  # 👈 Giới hạn dodge
            print(f"⏳ {self.name} đảo ngược số phận! Hồi đầy HP, ATK giảm còn {self.atk}, né tránh tăng {self.dodge}%!")
        else:
            penalty = rd.randint(5, 10)
            self.hp = max(1, self.hp - penalty)
            print(f"🌀 Thất bại! {self.name} bị tổn thương bởi nghịch lý thời gian ({penalty} HP mất). HP còn {self.hp}/{self.max_hp}")

    def nghi_le_hac_am(self):
        if self.dark_ritual_used:
            print(f"{self.name} đã hiến tế linh hồn một lần – không thể tái diễn nghi lễ hắc ám nữa...")
            return False

        if self.hp > 250:
            if hasattr(self, "is_bot") and self.is_bot:
                print(f"{self.name} còn quá sung sức để làm nghi lễ – chưa đủ điều kiện HP.")
                return False
            else:
                choice = input(f"❗ {self.name} còn {self.hp} HP (>250). Bạn có muốn tự giảm xuống 250 HP để dùng nghi lễ? (y/n): ").strip().lower()
                if choice != "y":
                    print("❌ Bạn từ chối thực hiện nghi lễ.")
                    return False
                self.hp = 250

        if self.current_stamina < 10:
            print(f"{self.name} quá kiệt sức để thực hiện nghi lễ!")
            self.rest()
            return True

        self.dark_ritual_used = True
        self.current_stamina = 0
        self.max_stamina = 0
        hp_sacrifice = math.ceil(rd.randint(1,10))
        self.hp = max(1, self.hp - hp_sacrifice)
        bonus_hp = rd.randint(10, 20)
        hp_recovery = math.ceil(self.max_hp * bonus_hp / 100)
        self.hp = min(self.hp + hp_recovery, self.max_hp)
        giam_yeu = self.so_lan_thoi_khong
        boost_min = 8 + 6 * giam_yeu
        boost_max = 12 + 10 * giam_yeu
        boost = rd.randint(boost_min, boost_max)

        self.atk += (boost * 3)
        self.crit = min(self.crit + 10, 50)  # 👈 Giới hạn crit
        self.next_attack_buffed = True

        print(f"🩸 {self.name} rạch tay nhỏ máu thực hiện nghi thức, hiến tế toàn bộ ma lực để nhận lấy sức mạnh vật lý thuần khiết...")
        print(f"💀 Đánh đổi vài giọt tinh huyết ({hp_sacrifice} HP) và khả năng dùng phép vĩnh viễn!")
        print(f"✨ Tăng mạnh {hp_recovery} sinh lực như một phần thưởng nghi lễ.")
        print(f"🔥 Nhận +{boost * 3} ATK, +10% Crit.")
        print(f"HP: {self.hp}/{self.max_hp}, ATK: {self.atk}, Crit: {self.crit}%, Stamina: {self.current_stamina}/{self.max_stamina}")
        return True

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
            self.crit = min(self.crit + 1, 50)   # 👈 Giới hạn crit
            self.dodge = min(self.dodge + 1, 33) # 👈 Giới hạn dodge

            print(f"🌓 {self.name} hấp thụ hắc khí trong không gian:")
            print(f"❤️ HP: {old_hp}/{old_max_hp} → {self.hp}/{self.max_hp}")
            print(f"⚡ Stamina: {old_stamina}/{old_max_stamina} → {self.current_stamina}/{self.max_stamina}")
            print(f"🔺 +8 ATK (Tổng: {self.atk}), +1% Crit ({self.crit}%), +1% Dodge ({self.dodge}%)")

    def choose_skill(self, enemy, auto=False):
        self.start_turn()
        if self.max_stamina == 0:
            if auto:
                print(f"\n🤖 {self.name} không còn phép – AI dùng đánh thường.")
            else:
                print(f"\n{self.name} không còn phép thuật sau nghi lễ – chỉ có thể đánh thường!")
            self.attack(enemy)
            return

        if auto:
            print(f"\n🤖 {self.name} (AI – Witch) đang chọn kỹ năng...")

            # 🔮 Phán đoán nếu lượt tới có nguy cơ HP xuống <250 mà chưa đủ stamina để dùng thời không
            potential_danger = enemy.atk * 1.5
            if (
                self.hp > 250 and
                (self.hp - potential_danger) <= 250 and
                self.current_stamina < 49 and
                self.so_lan_thoi_khong < 3
            ):
                print(f"⚠️ {self.name} dự đoán nguy hiểm cận kề – nghỉ để hồi stamina chuẩn bị dùng Thời Không!")
                self.rest()
                return

            # 1. HP < 250 và còn lượt dùng Thời Không
            if self.hp <= 250 and self.current_stamina >= 49 and self.so_lan_thoi_khong < 3:
                self.thoi_khong(enemy)
                return

            # 2. Kết liễu nếu kẻ địch sắp chết
            if enemy.hp <= 200:
                self.attack(enemy)
                return

            # 3. Nếu đã dùng thời không 3 lần → nghi lễ hắc ám
            if not self.dark_ritual_used and self.hp <= 250 and self.so_lan_thoi_khong >= 3:
                self.nghi_le_hac_am()
                return

            # 4. Ưu tiên nguyền rủa nếu chưa từng dùng thời không
            if self.so_lan_thoi_khong == 0 and self.current_stamina >= 4:
                self.nguyen_rua(enemy)
                return

            # 5. Nếu đã dùng thời không → ưu tiên độc dược nếu đủ
            if self.so_lan_thoi_khong >= 1 and self.current_stamina >= 12:
                self.doc_duoc(enemy)
                return

            # 6. Nếu có thể dùng thời không tiếp và HP hơi thấp
            if self.so_lan_thoi_khong < 3 and self.current_stamina >= 49 and self.hp < self.max_hp * 0.4:
                self.thoi_khong(enemy)
                return

            # 7. Không còn phép hoặc logic nào phù hợp – đánh thường
            self.attack(enemy)
            return

        # Người chơi tự chọn
        print(f"\n{self.name} (Phù thủy hắc ám) chọn kỹ năng:")
        print("👊 1. Đánh thường")

        if self.max_stamina > 0:
            print("2. 🕯️ Nguyền rủa (giảm 17~25% ATK địch, tăng 5% Crit) (4 stamina)")
            print("3. ☠️ Độc dược (sát thương cao theo % HP đối thủ + chí mạng, tăng dodge) (12 stamina)")

            if self.so_lan_thoi_khong < 3:
                print("4. ⏳ Phép thời không (hồi full HP, giảm ATK, rủi ro cao) (49 stamina)")

            if not self.dark_ritual_used:
                print("5. 🩸 Nghi lễ hắc ám (Từ bỏ phép thuật để +ATK +Crit +HP)")

        print("0. ⚑ Đầu hàng")

        choice = input("➤ Chọn kỹ năng: ").strip()

        if choice == '0':
            self.hp = 0
            print(f"{self.name} đã đầu hàng!")
        elif choice == "1":
            self.attack(enemy)
        elif choice == "2" and self.max_stamina > 0:
            self.nguyen_rua(enemy)
        elif choice == "3" and self.max_stamina > 0:
            self.doc_duoc(enemy)
        elif choice == "4" and self.max_stamina > 0:
            if self.so_lan_thoi_khong < 3:
                self.thoi_khong(enemy)
            else:
                print("❌ Phép thời không đã đạt giới hạn sử dụng!")
                self.attack(enemy)
        elif choice == "5" and self.max_stamina > 0:
            if not getattr(self, 'dark_ritual_used', False):
                pre_hp = self.hp
                self.nghi_le_hac_am()
                if self.hp == pre_hp:  # Nếu không thay đổi tức là nghi lễ bị từ chối hoặc thất bại
                    self.choose_skill(enemy)  # Gọi lại để chọn skill khác
            else:
                print("❌ Nghi lễ hắc ám chỉ được dùng một lần!")
                self.attack(enemy)
        else:
            print("Lựa chọn không hợp lệ. Tự động dùng tấn công cơ bản.")
            self.attack(enemy)
