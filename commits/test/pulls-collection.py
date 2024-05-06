import requests
import csv
import os

# GitHub repository details
owner = 'nodejs'  # Replace with the repository owner's username
repo = 'node-addon-api'    # Replace with the repository name

# Accessing the GitHub token from environment variables
token = os.getenv('GITHUB_TOKEN')
if token is None:
    print("GITHUB_TOKEN is not set")
    exit()

# Function to fetch pull requests from GitHub API
def fetch_pulls(owner, repo, token):
    pulls = []
    page = 1
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/pulls?page={page}&per_page=100'
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            return []
        data = response.json()
        if len(data) == 0:
            break
        pulls.extend(data)
        page += 1
    return pulls

# Fetch pull requests
pulls = fetch_pulls(owner, repo, token)

# Write pull requests to CSV
with open('pulls.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['number', 'user', 'body', 'state', 'merge_at', 'merge_sha'])

    for pull in pulls:
        number = pull['number']
        user = pull['user']['login']
        body = pull['body']
        state = pull['state']
        merged_at = pull['merged_at'] if 'merged_at' in pull else None
        merge_sha = pull['merge_commit_sha'] if 'merge_commit_sha' in pull else None
        writer.writerow([number, user, body, state, merged_at, merge_sha])

print("Pull requests have been written to file.")
