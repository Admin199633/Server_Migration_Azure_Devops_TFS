import requests
import base64
import json

# פרטי התחברות ל-Azure DevOps
organization = "DefaultCollection"
project = "DG-Dev"
pat = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"

# קידוד ה-PAT לצורך Authentication
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# כותרות (Headers)
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json"
}

# קריאת הנתונים מתוך הקובץ JSON
with open("updated_work_items_output.json", "r", encoding="utf-8") as f:
    work_items_data = json.load(f)

# הוספת הקישורים ל-Work Items
for item in work_items_data:
    work_item_id = item["id"]
    linked_item_id = item["work_item_link_id"]
    link_type = item["type"]

    patch_body = [
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": link_type,
                "url": f"http://192.168.1.91/{organization}/{project}/_apis/wit/workItems/{linked_item_id}",
                "attributes": {
                    "comment": "Link added automatically"
                }
            }
        }
    ]

    # כתובת ה-API לעדכון Work Item
    work_item_url = f"http://192.168.1.91/{organization}/{project}/_apis/wit/workItems/{work_item_id}?api-version=7.0"

    # שליחת הבקשה
    response = requests.patch(work_item_url, headers=headers, json=patch_body)

    if response.status_code == 200:
        print(f"קישור נוסף בהצלחה ל-Work Item {work_item_id}.")
    else:
        print(f"שגיאה בהוספת קישור ל-Work Item {work_item_id}: {response.status_code} - {response.text}")
