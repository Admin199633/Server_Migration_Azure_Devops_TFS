import json


# קריאת נתוני JSON
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []


# כתיבת נתוני JSON
def save_json(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving {file_path}: {e}")


# עדכון השדה JsonID בקובץ output.json
def update_json_ids(output_file, *match_files):
    # קריאת הקובץ output.json
    output_data = load_json(output_file)

    # יצירת מילון JsonID -> ID להתאמה מכל הקבצים שנשלחו כ-match_files
    match_dict = {}
    for match_file in match_files:
        match_data = load_json(match_file)
        # יצירת מילון JsonID -> ID מהקובץ הנוכחי
        match_dict.update({item["JsonID"]: item.get("ID") for item in match_data if "JsonID" in item})

    # עדכון הערכים בקובץ output.json
    for item in output_data:
        output_id = item.get("ID")
        if output_id in match_dict:
            item["JsonID"] = match_dict[output_id]

    # שמירת הקובץ המעודכן
    save_json(output_data, output_file)


# הרצת הסקריפט
if __name__ == "__main__":
    output_file = "output.json"
    match_files = ["work_items_match3.json", "non_matching_bugs.json"]  # רשימת קבצים להשוואה
    update_json_ids(output_file, *match_files)
