import requests
import json
import base64

# נתונים מזהים (מילוי פרטים מתאימים)
personal_access_token = "uidntx27sjveo2gf6rz2uw2wxnjubkdfchzks6j5sabwutxxnwia"

# כתובת בסיסית ל-API של Azure DevOps
base_api_url = "http://192.168.1.132/DefaultCollection/DG-Dev/_apis/wit/workitems"

# קידוד ה-PAT
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כותרות בקשה עם טוקן גישה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json"
}

# קריאה לקובץ JSON שמכיל את נתוני ה-Work Items
with open("non_matching_bugs.json", "r", encoding="utf-8") as file:
    work_items = json.load(file)

# פונקציה לעדכון ה-Work Item
def update_work_item_state(item):
    work_item_id = item.get("ID")
    new_state = item.get("State")

    if not work_item_id or not new_state:
        print(f"Work Item ID או State לא נמצא עבור הפריט: {item}")
        return

    # כתובת ה-API לעדכון ה-Work Item
    api_url = f"{base_api_url}/{work_item_id}?api-version=6.0"

    # נתוני העדכון
    patch_data = [{
        "op": "add",
        "path": "/fields/System.State",
        "value": new_state
    }]

    # שליחת הבקשה לעדכון ה-State
    response = requests.patch(api_url, headers=headers, json=patch_data)

    # בדיקת התגובה
    if response.status_code in [200, 201]:
        print(f"Work Item {work_item_id} עודכן בהצלחה עם State: {new_state}")
    else:
        print(f"שגיאה בעדכון Work Item {work_item_id}: {response.status_code} - {response.text}")

# עבור כל Work Item בקובץ, נעדכן את ה-State
for item in work_items:
    update_work_item_state(item)
