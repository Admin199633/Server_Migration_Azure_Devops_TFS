import requests
import json
import base64

# נתונים מזהים (מילוי פרטים מתאימים)
personal_access_token = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"

# כתובת בסיסית ל-API של Azure DevOps
url = "http://192.168.1.91/DefaultCollection/DG-Dev/_apis/wit/wiql?api-version=7.0"


# קידוד ה-PAT
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כותרות הבקשה עם טוקן גישה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json"  # עדכון לפורמט json רגיל
}

# גוף הבקשה עם WIQL (שאילתת Work Item)
wiql_query = {

"query": "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.WorkItemType] = 'Task'"}


# קריאת קובץ JSON (שמור אותו כ-JSON עם רשימת אובייקטים)
with open('filtered_bugs.json', 'r', encoding='utf-8') as f:
    work_items_json = json.load(f)

# רשימה חדשה שתאחסן את האובייקטים עם הערכים המבוקשים
result = []
# יצירת מבנה נתונים למעקב אחרי JsonIDs שכבר הותאמו
used_json_ids = set()

# ביצוע בקשה ל-API עם Wiql Query
response = requests.post(url, headers=headers, json=wiql_query, timeout=30)  # 30 שניות

# בדיקה אם הבקשה הצליחה
if response.status_code == 200:
    work_items = response.json()['workItems']  # המידע שהוחזר מה-API
    for item in work_items:
        work_item_id = item.get('id', 'לא נמצא ID')

        # ביצוע בקשה נוספת כדי לשלוף את ה-Title עבור כל Work Item
        details_url = f"http://192.168.1.91/DefaultCollection/DG-Dev/_apis/wit/workitems/{work_item_id}?api-version=7.0"
        details_response = requests.get(details_url, headers=headers)

        if details_response.status_code == 200:
            # שליפת ה-Title וה-State הישן מהתשובה
            title = details_response.json()['fields'].get('System.Title', 'לא נמצא כותרת')
            old_state = details_response.json()['fields'].get('System.State', 'לא נמצא סטטוס')

            # חיפוש התואם ב-JSON המקומי
            matching_item = next(
                (item_json for item_json in work_items_json
                 if item_json["Title"] == title and item_json["ID"] not in used_json_ids),
                None
            )

            if matching_item:
                json_id = matching_item["ID"]
                json_state = matching_item["State"]

                # סימון JsonID כמשומש
                used_json_ids.add(json_id)

                # יצירת אובייקט חדש עם המידע המבוקש
                new_item = {
                    "ID": work_item_id,
                    "Title": title,
                    "OldState": old_state,
                    "NewState": json_state,
                    "JsonID": json_id,
                    "AssignedTo": matching_item.get("AssignedTo", "לא הוקצה")
                }

                # הוספת המידע לרשימה
                result.append(new_item)

                # הדפסת התאמה בין IDs ו-Title
                print(f"ID מ-Azure: {work_item_id} - ID מ-JSON: {json_id} - Found match with Title: {title}")
                print(f"Old State in Azure: {old_state}")
                print(f"New State from JSON: {json_state}")
                print(response.json())

            else:
                print(f"ID מ-Azure: {work_item_id} - No match found for Title: {title}")
                print(response.json())

        else:
            print(f"שגיאה בקבלת פרטי Work Item ID: {work_item_id} - {details_response.status_code}")
            print(response.json())

else:
    print(f"שגיאה בביצוע הבקשה: {response.status_code}")
    print(response.text)

# שמירה של המידע לקובץ JSON
with open('work_items_match3.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
