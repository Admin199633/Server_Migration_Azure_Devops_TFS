import json
import re  # ספרייה לחיפוש טקסט באמצעות ביטויים רגולריים

# 1. קריאת קובץ ה-JSON הקיים
with open("changes_output.json", "r", encoding="utf-8") as file:
    changes_data = json.load(file)

# 2. לולאה לעיבוד כל שינוי (Change)
for change in changes_data:
    name = change.get("name", "")  # מקבל את שם ה-Change

    # 3. חיפוש מספר שמופיע אחרי 'Old ID:'
    match = re.search(r"Old ID:\s*(\d+)", name)

    # 4. אם נמצא מספר, נוסיף אותו לשדה החדש
    if match:
        change["old_id_change"] = int(match.group(1))  # המרת המזהה למספר שלם
    else:
        change["old_id_change"] = None  # אם אין מספר, נכניס ערך None

# 5. שמירה לקובץ JSON חדש עם הנתונים המעודכנים
with open("updated_changes_output.json", "w", encoding="utf-8") as file:
    json.dump(changes_data, file, ensure_ascii=False, indent=4)

print("✅ קובץ 'updated_changes_output.json' נוצר בהצלחה עם ה-Old ID!")
