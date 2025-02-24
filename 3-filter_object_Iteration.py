import json

# קריאת קובץ JSON
with open('filtered_testcase_with_comments.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# ספירת סך כל האובייקטים
total_objects = len(data)
print(f"סך כל האובייקטים בקובץ: {total_objects}")

# סינון אובייקטים עם Iteration="Nativ-Clearance-API" ו- State שאינו "closed"
filtered_objects = [
    obj for obj in data
    if obj.get("WorkItemType") == "Task"
]

# הדפסת מספר האובייקטים אחרי הסינון
print(f"מספר האובייקטים עם Iteration='Nativ-Clearance-API' ו-State שאינו 'closed': {len(filtered_objects)}")

# כתיבת האובייקטים הסינון לקובץ חדש
with open('filtered_bugs.json', 'w', encoding='utf-8') as output_file:
    json.dump(filtered_objects, output_file, ensure_ascii=False, indent=4)

print("הקובץ החדש נוצר בהצלחה כ-'production_DG-deleviry.json'")
