import pandas as pd
import matplotlib.pyplot as plt
import pytz

# Timezone for San Francisco
sf_timezone = pytz.timezone('America/Los_Angeles')

# Read CSV file
df = pd.read_csv('data/commits-node-addon-api.csv')

# Ensure the 'Time' column is properly handled for timezone
df['Time'] = pd.to_datetime(df['Time'])
if df['Time'].dt.tz is None:
    df['Time'] = df['Time'].dt.tz_localize('UTC').dt.tz_convert(sf_timezone)
else:
    df['Time'] = df['Time'].dt.tz_convert(sf_timezone)

df.set_index('Time', inplace=True)

# Resample data by month and count commits
monthly_data = df.resample('M').size()

# Plotting
monthly_data.plot(kind='line', figsize=(12, 6))
plt.title('Monthly Commit Trends')
plt.xlabel('Month')
plt.ylabel('Number of Commits to Files')
plt.show()
