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