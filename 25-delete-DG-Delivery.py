import json
import os

# קריאת קובץ ה-JSON
with open("saved_files.json", "r", encoding='utf-8') as file:
    data = json.load(file)

# פילטר את הרשימה כך שיכללו רק אובייקטים ש-file_path שלהם לא מכיל "DG-Delivery"
filtered_data = [item for item in data if "DG-Delivery" not in item["file_path"]]

# אובייקטים שנמחקו (כל האובייקטים שהיו עם "DG-Delivery")
removed_data = [item for item in data if "DG-Delivery" in item["file_path"]]

# קריאת קובץ removed_files.json אם קיים ואינו ריק
removed_files_existing = []

if os.path.exists("removed_files.json") and os.path.getsize("removed_files.json") > 0:
    with open("removed_files.json", "r", encoding='utf-8') as file:
        try:
            removed_files_existing = json.load(file)
        except json.JSONDecodeError:
            print("⚠️ קובץ removed_files.json פגום, מאתחל אותו מחדש.")
            removed_files_existing = []

# הוספת האובייקטים שנמחקו לקובץ removed_files.json הקיים
removed_files_existing.extend(removed_data)

# שמירה לקובץ saved_files.json עם האובייקטים שנשארו
with open("saved_files1.json", "w", encoding='utf-8') as file:
    json.dump(filtered_data, file, indent=4, ensure_ascii=False)

# שמירה לקובץ removed_files.json עם כל האובייקטים שנמחקו (כולל הישנים)
with open("removed_files.json", "w", encoding='utf-8') as file:
    json.dump(removed_files_existing, file, indent=4, ensure_ascii=False)

print("✅ האובייקטים עם DG-Delivery נמחקו בהצלחה. האובייקטים שנמחקו נשמרו בקובץ removed_files.json.")
