import requests
import json
from collections import defaultdict

def get_daily_contributions(username):
    url = f"https://api.github.com/users/{username}/events/public"
    contributions = defaultdict(int)
    pages = 0

    while url and pages < 10:
        response = requests.get(url)
        data = json.loads(response.text)

        for event in data:
            date = event["created_at"][:10]  # Extract the date part from timestamp
            contributions[date] += 1

        link_header = response.headers.get('Link')
        if link_header:
            links = requests.utils.parse_header_links(link_header.rstrip('>').replace('>,<', ',<'))
            url = next((link['url'] for link in links if link['rel'] == 'next'), None)
        else:
            url = None

        pages += 1

    for date, count in contributions.items():
        print(f"On {date}, {username} made {count} contributions.")

username = "aalemayhu"  # replace with your GitHub username
get_daily_contributions(username)
