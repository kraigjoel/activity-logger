import requests

response = requests.get("http://127.0.0.1:8000/activities")

print(f"HTTP Status: {response.status_code}")

activities = response.json()

print("\n=== Activity Logs ===")

for activity in activities:
    notes = activity['notes']
    if not notes:
        notes = "No notes"
    print(f"ID: {activity['log_id']}")
    print(f"Activity: {activity['activity']}")
    print(f"Duration: {activity['duration']}")
    print(f"Notes: {notes}\n")