import requests
import csv
import os

# Replace 'your_token_here' with your GitHub personal access token
# Accessing the GitHub token from environment variables
token = os.getenv('GITHUB_TOKEN')
if token is None:
    print("GITHUB_TOKEN is not set")
else:
    print("Token found")

GITHUB_API_URL = 'https://api.github.com/search/repositories'

# Headers for authentication
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

def fetch_repositories(start_date, end_date):
    repositories = []
    page = 1
    query_params = {
        'q': f'forks:>1000 created:{start_date}..{end_date}',
        'sort': 'forks',
        'order': 'desc',
        'per_page': 100
    }

    while True:
        query_params['page'] = page
        response = requests.get(GITHUB_API_URL, headers=headers, params=query_params)
        response_json = response.json()
        repos = response_json.get('items', [])

        if not repos:
            break

        for repo in repos:
            repositories.append({
                'name': repo['name'],
                'created_at': repo['created_at'],
                'forks': repo['forks_count'],
                'topics': repo['topics']
            })

        page += 1

    return repositories

def write_to_csv(repositories, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'created_at', 'forks', 'topics'])
        writer.writeheader()
        for repo in repositories:
            writer.writerow(repo)

def main():
    # Query for each year and combine the results
    all_repositories = []
    for i in range(2007, 2024):
        repositories = fetch_repositories(str(i) + '-01-01', str(i) + '-12-31')
        all_repositories += repositories

    # Sort the repositories by number of forks
    all_repositories.sort(key=lambda x: x['forks'], reverse=True)

    # Write to CSV
    write_to_csv(all_repositories, 'github_repos.csv')

if __name__ == '__main__':
    main()
