import sqlite3
import difflib
import random as rd

DB_PATH = "data/havocera.db"

def rand_stat(attr, base):
    delta = 115 if attr == "Vitality" else 5 if attr in ["Dexterity", "Agility"] else 15
    return max(0, base + rd.randint(-delta, delta))


def them_nhan_vat(species_base_stats):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    species_list = list(species_base_stats.keys())
    ten = input("Nhập tên nhân vật: ").strip()

    print("\nDanh sách Species hợp lệ:")
    for s in species_list:
        print(f"- {s}")

    chon_species = input("Chọn Species cho nhân vật: ").strip()

    if chon_species not in species_base_stats:
        closest = difflib.get_close_matches(chon_species, species_list, n=1)
        if closest:
            hoi = input(f"Species '{chon_species}' không tồn tại. Chọn '{closest[0]}'? (y/n): ").strip().lower()
            if hoi in ['y', 'yes']:
                chon_species = closest[0]
            else:
                conn.close()
                return

    base = species_base_stats[chon_species]

    cursor.execute("SELECT name FROM characters WHERE name = ?", (ten,))
    if cursor.fetchone():
        print(f"❌ Nhân vật '{ten}' đã tồn tại.")
        conn.close()
        return

    cursor.execute('''
        INSERT INTO characters (name, species, strength, stamina, vitality, dexterity, agility)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        ten, chon_species,
        rand_stat("Strength", base["Strength"]),
        rand_stat("Stamina", base["Stamina"]),
        rand_stat("Vitality", base["Vitality"]),
        rand_stat("Dexterity", base["Dexterity"]),
        rand_stat("Agility", base["Agility"])
    ))

    conn.commit()
    conn.close()
    print(f"✅ Đã thêm nhân vật '{ten}' vào species '{chon_species}'.")


def sua_nhan_vat():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT species FROM characters")
    species_list = [r[0] for r in cursor.fetchall()]
    class_nhan_vat = input("Nhập tên species muốn sửa: ").strip()

    if class_nhan_vat not in species_list:
        closest = difflib.get_close_matches(class_nhan_vat, species_list, n=1)
        if closest:
            hoi = input(f"Species '{class_nhan_vat}' không tồn tại. Chọn '{closest[0]}'? (y/n): ").strip().lower()
            if hoi in ["y", "yes"]:
                class_nhan_vat = closest[0]
            else:
                conn.close()
                return
        else:
            print("❌ Không tìm thấy species phù hợp.")
            conn.close()
            return

    cursor.execute("SELECT name FROM characters WHERE species = ?", (class_nhan_vat,))
    names = [r[0] for r in cursor.fetchall()]
    print(f"Các nhân vật hiện có: {names}")
    ten = input("Nhập tên nhân vật cần sửa: ").strip()

    if ten not in names:
        closest = difflib.get_close_matches(ten, names, n=1)
        if closest:
            hoi = input(f"Không tìm thấy. Chọn '{closest[0]}'? (y/n): ").strip().lower()
            if hoi != "y":
                conn.close()
                return
            ten = closest[0]
        else:
            print("❌ Không tìm thấy nhân vật.")
            conn.close()
            return

    ten_moi = input(f"Nhập tên mới (bỏ trống để giữ '{ten}'): ").strip()
    if ten_moi:
        cursor.execute("SELECT name FROM characters WHERE name = ?", (ten_moi,))
        if cursor.fetchone():
            print("❌ Tên đã tồn tại.")
            conn.close()
            return

    for attr in ["strength", "stamina", "vitality", "dexterity", "agility"]:
        val = input(f"{attr.capitalize()} (bỏ trống để giữ nguyên): ").strip()
        if val.isdigit():
            cursor.execute(f"UPDATE characters SET {attr} = ? WHERE name = ?", (int(val), ten))

    if ten_moi:
        cursor.execute("UPDATE characters SET name = ? WHERE name = ?", (ten_moi, ten))

    conn.commit()
    conn.close()
    print(f"✅ Đã cập nhật thông tin nhân vật.")


def xoa_nhan_vat():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT species FROM characters")
    species_list = [r[0] for r in cursor.fetchall()]
    class_nhan_vat = input("Nhập tên species muốn xoá nhân vật: ").strip()

    if class_nhan_vat not in species_list:
        closest = difflib.get_close_matches(class_nhan_vat, species_list, n=1)
        if closest:
            hoi = input(f"Species không tồn tại. Chọn '{closest[0]}'? (y/n): ").strip().lower()
            if hoi != "y":
                conn.close()
                return
            class_nhan_vat = closest[0]
        else:
            print("❌ Không tìm thấy species.")
            conn.close()
            return

    cursor.execute("SELECT name FROM characters WHERE species = ?", (class_nhan_vat,))
    names = [r[0] for r in cursor.fetchall()]
    print(f"Các nhân vật hiện có: {names}")
    ten = input("Nhập tên nhân vật cần xoá: ").strip()

    if ten not in names:
        closest = difflib.get_close_matches(ten, names, n=1)
        if closest:
            hoi = input(f"Không tìm thấy. Xoá '{closest[0]}'? (y/n): ").strip().lower()
            if hoi == "y":
                ten = closest[0]
            else:
                conn.close()
                return
        else:
            print("❌ Không tìm thấy nhân vật.")
            conn.close()
            return

    cursor.execute("DELETE FROM characters WHERE name = ?", (ten,))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM characters WHERE species = ?", (class_nhan_vat,))
    if cursor.fetchone()[0] == 0:
        print(f"Species '{class_nhan_vat}' không còn ai.")
        if input("Xoá luôn species này khỏi DB? (không ảnh hưởng logic) (y/n): ").strip().lower() == "y":
            # Không cần xóa gì thêm – vì species chỉ là giá trị trong cột thôi.
            pass

    conn.close()
    print(f"✅ Đã xoá nhân vật '{ten}'.")
