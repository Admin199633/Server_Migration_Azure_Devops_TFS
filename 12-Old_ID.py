import requests
import json
import base64

# פרטי האימות
personal_access_token = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"
base_api_url = 'http://192.168.1.91/DefaultCollection/DG-Dev/_apis/wit/workitems/'

encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json"
}

# קריאת קובץ JSON
with open('work_items_match3.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# פונקציה לעדכון שדה 'old_id' ב-Work Item
def update_work_item_field(work_item_id, json_id):
    api_url = f"{base_api_url}{work_item_id}?api-version=7.0"

    # גוף הבקשה לעדכון השדה
    body = [
        {
            "op": "add",
            "path": "/fields/Custom.old_id",  # הנתיב המדויק לשדה 'old_id'
            "value": json_id
        }
    ]

    response = requests.patch(api_url, headers=headers, json=body)

    if response.status_code == 200:
        print(f"השדה 'old_id' עודכן בהצלחה ל-Work Item {work_item_id} עם הערך {json_id}")
    else:
        print(f"שגיאה בעדכון Work Item {work_item_id}: {response.status_code} - {response.text}")

# פונקציה לעיבוד האובייקטים בקובץ ה-JSON
def process_work_items(data):
    for item in data:
        work_item_id = item.get("ID")
        json_id = item.get("JsonID")

        if work_item_id is not None and json_id is not None:
            update_work_item_field(work_item_id, json_id)
        else:
            print(f"נתונים חסרים עבור Work Item: ID={work_item_id}, JsonID={json_id}")

# קריאה לפונקציה
process_work_items(data)
