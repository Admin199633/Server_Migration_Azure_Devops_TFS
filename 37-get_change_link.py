import requests
import base64
import json

# פרטי התחברות ל-Azure DevOps
organization = "DefaultCollection"
project = "DG-Dev"
pat = "whjk462btnpjxcguf6klqfmcl4bw3l46jakhgauqrlbl6xfnkm4q"

# קידוד ה-PAT לצורך Authentication
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# כתובת ה-WIQL API
wiql_url = f"http://192.168.1.112/{organization}/{project}/_apis/wit/wiql?api-version=5.0"

# קריאת מזהי Work Items מתוך הקובץ JSON
print("📂 טוען Work Item IDs מהקובץ...")
with open("work_items_with_changeset_ids.json", "r", encoding="utf-8") as json_file:
    work_items_data = json.load(json_file)

# בדיקה אם הקובץ מכיל נתונים
if not work_items_data:
    print("❌ לא נמצאו Work Items בקובץ JSON.")
    exit()

print(f"✅ נמצא {len(work_items_data)} Work Items לטיפול.")

# כותרות (Headers)
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json"
}

detailed_work_items = []

# מעבר על כל Work Item בנפרד
for item in work_items_data:
    work_item_id = str(item["id"])  # קבלת ה-ID כטקסט
    print(f"\n🔍 בודק Work Item ID: {work_item_id}")

    # יצירת ה-WIQL Query עם המזהה הבודד
    wiql_query = {
        "query": f"""
            SELECT [System.Id]
            FROM WorkItems
            WHERE [System.Id] = {work_item_id}"""
    }

    # שליחת הבקשה ל-WIQL API
    response = requests.post(wiql_url, headers=headers, json=wiql_query)

    if response.status_code == 200:
        work_items = response.json().get("workItems", [])

        for item in work_items:
            work_item_id = item["id"]
            print(f"✅ נמצא Work Item ID: {work_item_id}, שולף פרטים...")

            # שליפת פרטי Work Item ספציפי
            work_item_url = f"http://192.168.1.112/{organization}/{project}/_apis/wit/workItems/{work_item_id}?$expand=relations&api-version=7.0"
            work_item_response = requests.get(work_item_url, headers=headers)

            if work_item_response.status_code == 200:
                work_item_data = work_item_response.json()
                relations = work_item_data.get("relations", [])

                if relations:
                    print(f"🔗 נמצא {len(relations)} קשרים ל-Work Item {work_item_id}:")
                else:
                    print("⚠️ אין קשרים ל-Work Item זה.")

                for relation in relations:
                    linked_id = relation.get("url", "").split("/")[-1]
                    relation_type = relation.get("rel", "Unknown")

                    print(f"  ➝ סוג קשר: {relation_type}, Work Item מקושר: {linked_id}")

                    detailed_work_items.append({
                        "id": work_item_id,
                        "work_item_link_id": linked_id,
                        "type": relation_type
                    })
            else:
                print(f"❌ שגיאה בשליפת Work Item {work_item_id}: {work_item_response.status_code} - {work_item_response.text}")
    else:
        print(f"❌ שגיאה בבקשה ל-ID {work_item_id}: {response.status_code} - {response.text}")

# כתיבה לקובץ JSON
print("\n💾 שומר נתונים בקובץ work_items_links1.json...")
with open("work_items_links1.json", "w", encoding="utf-8") as f:
    json.dump(detailed_work_items, f, ensure_ascii=False, indent=4)

print("✅ הקובץ work_items_links1.json נוצר בהצלחה! 🎉")
