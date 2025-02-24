import requests
import base64
import json
import asyncio
import aiohttp

# נתונים מזהים
personal_access_token = "whjk462btnpjxcguf6klqfmcl4bw3l46jakhgauqrlbl6xfnkm4q"
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כותרות הבקשה עם טוקן גישה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json"
}

# URL בסיסי לשרת
base_url = "http://192.168.1.112/DefaultCollection/DG-Dev/_apis"

# מגבלת בקשות במקביל
semaphore = asyncio.Semaphore(50)


# שליחה עם הגבלת בקשות
async def fetch_with_limit(coro):
    async with semaphore:
        return await coro


# שאילתה ל-WIQL לשליפת Work Items
async def fetch_work_items():
    url = f"{base_url}/wit/wiql?api-version=7.0"
    wiql_query = {
        "query": "SELECT [System.Id], [System.Title] FROM WorkItems WHERE [System.WorkItemType] = 'Task' AND [System.Id] >= '8384'"
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, json=wiql_query) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('workItems', [])
            else:
                print(f"Error fetching work items: {response.status}")
                return []


# שליפת פרטים על Work Item בודד עם ניסיונות חוזרים
async def fetch_with_retries(session, url, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error {response.status}: {await response.text()}")
        except aiohttp.ClientError as e:
            print(f"Client error on attempt {attempt + 1}: {e}")
        await asyncio.sleep(2 ** attempt)  # המתנה אקספוננציאלית
    return None


# שליפת פרטים על Work Item
async def fetch_work_item_details(session, work_item_id):
    url = f"{base_url}/wit/workitems/{work_item_id}?api-version=7.0"
    return await fetch_with_retries(session, url)


# שליפת תגובות על Work Item
async def fetch_work_item_comments(session, work_item_id):
    url = f"{base_url}/wit/workitems/{work_item_id}/comments?api-version=7.0-preview"
    return await fetch_with_retries(session, url)


# שמירת הנתונים לקובץ JSON
def save_to_json(data, filename="output.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# שליפת פרטים ותגובות לכל Work Item במקביל
async def process_work_items(work_items):
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for item in work_items:
            work_item_id = item.get('id')
            tasks.append(fetch_with_limit(fetch_work_item_details(session, work_item_id)))
            tasks.append(fetch_with_limit(fetch_work_item_comments(session, work_item_id)))

        responses = await asyncio.gather(*tasks)
        details = responses[::2]  # פרטים
        comments = responses[1::2]  # תגובות

        # עיבוד ויצירת רשימה של נתונים
        # עיבוד ויצירת רשימה של נתונים
        output_data = []
        for i, detail in enumerate(details):
            if detail:
                work_item_id = detail.get('id')
                jason_id = detail.get('fields', {}).get('System.Id', None)  # יש להתאים לפי מבנה השדות
                comment_data = comments[i] if comments[i] else None

                # בדיקה אם יש תגובות
                if comment_data and comment_data.get("totalCount", 0) > 0:
                    output_data.append({
                        "ID": work_item_id,
                        "JsonID": jason_id,
                        "Comments": comment_data
                    })

        return output_data


# פונקציה ראשית
async def main():
    print("Fetching Work Items...")
    work_items = await fetch_work_items()
    if work_items:
        print(f"{len(work_items)} Work Items fetched.")
        processed_data = await process_work_items(work_items)
        save_to_json(processed_data)  # שמירה לקובץ
        print("Data has been saved to 'output.json'.")
    else:
        print("No Work Items found.")


# הרצת התהליך
if __name__ == "__main__":
    asyncio.run(main())
