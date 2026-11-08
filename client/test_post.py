import requests

url = "http://127.0.0.1:8000/activities"

new_activity = {
    "activity": "CCNA Study",
    "duration": "60",
    "notes": "Practised subnetting"
}

response = requests.post(url, json=)