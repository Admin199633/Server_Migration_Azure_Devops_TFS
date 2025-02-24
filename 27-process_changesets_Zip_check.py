import json
import os
import base64
import zipfile

# פרטי ההתחברות לשרת
organization = "DG-Dev"
url_api = "http://192.168.1.91/DefaultCollection"
pat = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"  # Personal Access Token
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# כותרות עבור הבקשה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# נתיבים לקבצים
json_file_path = "all_changesets_with_pathactions_and_workitems.json"
saved_files_json_path = "saved_files1_modified.json"

# בדיקת קיום הקבצים
if not os.path.isfile(json_file_path):
    raise FileNotFoundError(f"The JSON file does not exist: {json_file_path}")
if not os.path.isfile(saved_files_json_path):
    raise FileNotFoundError(f"The saved files JSON does not exist: {saved_files_json_path}")

# טעינת הקבצים
with open(json_file_path, "r", encoding='utf-8') as json_file:
    all_changesets = json.load(json_file)

with open(saved_files_json_path, "r", encoding='utf-8') as json_file:
    saved_files = json.load(json_file)

# פונקציה לכיווץ קובץ גדול ל-ZIP
def compress_file(file_path):
    # עדכון שם הקובץ כך שיהיה לו סיומת .zip
    zip_path = f"{os.path.splitext(file_path)[0]}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    return zip_path

# יצירת מבנה נתונים לשינויים לפי changeset_id
changesets = {}

for file_info in saved_files:
    changeset_id = file_info["changeset_id"]
    file_path = file_info["file_path"]
    file_name = os.path.basename(file_path)

    if changeset_id not in changesets:
        changesets[changeset_id] = {"comment": "", "changes": []}

    # עדכון ה-comment מה-json
    for cs_id, changeset_data in all_changesets.items():
        if cs_id == changeset_id:
            changesets[changeset_id]["comment"] = changeset_data.get("comment", "")

    existing_paths = {change["item"]["path"] for change in changesets[changeset_id]["changes"]}

    for cs_id, changeset_data in all_changesets.items():
        for change in changeset_data.get("changes", []):
            path = change["item"].get("path")
            if path and os.path.basename(path) == file_name:
                if os.path.isfile(file_path):
                    # אם הקובץ גדול מ-15MB -> כיווץ ל-ZIP
                    # אם הקובץ גדול מ-15MB -> כיווץ ל-ZIP ועדכון הנתיב
                    # אם הקובץ גדול מ-15MB -> כיווץ ל-ZIP ועדכון הנתיב
                    if os.path.getsize(file_path) > 15 * 1024 * 1024:
                        print(f"Compressing large file: {file_name}")
                        zip_path = compress_file(file_path)  # יצירת ZIP
                        file_path = zip_path  # עדכון הנתיב כדי להעלות את ה-ZIP במקום הקובץ המקורי

                        # שינוי שם הקובץ עם סיומת ZIP
                        file_name = os.path.splitext(file_name)[0] + ".zip"

                        # עדכון הנתיב בנתונים שנשמרים ל-JSON
                        new_path = os.path.splitext(file_info["path_changeset"])[0] + ".zip"
                    else:
                        # אם הקובץ קטן מ-15MB, שמור על הנתיב המקורי
                        new_path = file_info["path_changeset"]

                    with open(file_path, "rb") as file:
                        file_content = base64.b64encode(file.read()).decode()



                    # בדיקה אם הקובץ כבר במערך ה-changes
                    if new_path not in existing_paths:
                        changesets[changeset_id]["changes"].append({
                            "changeType": "add",
                            "item": {
                                "path": new_path,
                                "contentMetadata": {"encoding": 65001, "contentType": "application/zip"}  # מגדירים את סוג התוכן כ-ZIP
                            },
                            "newContent": {
                                "content": file_content,
                                "contentType": "base64encoded"
                            },
                            "comment": changesets[changeset_id]["comment"]  # הוספת ה-comment
                        })

                else:
                    print(f"File {file_path} does not exist. Skipping...")

# שמירה של מבנה הנתונים כקובץ JSON
with open('changesets_output1_with_comment.json', 'w', encoding='utf-8') as json_file:
    json.dump(changesets, json_file, ensure_ascii=False, indent=4)

print("✅ Data processing and changeset building completed with comments and ZIP compression for large files.")
