import json
import requests
import base64

# קריאת הנתונים מתוך הקובץ work_items_with_changeset_ids.json
with open('work_items_with_changeset_ids.json', 'r') as file:
    work_items_data = json.load(file)

# הצגת הערכים של changesetId
print("Changeset IDs:")
for item in work_items_data:
    changeset_id = item["id"]
    print(f"Processing Changeset ID: {changeset_id}")

    # פרטי ההתחברות לשרת
    organization = "DG-Dev"
    url_api = "http://192.168.1.91/DefaultCollection"
    pat = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"  # Personal Access Token
    encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

    # כותרות עבור הבקשה
    headers = {
        "Authorization": f"Basic {encoded_pat}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # יצירת ה-URL לשאילתה על פי changesetId
    changeset_id_to_query = changeset_id  # ה-changeset_id מתוך הקובץ work_items_with_changeset_ids.json
    url = f"{url_api}/_apis/wit/wiql?api-version=7.1-preview.2"

    # יצירת השאילתה עבור ה-old_id
    query = {
        "query": f"SELECT [System.Id] FROM WorkItems WHERE [Custom.old_id] = '{changeset_id_to_query}'"
    }

    # ביצוע הבקשה
    response = requests.post(url, headers=headers, json=query)

    # בדיקת הצלחה ושליפת הנתונים
    if response.status_code == 200:
        work_items = response.json()

        # אם נמצאו work items, יש להוציא את ה-id ולהוסיף ל-item
        if work_items.get('workItems'):
            for work_item in work_items['workItems']:
                print(f"Found Work Item ID: {work_item['id']}")
                # הוספת ה-new_id לכל אובייקט
                item['new_id'] = work_item['id']
        else:
            print(f"No work items found for Changeset {changeset_id_to_query}")
    else:
        print(f"Failed to retrieve work items for changeset {changeset_id_to_query}. Status Code: {response.status_code}")
        print("Response:", response.text)

# שמירת הנתונים המעודכנים בקובץ work_items_with_changeset_ids.json
with open('work_items_with_changeset_ids.json', 'w', encoding='utf-8') as json_file:
    json.dump(work_items_data, json_file, ensure_ascii=False, indent=4)

print("Updated work items with new_id have been saved to 'updated_work_items_with_changeset_ids.json'.")
