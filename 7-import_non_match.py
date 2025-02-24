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


# פונקציה להוסיף Work Item
def add_work_item(item):
    # שליפת סוג ה-Work Item מתוך הנתונים (ברירת מחדל Bug)
    work_item_type = item.get("WorkItemType")

    # עדכון כתובת ה-API עם סוג ה-Work Item
    api_url = f"{base_api_url}/${work_item_type}?api-version=6.0"

    patch_data = []
    if item.get("Description"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.Description",
            "value": item["Description"]
        })

    # הוספת שדות נדרשים ל-Work Item
    if item.get("Title"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.Title",
            "value": item["Title"]
        })

    if item.get("State"):
        # כעת נעדכן את ה-State תמיד ל-"New"
        patch_data.append({
            "op": "add",
            "path": "/fields/System.State",
            "value": "New"
        })
    if item.get("Microsoft.VSTS.Common.StateChangeDate"):
        patch_data.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Common.StateChangeDate",
            "value": item["Microsoft.VSTS.Common.StateChangeDate"]
        })

    if item.get("System.Reason"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.Reason",
            "value": item["System.Reason"]
        })

    if item.get("System.BoardColumn"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.BoardColumn",
            "value": item["System.BoardColumn"]
        })

    if item.get("System.BoardLane"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.BoardLane",
            "value": item["System.BoardLane"]
        })

    assigned_to = item.get("AssignedTo")
    if assigned_to:
        if assigned_to in ["Daniel Bujold", "Luella", "Charles", "Noam Weil", "Josh McLean", "Gabby Delin",
                           "Bar Shitrit", "Rotem Zecharya", "Ben Duadi", "Sheli Comeau", "Roi Henigsberg",
                           "Guy Royburt", "Yuval Amsalem", "Daniel Bujold","Or Lahav","Yarin Zairy","Salvador Belilty"]:
            print(f"AssignedTo שונה ל-HMS\\LiorSw עבור {assigned_to}")
            assigned_to = "HMS\\LiorSw"
        patch_data.append({
            "op": "add",
            "path": "/fields/System.AssignedTo",
            "value": assigned_to
        })
    else:
        print("לא הוזן AssignedTo, הוזן ערך ברירת מחדל 'HMS\\LiorSw'")
        patch_data.append({
            "op": "add",
            "path": "/fields/System.AssignedTo",
            "value": "HMS\\LiorSw"
        })

    # הוספת שדות נוספים
    for field, path in [
        ("Tags", "/fields/System.Tags"),
        ("Version", "/fields/Custom.Version"),
        ("ApplicationName", "/fields/Custom.ApplicationName"),
        ("ClientType", "/fields/Custom.ClientType"),
        ("Priority", "/fields/Microsoft.VSTS.Common.Priority"),
        ("Deadline", "/fields/Microsoft.VSTS.Scheduling.TargetDate"),
        ("Activity", "/fields/Microsoft.VSTS.Common.Activity"),
        ("OriginalEstimate", "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate"),
        ("Remaining", "/fields/Microsoft.VSTS.Scheduling.RemainingWork"),
        ("Completed", "/fields/Microsoft.VSTS.Scheduling.CompletedWork"),
        ("StateGraph", "/fields/Custom.StateGraph"),
        ("Attachments", "/fields/System.AttachedFiles"),
        ("RepoSteps", "/fields/Custom.ReproSteps"),
        ("SystemInfo", "/fields/Custom.SystemInfo"),
        ("FoundInVersion", "/fields/Custom.FoundInVersion"),
        ("StoryPoints", "/fields/Microsoft.VSTS.Scheduling.StoryPoints"),
        ("Severity", "/fields/Custom.Severity"),
        ("FoundInBuild", "/fields/Custom.FoundInBuild"),
        ("Valuearea", "/fields/Custom.Valuearea"),
        ("Effort", "/fields/Custom.Effort"),
        ("Iteration", "/fields/System.IterationPath"),
    ]:
        if item.get(field):
            patch_data.append({
                "op": "add",
                "path": path,
                "value": item.get(field)
            })

    else:
        print(f"Work Item ID: {item.get('ID', 'ללא מזהה')}")

    # שליחת הבקשה
    response = requests.post(api_url, headers=headers, json=patch_data)

    # בדיקת התגובה
    if response.status_code in [200, 201]:
        new_id = response.json().get('id')  # קבלת ה-ID החדש שנוצר
        print(f"Work Item {item.get('ID', 'ללא מזהה')} נוצר בהצלחה כ-{work_item_type} עם ID חדש {new_id}")

        # עדכון ה-ID ב-JSON ל-ID החדש
        item["ID"] = new_id

        # שמירה של הקובץ המעודכן עם ה-ID החדש
        with open("non_matching_bugs.json", "w", encoding="utf-8") as file:
            json.dump(work_items, file, ensure_ascii=False, indent=4)

    else:
        print(f"שגיאה ביצירת Work Item {item.get('ID', 'ללא מזהה')}: {response.status_code} - {response.text}")


# הוספת JsonID לכל אובייקט בקובץ וכתיבת הקובץ המעודכן
for item in work_items:
    item["JsonID"] = item.get("ID")  # הוספת JsonID עם ערך ה-ID

# שמירה של הקובץ המעודכן
with open("non_matching_bugs.json", "w", encoding="utf-8") as file:
    json.dump(work_items, file, ensure_ascii=False, indent=4)

# מעבר על כל האובייקטים והוספתם
for item in work_items:
    add_work_item(item)
