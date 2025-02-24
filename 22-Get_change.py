import requests
import base64
import json

# פרטי התחברות ל-Azure DevOps
organization = "DefaultCollection"
project = "DG-Dev"
repository = "_versionControl"  # או מזהה המאגר

# פרטי התחברות עם PAT
pat = "whjk462btnpjxcguf6klqfmcl4bw3l46jakhgauqrlbl6xfnkm4q"
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# כותרות (Headers)
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json"
}


# פונקציה לשליפת work items
def get_work_items(changeset_data, headers, changeset_id):
    # קבלת קישור ל-work items מתוך ה- _links
    work_items_url = changeset_data["_links"]["workItems"]["href"]

    # שליחת בקשה נוספת לשליפת ה-work items
    work_items_response = requests.get(work_items_url, headers=headers)

    if work_items_response.status_code == 200:
        work_items_data = work_items_response.json()

        # הוספת שדה "changesetId" לכל work item
        for work_item in work_items_data.get("value", []):
            work_item["changesetId"] = changeset_id  # הוספת ה-changesetId לשדה
        return work_items_data  # מחזיר את נתוני ה-work items
    else:
        print("Failed to retrieve work items. Status Code:", work_items_response.status_code)
        print("Response:", work_items_response.text)
        return None


# מילון (dictionary) לאחסון כל ה-changesets
all_changesets = {}

# לולאת for לרוץ על כל ה-changeset_id מ-1 עד 1000
for changeset_id in range(7993 , 8610):
    # URL של ה-changeset
    url = f"http://192.168.1.112/{organization}/{project}/_apis/tfvc/changesets/{changeset_id}?api-version=7.0"

    # שליחת הבקשה
    response = requests.get(url, headers=headers)

    # בדיקה אם הבקשה הצליחה
    if response.status_code == 200:
        changeset_data = response.json()

        # שליפת מידע על השינויים (Changes) מתוך `_links.changes`
        changes_url = changeset_data.get("_links", {}).get("changes", {}).get("href")
        if changes_url:
            changes_response = requests.get(changes_url, headers=headers)
            if changes_response.status_code == 200:
                changes_data = changes_response.json()

                # הוספת נתוני ה-pathActions לכל שינוי
                for change in changes_data.get("value", []):
                    # אם יש pathActions, נוסיף אותו לשינוי
                    path_actions = change.get("pathActions", [])
                    change["pathActions"] = path_actions

                changeset_data["changes"] = changes_data.get("value", [])
            else:
                print(
                    f"שגיאה בבקשה עבור changes ב-changeset_id {changeset_id}: {changes_response.status_code} - {changes_response.text}")

        # שליפת work items בעזרת הפונקציה
        work_items_data = get_work_items(changeset_data, headers, changeset_id)
        if work_items_data:
            changeset_data["workItems"] = work_items_data  # הוספת נתוני ה-work items

        all_changesets[changeset_id] = changeset_data
        # הוספת ה-changeset למילון תחת המפתח של ה-changeset_id
        print(f"ה-changeset {changeset_id} נוסף בהצלחה.")
    elif response.status_code == 404:
        print(f"changeset_id {changeset_id} לא נמצא. יציאה מהלולאה.")
        break
    else:
        print(f"שגיאה בבקשה עבור changeset_id {changeset_id}: {response.status_code} - {response.text}")

# שמירה של כל הנתונים לקובץ JSON
with open("all_changesets_with_pathactions_and_workitems.json", "w", encoding="utf-8") as json_file:
    json.dump(all_changesets, json_file, ensure_ascii=False, indent=4)

print("הקובץ all_changesets_with_pathactions_and_workitems.json נוצר בהצלחה.")
