import requests
import json
import base64

# נתונים מזהים (מילוי פרטים מתאימים)
personal_access_token = "zriszeos4pqam2e4dkybxmmod7ulm52t5wprdplfkn4wm3lcbrcq"

# כתובת בסיסית ל-API של Azure DevOps
base_api_url = "http://192.168.1.91/DefaultCollection/DG-Dev/_apis/wit/workitems"

# קידוד ה-PAT
encoded_pat = base64.b64encode(f":{personal_access_token}".encode()).decode()

# כותרות בקשה עם טוקן גישה
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json-patch+json"
}

# קריאה לקובץ JSON שמכיל את נתוני ה-Work Items
with open("data_cleaned.json", "r", encoding="utf-8") as file:
    work_items = json.load(file)


# פונקציה להוסיף Work Item
def add_work_item(item):
    # שליפת סוג ה-Work Item מתוך הנתונים (ברירת מחדל Bug)
    work_item_type = item.get("WorkItemType")

    # עדכון כתובת ה-API עם סוג ה-Work Item
    api_url = f"{base_api_url}/${work_item_type}?api-version=6.0"

    patch_data = []
    if item.get("Description"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.Description",
            "value": item["Description"]
        })

    # הוספת שדות נדרשים ל-Work Item
    if item.get("Title"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.Title",
            "value": item["Title"]
        })

    if item.get("State"):
        # כעת נעדכן את ה-State תמיד ל-"New"
        patch_data.append({
            "op": "add",
            "path": "/fields/System.State",
            "value": "New"
        })




    for field, path in [
        ("AcceptanceCriteria", "/fields/Microsoft.VSTS.Common.AcceptanceCriteria"),

    ]:
        if item.get(field):
            patch_data.append({
                "op": "add",
                "path": path,
                "value": item.get(field)
            })


    if item.get("Microsoft.VSTS.Common.StateChangeDate"):
        patch_data.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Common.StateChangeDate",
            "value": item["Microsoft.VSTS.Common.StateChangeDate"]
        })

    if item.get("SystemiInfo"):
        patch_data.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.TCM.SystemInfo",
            "value":  item["SystemiInfo"]
        })



    if item.get("SystemInfo"):
        patch_data.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.TCM.SystemInfo",
            "value":  item["SystemInfo"]
        })

    if item.get("Source"):
        print(item.get("Source"))  # סוגריים נסגרים כאן
        patch_data.append({
            "op": "add",
            "path": "/fields/Custom.Source",
            "value": item["Source"]
        })

    if item.get("System.Reason"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.Reason",
            "value": item["System.Reason"]
        })

    if item.get("System.BoardColumn"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.BoardColumn",
            "value": item["System.BoardColumn"]
        })

    if item.get("System.BoardLane"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.BoardLane",
            "value": item["System.BoardLane"]
        })

#    if item.get("History"):
#        patch_data.append({
#            "op": "add",
#            "path": "/fields/System.History",
#            "value": item["History"]
#        })



    if item.get("Area"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.AreaPath",
            "value": item["Area"]
        })
    if item.get("IntegrationBuild"):
        patch_data.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Build.IntegrationBuild",
            "value": item["IntegrationBuild"]
        })

    if item.get("ReproSteps"):
        patch_data.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.TCM.ReproSteps",
            "value": item["ReproSteps"]
        })
        #("Effort", "/fields/Microsoft.VSTS.Scheduling.Effort"),
    if item.get("Effort"):
        patch_data.append({
            "op": "add",
            "path": "/fields/Microsoft.VSTS.Scheduling.Effort",
            "value": item["Effort"]
        })

    if item.get("Iteration"):
        patch_data.append({
            "op": "add",
            "path": "/fields/System.IterationPath",
            "value": item["Iteration"]
        })
    assigned_to = item.get("AssignedTo")
    if assigned_to:
        if assigned_to in ["Daniel Bujold","Luella","Charles","Noam Weil","Josh McLean","Gabby Delin","Bar Shitrit","Rotem Zecharya","Ben Duadi","Sheli Comeau","Roi Henigsberg","Guy Royburt","Yuval Amsalem","Daniel Bujold","Michael Kuropatkin", "Tomer Rasad", "Igor Kulyk", "Katya Fialkan", "Alina Svyrydova",
                           "Judy Mandelboim","Eyal Madar","Dima Nirenshteyn","Ran Ben Shimol","Liel Eliyahu","Victoria Gurevich"]:
            print(f"AssignedTo שונה ל-HMS\\LiorSw עבור {assigned_to}")
            assigned_to = "HMS\\LiorSw"
        patch_data.append({
            "op": "add",
            "path": "/fields/System.AssignedTo",
            "value": assigned_to
        })
    else:
        print("לא הוזן AssignedTo, הוזן ערך ברירת מחדל 'HMS\\LiorSw'")
        patch_data.append({
            "op": "add",
            "path": "/fields/System.AssignedTo",
            "value": "HMS\\LiorSw"
        })

    # הוספת שדות נוספים
    for field, path in [
        ("Tags", "/fields/System.Tags"),
#        ("Version", "/fields/Custom.Version"),
        ("ApplicationName", "/fields/Custom.ApplicationName"),
        ("ClientType", "/fields/Custom.ClientType"),
        ("Priority", "/fields/Microsoft.VSTS.Common.Priority"),
        ("Deadline", "/fields/Microsoft.VSTS.Scheduling.TargetDate"),
        ("Activity", "/fields/Microsoft.VSTS.Common.Activity"),
        ("OriginalEstimate", "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate"),
        ("Remaining", "/fields/Microsoft.VSTS.Scheduling.RemainingWork"),
        ("Completed", "/fields/Microsoft.VSTS.Scheduling.CompletedWork"),
        ("StateGraph", "/fields/Custom.StateGraph"),
        ("Attachments", "/fields/System.AttachedFiles"),
    #    ("RepoSteps", "/fields/Custom.ReproSteps"),

       # ("SystemInfo", "/fields/Microsoft.VSTS.TCM.SystemInfo"),
        ("FoundInVersion", "/fields/Custom.FoundInVersion"),
        ("StoryPoints", "/fields/Microsoft.VSTS.Scheduling.StoryPoints"),
        ("Severity", "/fields/Custom.Severity"),
        ("FoundInBuild", "/fields/Custom.FoundInBuild"),
        ("Valuearea", "/fields/Custom.Valuearea"),
     #   ("BusinessValue", "/fields/Custom.BusinessValue"),
        #("Effort", "/fields/Microsoft.VSTS.Scheduling.Effort"),
        #("Iteration", "/fields/System.IterationPath"),
  #      ("History", "/fields/System.H  istory"),
  #      ("AcceptanceCriteria", "/fields/Microsoft.VSTS.Scheduling.AcceptanceCriteria"),
     #   ("StepstoReproduce", "/fields/Custom.StepstoReproduce"),
        ("CustomerName", "/fields/Custom.CustomerName"),
        ("CustomerBugNumber", "/fields/Custom.CustomerBugNumber"),
        ("FoundIn", "/fields/Microsoft.VSTS.Build.FoundIn"),
        #("IntegrationBuild", "/fields/Microsoft.VSTS.Build.IntegrationBuild"),
       # ("Source", "/fields/HMS.Source")

    ]:
        if item.get(field):
            patch_data.append({
                "op": "add",
                "path": path,
                "value": item.get(field)
            })

    else:
        print(f"BusinessValue חסר עבור Work Item ID: {item.get('ID', 'ללא מזהה')}")

    # שליחת הבקשה
    response = requests.post(api_url, headers=headers, json=patch_data)
    print("Patch data:", json.dumps(patch_data, indent=4))

    # בדיקת התגובה
    if response.status_code in [200, 201]:
        print(f"Work Item {item.get('ID', 'ללא מזהה')} נוצר בהצלחה כ-{work_item_type}")
    else:
        print(f"שגיאה ביצירת Work Item {item.get('ID', 'ללא מזהה')}: {response.status_code} - {response.text}")


# מעבר על כל האובייקטים והוספתם
for item in work_items:
    add_work_item(item)
