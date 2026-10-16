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

selected_activity = int(input("Select an activity (1-5): "))

print(activities[selected_activity])

