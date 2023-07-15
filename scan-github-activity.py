import requests
import argparse

# Set up command-line arguments
parser = argparse.ArgumentParser(description="Scan a GitHub organization's repositories and list them by activity.")
parser.add_argument("organization_name", help="Name of the GitHub organization to scan.")
args = parser.parse_args()

# Fetch repositories
page = 1
all_repos = []

while True:
    response = requests.get(f'https://api.github.com/orgs/{args.organization_name}/repos?page={page}&per_page=100')

    # Make sure the request was successful
    if response.status_code != 200:
        raise Exception("Error while fetching the repositories")

    # Convert the response to JSON
    data = response.json()

    # If no more repos on the page, break out of the loop
    if not data:
        break

    all_repos.extend(data)
    page += 1

# Sort the repositories by the date of their last push
sorted_repos = sorted(all_repos, key=lambda x: x['pushed_at'])

# Print the names and last push date of the repositories, in ascending order of activity
for repo in sorted_repos:
    print(f"Repository name: {repo['name']}, last push date: {repo['pushed_at']}")
