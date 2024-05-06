import pandas as pd

# Load the data from the CSV file
file_path = 'commits.csv'
data = pd.read_csv(file_path)

# Filter out rows where the Name column is 'Github'
filtered_data = data[data['Name'] != 'dependabot[bot]']

# Save the filtered data to a new CSV file
output_file_path = 'filtered_output.csv'
filtered_data.to_csv(output_file_path, index=False)

print(f"Filtered data saved to {output_file_path}")
