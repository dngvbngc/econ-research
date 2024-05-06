import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('data/github_repos.csv')

# Select entries of year
df['created_at'] = pd.to_datetime(df['created_at'])
year_df = df[df['created_at'].dt.year == 2023]

# Extract keywords and create a single string
all_keywords = ' '.join(year_df['topics'].dropna().tolist())
all_keywords = all_keywords.replace('[', '').replace(']', '').replace('\'', '').replace(',', '')

# Remove any leading/trailing whitespace that might create separate entries
all_keywords = ' '.join(set(all_keywords.split()))

# Create a WordCloud object
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                min_font_size = 10).generate(all_keywords)

# Plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show()
