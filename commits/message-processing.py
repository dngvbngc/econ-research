import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

# Step 1: Read the CSV Data
df = pd.read_csv('data/commits-node-addon-api.csv')
df['Time'] = pd.to_datetime(df['Time']).dt.to_period('M')  # Convert Time to month-year format

# Exclude commits by GitHub bots or services
df = df[~df['Email'].str.contains('noreply@github.com')]  # Adjust this condition as needed

# List of common stopwords to exclude
stopwords = {'a', 'the', 'for', 'from', 'of', 'in', 'and', 'is', 'on', 'to', 'this', 'that', 'with', 'as', 'not', 'be', 'which'}

# Step 2: Text Processing
def clean_text(text):
    # Remove special characters and numbers, convert to lower case, and filter stopwords
    words = re.sub(r'[^a-zA-Z\s]', '', text).lower().split()
    return ' '.join([word for word in words if word not in stopwords])

df['cleaned_messages'] = df['Message'].apply(clean_text)

# Step 3: Count Word Frequencies
all_words = ' '.join(df['cleaned_messages']).split()
word_counts = Counter(all_words)

# Step 4: Filter Top Words
top_words = [word for word, count in word_counts.most_common(50)]

# Step 5: Aggregate Data Over Time
time_data = {word: [] for word in top_words}
time_index = []

for time, group in df.groupby('Time'):
    # Convert Period to datetime for plotting
    current_time = time.to_timestamp()
    time_index.append(current_time)
    words = ' '.join(group['cleaned_messages']).split()
    counts = Counter(words)
    for word in top_words:
        time_data[word].append(counts.get(word, 0))

# Step 6: Plotting
fig, ax = plt.subplots(figsize=(14, 7))
for word in top_words:
    ax.plot(time_index, time_data[word], label=word)

ax.set_title('Top 50 Words in Commit Messages Over Time (Excluding GitHub Commits and Common Stopwords)')
ax.set_xlabel('Time (Month-Year)')
ax.set_ylabel('Word Count')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
