import json

# קריאת קובץ JSON
with open('all_changesets_with_pathactions_and_workitems.json', 'r',encoding='utf-8') as file:
    data = json.load(file)


# פונקציה שמחפשת את המפתחות 'changesetId' ואת המפתחות 'path' ומחזירה את הערכים שלהם
def find_changes(obj):
    changesets = {}

    # אם האובייקט הוא מילון (dictionary)
    if isinstance(obj, dict):
        changeset_id = None
        changes = []

        # אם נמצא המפתח 'changesetId', נשמור אותו
        if 'changesetId' in obj:
            changeset_id = obj['changesetId']

        # אם נמצא המפתח 'changes', נריץ חיפוש נוסף במערך הערכים
        if 'changes' in obj:
            for change in obj['changes']:
                if 'item' in change and 'path' in change['item']:
                    file_name = change['item']['path'].split('/')[-1]  # הוצאת שם הקובץ מתוך הנתיב
                    paths = change['item']['path']
                    changes.append({
                        "name_file": file_name,
                        "paths": paths
                    })

        # אם נמצא changesetId, נוסיף אותו לדיקציהן
        if changeset_id:
            changesets[changeset_id] = {
                'changesetId': changeset_id,
                'changes': changes
            }

        # נבצע חיפוש לכל המפתחות והמילונים בתוך האובייקט
        for key, value in obj.items():
            if key not in ['changesetId', 'changes']:
                nested_changesets = find_changes(value)
                for nested_changeset_id, nested_data in nested_changesets.items():
                    if nested_changeset_id not in changesets:
                        changesets[nested_changeset_id] = nested_data

    # אם האובייקט הוא רשימה (list), נבצע חיפוש על כל אחד מהאיברים
    elif isinstance(obj, list):
        for item in obj:
            nested_changesets = find_changes(item)
            for nested_changeset_id, nested_data in nested_changesets.items():
                if nested_changeset_id not in changesets:
                    changesets[nested_changeset_id] = nested_data

    return changesets


# חיפוש כל הערכים של 'changesetId' ו-'path' באובייקט
changesets = find_changes(data)

# כתיבת התוצאה לקובץ JSON חדש
with open('output.json', 'w') as output_file:
    json.dump(changesets, output_file, indent=4)

print("הקובץ נוצר בהצלחה!")
