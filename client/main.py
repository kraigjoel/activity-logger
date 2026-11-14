import requests

BASE_URL = "http://127.0.0.1:8000"

def view_activities():
    print("\nConnecting to server...")
    try:
        response = requests.get(f"{BASE_URL}/activities", timeout=5)
        response.raise_for_status()

    except requests.exceptions.HTTPError:
        print(f"\nServer returned HTTP {response.status_code}")
        return

    except (requests.exceptions.ConnectionError,
            requests.exceptions.Timeout):
        print("\nCannot connect to the server.")
        return

    print("\nConnected to server!\n")
    try:
        activities = response.json()

    except requests.exceptions.JSONDecodeError:
        print("Server responded with non-json format")
        return

    if not activities:
        print("No activities logged yet")
        return
    
    for activity in activities:
        notes = activity['notes']
        if not notes:
            notes = "No notes"
        print(f"ID: {activity['log_id']}")
        print(f"Activity: {activity['activity']}")
        print(f"Duration: {activity['duration']}")
        print(f"Notes: {notes}\n")

def log_activity():

    while True:
        activity = input("Activity: ").strip()

        if not activity:
            print("Activity name cannot be empty.")

        else:
            break
        
    
    
    while True:

        duration_input = input("Duration (minutes): ")

        try:
            duration = int(duration_input)
            if duration > 0:
                break
            else:
                print("Please enter a positive integer")

        except ValueError:
            print("Please enter a valid whole number")
    
    notes = input("Notes (optional): ")

    log_dict = {
        "activity": activity,
        "duration": duration,
        "notes": notes
    }

    try:
        response = requests.post(f"{BASE_URL}/activities",json=log_dict,
                                  timeout=5)
        response.raise_for_status()
        
        print("Connected to server!")

    except requests.exceptions.HTTPError:
        print(f"\nServer returned HTTP {response.status_code}")
        return

    except requests.exceptions.ConnectionError:
        print("\nConnection failed. The activity may or may not have been saved.")
        return

    except requests.exceptions.Timeout:
        print("\nRequest timed out. Check your activities before retrying.")
        return

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