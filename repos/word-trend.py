import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import ast

# Read the CSV file
df = pd.read_csv('data/ml_repos.csv')

# If 'created_at' is in a different timezone, convert it to a common timezone (e.g., UTC)
df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert(None)

# Group by month
df['created_at'] = df['created_at'].dt.to_period('M')

# Prepare a dictionary to count keyword occurrences by date
keyword_counts = defaultdict(lambda: defaultdict(int))

# Process each row
for _, row in df.iterrows():
    if pd.notna(row['topics']):
        try:
            # Assuming topics are stored as a stringified list
            keywords = ast.literal_eval(row['topics'])
        except (ValueError, SyntaxError):
            # Handle the case where it's not a stringified list
            keywords = row['topics'].split(',')  # adjust this based on the actual format

        for keyword in keywords:
            keyword = keyword.strip()
            keyword_counts[keyword][row['created_at']] += 1

# Prepare DataFrame for plotting
plot_data = pd.DataFrame()

for keyword, counts in keyword_counts.items():
    temp_df = pd.DataFrame.from_dict(counts, orient='index', columns=[keyword])
    plot_data = pd.concat([plot_data, temp_df], axis=1)

plot_data.fillna(0, inplace=True)
plot_data = plot_data.sort_index()

# Convert PeriodIndex to DateTimeIndex for plotting
plot_data.index = plot_data.index.to_timestamp()

# Plot
plt.figure(figsize=(15, 8))
for keyword in keyword_counts.keys():
    plt.plot(plot_data.index, plot_data[keyword], label=keyword)

plt.xlabel('Date')
plt.ylabel('Frequency')
plt.title('Keyword Usage Over Time')
plt.legend()
plt.show()
