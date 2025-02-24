import json
import requests
import base64
import time
from datetime import datetime
import os

# פרטי ההתחברות לשרת
organization = "DG-Dev"
url_api = "http://192.168.1.91/DefaultCollection"
pat = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"  # Personal Access Token
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# כותרות עבור הבקשה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# נתיבים לקבצים
json_file_path = "changesets_output1_modified_filtered.json"
saved_files_json_path = "saved_files1_modified.json"

# קריאת הקבצים
with open(json_file_path, "r", encoding='utf-8') as f:
    changesets = json.load(f)

with open(saved_files_json_path, "r", encoding='utf-8') as f:
    saved_files = json.load(f)

# URL של ה-API
api_url = f"{url_api}/{organization}/_apis/tfvc/changesets?api-version=7.0"

# משתנים למעקב אחרי הצלחות וכישלונות
success_count = 0
failed_changesets = []

# הגדרות ניסיונות חוזרים
max_retries = 5   # מספר ניסיונות חוזרים לפני כישלון
retry_delay = 5   # זמן המתנה (בשניות) בין כל ניסיון

# לולאה על כל ה-changesets ושליחתם ל-API
for changeset_id, changeset_data in changesets.items():
    # טיפול בקידוד של pathActions
    for change in changeset_data.get("changes", []):
        if 'item' in change and 'path' in change['item']:
            # יצירת חותמת זמן
            current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_path = change['item']['path']
            path_parts = os.path.splitext(original_path)

            # הוספת חותמת הזמן לנתיב
            updated_path = f"{path_parts[0]}-{current_timestamp}{path_parts[1]}"
            change['item']['path'] = updated_path
            print(f"Updated path: {updated_path}")

    # מבנה הנתונים להעלאה
    changeset_data_for_upload = {
        "changes": changeset_data.get("changes"),
        "comment": f"{changeset_data.get('comment', '')} (Old ID: {changeset_id})"
    }

    # שליחת הבקשה עם מנגנון ניסיונות חוזרים
    attempt = 0
    while attempt < max_retries:
        try:
            response = requests.post(api_url, headers=headers, json=changeset_data_for_upload, timeout=10)  # הוספתי timeout כדי למנוע תקיעות
            print(json.dumps(changeset_data_for_upload, indent=2))  # הדפסת JSON שנשלח

            # בדיקת הצלחה
            if response.status_code in [200, 201]:
                print(f"✅ Changeset {changeset_id} uploaded successfully!")
                success_count += 1
                break  # יציאה מהלולאה במקרה של הצלחה
            else:
                print(f"❌ Attempt {attempt + 1} failed for {changeset_id}. Status: {response.status_code}, Error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Network error on attempt {attempt + 1} for {changeset_id}: {e}")

        attempt += 1
        if attempt < max_retries:
            print(f"🔄 Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    # אם כל הניסיונות נכשלו, נוסיף לרשימת הכישלונות
    if attempt == max_retries:
        failed_changesets.append(changeset_id)

# הצגת סיכום התהליך
print("\n=== Summary ===")
print(f"✅ Successful uploads: {success_count}")
print(f"❌ Failed uploads: {len(failed_changesets)}")
if failed_changesets:
    print("Failed Changeset IDs:", ", ".join(failed_changesets))

# שמירת changeset_id שנכשלו לקובץ JSON
failed_json_path = "failed_changesets.json"

if failed_changesets:
    with open(failed_json_path, "w", encoding="utf-8") as failed_file:
        json.dump(failed_changesets, failed_file, indent=4, ensure_ascii=False)
    print(f"📄 Failed changeset IDs saved to {failed_json_path}")
