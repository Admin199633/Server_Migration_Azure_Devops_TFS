import subprocess
import json
import os

# פרטי המשתמש שלך
tfs_url = "http://192.168.1.91/DefaultCollection"
username = "liorsw"
password = "Myfirstaccount12"

# קריאת קובץ JSON
json_file_path = "saved_files.json"

try:
    with open(json_file_path, "r", encoding="utf-8") as file:
        files_to_delete = json.load(file)
except Exception as e:
    print(f"❌ שגיאה בטעינת קובץ JSON: {e}")
    exit(1)

for file_obj in files_to_delete:
    file_path = file_obj.get("file_path")

    if not file_path:
        print("⚠️ שדה file_path חסר באובייקט JSON, מדלג...")
        continue

    # בדיקה אם הקובץ קיים מקומית
    if not os.path.exists(file_path):
        print(f"⚠️ הקובץ לא נמצא במיקום המקומי: {file_path}")
        continue

    try:
        # מחיקת הקובץ מהדיסק
        os.remove(file_path)
        print(f"🗑️ קובץ נמחק מקומית: {file_path}")

        # פקודת מחיקה ב-TFS
        delete_command = f'tf delete "{file_path}" /login:{username},{password} /noprompt /recursive'
        subprocess.run(delete_command, check=True, shell=True)
        print(f"✅ סומן למחיקה ב-TFS: {file_path}")

        # Check-in כדי להחיל את השינוי ב-TFS
        checkin_command = f'tf checkin /comment:"Deleted {file_path}" /login:{username},{password} /noprompt'
        subprocess.run(checkin_command, check=True, shell=True)
        print(f"✅ Check-in הושלם בהצלחה עבור: {file_path}")

    except FileNotFoundError:
        print(f"⚠️ הקובץ כבר לא קיים: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ שגיאה בעת מחיקת הקובץ מ-TFS: {e}")

print("🎉 מחיקת הקבצים הסתיימה בהצלחה!")
