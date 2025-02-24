import json

# קריאה מקובץ JSON
with open("updated_work_items_output1.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

# סינון האובייקטים שה-type שלהם הוא "ArtifactLink"
filtered_data = [item for item in json_data if item.get("type") == "ArtifactLink"]

# כתיבה לקובץ חדש
with open("filtered_data.json", "w", encoding="utf-8") as file:
    json.dump(filtered_data, file, indent=4, ensure_ascii=False)

print("סינון הושלם. הנתונים נשמרו ב-filtered_data.json")
