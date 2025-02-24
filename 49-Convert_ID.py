import json

def convert_work_item_link_ids_and_ids():
    # טוען את קבצי ה-JSON
    with open('work_items_links.json', 'r', encoding='utf-8') as file:
        all_work_items = json.load(file)

    with open('work_items_match3.json', 'r', encoding='utf-8') as file:
        id_mapping = json.load(file)

    # יצירת מפת ID ישן לחדש
    id_map = {str(item['JsonID']): str(item['ID']) for item in id_mapping}

    # עיבוד כל Work Item
    for work_item in all_work_items:
        old_id = str(work_item['id'])  # הופך את ה-`id` ל-string במקרה שזה לא string
        # מחליף את ה-ID של ה-Work Item עצמו
        if old_id in id_map:
            new_id = id_map[old_id]
            work_item['id'] = new_id
            print(f"מעודכן ID עבור Work Item {old_id} -> {new_id}")

        # בדיקת קשרים ב-Work Item
        if 'work_item_link_id' in work_item:
            old_link_id = str(work_item['work_item_link_id'])  # הופך ל-string
            print(f"יש קשר עם work_item_link_id ישן: {old_link_id}")

            # אם יש קשר עם ID ישן, מחליפים אותו ל-ID החדש
            if old_link_id in id_map:
                new_link_id = id_map[old_link_id]
                work_item['work_item_link_id'] = new_link_id

                print(f"מעודכן קשר עבור Work Item {work_item['id']} - {old_link_id} -> {new_link_id}")
            else:
                print(f"לא נמצא ID חדש לקשר עבור {old_link_id}")
        else:
            print(f"לא נמצא work_item_link_id עבור Work Item {work_item['id']}")

    # שמירה לקובץ חדש
    with open('updated_work_items_output.json', 'w', encoding='utf-8') as file:
        json.dump(all_work_items, file, ensure_ascii=False, indent=4)


# קריאה לפונקציה
convert_work_item_link_ids_and_ids()
