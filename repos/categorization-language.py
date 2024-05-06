import pandas as pd

# Define the keyword lists and their corresponding categories
keyword_categories = {
    'python': 'Python',
    'javascript': 'TS/JS',
    'typescript': 'TS/JS',
    'c': 'C',
    'cplusplus': 'C++',
    'c-plus-plus': 'C++',
    'c-sharp': 'C#',
    'csharp': 'C#',
    'java': 'Java',
    'go': 'Go',
    'golang': 'Go',
    'php': 'PHP',
    'kotlin': 'Kotlin'
}

# Read the CSV file into a DataFrame
df = pd.read_csv("data/github_repos.csv")

# Function to assign categories based on keywords
def assign_category(topics):
    for keyword, category in keyword_categories.items():
        if keyword in topics:
            return category
    return 'Others'

# Apply the function to create the 'category' column
df['category'] = df['topics'].apply(lambda x: assign_category(eval(x.lower())))

# Write the DataFrame back to the same CSV file
df.to_csv("data/github_repos_lang.csv", index=False)
