import math
import random as rd
from character_base import Character

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
        self.crit = min(self.crit + 7, 50)

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
            self.dodge = min(self.dodge + 5, 33)
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
            self.atk = max(1, math.ceil(self.atk * 0.55))
            self.dodge = min(self.dodge + 10, 33)
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
        hp_sacrifice = rd.randint(1, 10)
        self.hp = max(1, self.hp - hp_sacrifice)
        bonus_hp = rd.randint(10, 20)
        self.hp = min(self.hp + math.ceil(self.max_hp * bonus_hp / 100), self.max_hp)

        boost = rd.randint(8 + 6 * self.so_lan_thoi_khong, 12 + 10 * self.so_lan_thoi_khong)
        self.atk += boost * 3
        self.crit = min(self.crit + 10, 50)
        self.next_attack_buffed = True

        print(f"🩸 {self.name} thực hiện nghi lễ hắc ám, nhận +{boost * 3} ATK, +10% Crit, HP tăng nhẹ.")
        return True

    def start_turn(self):
        self.turn_count += 1
        if self.turn_count <= 5:
            self.max_hp += 56
            self.hp = min(self.hp + 56, self.max_hp)

            self.max_stamina += 7
            self.current_stamina = min(self.current_stamina + 7, self.max_stamina)

            self.atk += 8
            self.crit = min(self.crit + 1, 50)
            self.dodge = min(self.dodge + 1, 33)

            print(f"🌓 {self.name} hấp thụ hắc khí – +56 HP, +7 ⚡, +8 ATK, +1% Crit, +1% Dodge")

    def choose_skill(self, enemy, auto=False):
        self.start_turn()
        print(f"\n{self.name} (Phù thủy hắc ám) chọn kỹ năng:")
        print("1. 👊 Đánh thường")
        print("2. 🕯️ Nguyền rủa (4 ⚡)")
        print("3. ☠️ Độc Dược (12 ⚡)")
        if self.so_lan_thoi_khong < 3:
            print("4. ⏳ Thời Không (49 ⚡)")
        if not self.dark_ritual_used:
            print("5. 🩸 Nghi lễ hắc ám")
        print("0. ⚑ Đầu hàng")

        choice = input("➤ Chọn kỹ năng: ").strip()
        if choice == "1":
            self.attack(enemy)
        elif choice == "2":
            self.nguyen_rua(enemy)
        elif choice == "3":
            self.doc_duoc(enemy)
        elif choice == "4" and self.so_lan_thoi_khong < 3:
            self.thoi_khong(enemy)
        elif choice == "5" and not self.dark_ritual_used:
            pre_hp = self.hp
            self.nghi_le_hac_am()
            if self.hp == pre_hp:
                self.choose_skill(enemy)
        elif choice == "0":
            self.hp = 0
            print(f"{self.name} đã đầu hàng.")
        else:
            print("Lựa chọn không hợp lệ. Tự động đánh thường.")
            self.attack(enemy)
