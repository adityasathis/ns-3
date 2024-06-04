import pandas as pd
import matplotlib.pyplot as plt
import glob

# Step 1: Parse log files and extract relevant data
log_files = glob.glob('output*.csv')

dataframes = []
for file in log_files:
    df = pd.read_csv(file, header=None, names=['Event', 'Timestamp1', 'Timestamp2', 'Value'])
    print(df)
    access_delay_df = df[df['Event'] == 'HOL Packet Delay']
    access_delay_df['Timestamp2'] = access_delay_df['Timestamp2'].astype(float) / 1e6  # Convert nanoseconds to microseconds
    access_delay_df['Value'] = access_delay_df['Value'].astype(float) / 1e6
    dataframes.append(access_delay_df[['Timestamp2', 'Value']])

# print(dataframes)

# # Step 2: Synchronize timestamps and interpolate access delay values
timestamps = pd.concat([df['Timestamp2'] for df in dataframes]).unique()
interpolated_dfs = []
for df in dataframes:
    interpolated_df = pd.DataFrame({'Timestamp2': timestamps}).merge(df, on='Timestamp2', how='left')
    interpolated_df['Value'] = interpolated_df['Value'].interpolate(method='linear')
    interpolated_dfs.append(interpolated_df)

# # Step 3: Calculate the average access delay for each timestamp across all files
combined_df = pd.concat(interpolated_dfs)
avg_delay_df = combined_df.groupby('Timestamp2').mean().reset_index()

# print(avg_delay_df)

# # Step 4: Plot the average access delay over time
plt.figure(figsize=(10, 6))
plt.plot(avg_delay_df['Timestamp2'], avg_delay_df['Value'], marker='o', linestyle='-')
plt.title('Average Access Delay Over Time')
plt.xlabel('Time (microseconds)')
plt.ylabel('Access Delay')
plt.grid(True)
plt.show()
