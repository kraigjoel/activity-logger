from server.database import initialise_database, insert_activity

initialise_database()

activities = {
    1: 'coding',
    2: 'ccna study',
    3: 'uni',
    4: 'gym',
    5: 'guitar'
}

print("=== Activity Logger ===")

for number, activity in activities.items():
    print(f"{number}. {activity}")

while True: 
    selection = input("Select activity: ")
    if selection.isdigit():
        selection = int(selection)

        if selection in activities:
            break

    print("Invalid activity, please try again.")

print(f"Selected: {activities[selection]}")

while True:
    try:
        duration = int(input("Duration (minutes): "))

        if duration > 0:
            break

        print("Duration must be greater than 0")

    except (ValueError):
        print("Please enter a valid integer")


notes = input("Notes (optional): ").strip()

if notes == "":
    notes = None

log_id = insert_activity(
    activities[selection],
    duration,
    notes
)

print(f"\nActivity logged successfully! ID: {log_id}")

print("\n=== Activity Summary ===")
print(f"Activity: {activities[selection]}")
print(f"Duration: {duration} minutes")
print(f"Notes: {notes if notes is not None else 'No notes'}")
