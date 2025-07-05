import math
import random as rd
from character_base import Character

class Vampire(Character):
    def __init__(self, name, species, atk, stamina, hp, crit, dodge):
        super().__init__(name, species, atk, stamina, hp, crit, dodge)
        self.khat_mau = False
        self.huyet_cau = 0
        self.rebirth_uses = 0

    def take_damage(self, damage, attacker=None):
        if self.hp <= 0:
            print(f"{self.name} đã bị hạ gục, linh hồn tạm thời yên nghỉ...")
            return False

        hit = super().take_damage(damage, attacker)

        if self.hp > 0 and self.hp < self.max_hp * 0.2 and not self.khat_mau:
            self.khat_mau = True
            self.atk = math.ceil(self.atk * 1.5)
            self.crit += 5  # Buff thêm crit khi Khát Máu
            self.hp = min(math.ceil(self.hp + 250), self.max_hp)
            print(f"{self.name} gầm lên trong cơn đói khát – KHÁT MÁU trỗi dậy! ATK tăng lên {self.atk}, Crit +5%, HP hồi thêm 250 → {self.hp}.")
        return hit

    def hap_huyet(self, enemy):
        cost = 2
        if self.current_stamina < cost:
            print(f"{self.name} không đủ sức để Hấp huyết!")
            self.rest()
            return

        crit_rate = 2 if rd.random() < self.crit / 100 else 1
        damage_variation = rd.randint(math.ceil(-self.atk * 0.3), math.ceil(self.atk * 0.3))
        base_damage = self.atk + damage_variation
        damage = math.ceil(base_damage * crit_rate) + 10

        print(f"{self.name} lao tới với ánh mắt khát máu, hắn chuẩn bị hút máu {enemy.name}!")
        if crit_rate == 2:
            print(f"💢 CHÍ MẠNG! Cú cắn thấm đẫm máu!")

        result = enemy.take_damage(damage, self)

        if result:
            heal_amount = math.ceil(result * 0.85) + rd.randint(-10, 10)
            self.hp = min(self.hp + heal_amount, self.max_hp)
            print(f"{self.name} hút được {heal_amount} HP – máu hiện tại: {self.hp}")
            self.current_stamina = min(self.current_stamina + 1, self.stamina)
            print(f"{self.name} hồi lại 1 ⚡ Stamina (hiện tại: {self.current_stamina})")

            if self.khat_mau:
                extra_heal = heal_amount
                self.hp = min(self.hp + extra_heal, self.max_hp)
                self.atk += 3
                print(f"{self.name} khát máu cuồng loạn, hút thêm {extra_heal} HP! ATK tăng lên {self.atk}!")

        self.current_stamina -= cost

    def huyet_bao(self, enemy, auto=False):
        cost = 11
        max_te = math.ceil(self.max_hp * 0.07)

        if self.current_stamina < cost:
            print(f"{self.name} không đủ sức thi triển Huyết Bạo.")
            self.rest()
            return

        if auto:
            expected_hp = enemy.hp
            for sacrifice in reversed(range(1, max_te + 1)):
                predicted_dmg = math.ceil(sacrifice * (rd.randint(17, 22) / 10)) + rd.randint(-8, 8)
                if predicted_dmg >= expected_hp:
                    chosen_sacrifice = sacrifice
                    break
            else:
                chosen_sacrifice = max_te
        else:
            while True:
                try:
                    sacrifice = int(input(f"{self.name}, chọn lượng máu để tế (tối đa {max_te} HP): "))
                    if 0 < sacrifice <= max_te and sacrifice <= self.hp:
                        chosen_sacrifice = sacrifice
                        break
                    else:
                        print(f"Số không hợp lệ! (1 ~ {max_te}, và không vượt quá HP hiện tại: {self.hp})")
                except ValueError:
                    print("Vui lòng nhập số nguyên hợp lệ.")

        self.hp = max(self.hp - chosen_sacrifice, 0)
        self.huyet_cau = math.ceil(chosen_sacrifice * (rd.randint(13, 16) / 10)) + rd.randint(-8, 12)
        print(f"{self.name} hiến tế {chosen_sacrifice} máu – 🔴 **HUYẾT BẠO** khai triển ({self.huyet_cau} sát thương)!")

        crit_chance = 0.23
        crit_rate = 2 if rd.random() < crit_chance else 1
        damage = math.ceil(self.huyet_cau * crit_rate) + rd.randint(-10, 10)

        if crit_rate == 2:
            print(f"💥 Huyết Cầu CHÍ MẠNG phát nổ – đâm sầm vào {enemy.name}!")
        else:
            print(f"{self.name} ném Huyết Cầu – tia máu xoáy lao về phía {enemy.name}!")

        result = enemy.take_damage(damage, self)
        if result:
            print(f"{enemy.name} dính {result} sát thương, máu còn lại: {enemy.hp}")
        else:
            poison_dmg = math.ceil(damage * 0.3)
            enemy.hp = max(enemy.hp - poison_dmg, 0)
            print(f"{enemy.name} né được... nhưng khí huyết nhiễm độc – vẫn chịu {poison_dmg} sát thương huyết độc!")

        self.huyet_cau = 0
        self.current_stamina -= cost

    def tai_sinh(self):
        if self.rebirth_uses >= 3:
            print(f"⚠️ {self.name} đã vượt giới hạn luân hồi. Không thể tái sinh thêm nữa.")
            self.rest()
            return

        cost = 21
        if self.current_stamina < cost:
            print(f"{self.name} không đủ sức tái sinh.")
            self.rest()
            return

        heal_amount = cost * rd.randint(6, 9) + rd.randint(-10, 10)
        chance = 1
        count = 0
        print(f"{self.name} niệm chú cổ đại… thực hiện nghi lễ TÁI SINH!")

        while chance > 0:
            roll = rd.random()
            if roll < chance:
                self.hp = min(math.ceil(self.hp + heal_amount), self.max_hp)
                count += 1
                print(f"  Lần thay máu thứ {count}: hồi {heal_amount} HP → HP hiện tại: {self.hp}")
                chance -= 0.25
            else:
                print(f"  Lần thay máu thứ {count + 1}: linh hồn phản kháng, hồi phục thất bại.")
                break

        self.current_stamina -= cost
        self.rebirth_uses += 1

    def choose_skill(self, enemy, auto=False):
        if auto:
            print(f"\n🤖 {self.name} (AI – Vampire) đang phân tích tình hình...")

            danger_threshold = self.max_hp * 0.2
            potential_danger = enemy.atk * 1.4 + 10  # Ước lượng địch sẽ gây ra

            # 🎯 1. Nếu có Huyết Cầu → Ưu tiên ném
            if self.huyet_cau > 0:
                print(f"{self.name} vẫn còn Huyết Cầu – ưu tiên ném ngay!")
                self.nem_huyet_cau(enemy)  # Tách logic ra hàm riêng nếu cần
                return

            # ☯️ 2. Nếu chuẩn bị nguy hiểm, nhưng chưa đủ điều kiện Tái Sinh, nghỉ dưỡng
            if (
                self.hp > danger_threshold and
                (self.hp - potential_danger) <= danger_threshold and
                self.rebirth_uses < 3 and
                self.current_stamina < 21 and
                not self.khat_mau
            ):
                print(f"⚠️ {self.name} cảm thấy sắp nguy – nghỉ để phục hồi trước Tái Sinh hoặc Khát Máu.")
                self.rest()
                return

            # 🔄 3. Chỉ Tái Sinh khi:
            #     - Đã Khát Máu rồi, hoặc
            #     - Sắp chết (không thể chờ Khát Máu), và còn lượt dùng
            if self.hp < danger_threshold and self.rebirth_uses < 3 and self.current_stamina >= 21:
                if self.khat_mau or (self.hp - potential_danger <= 0):
                    print("💀 Kích hoạt Tái Sinh!")
                    self.tai_sinh()
                    return
                else:
                    print("🔄 Chờ Khát Máu, chưa vội Tái Sinh.")
                    self.rest()
                    return

            # 💉 4. Nếu đủ stamina và máu an toàn → cân nhắc Huyết Bạo
            if self.current_stamina >= 11:
                max_te = math.ceil(self.max_hp * 0.07)
                enemy_dodge_risk = enemy.dodge > 35
                vampire_safe = self.hp >= max_te + 10 and self.hp >= self.max_hp * 0.4

                if vampire_safe and not enemy_dodge_risk:
                    print("🩸 Thời cơ hoàn hảo – thi triển Huyết Bạo!")
                    self.huyet_bao(enemy, auto=True)
                    return
                else:
                    print("⏳ Chưa nên dùng Huyết Bạo – quá rủi ro hoặc máu thấp.")

            # 🦇 5. Nếu máu thấp → ưu tiên Hấp Huyết
            if self.hp < self.max_hp * 0.3 and self.current_stamina >= 2:
                self.hap_huyet(enemy)
                return

            # ⚔️ 6. Nếu có stamina → dùng Hấp Huyết
            if self.current_stamina >= 2:
                self.hap_huyet(enemy)
                return

            # 💤 7. Nếu stamina cạn kiệt → đánh thường
            self.attack(enemy)
            return

        # === Chế độ người chơi ===
        print(f"\n🧛 {self.name} (Ma cà rồng) chọn kỹ năng:")
        print("1. 👊  Đánh thường")
        print("2. 🩸 Hấp Huyết (2 ⚡ Stamina)")
        print("3. 🔥 Huyết Bạo (Hiến tế máu + Ném Huyết Cầu – 11 ⚡)")
        print("4. ♻️  Tái Sinh (21 ⚡ – hồi HP ngẫu nhiên)")
        print("0. ⚑  Đầu hàng")

        choice = input("➤ Chọn kỹ năng: ").strip()

        if choice == '0':
            self.hp = 0
            print(f"{self.name} đã đầu hàng!")
        elif choice == "1":
            self.attack(enemy)
        elif choice == "2":
            self.hap_huyet(enemy)
        elif choice == "3":
            self.huyet_bao(enemy)
        elif choice == "4":
            self.tai_sinh()
        else:
            print("Lựa chọn không hợp lệ. Tự động dùng tấn công cơ bản.")
            self.attack(enemy)
