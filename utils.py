import pandas as pd
import random as rd
from tabulate import tabulate
from character_base import Character  # Giả định bạn có class cha Character

# ========================= LOAD DỮ LIỆU =========================

def load_base_stats(base_path="data/HAVOCERA.xlsx"):
    try:
        df = pd.read_excel(base_path)
        df = df[df["Species"].notna()]
        stats_dict = {
            row["Species"]: {
                "Role(s)": row["Role(s)"],
                "Strength": row["Strength"],
                "Stamina": row["Stamina"],
                "Vitality": row["Vitality"],
                "Dexterity": row["Dexterity"],
                "Agility": row["Agility"]
            }
            for _, row in df.iterrows()
        }
        return stats_dict
    except Exception as e:
        print(f"⚠️ Lỗi khi load base stats: {e}")
        return {}

def load_character_classes(characters_path="data/HAVOCERA_Characters.xlsx"):
    try:
        with pd.ExcelFile(characters_path) as xls:
            return {sheet_name: pd.read_excel(xls, sheet_name=sheet_name) for sheet_name in xls.sheet_names}
    except FileNotFoundError:
        print("⚠️ File nhân vật không tồn tại. Kiểm tra lại đường dẫn.")
        return {}

def get_species_list(path):
    with pd.ExcelFile(path) as xls:
        return xls.sheet_names

def load_characters(path):
    species_list = get_species_list(path)
    all_chars = []
    for sp in species_list:
        df = pd.read_excel(path, sheet_name=sp)
        class_type = globals().get(sp, Character)
        for _, row in df.iterrows():
            c = class_type(
                row['Name'], sp,
                row['Strength'], row['Stamina'], row['Vitality'],
                row['Dexterity'], row['Agility']
            )
            all_chars.append(c)
    return all_chars

def load_characters_by_species(species_name, characters_path="data/HAVOCERA_Characters.xlsx"):
    try:
        df = pd.read_excel(characters_path, sheet_name=species_name)
        characters = []
        class_type = globals().get(species_name, Character)
        for _, row in df.iterrows():
            character = class_type(
                row['Name'], species_name,
                row['Strength'], row['Stamina'], row['Vitality'],
                row['Dexterity'], row['Agility']
            )
            characters.append(character)
        return characters
    except Exception as e:
        print(f"Lỗi khi tải nhân vật thuộc species {species_name}: {e}")
        return []

# ========================= HIỂN THỊ =========================

def display_characters(characters):
    table = [["STT", "Character Name", "Species", "Strength", "Stamina", "Vitality", "Dexterity", "Agility"]]
    for idx, char in enumerate(characters, 1):
        table.append([idx, char.name, char.species, char.atk, char.stamina, char.hp, char.crit, char.dodge])
    print(tabulate(table, headers="firstrow", tablefmt="grid"))

def show_info(char):
    print(f"Thông tin của {char.name}:")
    char.info()
    print()

# ========================= CHỌN NHÂN VẬT =========================

def choose_species(valid_classes):
    print("📜 Các chủng loài có sẵn:")
    for idx, sp in enumerate(valid_classes, 1):
        print(f"{idx}. {sp}")
    while True:
        try:
            choice = int(input("Chọn số tương ứng với species: ")) - 1
            if 0 <= choice < len(valid_classes):
                return valid_classes[choice]
            else:
                print("Lựa chọn không hợp lệ, vui lòng nhập lại.")
        except ValueError:
            print("Vui lòng nhập số hợp lệ.")

def choose_character(filtered_chars, player_name):
    display_characters(filtered_chars)
    while True:
        try:
            idx = int(input(f"{player_name}, chọn nhân vật bằng cách nhập STT: ")) - 1
            if 0 <= idx < len(filtered_chars):
                return filtered_chars[idx]
            else:
                print("Lựa chọn không hợp lệ, vui lòng nhập lại.")
        except ValueError:
            print("Vui lòng nhập số hợp lệ.")

# ========================= TIỆN ÍCH =========================

def roll_dice():
    return rd.randint(1, 6)

def auto_choose_skill(bot, enemy):
    print(f"\n🤖 Bot {bot.name} đang hành động...")
    if hasattr(bot, 'choose_skill'):
        bot.choose_skill(enemy, auto=True)
    else:
        bot.attack(enemy)
