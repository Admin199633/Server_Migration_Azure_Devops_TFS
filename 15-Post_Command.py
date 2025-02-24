from datetime import datetime
import requests
import json
import base64

# פרטי התחברות ל-Azure DevOps
personal_access_token = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"
base_api_url = 'http://192.168.1.91/DefaultCollection/DG-Dev/_apis/wit/workitems/'

# קידוד ה-PAT לצורך Authentication
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# הגדרת כותרות הבקשה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json; charset=utf-8"
}

# קריאת קובץ JSON
def load_json_data(file_path='output.json'):
    try:
        print("טוען את קובץ ה-JSON...")
        with open('output.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"נמצא {len(data)} Work Items בקובץ.")
        return data
    except Exception as e:
        print(f"שגיאה בקריאת הקובץ: {e}")
        return []

# שליחת תגובה ל-Work Item
def send_comment_to_server(item_id, comment, user_name, created_date):
    # המרה של פורמט התאריך
    try:
        # המרת הפורמט המקורי לפורמט הרצוי
        parsed_date = datetime.strptime(created_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        # אם התאריך אינו בפורמט הצפוי
        formatted_date = created_date

    # הוספת שם המשתמש והתאריך בתבנית חדשה
    comment_with_user = (
        f"{user_name}\n"
        f"{formatted_date}\n\n"
        f"{comment}"
    )

    # הדפסת התגובה לפני שליחה ל-API לצורך בדיקה
    print("תגובה לפני שליחה ל-API:")
    print(comment_with_user)

    url = f"{base_api_url}{item_id}/comments?api-version=6.0-preview"
    payload = {
        "text": comment_with_user
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"המידע נשלח בהצלחה ל-Work Item {item_id}.")
        else:
            print(f"שגיאה בשליחת המידע ל-Work Item {item_id}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"שגיאה בביצוע הבקשה עבור Work Item {item_id}: {e}")

# הרצת הסקריפט
def main():
    data = load_json_data()

    for item in data:
        item_id = item.get("JsonID")
        comments_data = item.get("Comments", {})

        if not item_id:
            print(f"ID חסר באובייקט: {item}")
            continue

        comments = comments_data.get("comments", [])
        if not comments:
            print(f"Comments חסרים עבור Work Item {item_id}.")
            continue

        # שליחה של כל הערות ה-Comments אחת-אחת
        for comment_data in comments:
            user_name = comment_data.get("createdBy", {}).get("displayName", "Unknown User")
            comment_text = comment_data.get("text", "")
            created_date = comment_data.get("createdDate", "Unknown Date")
            send_comment_to_server(item_id, comment_text, user_name, created_date)


if __name__ == "__main__":
    main()
