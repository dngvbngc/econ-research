import requests
from datetime import datetime, timedelta

# Configuration
TOKEN = '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'  
HEADERS = {'Authorization': f'token {TOKEN}'}
START_DATE = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')  # 2 years ago
PER_PAGE = 100  # Adjust as needed (up to 100, GitHub API limit)

def get_repos(start_date, min_forks, per_page):
    """
    Fetch repositories created since start_date with more than min_forks.
    """
    query = f'created:>{start_date} forks:>{min_forks}'
    page = 1
    repos = []

    while True:
        url = f'https://api.github.com/search/repositories?q={query}&per_page={per_page}&page={page}'
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f'Failed to fetch data: {response.status_code}')
        
        data = response.json()['items']
        repos.extend(data)

        if 'next' not in response.links:
            break

        page += 1

    return repos

def get_repo_topics(repo_full_name):
    """
    Fetch topics for a given repository.
    """
    url = f'https://api.github.com/repos/{repo_full_name}/topics'
    response = requests.get(url, headers={'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.mercy-preview+json'})
    if response.status_code != 200:
        raise Exception(f'Failed to fetch topics: {response.status_code}')

    topics = response.json().get('names', [])
    return topics

# Fetch repositories
repos_with_forks = get_repos(START_DATE, 100, PER_PAGE)

# Output the results
for repo in repos_with_forks:
    topics = get_repo_topics(repo['full_name'])
    print(f"Repo: {repo['full_name']} | Forks: {repo['forks_count']} | Topics: {', '.join(topics)}")
