import requests
import base64
import json
import os
from urllib.parse import urlparse

# נתונים מזהים
personal_access_token = "qqdllaihdfyp4ta5ke6mbtwzr6cwcyo4xhedudoaxhifev3penua"
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כותרות הבקשה עם טוקן גישה
headers = {
    "Authorization": f"Basic {encoded_pat}"
}

# URL בסיסי לשרת
base_url = "http://192.168.1.112/DefaultCollection/DG-Dev/_apis"

# פונקציה לשליפת מזהים מהקובץ JSON
def get_all_item_ids(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

            # בדיקה אם הנתונים הם רשימה של אובייקטים
            if isinstance(data, list):
                return [item.get("JsonID") for item in data if "JsonID" in item]
            else:
                print("Invalid JSON structure.")
                return []
    except FileNotFoundError:
        print(f"JSON file not found: {json_file_path}")
        return []

# פונקציה לשליפת קבצים מצורפים מ-Work Item
def fetch_work_item_attachments(work_item_id):
    print(f"Fetching attachments for Work Item ID: {work_item_id}")
    url = f"{base_url}/wit/workitems/{work_item_id}/?$expand=all&api-version=5.0"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        work_item_data = response.json()
        attachments = work_item_data.get('relations', [])
        attachment_data = []

        for attachment in attachments:
            if attachment.get('rel') == 'AttachedFile':
                file_name = attachment.get('attributes', {}).get('name')
                file_url = attachment.get('url')
                bin_file_name = f"{os.path.splitext(file_name)[0]}.bin"

                attachment_info = {
                    'work_item_id': work_item_id,
                    'file_name': file_name,
                    'bin_file_name': bin_file_name,
                    'url': file_url,
                    'comment': attachment.get('attributes', {}).get('comment')
                }
                attachment_data.append(attachment_info)

        return attachment_data
    else:
        print(f"Error fetching attachments for Work Item {work_item_id}: {response.status_code} - {response.text}")
        return []

# הורדת הקובץ מה-URL
def download_file(file_url, file_name):
    response = requests.get(file_url, headers={"Authorization": f"Basic {encoded_pat}"}, stream=True)

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded successfully as {file_name}.")
        return file_name
    else:
        print(f"Failed to download file: {response.status_code}")
        return None

# פונקציה ראשית
def main():
    json_file_path = 'non_matching_bugs.json'
    item_ids = get_all_item_ids(json_file_path)

    if not item_ids:
        print("No Work Item IDs found. Exiting.")
        return

    all_attachments = []

    for item_id in item_ids:
        attachments = fetch_work_item_attachments(item_id)
        if attachments:
            all_attachments.extend(attachments)

            # הורדת הקבצים
            for attachment in attachments:
                file_url = attachment['url']
                file_name = attachment['file_name']
                downloaded_file_name = download_file(file_url, file_name)
                if downloaded_file_name:
                    os.rename(downloaded_file_name, file_name)
                    print(f"File renamed to {file_name}")

    if all_attachments:
        with open('attachments_unmatch.json', 'w') as json_file:
            json.dump(all_attachments, json_file, indent=4)
            print("All attachment data has been saved to 'attachments_unmatch.json'.")
    else:
        print("No attachments found for any Work Item.")

# הרצת התהליך
if __name__ == "__main__":
    main()
