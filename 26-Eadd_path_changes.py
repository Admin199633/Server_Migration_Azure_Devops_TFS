import json


# פונקציה למעבר והמרת הנתיב
def modify_path(file_path):
    # 1. הסרת החלק 'C:\Users\LiorSw' והחלפתו ב-$
    modified_path = file_path.replace("C:\\Users\\LiorSw", "$")

    # 2. המרת כל זוג סלאשים כפולים \\ ל-/
    modified_path = modified_path.replace("\\", "/")

    return modified_path


# קריאת הקובץ JSON (תן את הנתיב לקובץ שלך)
with open('saved_files1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# מעבר על כל האובייקטים בקובץ והוספת שדה path_changeset
for item in data:
    if 'file_path' in item:
        # יצירת השדה path_changeset
        item['path_changeset'] = modify_path(item['file_path'])

# שמירת הקובץ עם השדה החדש
with open('saved_files1_modified.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)

print("שדה path_changeset נוסף והקובץ נשמר בהצלחה.")
