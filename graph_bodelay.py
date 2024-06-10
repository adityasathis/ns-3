import pandas as pd
import matplotlib.pyplot as plt

# Function to parse a line from the log file
def parse_line(line):
    try:
        parts = line.split(',')
        if len(parts) != 5:
            return None
        metric, gNB_ID, timestamp, CAPC, backoff_delay = parts
        if metric != 'AverageBackoffDelay':
            return None
        return {'gNB_ID': gNB_ID, 'Timestamp': int(timestamp), 'CAPC': int(CAPC), 'Backoff_Delay': float(backoff_delay)}
    except Exception as e:
        print(f"Error parsing line: {line}. Error: {e}")
        return None

# Read the log file line by line and parse each line
parsed_data = []
with open('output_backoffdelay.log', 'r') as file:
    for line in file:
        data = parse_line(line.strip())
        if data:
            parsed_data.append(data)

# Create a DataFrame from parsed data
df = pd.DataFrame(parsed_data)

# Get unique gNB IDs and CAPCs
gNB_IDs = df['gNB_ID'].unique()
CAPCs = df['CAPC'].unique()

# Create subplots for each gNB ID and CAPC combination
fig, axes = plt.subplots(len(CAPCs), len(gNB_IDs), figsize=(15, 15))

# Plot each gNB ID and CAPC combination separately
for i, CAPC in enumerate(CAPCs):
    for j, gNB_ID in enumerate(gNB_IDs):
        temp_df = df[(df['gNB_ID'] == gNB_ID) & (df['CAPC'] == CAPC)]
        ax = axes[i, j] if len(CAPCs) > 1 else axes[j]
        ax.plot(temp_df['Timestamp'], temp_df['Backoff_Delay'])
        ax.set_title(f'gNB_ID {gNB_ID}, CAPC {CAPC}')
        ax.set_xlabel('Timestamp (nanoseconds)')
        ax.set_ylabel('Backoff Delay')

plt.tight_layout()
plt.show()
