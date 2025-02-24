import requests
import base64
import json

# פרטי התחברות ל-Azure DevOps
organization = "DefaultCollection"
project = "DG-Dev"
pat = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"

# קידוד ה-PAT לצורך Authentication
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# כתובת ה-WIQL API
wiql_url = f"http://192.168.1.91/{organization}/{project}/_apis/wit/wiql?api-version=5.0"

# בקשת WIQL לקבלת Work Items מסוג "Product Backlog Item"
wiql_query = {
    "query": """
        SELECT [System.Id]
        FROM WorkItems
        WHERE [System.TeamProject] = 'DG-Dev'
        AND [System.ExternalLinkCount] > 0
        """

}



# כותרות (Headers)
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json"
}

# שליחת הבקשה
response = requests.post(wiql_url, headers=headers, json=wiql_query)
if response.status_code == 200:
    work_items = response.json().get("workItems", [])

    detailed_work_items = []
    for item in work_items:
        work_item_id = item["id"]
        # שליפת פרטי Work Item ספציפי
        work_item_url = f"http://192.168.1.91/{organization}/{project}/_apis/wit/workItems/{work_item_id}?$expand=relations&api-version=7.0"
        work_item_response = requests.get(work_item_url, headers=headers)

        if work_item_response.status_code == 200:
            work_item_data = work_item_response.json()
            relations = work_item_data.get("relations", [])

            for relation in relations:
                detailed_work_items.append({
                    "id": work_item_id,
                    "work_item_link_id": relation.get("url", "").split("/")[-1],  # שליפת מזהה ה-Work Item מה-URL
                    "type": relation.get("rel", "Unknown")
                })

    # כתיבה לקובץ JSON
    with open("work_items_links.json", "w", encoding="utf-8") as f:
        json.dump(detailed_work_items, f, ensure_ascii=False, indent=4)

    print("הקובץ work_items_links.json נוצר בהצלחה.")
else:
    print(f"שגיאה בבקשה: {response.status_code} - {response.text}")
