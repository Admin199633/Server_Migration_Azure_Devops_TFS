import requests
import json
import base64

# נתונים מזהים (מילוי פרטים מתאימים)
personal_access_token = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"

# כתובת בסיסית ל-API של Azure DevOps
base_api_url = 'http://192.168.1.91/DefaultCollection/DG-Dev/_apis/wit/workitems/'

# קידוד ה-PAT
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כותרות בקשה עם טוקן גישה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json"
}


# פונקציה לשינוי ה-state של Work Item
def update_work_item_state(work_item_id, new_state):
    api_url = f"{base_api_url}{work_item_id}?api-version=5.0" # הכתובת כולל מזהה ה-Work Item
    # גוף הבקשה (שינוי שדה System.State)
    body = [
        {
            "op": "replace",
            "path": "/fields/System.State",
            "value": new_state
        }
    ]

    # שליחת בקשת PATCH
    response = requests.patch(api_url, headers=headers, json=body)

    if response.status_code == 200:
        print(f"סטייט של Work Item עם מזהה {work_item_id} שונה בהצלחה ל-{new_state}")
    else:
        print(f"שגיאה בעדכון ה-Work Item: {response.status_code} - {response.text}")


# קריאה לקובץ JSON
with open("work_items_match3.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# עבור כל אובייקט ב-JSON
for item in data:
    work_item_id = item.get("ID")
    if work_item_id:
        old_state = item.get("OldState")  # אם יש שדה "OldState"
        new_state = item.get("NewState")  # אם יש שדה "NewState"

        print(f"ID מ-Azure: {work_item_id} - ID מ-JSON: {work_item_id} - Found match with Title: {item.get('Title')}")
        print(f"Old State in Azure: {old_state}")
        print(f"New State from JSON: {new_state}")

        if old_state != new_state:
            # קריאה לפונקציה לשינוי ה-State של ה-Work Item
            update_work_item_state(work_item_id, new_state)
