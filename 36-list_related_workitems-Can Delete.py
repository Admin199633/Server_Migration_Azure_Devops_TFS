import json

# קריאת הנתונים מקובץ ה-JSON
with open("file_no_duplicates.json", "r", encoding="utf-8") as file:
    merged_data = json.load(file)

# רשימה לאובייקטים שעונים על הדרישה
valid_items = []

# עיבוד הנתונים
for item in merged_data:
    work_item_id = item.get("id")  # מזהה ה-Work Item מתוך השדה id
    work_item_link_id = item.get("work_item_link_id")  # מזהה ה-Changeset מתוך השדה work_item_link_id

    if work_item_id is None or work_item_link_id is None:
        print(f"Skipping item due to missing data: {item}")
        continue

    try:
        # המרת הערך לפורמט float
        work_item_link_id_float = float(work_item_link_id)

        # בדיקה אם הערך הוא מספר עשרוני
        if '.' in work_item_link_id and work_item_link_id_float != int(work_item_link_id_float):
            print(f"Skipping item with decimal work_item_link_id: {work_item_link_id}")
            continue

        # אם הערך הוא לא בין 1 ל-9, נדלג עליו
        if work_item_link_id_float < 1 or work_item_link_id_float > 9:
            print(f"Skipping item with invalid work_item_link_id: {work_item_link_id}")
            continue

    except ValueError:
        # אם לא ניתן להמיר את הערך למספר, נדלג עליו
        print(f"Skipping item with non-numeric work_item_link_id: {work_item_link_id}")
        continue

    # אם הערך תקין, נוסיף את האובייקט לרשימה החדשה
    valid_items.append(item)

# שמירה של האובייקטים התקינים לקובץ JSON חדש
with open("valid_items.json", "w", encoding="utf-8") as output_file:
    json.dump(valid_items, output_file, ensure_ascii=False, indent=4)

print(f"Created valid_items.json with {len(valid_items)} valid items.")
