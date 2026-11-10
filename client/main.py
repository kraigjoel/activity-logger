import requests

BASE_URL = "http://127.0.0.1:8000"

def view_activities():
    response = requests.get(f"{BASE_URL}/activities")
    activities = response.json()
    
    for activity in activities:
        notes = activity['notes']
        if not notes:
            notes = "No notes"
        print(f"ID: {activity['log_id']}")
        print(f"Activity: {activity['activity']}")
        print(f"Duration: {activity['duration']}")
        print(f"Notes: {notes}\n")

def log_activity():
    activity = input("Activity: ")
    duration = int(input("Duration (minutes): "))
    notes = input("Notes (optional): ")

    log_dict = {
        "activity": activity,
        "duration": duration,
        "notes": notes
    }

    response = requests.post(f"{BASE_URL}/activities",json=log_dict)

    print(f"HTTP Status: {response.status_code}")
    print(response.json())

def main():
    while True:
        print("\n=== Activity Logger ===")
        print("1. Log a new activity")
        print("2. View all activities")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            log_activity()

        elif choice == "2":
            view_activities()

        elif choice == "3":
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()