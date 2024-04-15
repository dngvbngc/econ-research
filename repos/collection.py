import requests
import time
import os

# Constants
GITHUB_API = "https://api.github.com/search/repositories"

# Accessing the GitHub token from environment variables
token = os.getenv('GITHUB_TOKEN')
if token is None:
    print("GITHUB_TOKEN is not set")
else:
    print("Token found")

HEADERS = {"Authorization": f"token {token}"}
PARAMS = {
    "q": "forks:>300 created:>2022-01-01",  # Adjust date as needed
    "sort": "forks",
    "order": "desc",
    "per_page": 100  # Max items per page
}

def get_repos(page):
    """Fetch repositories from GitHub API."""
    params = PARAMS.copy()
    params['page'] = page
    response = requests.get(GITHUB_API, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def main():
    all_repos = []
    page = 1
    while len(all_repos) < 30:
        repos = get_repos(page)
        if not repos:
            break
        all_repos.extend(repos)
        page += 1
        time.sleep(10)  # To respect rate limits

    # Sort repos by number of forks (if needed)
    all_repos.sort(key=lambda r: r['forks_count'], reverse=True)

    # Extract and print required data
    for repo in all_repos[:3000]:
        print(repo['full_name'], repo['forks_count'])

if __name__ == "__main__":
    main()
