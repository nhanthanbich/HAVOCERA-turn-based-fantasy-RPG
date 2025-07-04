import pandas as pd
import difflib
import random as rd

def rand_stat(attr, base):
    delta = 115 if attr == "Vitality" else 5 if attr in ["Dexterity", "Agility"] else 15
    return max(0, base + rd.randint(-delta, delta))


def them_nhan_vat(classes, species_base_stats, characters_path):
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
                return

    base = species_base_stats[chon_species]

    nhan_vat_moi = {
        "Name": [ten],
        "Species": [chon_species],
        "Role(s)": [base["Role(s)"]],
        "Strength": [rand_stat("Strength", base["Strength"])],
        "Stamina": [rand_stat("Stamina", base["Stamina"])],
        "Vitality": [rand_stat("Vitality", base["Vitality"])],
        "Dexterity": [rand_stat("Dexterity", base["Dexterity"])],
        "Agility": [rand_stat("Agility", base["Agility"])]
    }

    df_class = classes.get(chon_species, pd.DataFrame())
    if ten in df_class.get("Name", []):
        print(f"❌ Nhân vật '{ten}' đã tồn tại.")
        return

    df_class = pd.concat([df_class, pd.DataFrame(nhan_vat_moi)], ignore_index=True)
    classes[chon_species] = df_class

    with pd.ExcelWriter(characters_path, mode="w", engine="openpyxl") as writer:
        for class_name, df in classes.items():
            df.to_excel(writer, sheet_name=class_name, index=False)

    print(f"✅ Đã thêm nhân vật '{ten}' vào species '{chon_species}'.")


def sua_nhan_vat(classes, valid_classes, characters_path):
    class_nhan_vat = input(f"Nhập tên species muốn sửa: ").strip()
    df_class = classes.get(class_nhan_vat)

    if df_class is None:
        closest = difflib.get_close_matches(class_nhan_vat, valid_classes, n=1)
        if closest:
            hoi = input(f"Species '{class_nhan_vat}' không tồn tại. Chọn '{closest[0]}'? (y/n): ").strip().lower()
            if hoi in ["y", "yes"]:
                class_nhan_vat = closest[0]
                df_class = classes[class_nhan_vat]
            else:
                return
        else:
            print("❌ Không tìm thấy species phù hợp.")
            return

    print(f"Các nhân vật hiện có: {df_class['Name'].tolist()}")
    ten = input("Nhập tên nhân vật cần sửa: ").strip()

    if ten not in df_class["Name"].values:
        closest = difflib.get_close_matches(ten, df_class["Name"].tolist(), n=1)
        if closest:
            hoi = input(f"Không tìm thấy. Chọn '{closest[0]}'? (y/n): ").strip().lower()
            if hoi == "y":
                sua_nhan_vat(classes, valid_classes, characters_path)
            return

    idx = df_class[df_class["Name"] == ten].index[0]

    ten_moi = input(f"Nhập tên mới (bỏ trống để giữ '{ten}'): ").strip()
    if ten_moi:
        if ten_moi in df_class["Name"].values:
            print("❌ Tên đã tồn tại.")
            return
        df_class.at[idx, "Name"] = ten_moi

    for attr in ["Strength", "Stamina", "Vitality", "Dexterity", "Agility"]:
        val = input(f"{attr} (hiện tại: {df_class.at[idx, attr]}): ").strip()
        if val.isdigit():
            df_class.at[idx, attr] = int(val)

    classes[class_nhan_vat] = df_class
    with pd.ExcelWriter(characters_path, mode="w", engine="openpyxl") as writer:
        for name, df in classes.items():
            df.to_excel(writer, sheet_name=name, index=False)
    print(f"✅ Đã cập nhật thông tin nhân vật.")


def xoa_nhan_vat(classes, valid_classes, characters_path):
    class_nhan_vat = input("Nhập tên species muốn xoá: ").strip()
    df_class = classes.get(class_nhan_vat)

    if df_class is None:
        closest = difflib.get_close_matches(class_nhan_vat, valid_classes, n=1)
        if closest:
            hoi = input(f"Species không tồn tại. Chọn '{closest[0]}'? (y/n): ").strip().lower()
            if hoi == "y":
                class_nhan_vat = closest[0]
                df_class = classes[class_nhan_vat]
            else:
                return
        else:
            print("❌ Không tìm thấy species.")
            return

    print(f"Các nhân vật hiện có: {df_class['Name'].tolist()}")
    ten = input("Nhập tên nhân vật cần xoá: ").strip()

    if ten not in df_class["Name"].values:
        closest = difflib.get_close_matches(ten, df_class["Name"].tolist(), n=1)
        if closest:
            hoi = input(f"Không tìm thấy. Xoá '{closest[0]}'? (y/n): ").strip().lower()
            if hoi == "y":
                ten = closest[0]
            else:
                return
        else:
            print("❌ Không tìm thấy nhân vật.")
            return

    df_class = df_class[df_class["Name"] != ten]
    classes[class_nhan_vat] = df_class

    if df_class.empty:
        if input("Species không còn ai. Xoá luôn species? (y/n): ").strip().lower() == "y":
            del classes[class_nhan_vat]

    with pd.ExcelWriter(characters_path, mode="w", engine="openpyxl") as writer:
        for name, df in classes.items():
            df.to_excel(writer, sheet_name=name, index=False)

    print(f"✅ Đã xoá nhân vật '{ten}'.")
