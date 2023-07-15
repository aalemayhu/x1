import requests
import json
from collections import defaultdict

def get_daily_contributions(username):
    url = f"https://api.github.com/users/{username}/events/public"
    response = requests.get(url)
    data = json.loads(response.text)
    
    contributions = defaultdict(int)

    for event in data:
        date = event["created_at"][:10]  # Extract the date part from timestamp
        contributions[date] += 1

    for date, count in contributions.items():
        print(f"On {date}, {username} made {count} contributions.")

username = "aalemayhu"  # replace with your GitHub username
get_daily_contributions(username)
