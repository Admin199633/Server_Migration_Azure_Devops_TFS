import requests
import base64
import os
import json

# נתונים מזהים
personal_access_token = "pehwyr4cghprowzrxr6sqfgodjdbys7fgraae3orq2qumjrorsqq"
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# URL בסיסי לשרת B
base_url_B = "http://192.168.1.132/DefaultCollection/DG-Dev/_apis"

# העלאת הקובץ לשרת B
def upload_attachment_to_work_item(file_path, work_item_id):
    upload_url = f"{base_url_B}/wit/attachments?fileName={os.path.basename(file_path)}&api-version=5.0"

    try:
        with open(file_path, 'rb') as file:
            response = requests.post(upload_url, headers={
                "Authorization": f"Basic {encoded_pat}",
                "Content-Type": "application/octet-stream"
            }, data=file)

            if response.status_code == 201:
                print(f"File uploaded successfully to Work Item {work_item_id}.")
                return response.json().get('url')
            else:
                print(f"Failed to upload file: {response.status_code} - {response.text}")
                return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# הוספת הקובץ ל-Work Item בשרת B
def add_attachment_to_work_item(work_item_id, attachment_url):
    url = f"{base_url_B}/wit/workitems/{work_item_id}?api-version=5.0"

    # יצירת body להוספת הקובץ
    body = [
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "AttachedFile",
                "url": attachment_url,
                "attributes": {
                    "comment": "File uploaded from server B"
                }
            }
        }
    ]

    response = requests.patch(url, headers={
        "Authorization": f"Basic {encoded_pat}",
        "Content-Type": "application/json-patch+json"
    }, json=body)

    if response.status_code == 200:
        print(f"Attachment added successfully to Work Item {work_item_id}.")
    else:
        print(f"Failed to add attachment to Work Item: {response.status_code} - {response.text}")

# שלב כל הפעולות על כל האובייקטים ב-JSON
def process_attachments(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

            # וידוא שהנתונים הם רשימה
            if not isinstance(data, list):
                print("Invalid JSON structure. Expected a list of objects.")
                return

            for item in data:
                file_name = item.get("file_name")
                work_item_id = item.get("ID")

                if file_name and work_item_id:
                    print(f"Processing file: {file_name} for Work Item: {work_item_id}")

                    # העלאת הקובץ
                    attachment_url = upload_attachment_to_work_item(file_name, work_item_id)

                    if attachment_url:
                        # הוספת הקובץ ל-Work Item
                        add_attachment_to_work_item(work_item_id, attachment_url)
                else:
                    print(f"Missing file_name or ID for item: {item}")

    except FileNotFoundError:
        print(f"JSON file not found: {json_file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# קריאה לפונקציה
json_path = "attachments_unmatch.json"  # נתיב קובץ JSON
process_attachments(json_path)
