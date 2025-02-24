import json

# נתיבים לקבצים
changesets_file_path = 'changesets_output1_modified.json'
saved_files_file_path = 'saved_files1_modified.json'

# טעינת הנתונים מהקבצים
with open(changesets_file_path, 'r', encoding='utf-8') as file:
    changesets = json.load(file)

with open(saved_files_file_path, 'r', encoding='utf-8') as file:
    saved_files = json.load(file)

# יצירת מילון עם נתיב ה-path_changeset לפי changeset_id
saved_files_dict = {file_info['changeset_id']: file_info['path_changeset'] for file_info in saved_files}

# השוואת ה-pathים והסרת שינויים לא תואמים
for changeset_id, changeset_data in changesets.items():
    if changeset_id not in saved_files_dict:
        continue  # אם ה-changeset_id לא נמצא, אין צורך לבדוק אותו

    expected_path = saved_files_dict[changeset_id]  # הנתיב הצפוי מה-saved_files

    # ודא ש-changeset_data הוא רשימה
    if not isinstance(changeset_data, list):
        print(f"Skipping invalid changeset format for {changeset_id}: {changeset_data}")
        continue

    filtered_changes = []  # שמירת השינויים התואמים בלבד

    for change in changeset_data:
        if not isinstance(change, dict):  # לוודא ש-change הוא מילון
            print(f"Skipping invalid change entry in {changeset_id}: {change}")
            continue

        path = change.get('item', {}).get('path')
        if path == expected_path:
            filtered_changes.append(change)

    # עדכון ה-changeset עם השינויים המתאימים בלבד
    changesets[changeset_id] = filtered_changes

# שמירת הקובץ החדש
with open('changesets_output1_modified_filtered.json', 'w', encoding='utf-8') as file:
    json.dump(changesets, file, ensure_ascii=False, indent=4)

print("✅ Comparison done and file saved as 'changesets_output1_modified_filtered.json'.")
