import json
import subprocess
import os
import time
import urllib.parse

# קריאת קובץ ה-JSON
# קריאת קובץ ה-JSON עם קידוד UTF-8
with open('all_changesets_with_pathactions_and_workitems.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# רשימה לאחסון הנתיבים החדשים
saved_files = []

# עבור כל changeset במילון
for changeset_id, changeset_data in data.items():
    # שמירת הנתונים כמשתנים
    url = changeset_data["url"]
    author_display_name = changeset_data["author"]["displayName"]
    author_unique_name = changeset_data["author"]["uniqueName"]
    checked_in_by_display_name = changeset_data["checkedInBy"]["displayName"]
    created_date = changeset_data["createdDate"]
    comment = changeset_data.get("comment", "")

    # הגדרת המידע על קבצים ששונו
    changed_files = []
    for change in changeset_data["changes"]:
        changed_files.append({
            "path": change["item"]["path"],
            "change_type": change["changeType"],
            "url": change["item"]["url"]
        })

    # הפעלת tf commands דרך subprocess להוריד את הקבצים
    for file in changed_files:
        print(changed_files)  # בסיס הנתיב המקומי
        base_local_path = r"C:\Users\LiorSw"

        # יצירת נתיב מקומי מתאים
        decoded_path = urllib.parse.unquote(file["path"])

        # המרת הנתיב לפורמט מקומי (מניחים שמדובר בנתיב Windows)
        local_path = os.path.join(base_local_path,
                                  decoded_path.replace("$/", "").lstrip("/").replace("/", "\\").replace("$\\", ""))

        # יצירת תיקיות אם יש צורך
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # הוספת הנתיב החדש לרשימה
        saved_files.append({
            "changeset_id": changeset_id,
            "file_path": local_path  # שמירה כנתיב שלם
        })

        print(local_path)  # לראות את התוצאה
        # בדיקה אם הקובץ כבר קיים
        if not os.path.exists(local_path):
            # הפעלת פקודת tf get
            subprocess.run([
                r"C:\Program Files\Microsoft Visual Studio\2022\TeamExplorer\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer\TF.exe",
                "get",
                file["path"],
                "/version:{}".format(changeset_id),
                "/recursive",
                "/login:liorsw,Myfirstaccount12"])

            print(f"Downloaded: {file['path']}")
        else:
            print(f"File already exists: {local_path}")

        # אפשרות להשהיה קלה כדי למנוע בעיות ביצועים
        time.sleep(0.5)

# שמירת הנתיבים לקובץ JSON חדש
with open('saved_files.json', 'w', encoding='utf-8') as json_file:
    json.dump(saved_files, json_file, ensure_ascii=False, indent=4)  # ensure_ascii=False שומר על עברית

print("Files have been saved and paths are written to 'saved_files.json'.")
