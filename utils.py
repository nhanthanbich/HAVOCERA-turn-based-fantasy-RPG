import pandas as pd

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
