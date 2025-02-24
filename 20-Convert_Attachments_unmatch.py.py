import json


# קריאת קובץ attachments.json
def load_attachments():
    with open('attachments_unmatch.json', 'r', encoding='utf-8') as f:
        return json.load(f)


# קריאת קובץ work_items_match3.json
def load_work_items():
    with open('non_matching_bugs.json', 'r', encoding='utf-8') as f:
        return json.load(f)


# עדכון של attachments.json על פי ההתאמה ב-work_items_match3.json
def update_attachments_with_ids(attachments, work_items):
    for attachment in attachments:
        # קבלת ה-work_item_id מהקובץ attachments.json
        work_item_id = attachment.get('work_item_id')

        # חיפוש התאמה ב-work_items_match3.json על פי JsonID
        matching_work_item = next((item for item in work_items if item['JsonID'] == work_item_id), None)

        # אם נמצא התאמה, הוסף את ה-ID ל-attachment
        if matching_work_item:
            attachment['ID'] = matching_work_item.get('ID')
            print(f"Updated attachment for Work Item ID {work_item_id} with ID {matching_work_item.get('ID')}")
        else:
            print(f"No match found for Work Item ID {work_item_id}")


# שמירת הקובץ המעודכן attachments.json
def save_updated_attachments(attachments):
    with open('attachments_unmatch.json', 'w', encoding='utf-8') as f:
        json.dump(attachments, f, ensure_ascii=False, indent=4)
    print("Updated attachments saved to 'attachments.json'.")


# פונקציה ראשית
def main():
    # טוען את הנתונים מקבצי JSON
    attachments = load_attachments()
    work_items = load_work_items()

    # עדכון ה-attachments עם ה-ID מהקובץ work_items_match3.json
    update_attachments_with_ids(attachments, work_items)

    # שמירת הקובץ המעודכן
    save_updated_attachments(attachments)


# הרצת הסקריפט
if __name__ == "__main__":
    main()
