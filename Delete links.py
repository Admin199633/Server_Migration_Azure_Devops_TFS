import requests
import base64
import json

# 🔹 פרטי התחברות ל-Azure DevOps
organization = "DefaultCollection"
project = "DG-Dev"
pat = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"
base_url = "http://192.168.1.91"

# 🔹 קידוד ה-PAT לאימות
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# 🔹 כותרות לבקשות API
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json",
    "Accept": "application/json"
}

# 🔹 קריאת קובץ JSON עם ה-Work Items והקישורים
with open("work_items_links.json", "r", encoding="utf-8") as file:
    work_items_links = json.load(file)

# 🔹 רשימת Work Items לטיפול
work_items_dict = {}
for item in work_items_links:
    work_item_id = item["id"]
    link_id = item["work_item_link_id"]
    link_type = item["type"]

    if work_item_id not in work_items_dict:
        work_items_dict[work_item_id] = []
    work_items_dict[work_item_id].append({"id": link_id, "type": link_type})

# 🔹 מחיקת כל ה-Changesets בלבד
for work_item_id, links in work_items_dict.items():
    # 🔹 שליפת כל הקישורים של ה-Work Item מה-API
    work_item_url = f"{base_url}/{organization}/{project}/_apis/wit/workItems/{work_item_id}?$expand=relations&api-version=7.0"
    response = requests.get(work_item_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ שגיאה בקבלת Work Item {work_item_id}: {response.status_code} - {response.text}")
        continue

    work_item_data = response.json()
    relations = work_item_data.get("relations", [])

    # 🔹 מציאת כל ה-Changesets (ArtifactLink) שצריך למחוק
    delete_operations = []
    for i, relation in enumerate(relations):
        rel_type = relation["rel"]

        # ✅ מוחק רק Changesets שהם מסוג ArtifactLink
        if rel_type == "ArtifactLink":
            delete_operations.append({"op": "remove", "path": f"/relations/{i}"})

    # 🔹 אם אין Changesets למחיקה, לדלג
    if not delete_operations:
        print(f"⚠️ אין Changesets למחיקה עבור Work Item {work_item_id}. מדלג.")
        continue

    # 🔹 שליחת הבקשה למחיקת ה-Changesets
    patch_url = f"{base_url}/{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version=7.0"
    delete_response = requests.patch(patch_url, headers=headers, data=json.dumps(delete_operations))

    if delete_response.status_code in [200, 204]:
        print(f"✅ נמחקו כל ה-Changesets מ-Work Item {work_item_id}.")
    else:
        print(
            f"❌ נכשל במחיקת Changesets עבור Work Item {work_item_id}. תגובה: {delete_response.status_code}, {delete_response.text}")
