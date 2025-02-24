import json

# קריאת קובץ ה-JSON
with open("all_changesets_with_pathactions_and_workitems.json", "r", encoding="utf-8") as json_file:
    all_changesets = json.load(json_file)

# יצירת רשימה לאחסון הנתונים החדשים
work_items_data = []

# מעבר על כל ה-changesets
for changeset_id, changeset_data in all_changesets.items():
    # אם ישנם workItems בתוך ה-changeset
    if "workItems" in changeset_data:
        work_items = changeset_data["workItems"].get("value", [])

        # מעבר על כל ה-workItems
        for work_item in work_items:
            # הוצאת ה-id ו-changesetId של כל work item
            work_item_id = work_item.get("id")
            work_item_changeset_id = changeset_id  # השדה changesetId הוא למעשה ה-changeset_id של ה-changeset הנוכחי

            # הוספת הנתונים לרשימה
            work_items_data.append({
                "id": work_item_id,
                "changesetId": work_item_changeset_id
            })

# שמירה של הנתונים לקובץ JSON חדש
with open("work_items_with_changeset_ids.json", "w", encoding="utf-8") as json_file:
    json.dump(work_items_data, json_file, ensure_ascii=False, indent=4)

print("הנתונים נשמרו בהצלחה בקובץ 'work_items_with_changeset_ids.json'.")
