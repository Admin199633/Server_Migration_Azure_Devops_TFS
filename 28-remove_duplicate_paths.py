import json

# נתיב לקובץ JSON
json_file_path = 'changesets_output1_with_comment.json'

# טעינת הנתונים מהקובץ
with open(json_file_path, 'r', encoding='utf-8') as file:
    changesets = json.load(file)

# עבור כל changeset, נבדוק את ה-pathים ונוודא שכל path יופיע רק פעם אחת
for changeset_id, changeset_data in changesets.items():
    if not isinstance(changeset_data, dict) or "changes" not in changeset_data:
        print(f"Skipping invalid changeset format: {changeset_id}")
        continue  # דילוג על רשומות לא תקינות

    seen_paths = set()  # שמירה על נתיבי ה-path שכבר נוספו
    filtered_changes = []  # רשימה חדשה שתכיל רק את השינויים הייחודיים

    for change in changeset_data.get("changes", []):
        if not isinstance(change, dict):  # בדיקה אם change הוא מילון
            print(f"Skipping invalid change entry in {changeset_id}: {change}")
            continue

        path = change.get('item', {}).get('path')
        if path and path not in seen_paths:
            filtered_changes.append(change)
            seen_paths.add(path)

    # עדכון ה-changeset עם רשימת השינויים הייחודיים
    changesets[changeset_id]["changes"] = filtered_changes

# שמירת השינויים לקובץ חדש
with open('changesets_output1_modified.json', 'w', encoding='utf-8') as file:
    json.dump(changesets, file, ensure_ascii=False, indent=4)

print("✅ Duplicates removed and file saved as 'changesets_output1_modified.json'.")
