import json

def remove_duplicates(input_file, output_file):
    # קריאה לקובץ JSON
    with open(input_file, 'r') as f:
        data = json.load(f)

    # כאן נשתמש במבנה set כדי למנוע כפילויות
    unique_data = []
    seen = set()

    for obj in data:
        # המרת האובייקט ל-string כך שנוכל לבדוק אם הוא כבר קיים
        obj_str = json.dumps(obj, sort_keys=True)
        if obj_str not in seen:
            unique_data.append(obj)
            seen.add(obj_str)

    # שמירה לקובץ JSON חדש
    with open(output_file, 'w') as f:
        json.dump(unique_data, f, indent=4)

# קריאה לפונקציה עם שם הקובץ הקיים ושם הקובץ החדש
remove_duplicates('filtered_data.json', 'file_no_duplicates.json')
