import random as rd

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

        self.logs = []  # 💡 Lưu toàn bộ hành động trong lượt để hiển thị bằng Streamlit

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
