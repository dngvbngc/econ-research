from github import Github
from github import Auth

# Initialize Github instance with access token
access_token = "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"
auth = Auth.Token(access_token)
g = Github(auth=auth)

# Get the repository
repo_url = "vercel/next.js"
repo = g.get_repo(repo_url)

# List commit times
commits = repo.get_commits()
for commit in commits[:3]:
    print(commit.commit.committer.date)
    stats = commit.stats
    print(f"Lines Added: {stats.additions}")
    print(f"Lines Deleted: {stats.deletions}")
    print(f"Total Lines Affected: {stats.total}\n")

g.close()