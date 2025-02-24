import base64
import requests
import json

# 1. פרטי ההתחברות לשרת
organization = "DG-Dev"
url_api = "http://192.168.1.91/DefaultCollection"
pat = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"  # Personal Access Token
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# 2. כותרות הבקשה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 3. טווח מזהים לבחירה
from_id = 6  # מזהה התחלתי
to_id = 614  # מזהה סופי
top_results = 1000  # מספר מקסימלי של תוצאות

# 4. כתובת ה-API לקבלת ה-Changes עם טווח מזהים
changes_url = f"{url_api}/_apis/tfvc/changesets?fromId={from_id}&toId={to_id}&$top={top_results}&api-version=7.1-preview.3"

# 5. שליחת הבקשה לשרת
response = requests.get(changes_url, headers=headers)

# 6. בדיקה אם הבקשה הצליחה
if response.status_code == 200:
    changesets = response.json().get("value", [])

    # יצירת רשימת אובייקטים עם שם ה-Change וה-ID שלו
    changes_data = [
        {"id": change["changesetId"], "name": change.get("comment", "No Name")}
        for change in changesets
    ]

    # שמירת התוצאה לקובץ JSON
    with open("changes_output.json", "w", encoding="utf-8") as file:
        json.dump(changes_data, file, ensure_ascii=False, indent=4)

    print(f"✅ קובץ 'changes_output.json' נוצר בהצלחה! (Changes {from_id} - {to_id})")
    print(f"🔢 סה\"כ שינויים שהתקבלו: {len(changes_data)}")
else:
    print(f"❌ שגיאה בקבלת הנתונים. סטטוס: {response.status_code}, תגובה: {response.text}")
