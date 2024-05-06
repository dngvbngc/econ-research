import pandas as pd
import json
import re

# Load the dictionary from the JSON file
with open('data/keyword_categories.json', 'r') as file:
    keyword_categories = json.load(file)

# Read the CSV file into a DataFrame
df = pd.read_csv("data/github_repos.csv")

# Function to assign categories based on keywords
def assign_category(topics):
    if len(topics) == 0:
        return "Unspecified"
    max_count = 0
    max_cat = "Others"
    cat_count = {}
    for keyword, category in keyword_categories.items():
        if re.search(keyword, ''.join(topics)):
            if category not in cat_count:
                cat_count[category] = 1
            else:
                cat_count[category] += 1
    for category, count in cat_count.items():
        if count > max_count:
            max_count = count
            max_cat = category
    return max_cat

# Apply the function to create the 'category' column
df['category'] = df['topics'].apply(lambda x: assign_category(eval(x.lower())))

# Write the DataFrame back to the same CSV file
df.to_csv("data/github_repos_cat.csv", index=False)
