import random as rd
import streamlit as st
from stats import compute_combat_stats
import math

species_icon_map = {
    "Witch": "🧙", "Vampire": "🧛", "Werewolf": "🐺", "Skeleton": "💀",
    "Demon": "😈", "Scarecrow": "🎃", "Butcher": "🔪", "Yeti": "🧊",
}

def show_combat_info(self, role="hành động"):
    icon = species_icon_map.get(self.species, "🧍")
    st.markdown(f"## {icon} **{self.name} ({self.species})** – {role}")
    st.markdown(
        f"❤️ HP: `{self.hp}/{self.max_hp}` | ⚡ Stamina: `{self.current_stamina}/{self.stamina}` | "
        f"🔺 ATK: `{self.atk}` | 🎯 Crit: `{self.crit}%`"
    )

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
        combat_stats["dodge"],
        role=info.get("role", "Không rõ")
    )
# --- Base class ---
class Character:
    def __init__(self, name, species, atk, stamina, hp, crit, dodge, role=None):
        self.name = name
        self.species = species
        self.atk = int(atk)
        self.stamina = int(stamina)
        self.max_hp = int(hp)
        self.hp = int(hp)
        self.crit = int(crit)
        self.dodge = int(dodge)
        self.current_stamina = int(stamina)
        self.role = role
        self.logs = []

    def is_alive(self):
        return self.hp > 0

    def basic_attack(self, target):
        if self.current_stamina < 5:
            self.logs.append(f"{self.name} không đủ stamina để tấn công.")
            return

        self.current_stamina -= 5
        crit = rd.random() < self.crit / 100
        damage = self.atk * (2 if crit else 1)

        if rd.random() < target.dodge / 100:
            self.logs.append(f"{self.name} tấn công nhưng {target.name} né được!")
        else:
            target.hp -= damage
            self.logs.append(
                f"{self.name} dùng đòn đánh thường gây {damage} sát thương lên {target.name}{' (Chí mạng!)' if crit else ''}."
            )

    def rest(self):
        stamina_gained = math.ceil(self.stamina * 0.3)
        self.current_stamina = min(self.stamina, self.current_stamina + stamina_gained)
        self.logs.append(f"{self.name} nghỉ ngơi, hồi {stamina_gained} stamina.")

    def choose_skill(self, enemy):
        # Mặc định sẽ chỉ dùng basic_attack hoặc rest nếu không có kỹ năng
        if self.current_stamina >= 5:
            return self.basic_attack(enemy)
        else:
            return self.rest()

    def show_log(self):
        for log in self.logs:
            st.markdown(f"- {log}")
        self.logs.clear()
class Witch(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_stamina = self.stamina
        self.turn_count = 0

    def dark_bolt(self, target):
        cost = 12
        if self.current_stamina < cost:
            self.logs.append(f"{self.name} không đủ stamina để dùng Hắc Lôi.")
            return self.rest()

        self.current_stamina -= cost
        base_damage = self.atk + 40
        target.hp -= base_damage
        self.logs.append(f"{self.name} dùng Hắc Lôi gây {base_damage} sát thương lên {target.name}.")

    def choose_skill(self, enemy):
        self.turn_count += 1
        if self.current_stamina >= 12:
            return self.dark_bolt(enemy)
        elif self.current_stamina >= 5:
            return self.basic_attack(enemy)
        else:
            return self.rest()
class Werewolf(Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def furious_bite(self, target):
        cost = 15
        if self.current_stamina < cost:
            self.logs.append(f"{self.name} không đủ stamina để dùng Cắn Cuồng Nộ.")
            return self.rest()

        self.current_stamina -= cost
        damage = self.atk + 50
        target.hp -= damage
        self.logs.append(f"{self.name} dùng Cắn Cuồng Nộ gây {damage} sát thương lên {target.name}.")

    def choose_skill(self, enemy):
        if self.current_stamina >= 15:
            return self.furious_bite(enemy)
        elif self.current_stamina >= 5:
            return self.basic_attack(enemy)
        else:
            return self.rest()
