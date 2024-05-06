import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json
import re
import os

# Load the keyword categories from JSON file to form the exclusion list
def load_exclusion_list():
    with open('data/keyword_categories.json', 'r') as file:
        keyword_categories = json.load(file)
    return set(k.lower().strip() for k in keyword_categories.keys())

def should_exclude(keyword, stopwords):
    # Use regex to check if the keyword contains any of the stopwords
    pattern = '|'.join(re.escape(sw) for sw in stopwords)  # Create a regex pattern for all stopwords
    return re.search(pattern, keyword) is not None

# Load stopwords
stopwords = load_exclusion_list()

# Read the CSV file
df = pd.read_csv('data/github_repos.csv')
df['created_at'] = pd.to_datetime(df['created_at'])

# Create a directory for plots if it doesn't exist
os.makedirs('data/plots', exist_ok=True)

# Generate word clouds for each year from 2014 to 2023
for year in range(2014, 2024):
    # Select entries of the year
    year_df = df[df['created_at'].dt.year == year]

    # Extract keywords and create a single string
    all_keywords = ' '.join(year_df['topics'].dropna().tolist())
    all_keywords = all_keywords.replace('[', '').replace(']', '').replace('\'', '').replace(',', ' ')
    all_keywords = ' '.join(all_keywords.split())  # Ensures extra spaces are removed
    all_keywords = set(all_keywords.split())

    # Filter out stopwords using the new regex function
    filtered_keywords = [keyword for keyword in all_keywords if not should_exclude(keyword, stopwords)]

    # Join non-stopwords for word cloud
    filtered_keywords = ' '.join(filtered_keywords)

    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          min_font_size=10).generate(filtered_keywords)

    # Plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Save the figure
    plt.savefig(f'data/plots/wc-{year}-wo-kw.png')
    plt.close() 
