import json

# קריאת קובץ JSON
with open("filtered_bugs.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# רשימת הערכים שיש לנקות
values_to_remove = {"שדה לא נמצא", "<None>", "0"}

# מעבר על כל האובייקטים ועדכון השדה אם צריך
def clean_integration_build(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "FoundIn" and value in values_to_remove:
                obj[key] = ""  # השארת השדה ריק
            else:
                clean_integration_build(value)  # ריקורסיה לעבור על כל המבנה
    elif isinstance(obj, list):
        for item in obj:
            clean_integration_build(item)

clean_integration_build(data)

# כתיבת הקובץ המעודכן חזרה
with open("data_cleaned.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("הקובץ עודכן ונשמר בשם 'data_cleaned.json'")
