import json

# קריאת קובץ filtered_bugs.json
with open('filtered_bugs.json', 'r', encoding='utf-8') as f:
    filtered_bugs = json.load(f)

# קריאת קובץ work_items_result.json
with open('work_items_match3.json', 'r', encoding='utf-8') as f:
    work_items_result = json.load(f)

# רשימה לאחסון אובייקטים שלא תואמים
non_matching_items = []

# יצירת מילון מ-ID ל-JsonID מתוך work_items_result.json
work_items_dict = {item['JsonID']: item for item in work_items_result}

# לולאת בדיקה אם ID שונה מ-JsonID
for bug in filtered_bugs:
    bug_id = bug.get('ID')
    if bug_id not in work_items_dict or work_items_dict[bug_id]['JsonID'] != bug_id:
        # הוספת האובייקט לקובץ חדש אם לא תואם
        non_matching_items.append(bug)

# יצירת קובץ JSON חדש עם האובייקטים שלא תואמים
with open('non_matching_bugs.json', 'w', encoding='utf-8') as f:
    json.dump(non_matching_items, f, ensure_ascii=False, indent=4)

print(f"הסקריפט הושלם! נמצאו {len(non_matching_items)} אובייקטים שלא תואמים, והם נשמרו ב- 'non_matching_bugs.json'.")
