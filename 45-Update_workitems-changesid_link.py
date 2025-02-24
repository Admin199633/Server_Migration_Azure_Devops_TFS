import base64
import requests
import json

# קריאת הנתונים מקובץ ה-JSON
with open("file_no_duplicates.json", "r", encoding="utf-8") as file:
    merged_data = json.load(file)

# 1. פרטי ההתחברות לשרת
organization = "DG-Dev"
url_api = "http://192.168.1.91/DefaultCollection"
pat = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"  # Personal Access Token
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# כותרות עבור הבקשה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json",
    "Accept": "application/json"
}

# סינון הנתונים כך שיכלול רק פריטים מסוג "ArtifactLink"
filtered_data = [item for item in merged_data if item.get("type") == "ArtifactLink"]

# עיבוד הנתונים המסוננים
for item in filtered_data:
    work_item_id = item.get("id")  # מזהה ה-Work Item מתוך השדה id
    change_id = item.get("work_item_link_id")  # מזהה ה-Changeset מתוך השדה work_item_link_id

    if work_item_id is None or change_id is None:
        print(f"Skipping item due to missing data: {item}")
        continue

    changeset_url = f"vstfs:///VersionControl/Changeset/{change_id}"  # יצירת ה-URL של ה-Changeset

    # כתובת ה-API לקישור Work Item
    url = f"{url_api}/_apis/wit/workitems/{work_item_id}?api-version=7.1-preview.3"

    # תוכן הבקשה
    data = [
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "ArtifactLink",
                "url": changeset_url,
                "attributes": {
                    "name": "Fixed in Changeset"
                }
            }
        }
    ]

    # שליחת הבקשה
    response = requests.patch(url, headers=headers, data=json.dumps(data))

    # בדיקת תוצאה
    if response.status_code in [200, 201]:
        print(f"Successfully linked Work Item {work_item_id} to Changeset {change_id}.")
    else:
        print(f"Failed to link Work Item {work_item_id} to Changeset {change_id}.")
        print("Response:", response.status_code, response.text)
