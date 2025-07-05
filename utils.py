# ========================= LOAD DỮ LIỆU =========================

def load_all_characters():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, species, strength, stamina, vitality, dexterity, agility FROM characters")
    rows = cursor.fetchall()
    conn.close()

    characters = []
    for row in rows:
        name, species, str_, sta, vit, dex, agi = row
        class_type = globals().get(species, Character)
        characters.append(class_type(name, species, str_, sta, vit, dex, agi))
    return characters

def load_characters_by_species(species_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, species, strength, stamina, vitality, dexterity, agility FROM characters WHERE species = ?", (species_name,))
    rows = cursor.fetchall()
    conn.close()

    characters = []
    class_type = globals().get(species_name, Character)
    for row in rows:
        name, species, str_, sta, vit, dex, agi = row
        characters.append(class_type(name, species, str_, sta, vit, dex, agi))
    return characters

def get_species_list():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT species FROM characters")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

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

def choose_species(valid_species):
    print("📜 Các chủng loài có sẵn:")
    for idx, sp in enumerate(valid_species, 1):
        print(f"{idx}. {sp}")
    while True:
        try:
            choice = int(input("Chọn số tương ứng với species: ")) - 1
            if 0 <= choice < len(valid_species):
                return valid_species[choice]
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
