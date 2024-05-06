import requests
import csv
import os

# GitHub repository details
owner = 'dngvbngc'  # Replace with the repository owner's username
repo = 'ysc3232-carpool'    # Replace with the repository name

# Accessing the GitHub token from environment variables
token = os.getenv('GITHUB_TOKEN')
if token is None:
    print("GITHUB_TOKEN is not set")
else:
    print("Token found")

# Function to fetch commits from GitHub API
def fetch_commits(owner, repo, token):
    commits = []
    page = 1
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/commits?page={page}'
        headers = {'Authorization': f'token {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            return []
        data = response.json()
        if len(data) == 0:
            break
        commits.extend(data)
        page += 1
    return commits

# Function to fetch file changes for a specific commit
def fetch_commit_files(commit_url, token):
    headers = {'Authorization': f'token {token}'}
    response = requests.get(commit_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch commit details: {response.status_code}")
        return []
    commit_data = response.json()
    file_changes = []
    for file in commit_data['files']:
        file_changes.append({
            'filename': file['filename'],
            'additions': file['additions'],
            'deletions': file['deletions']
        })
    return file_changes

# Fetch commits
commits = fetch_commits(owner, repo, token)

# Write commits to CSV
with open('commits2.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['SHA', 'Author', 'Committer', 'Time', 'Message', 'Parents', 'Files'])

    for commit in commits:
        sha = commit['sha']
        author = commit['commit']['author']['name']
        committer = commit['commit']['committer']['name']
        time = commit['commit']['committer']['date']
        message = commit['commit']['message']
        parents = '| '.join([parent['sha'] for parent in commit['parents']])
        files = commit_files = fetch_commit_files(commit['url'], token)
        writer.writerow([sha, author, committer, time, message, parents, files])

print("Commits have been written to file")
