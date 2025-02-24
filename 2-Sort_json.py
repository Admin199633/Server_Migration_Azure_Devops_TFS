import json

# קריאת קובץ JSON
with open('updated_work_items_output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# ספירת סך כל האובייקטים
total_objects = len(data)
print(f"סך כל האובייקטים בקובץ: {total_objects}")

# סינון אובייקטים עם Iteration="Nativ-Clearance-API" ו- State שאינו "closed"
filtered_objects = [
    obj for obj in data
    if obj.get("WorkItemType") == "Bug"
# קוד לביצוע אם שני התנאים מתקיימים
]

# הדפסת מספר האובייקטים אחרי הסינון
print(f" ו-State שאינו 'closed': {len(filtered_objects)}")
