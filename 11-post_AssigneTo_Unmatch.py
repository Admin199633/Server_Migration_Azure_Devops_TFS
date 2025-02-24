import requests
import json
import base64

# נתונים מזהים (מילוי פרטים מתאימים)
personal_access_token = "uidntx27sjveo2gf6rz2uw2wxnjubkdfchzks6j5sabwutxxnwia"

# כתובת בסיסית ל-API של Azure DevOps
base_api_url = 'http://192.168.1.132/DefaultCollection/DG-Dev/_apis/wit/workitems/'

# קידוד ה-PAT
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כותרות בקשה עם טוקן גישה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json"
}


# פונקציה לעדכון ה-Assignee של Work Item
def update_assignee(work_item_id, new_assignee):
    api_url = f"{base_api_url}{work_item_id}?api-version=7.0"  # הכתובת כולל מזהה ה-Work Item
    # גוף הבקשה (שינוי שדה System.AssignedTo)
    body = [
        {
            "op": "replace",
            "path": "/fields/System.AssignedTo",
            "value": new_assignee
        }
    ]

    # שליחת בקשת PATCH
    response = requests.patch(api_url, headers=headers, json=body)

    if response.status_code == 200:
        print(f"AssignedTo של Work Item עם מזהה {work_item_id} שונה בהצלחה ל-{new_assignee}")
    else:
        print(f"שגיאה בעדכון ה-Work Item: {response.status_code} - {response.text}")


# קריאה לקובץ JSON
with open("non_matching_bugs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# עבור כל אובייקט ב-JSON
for item in data:
    work_item_id = item.get("ID")  # מזהה ה-Work Item
    new_assignee = item.get("AssignedTo")  # השדה AssignedTo מתוך ה-JSON


    # קריאה לפונקציה לעדכון ה-AssignedTo של ה-Work Item
    update_assignee(work_item_id, new_assignee)
