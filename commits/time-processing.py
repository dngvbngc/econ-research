import pandas as pd
import matplotlib.pyplot as plt
import pytz

# Timezone for San Francisco
sf_timezone = pytz.timezone('America/Los_Angeles')

# Function to categorize commit time
def categorize_commit_time(row):
    # Ensure the timestamp is timezone-aware, converting only if it's naive
    commit_time = pd.to_datetime(row['Time'])
    if commit_time.tzinfo is None or commit_time.tzinfo.utcoffset(commit_time) is None:
        commit_time = commit_time.tz_localize('UTC').tz_convert(sf_timezone)
    else:
        commit_time = commit_time.tz_convert(sf_timezone)

    if 9 <= commit_time.hour < 17:
        return 'During Work Hours'
    else:
        return 'Outside Work Hours'

# Read CSV file
df = pd.read_csv('data/commits-node-addon-api.csv')

# Categorize commits
df['Category'] = df.apply(categorize_commit_time, axis=1)

# Ensure the 'Time' column is properly handled for timezone
df['Time'] = pd.to_datetime(df['Time'])
if df['Time'].dt.tz is None:
    df['Time'] = df['Time'].dt.tz_localize('UTC').dt.tz_convert(sf_timezone)
else:
    df['Time'] = df['Time'].dt.tz_convert(sf_timezone)

df.set_index('Time', inplace=True)

# Resample data by month and count commits
monthly_data = df.groupby('Category').resample('M').size().unstack(0)

# Plotting
monthly_data.plot(kind='line', figsize=(12, 6))
plt.title('Monthly Commit Trends: Work Hours vs Outside Work Hours')
plt.xlabel('Month')
plt.ylabel('Number of Commits')
plt.show()
