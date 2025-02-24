import json

# 1. קריאת קובץ ה-JSON הראשון (updated_changes_output.json)
with open('updated_changes_output.json', 'r', encoding='utf-8') as file:
    updated_changes = json.load(file)

# 2. יצירת מילון שמכיל את old_id_change וה-id המתאים לו
id_map = {str(change['old_id_change']): change['id'] for change in updated_changes}

# 3. קריאת קובץ ה-JSON השני (work_items_links1.json)
with open('work_items_links1.json', 'r', encoding='utf-8') as file:
    work_items = json.load(file)

# 4. עיבוד אובייקטים מהסוג ArtifactLink
for work_item in work_items:
    if work_item.get('type') == 'ArtifactLink':
        old_link_id = str(work_item['work_item_link_id'])  # הופך את work_item_link_id ל-string
        # 5. אם נמצא old_id_change תואם ב-id_map, מחליפים את work_item_link_id ב-id החדש
        if old_link_id in id_map:
            new_id = id_map[old_link_id]
            # עדכון ה-work_item_link_id רק אם יש התאמה ב-id_map
            work_item['work_item_link_id'] = new_id
            print(f"מעודכן work_item_link_id עבור work_item {work_item['id']} מ-{old_link_id} ל-{new_id}")
        else:
            print(f"לא נמצא old_id_change תואם עבור work_item_link_id {old_link_id} ב-work_item {work_item['id']}")

# 6. שמירה לקובץ JSON חדש עם הנתונים המעודכנים
with open('updated_work_items_links1.json', 'w', encoding='utf-8') as file:
    json.dump(work_items, file, ensure_ascii=False, indent=4)

print("✅ קובץ 'updated_work_items_links.json' נוצר בהצלחה עם ה-work_item_link_id המעודכן!")
