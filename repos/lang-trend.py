import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import ast

# Read the CSV file
df = pd.read_csv('data/github_repos_lang.csv')

# If 'created_at' is in a different timezone, convert it to a common timezone (e.g., UTC)
df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert(None)

# Group by month
df['created_at'] = df['created_at'].dt.to_period('M')

# Prepare a dictionary to count keyword occurrences by date
category_counts = defaultdict(lambda: defaultdict(int))

# Process each row
for _, row in df.iterrows():
    if pd.notna(row['category']):
        if row['category'] != "Others":
            category = row['category']
            category_counts[category][row['created_at']] += 1

# Prepare DataFrame for plotting
plot_data = pd.DataFrame()

for category, counts in category_counts.items():
    temp_df = pd.DataFrame.from_dict(counts, orient='index', columns=[category])
    plot_data = pd.concat([plot_data, temp_df], axis=1)

plot_data.fillna(0, inplace=True)
plot_data = plot_data.sort_index()

# Convert PeriodIndex to DateTimeIndex for plotting
plot_data.index = plot_data.index.to_timestamp()

# Plot
plt.figure(figsize=(15, 8))
for category in category_counts.keys():
    plt.plot(plot_data.index, plot_data[category], label=category)

plt.xlabel('Date')
plt.ylabel('Frequency')
plt.title("Languages' Popularity Over Time")
plt.legend()
plt.show()
