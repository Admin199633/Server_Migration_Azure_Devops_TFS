import requests
import base64
import json

# פרטי התחברות ל-Azure DevOps
organization = "DefaultCollection"
project = "DG-Dev"

# הגדרת ה-PAT (Personal Access Token)
pat = "whjk462btnpjxcguf6klqfmcl4bw3l46jakhgauqrlbl6xfnkm4q"

# קידוד ה-PAT לצורך Authentication
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# כתובת ה-WIQL API
wiql_url = f"http://192.168.1.112/{organization}/{project}/_apis/wit/wiql?api-version=7.0-preview"

# כתובת ה-Work Item API
work_item_url_template = f"http://192.168.1.112/{organization}/_apis/wit/workitems/{{id}}?api-version=7.0-preview"
comments_url_template = f"http://192.168.1.112/{organization}/{project}/_apis/wit/workItems/{{id}}/comments?api-version=7.0-preview"

# הכותרות (Headers)
headers = {
    "Authorization": f"Basic {encoded_pat}",
    "Content-Type": "application/json"
}

# שאילתת WIQL לשליפת כל ה-IDs של Test Cases
#    WHERE [System.WorkItemType] IN ('Task', 'Bug', 'Epic', 'Impediment', 'Feature', 'Product Backlog Item', 'Test Case')    """


# שאילתת WIQL לשליפת כל ה-IDs של Test Cases
#    WHERE [System.WorkItemType] IN ('Task', 'Bug', 'Epic', 'Impediment', 'Feature', 'Product Backlog Item', 'Test Case')    """
query = {
    "query": """
SELECT [System.Id]
FROM WorkItems
WHERE [System.WorkItemType] IN ('Task') 
AND [System.Id] > 6502

    """
}






try:
    # שליחת השאילתה ל-WIQL API
    response = requests.post(wiql_url, headers=headers, json=query)
    response.raise_for_status()
    work_item_ids = [item['id'] for item in response.json().get('workItems', [])]

    selected_fields = []
    for work_item_id in work_item_ids:
        work_item_response = requests.get(work_item_url_template.format(id=work_item_id), headers=headers)
        work_item_response.raise_for_status()
        work_item_data = work_item_response.json()

        fields = work_item_data.get("fields", {})

        # קבלת התגובות
        comments_response = requests.get(comments_url_template.format(id=work_item_id), headers=headers)
        comments_response.raise_for_status()
        comments_data = comments_response.json()

        comments = comments_data.get("comments", [])

        # שליפת כל השדות המבוקשים
        selected_fields.append({
            "ID": work_item_data["id"],
            "Title": fields.get("System.Title", ""),
            "State": fields.get("System.State", ""),
            "AssignedTo": fields.get("System.AssignedTo", {}).get("displayName", ""),
            "CreatedBy": fields.get("System.CreatedBy", {}).get("displayName", ""),
            "Description": fields.get("System.Description", ""),
            "Area": fields.get("System.AreaPath", ""),
            "Iteration": fields.get("System.IterationPath", ""),
            "Tags": fields.get("System.Tags", ""),
            "Version": fields.get("Custom.Version", ""),
            "ApplicationName": fields.get("Custom.ApplicationName", ""),
            "ClientType": fields.get("Custom.ClientType", ""),
            "Priority": fields.get("Microsoft.VSTS.Common.Priority", ""),
            "Deadline": fields.get("Microsoft.VSTS.Scheduling.TargetDate", ""),
            "Activity": fields.get("Microsoft.VSTS.Common.Activity", ""),
            "OriginalEstimate": fields.get("Microsoft.VSTS.Scheduling.OriginalEstimate", ""),
            "Remaining": fields.get("Microsoft.VSTS.Scheduling.RemainingWork", ""),
            "Completed": fields.get("Microsoft.VSTS.Scheduling.CompletedWork", ""),
            "Discussion": fields.get("System.History", ""),
            "StateGraph": fields.get("Custom.StateGraph", ""),
            "History": work_item_data.get("rev", ""),
            "Links": work_item_data.get("_links", {}),
            "Attachments": fields.get("System.AttachedFiles", []),
            "RepoSteps": fields.get("Custom.ReproSteps", ""),
            "SystemInfo": fields.get("Custom.SystemInfo", ""),
            "FoundInVersion": fields.get("Custom.FoundInVersion", ""),
            "ResolvedReason": fields.get("Microsoft.VSTS.Common.ResolvedReason", ""),
            "StoryPoints": fields.get("Microsoft.VSTS.Scheduling.StoryPoints", ""),
            "Severity": fields.get("Custom.Severity", ""),
            "FoundInBuild": fields.get("Custom.FoundInBuild", ""),
            "IntegratedInBuild": fields.get("Custom.IntegratedInBuild", ""),
            "WorkItemType": fields.get("System.WorkItemType", ""),
            "ResolvedBy": fields.get("Microsoft.VSTS.Common.ResolvedBy", {}).get("displayName", ""),
            "Reason": fields.get("System.Reason", ""),
            "StateChangeDate": fields.get("Microsoft.VSTS.Common.StateChangeDate", ""),
            "Effort":fields.get("Microsoft.VSTS.Scheduling.Effort", ""),
            "BusinessValue": fields.get("Microsoft.VSTS.Common.BusinessValue", ""),
            "TimeCriticality": fields.get("Microsoft.VSTS.Common.TimeCriticality", ""),
            "Valuearea": fields.get("Microsoft.VSTS.Common.Valuearea", ""),
            "AcceptanceCriteria": fields.get("Microsoft.VSTS.Common.AcceptanceCriteria", ""),
            "ReproSteps": fields.get("Microsoft.VSTS.TCM.ReproSteps", ""),
            "SystemiInfo": fields.get("Microsoft.VSTS.TCM.SystemInfo", ""),
            "CustomerName": fields.get("HMS.CustomerName", ""),
            "CustomerBugNumber": fields.get("HMS.CustomerBug", ""),
            "FoundIn": fields.get("Microsoft.VSTS.Build.FoundIn", "שדה לא נמצא"),
            "IntegrationBuild": fields.get("Microsoft.VSTS.Build.IntegrationBuild", "שדה לא נמצא"),
            "Source": fields.get("HMS.Source", "שדה לא נמצא"),

            "Comments": comments  # הוספת התגובות

        })

    # שמירת כל הנתונים בקובץ JSON
        with open("filtered_testcase_with_comments.json", "w", encoding="utf-8") as file:
          json.dump(selected_fields, file, ensure_ascii=False, indent=4)

    print("הנתונים שנבחרו נשמרו בקובץ filtered_testcase_with_comments.json")

except requests.exceptions.RequestException as e:
    print(f"שגיאה בביצוע הבקשה: {e}")
