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

    def attack(self, enemy):
        if self.current_stamina < 10:
            print(f"{self.name} đã kiệt sức, phải tạm lui về dưỡng thần, tích lũy lại sức mạnh.")
            self.rest()
            return

        crit_rate = 2 if rd.random() < self.crit / 100 else 1
        damage = rd.randint(1, 6) + self.atk * crit_rate

        if crit_rate == 2:
            print(f"{self.name} bùng nổ sức mạnh, tung ra đòn CHÍ MẠNG kinh thiên động địa, hướng thẳng vào {enemy.name}, gây {damage} sát thương chí mạng!")
        else:
            print(f"{self.name} nhanh như chớp, phóng chiêu tấn công uy lực vào {enemy.name}, gây {damage} sát thương!")

        enemy.take_damage(damage, self)
        self.current_stamina = min(self.current_stamina + 5, self.stamina)
        print(f"Khí lực của {self.name} thăng hoa, hồi phục 5 stamina, hiện tại stamina: {self.current_stamina}/{self.stamina}.")

    def rest(self):
        restored = int(self.stamina * 0.5)
        self.current_stamina = min(self.current_stamina + restored, self.stamina)
        print(f"{self.name} tạm thời lui về, thở gấp hồi lại {restored} stamina.")

    def take_damage(self, damage, attacker=None, ignore_dodge=False):
        if self.hp <= 0:
            return False

        if not ignore_dodge and rd.random() < self.dodge / 100:
            print(f"Tuy nhiên {self.name} đã lướt đi như một bóng ma và né tránh được đòn công kích!")
            return False
        else:
            self.hp = max(self.hp - damage, 0)
            print(f"{self.name} bị tấn công, chịu {damage} sát thương, máu còn lại: {self.hp}!")
            return damage

    def info(self):
        print(f"{self.name} ({self.species}) - ATK: {self.atk}, HP: {self.hp}/{self.max_hp}, "
              f"Stamina: {self.current_stamina}/{self.stamina}, Crit: {self.crit}%, Dodge: {self.dodge}%")
