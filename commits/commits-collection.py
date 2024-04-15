import requests
import csv
import json
from datetime import datetime
import os

# GitHub repository details
owner = 'nodejs'  # Replace with the repository owner's username
repo = 'node-addon-api'    # Replace with the repository name

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

# Write commits and file changes to CSV
filename = 'commits-' + repo + '.csv'

with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Name', 'Email', 'Time', 'Message', 'File Changes'])

    for commit in commits:
        name = commit['commit']['committer']['name']
        email = commit['commit']['committer']['email']
        time = commit['commit']['committer']['date']
        message = commit['commit']['message']
        commit_files = fetch_commit_files(commit['url'], token)

        # Convert file changes list to JSON string for CSV output
        file_changes_str = json.dumps(commit_files)
        writer.writerow([name, email, time, message, file_changes_str])

print(f"Commits and file changes have been written to {filename}")
